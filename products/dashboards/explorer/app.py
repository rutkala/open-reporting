#!/usr/bin/env python3
"""
Open Reporting — Data Explorer
Pivot-style explorer over the curated DuckDB layer.
Run: PYTHONPATH=/opt/open-reporting DUCKDB_PATH=/opt/open-reporting/data/warehouse.duckdb \
     python3 products/dashboards/explorer/app.py
"""
import logging
import os

import duckdb
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, Input, Output, State, callback, dash_table, dcc, html, no_update

import products.visuals.lib.theme as _theme  # noqa: F401 — registers nordic template
from products.visuals.lib.theme import (
    AZURE_1, AZURE_3, BG_PAGE, BG_SURFACE, BORDER,
    COLORWAY, SUBTEXT, TEXT,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

CURATED_SCHEMA = "main_curated"
MAX_PIVOT_COLS  = 60
PORT            = 8051

# Staging / internal tables to exclude from the table picker
_HIDDEN_TABLES = {"stg_eurostat"}

# Human-friendly display names for the table dropdown
_TABLE_LABELS: dict[str, str] = {
    "all_indicators":      "All indicators (Eurostat)",
    "fin_exchange_rates":  "Finance — Exchange Rates (NBP)",
    "agr_indicators":      "Agriculture",
    "bus_indicators":      "Business",
    "clt_indicators":      "Culture & Tourism",
    "crm_indicators":      "Crime & Justice",
    "edu_indicators":      "Education",
    "ene_indicators":      "Energy",
    "env_indicators":      "Environment",
    "hlt_indicators":      "Health",
    "lab_indicators":      "Labour",
    "mac_indicators":      "Macroeconomics",
    "pop_indicators":      "Population",
    "prc_indicators":      "Prices",
    "pub_indicators":      "Public Finance",
    "sci_indicators":      "Science & Technology",
    "soc_indicators":      "Society",
    "trd_indicators":      "Trade",
    "trp_indicators":      "Transport",
}

# Friendly display names for individual indicators (detail_id → label)
_INDICATOR_LABELS: dict[str, str] = {}  # populated lazily from catalogue if available


# ── DuckDB helpers ────────────────────────────────────────────────────────────

def _db():
    path = os.environ.get("DUCKDB_PATH", "/opt/open-reporting/data/warehouse.duckdb")
    return duckdb.connect(path, read_only=True)


def list_tables() -> list[str]:
    conn = _db()
    rows = conn.execute(
        "SELECT table_name FROM information_schema.tables "
        "WHERE table_schema = ? ORDER BY table_name",
        [CURATED_SCHEMA],
    ).fetchall()
    conn.close()
    tables = [r[0] for r in rows if r[0] not in _HIDDEN_TABLES]
    priority = ["all_indicators", "fin_exchange_rates"]
    ordered  = [t for t in priority if t in tables]
    ordered += sorted(t for t in tables if t not in priority)
    return ordered


def _table_option(name: str) -> dict:
    return {"label": _TABLE_LABELS.get(name, name), "value": name}


def table_columns(table: str) -> pd.DataFrame:
    """Return (column_name, data_type, is_numeric, is_date) for a curated table."""
    conn = _db()
    df = conn.execute(
        "SELECT column_name, data_type FROM information_schema.columns "
        "WHERE table_schema = ? AND table_name = ? ORDER BY ordinal_position",
        [CURATED_SCHEMA, table],
    ).df()
    conn.close()
    df["is_numeric"] = df["data_type"].str.upper().str.contains(
        r"INT|FLOAT|DOUBLE|DECIMAL|NUMERIC|HUGEINT|UBIGINT|REAL", regex=True
    )
    df["is_date"] = df["data_type"].str.upper().str.contains(
        r"DATE|TIMESTAMP", regex=True
    )
    return df


def get_distinct(table: str, column: str,
                 filter_col: str | None = None,
                 filter_vals: list | None = None) -> list[str]:
    """Return sorted distinct values for a column, with optional WHERE filter."""
    params = [CURATED_SCHEMA, table]
    sql = f'SELECT DISTINCT "{column}" FROM information_schema.tables WHERE 1=0'  # placeholder
    # Build directly against the table
    sql = f'SELECT DISTINCT "{column}" FROM {CURATED_SCHEMA}."{table}"'
    if filter_col and filter_vals:
        placeholders = ", ".join(["?"] * len(filter_vals))
        sql += f' WHERE "{filter_col}" IN ({placeholders})'
        params = filter_vals
    else:
        params = []
    sql += f' ORDER BY "{column}"'
    conn = _db()
    rows = conn.execute(sql, params).fetchall()
    conn.close()
    return [r[0] for r in rows if r[0] is not None]


def run_query(
    table: str,
    row_dims: list[str],
    col_dim: str | None,
    measure: str,
    agg: str,
    domain_filter: list[str] | None,
    indicator_filter: list[str] | None,
    period_from: str | None,
    period_to: str | None,
    period_col: str | None,
) -> pd.DataFrame:
    group_cols = list(row_dims)
    if col_dim and col_dim not in group_cols:
        group_cols.append(col_dim)

    select_parts = [f'"{c}"' for c in group_cols]
    select_parts.append(f'{agg}("{measure}") AS value')

    sql = f'SELECT {", ".join(select_parts)} FROM {CURATED_SCHEMA}."{table}"'
    params: list = []

    conditions: list[str] = []

    if domain_filter:
        placeholders = ", ".join(["?"] * len(domain_filter))
        conditions.append(f'"domain_id" IN ({placeholders})')
        params.extend(domain_filter)

    if indicator_filter:
        placeholders = ", ".join(["?"] * len(indicator_filter))
        conditions.append(f'"detail_id" IN ({placeholders})')
        params.extend(indicator_filter)

    if period_col and period_from:
        conditions.append(f'CAST("{period_col}" AS VARCHAR) >= ?')
        params.append(str(period_from))
    if period_col and period_to:
        conditions.append(f'CAST("{period_col}" AS VARCHAR) <= ?')
        params.append(str(period_to))

    if conditions:
        sql += " WHERE " + " AND ".join(conditions)

    if group_cols:
        sql += f' GROUP BY {", ".join(f"{chr(34)}{c}{chr(34)}" for c in group_cols)}'
        sql += f' ORDER BY {", ".join(f"{chr(34)}{c}{chr(34)}" for c in group_cols)}'

    log.info("Explorer query: %s | params: %s", sql, params)
    conn = _db()
    df = conn.execute(sql, params).df()
    conn.close()
    return df


def pivot_df(df: pd.DataFrame, row_dims: list[str], col_dim: str) -> pd.DataFrame:
    """Pivot df so col_dim values become columns."""
    distinct = df[col_dim].nunique()
    if distinct > MAX_PIVOT_COLS:
        log.warning("Column dimension has %d distinct values — capping at %d", distinct, MAX_PIVOT_COLS)
        top = df.groupby(col_dim)["value"].sum().nlargest(MAX_PIVOT_COLS).index
        df = df[df[col_dim].isin(top)]

    index = row_dims[0] if len(row_dims) == 1 else row_dims
    return df.pivot_table(index=index, columns=col_dim, values="value", aggfunc="sum").reset_index()


# ── App ───────────────────────────────────────────────────────────────────────

app = Dash(
    __name__,
    title="Open Reporting — Explorer",
    suppress_callback_exceptions=True,
    requests_pathname_prefix="/explorer/",
    routes_pathname_prefix="/explorer/",
)

# ── Styles ────────────────────────────────────────────────────────────────────

S = {
    "body": {
        "fontFamily": "Inter, 'Segoe UI', system-ui, sans-serif",
        "background": BG_PAGE, "color": TEXT,
        "minHeight": "100vh", "display": "flex", "flexDirection": "column", "margin": 0,
    },
    "header": {
        "background": BG_SURFACE, "borderBottom": f"1px solid {BORDER}",
        "padding": "14px 32px", "display": "flex", "alignItems": "baseline",
        "gap": "24px", "flexShrink": 0,
    },
    "layout": {"display": "flex", "flex": 1},
    "sidebar": {
        "width": "260px", "flexShrink": 0,
        "background": BG_SURFACE, "borderRight": f"1px solid {BORDER}",
        "padding": "20px 16px", "position": "sticky",
        "top": 0, "height": "100vh", "overflowY": "auto",
    },
    "main": {"flex": 1, "padding": "28px 24px 56px", "minWidth": 0},
    "section_header": {
        "fontSize": "10px", "fontWeight": 700, "textTransform": "uppercase",
        "letterSpacing": "0.10em", "color": AZURE_3,
        "margin": "20px 0 10px", "paddingBottom": "6px",
        "borderBottom": f"1px solid {BORDER}",
    },
    "label": {
        "fontSize": "11px", "fontWeight": 600, "textTransform": "uppercase",
        "letterSpacing": "0.07em", "color": SUBTEXT,
        "marginBottom": "6px", "marginTop": "14px", "display": "block",
    },
    "card": {
        "background": BG_SURFACE, "borderRadius": "6px",
        "boxShadow": "0 1px 4px rgba(0,0,0,0.07), 0 0 1px rgba(0,0,0,0.04)",
        "padding": "20px", "marginBottom": "20px",
    },
    "footer": {
        "background": BG_SURFACE, "borderTop": f"1px solid {BORDER}",
        "padding": "12px 32px", "fontSize": "12px", "color": SUBTEXT,
        "flexShrink": 0,
    },
    "hint": {"fontSize": "12px", "color": SUBTEXT, "marginTop": "6px"},
    "warn": {
        "fontSize": "12px", "color": "#D4874A",
        "padding": "8px 12px", "background": "#FEF3E8",
        "borderRadius": "4px", "marginBottom": "12px",
    },
    "empty_state": {
        "padding": "48px 24px", "textAlign": "center",
        "color": SUBTEXT, "fontSize": "14px",
    },
}

_dd_style = {"fontSize": "13px"}
_tables    = list_tables()
_table_opts = [_table_option(t) for t in _tables]

# ── Layout ────────────────────────────────────────────────────────────────────

app.layout = html.Div(style=S["body"], children=[

    html.Header(style=S["header"], children=[
        html.A("Open Reporting", href="/",
               style={"fontSize": "15px", "fontWeight": 600, "color": TEXT, "textDecoration": "none"}),
        html.Span("Explorer",
                  style={"fontSize": "13px", "color": SUBTEXT}),
    ]),

    html.Div(style=S["layout"], children=[

        # ── Sidebar ───────────────────────────────────────────────────────────
        html.Aside(style=S["sidebar"], children=[

            # — Data source —
            html.Div("Data source", style=S["section_header"]),

            html.Span("Table", style={**S["label"], "marginTop": 0}),
            dcc.Dropdown(
                id="dd-table",
                options=_table_opts,
                value=_tables[0] if _tables else None,
                clearable=False,
                style=_dd_style,
            ),

            # — Filters — (shown when domain_id / detail_id columns exist)
            html.Div(id="filters-section", children=[
                html.Div("Filters", style=S["section_header"]),

                html.Div(id="domain-filter-container", style={"display": "none"}, children=[
                    html.Span("Domain", style={**S["label"], "marginTop": 0}),
                    dcc.Dropdown(id="dd-domain", multi=True, style=_dd_style,
                                 placeholder="All domains"),
                ]),

                html.Div(id="indicator-filter-container", style={"display": "none"}, children=[
                    html.Span("Indicators", style=S["label"]),
                    dcc.Dropdown(id="dd-indicator", multi=True, style=_dd_style,
                                 placeholder="All indicators"),
                ]),

                html.Div(id="period-filter-container", style={"display": "none"}, children=[
                    html.Span("Period from", style=S["label"]),
                    dcc.Input(id="period-from", type="text", placeholder="e.g. 2010",
                              debounce=True,
                              style={"width": "100%", "fontSize": "12px", "padding": "6px",
                                     "border": f"1px solid {BORDER}", "borderRadius": "4px",
                                     "color": TEXT, "background": BG_PAGE}),
                    html.Span("Period to", style=S["label"]),
                    dcc.Input(id="period-to", type="text", placeholder="e.g. 2024",
                              debounce=True,
                              style={"width": "100%", "fontSize": "12px", "padding": "6px",
                                     "border": f"1px solid {BORDER}", "borderRadius": "4px",
                                     "color": TEXT, "background": BG_PAGE}),
                ]),
            ]),

            # — Pivot —
            html.Div("Pivot", style=S["section_header"]),

            html.Span("Rows", style={**S["label"], "marginTop": 0}),
            dcc.Dropdown(id="dd-rows", multi=True, style=_dd_style,
                         placeholder="Select columns…"),

            html.Span("Columns  (optional pivot)", style=S["label"]),
            dcc.Dropdown(id="dd-col", multi=False, style=_dd_style,
                         placeholder="None — flat table"),

            html.Span("Values", style=S["label"]),
            dcc.Dropdown(id="dd-measure", clearable=False, style=_dd_style,
                         placeholder="Select measure…"),

            html.Span("Aggregation", style=S["label"]),
            dcc.Dropdown(
                id="dd-agg",
                options=[
                    {"label": "Average", "value": "AVG"},
                    {"label": "Sum",     "value": "SUM"},
                    {"label": "Min",     "value": "MIN"},
                    {"label": "Max",     "value": "MAX"},
                    {"label": "Count",   "value": "COUNT"},
                ],
                value="SUM",
                clearable=False,
                style=_dd_style,
            ),

            html.Div(style={"marginTop": "20px"}, children=[
                html.Button("Run", id="btn-run",
                            style={
                                "width": "100%", "padding": "8px",
                                "background": AZURE_1, "color": "#fff",
                                "border": "none", "borderRadius": "4px",
                                "fontSize": "13px", "fontWeight": 600,
                                "cursor": "pointer",
                            }),
            ]),

            # Hidden stores
            dcc.Store(id="store-columns"),
        ]),

        # ── Main content ──────────────────────────────────────────────────────
        html.Main(style=S["main"], children=[
            html.Div(id="output-warning"),
            html.Div(id="output-area", children=[
                html.Div(style=S["empty_state"], children=[
                    html.Div("Configure your selection in the sidebar and click Run.",
                             style={"marginBottom": "8px"}),
                    html.Div("Rows → what goes on the Y-axis / table index",
                             style={"fontSize": "12px", "color": SUBTEXT}),
                    html.Div("Columns → optional pivot dimension (creates one column per value)",
                             style={"fontSize": "12px", "color": SUBTEXT}),
                    html.Div("Values → the numeric measure to aggregate",
                             style={"fontSize": "12px", "color": SUBTEXT}),
                ]),
            ]),
        ]),
    ]),

    html.Footer(style=S["footer"], children=[
        html.Span("Open Reporting — internal data explorer"),
    ]),
])


# ── Callbacks ─────────────────────────────────────────────────────────────────

@callback(
    Output("store-columns", "data"),
    Input("dd-table", "value"),
)
def load_columns(table):
    if not table:
        return {}
    cols = table_columns(table)
    return cols.to_dict("records")


@callback(
    Output("dd-rows",    "options"),
    Output("dd-col",     "options"),
    Output("dd-measure", "options"),
    Output("dd-rows",    "value"),
    Output("dd-col",     "value"),
    Output("dd-measure", "value"),
    Input("store-columns", "data"),
    State("dd-table", "value"),
)
def populate_pivot_dropdowns(col_records, table):
    if not col_records:
        empty: list = []
        return empty, empty, empty, None, None, None

    cols     = pd.DataFrame(col_records)
    all_cols = cols["column_name"].tolist()
    nums     = cols[cols["is_numeric"]]["column_name"].tolist()
    # Exclude metadata/system columns from dim options
    exclude  = {"geo", "obs_status", "dataset_code", "fetched_at", "updated_at"}
    dims     = [c for c in all_cols if c not in nums and c not in exclude]

    dim_opts     = [{"label": c, "value": c} for c in dims]
    measure_opts = [{"label": c, "value": c} for c in nums]

    # Smart defaults per table type
    if table in ("all_indicators",) or (table and table.endswith("_indicators")):
        default_rows    = ["detail_id"] if "detail_id" in dims else dims[:1]
        default_col     = "period" if "period" in dims else None
        default_measure = "value" if "value" in nums else (nums[0] if nums else None)
    elif table == "fin_exchange_rates":
        default_rows    = ["period"] if "period" in dims else dims[:1]
        default_col     = "currency" if "currency" in dims else None
        default_measure = nums[0] if nums else None
    else:
        default_rows    = dims[:1]
        default_col     = None
        default_measure = nums[0] if nums else None

    return dim_opts, dim_opts, measure_opts, default_rows, default_col, default_measure


@callback(
    Output("domain-filter-container",    "style"),
    Output("indicator-filter-container", "style"),
    Output("period-filter-container",    "style"),
    Output("dd-domain",    "options"),
    Input("store-columns", "data"),
    State("dd-table", "value"),
)
def show_filter_sections(col_records, table):
    hidden = {"display": "none"}
    shown  = {}

    if not col_records or not table:
        return hidden, hidden, hidden, []

    cols      = pd.DataFrame(col_records)
    col_names = cols["column_name"].tolist()

    has_domain    = "domain_id" in col_names
    has_indicator = "detail_id" in col_names
    has_period    = "period"    in col_names

    domain_opts: list = []
    if has_domain:
        vals = get_distinct(table, "domain_id")
        domain_opts = [{"label": v, "value": v} for v in vals]

    return (
        shown if has_domain    else hidden,
        shown if has_indicator else hidden,
        shown if has_period    else hidden,
        domain_opts,
    )


@callback(
    Output("dd-indicator", "options"),
    Input("dd-domain", "value"),
    State("dd-table", "value"),
    State("store-columns", "data"),
)
def update_indicator_options(domain_vals, table, col_records):
    if not table or not col_records:
        return []
    cols      = pd.DataFrame(col_records)
    col_names = cols["column_name"].tolist()
    if "detail_id" not in col_names:
        return []

    vals = get_distinct(table, "detail_id",
                        filter_col="domain_id" if domain_vals else None,
                        filter_vals=domain_vals or None)
    return [{"label": v, "value": v} for v in vals]


@callback(
    Output("output-warning", "children"),
    Output("output-area",    "children"),
    Input("btn-run", "n_clicks"),
    State("dd-table",     "value"),
    State("dd-rows",      "value"),
    State("dd-col",       "value"),
    State("dd-measure",   "value"),
    State("dd-agg",       "value"),
    State("store-columns","data"),
    State("dd-domain",    "value"),
    State("dd-indicator", "value"),
    State("period-from",  "value"),
    State("period-to",    "value"),
    prevent_initial_call=True,
)
def run_explorer(_, table, row_dims, col_dim, measure, agg, col_records,
                 domain_filter, indicator_filter, period_from, period_to):
    if not table or not row_dims or not measure:
        msg = html.Div("Select a table, at least one row dimension, and a measure.", style=S["hint"])
        return msg, no_update

    cols     = pd.DataFrame(col_records) if col_records else pd.DataFrame()
    col_names = cols["column_name"].tolist() if not cols.empty else []

    # Find period column (text, not date) for filtering
    period_col = "period" if "period" in col_names else None

    try:
        df = run_query(
            table, row_dims, col_dim, measure, agg,
            domain_filter   or None,
            indicator_filter or None,
            period_from or None,
            period_to   or None,
            period_col,
        )
    except Exception as e:
        err = html.Div(f"Query error: {e}", style=S["warn"])
        return err, no_update

    if df.empty:
        return (
            html.Div("No data returned. Try adjusting your filters or selections.", style=S["hint"]),
            no_update,
        )

    warning_text = None
    df_flat = df.copy()  # keep pre-pivot data for the chart

    # Pivot if column dimension selected
    if col_dim:
        distinct = df[col_dim].nunique()
        if distinct > MAX_PIVOT_COLS:
            warning_text = (
                f"Column dimension '{col_dim}' has {distinct} distinct values — "
                f"showing top {MAX_PIVOT_COLS} by sum."
            )
        df = pivot_df(df, row_dims, col_dim)

    # ── Table ─────────────────────────────────────────────────────────────────
    table_component = dash_table.DataTable(
        data=df.head(500).to_dict("records"),
        columns=[{"name": c, "id": c} for c in df.columns],
        page_size=20,
        sort_action="native",
        filter_action="native",
        style_table={"overflowX": "auto"},
        style_header={
            "backgroundColor": BG_PAGE,
            "fontWeight": 600,
            "fontSize": "12px",
            "color": SUBTEXT,
            "border": f"1px solid {BORDER}",
            "textTransform": "uppercase",
            "letterSpacing": "0.06em",
        },
        style_cell={
            "backgroundColor": BG_SURFACE,
            "color": TEXT,
            "fontSize": "13px",
            "border": f"1px solid {BORDER}",
            "padding": "8px 12px",
            "fontFamily": "Inter, 'Segoe UI', system-ui, sans-serif",
        },
        style_data_conditional=[
            {"if": {"row_index": "odd"}, "backgroundColor": BG_PAGE},
        ],
    )

    # ── Chart — uses flat data so axes match the pivot layout ─────────────────
    fig = _build_chart(df_flat, row_dims, col_dim, measure, agg)

    output = [
        html.Div(style=S["card"], children=[table_component]),
        html.Div(style=S["card"], children=[
            dcc.Graph(figure=fig, config={"displayModeBar": False}),
        ]),
    ]

    warning = html.Div(warning_text, style=S["warn"]) if warning_text else ""
    return warning, output


def _build_chart(df_flat: pd.DataFrame, row_dims: list[str], col_dim: str | None,
                 measure: str, agg: str) -> go.Figure:
    """
    Chart mirrors the pivot table layout:
      - X axis  = column dimension (col_dim) values
                  or, when no pivot, the first row dimension
      - Series  = row dimension values (one line per row)
      - Y axis  = aggregated measure
    """
    fig = go.Figure()

    if col_dim and col_dim in df_flat.columns:
        # Pivoted mode: x=col_dim, one series per unique value of row_dims[0]
        series_dim = row_dims[0] if row_dims else None
        series_vals = sorted(df_flat[series_dim].unique()) if series_dim else [None]

        for i, sv in enumerate(series_vals):
            sub = df_flat[df_flat[series_dim] == sv].sort_values(col_dim) if series_dim else df_flat
            fig.add_trace(go.Scatter(
                x=sub[col_dim],
                y=sub["value"],
                name=str(sv) if sv is not None else measure,
                mode="lines+markers",
                line=dict(color=COLORWAY[i % len(COLORWAY)], width=1.5),
                marker=dict(size=4),
            ))
        x_label = col_dim
    else:
        # Flat mode: x=first row dim, series=second row dim (if any)
        x_col = row_dims[0] if row_dims else df_flat.columns[0]
        y_col = "value" if "value" in df_flat.columns else df_flat.select_dtypes("number").columns[0]
        other_dims = [d for d in row_dims if d != x_col]

        if other_dims:
            for i, grp_val in enumerate(sorted(df_flat[other_dims[0]].unique())):
                sub = df_flat[df_flat[other_dims[0]] == grp_val].sort_values(x_col)
                fig.add_trace(go.Scatter(
                    x=sub[x_col], y=sub[y_col],
                    name=str(grp_val), mode="lines+markers",
                    line=dict(color=COLORWAY[i % len(COLORWAY)], width=1.5),
                    marker=dict(size=4),
                ))
        else:
            plot_df = df_flat.sort_values(x_col)
            fig.add_trace(go.Scatter(
                x=plot_df[x_col], y=plot_df[y_col],
                mode="lines+markers", name=measure,
                line=dict(color=AZURE_1, width=2),
                marker=dict(size=5),
            ))
        x_label = x_col

    fig.update_layout(
        title=f"{agg}({measure})",
        xaxis_title=x_label,
        yaxis_title=measure,
        height=400,
        margin=dict(l=60, r=24, t=48, b=40),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
            font=dict(size=11),
        ),
    )
    return fig


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    log.info("Explorer starting on port %d — tables: %s", PORT, list_tables())
    app.run(host="0.0.0.0", port=PORT, debug=False)
