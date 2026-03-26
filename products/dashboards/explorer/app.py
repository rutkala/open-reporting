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
MAX_PIVOT_COLS  = 50
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
    # Put all_indicators and fin_exchange_rates first, then rest alphabetically
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


def run_query(table: str, row_dims: list[str], col_dim: str | None,
              measure: str, agg: str,
              date_col: str | None, date_from: str | None, date_to: str | None) -> pd.DataFrame:
    group_cols = list(row_dims)
    if col_dim and col_dim not in group_cols:
        group_cols.append(col_dim)

    select_parts = [f'"{c}"' for c in group_cols]
    select_parts.append(f'{agg}("{measure}") AS value')

    sql = f'SELECT {", ".join(select_parts)} FROM {CURATED_SCHEMA}."{table}"'
    params = []

    conditions = []
    if date_col and date_from:
        conditions.append(f'"{date_col}" >= ?')
        params.append(date_from)
    if date_col and date_to:
        conditions.append(f'"{date_col}" <= ?')
        params.append(date_to)
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

    if len(row_dims) == 1:
        index = row_dims[0]
    else:
        index = row_dims

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
        "width": "240px", "flexShrink": 0,
        "background": BG_SURFACE, "borderRight": f"1px solid {BORDER}",
        "padding": "20px 16px", "position": "sticky",
        "top": 0, "height": "100vh", "overflowY": "auto",
    },
    "main": {"flex": 1, "padding": "28px 24px 56px", "minWidth": 0},
    "label": {
        "fontSize": "11px", "fontWeight": 600, "textTransform": "uppercase",
        "letterSpacing": "0.07em", "color": SUBTEXT,
        "marginBottom": "6px", "marginTop": "16px", "display": "block",
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
}

_dd_style = {"fontSize": "13px"}
_tables   = list_tables()
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

            html.Span("Table", style=S["label"]),
            dcc.Dropdown(
                id="dd-table",
                options=_table_opts,
                value=_tables[0] if _tables else None,
                clearable=False,
                style=_dd_style,
            ),

            html.Span("Row dimensions", style=S["label"]),
            dcc.Dropdown(id="dd-rows", multi=True, style=_dd_style,
                         placeholder="Select columns…"),

            html.Span("Column pivot  (optional)", style=S["label"]),
            dcc.Dropdown(id="dd-col", multi=False, style=_dd_style,
                         placeholder="None"),

            html.Span("Measure", style=S["label"]),
            dcc.Dropdown(id="dd-measure", clearable=False, style=_dd_style,
                         placeholder="Select measure…"),

            html.Span("Aggregation", style=S["label"]),
            dcc.Dropdown(
                id="dd-agg",
                options=[
                    {"label": "Average",  "value": "AVG"},
                    {"label": "Sum",      "value": "SUM"},
                    {"label": "Min",      "value": "MIN"},
                    {"label": "Max",      "value": "MAX"},
                    {"label": "Count",    "value": "COUNT"},
                ],
                value="AVG",
                clearable=False,
                style=_dd_style,
            ),

            # Date range — shown only when a date column is in row dims
            html.Div(id="date-filter-container", children=[
                html.Span("Date from", style=S["label"]),
                dcc.Input(id="date-from", type="text", placeholder="YYYY-MM-DD",
                          debounce=True,
                          style={"width": "100%", "fontSize": "12px", "padding": "6px",
                                 "border": f"1px solid {BORDER}", "borderRadius": "4px",
                                 "color": TEXT, "background": BG_PAGE}),
                html.Span("Date to", style=S["label"]),
                dcc.Input(id="date-to", type="text", placeholder="YYYY-MM-DD",
                          debounce=True,
                          style={"width": "100%", "fontSize": "12px", "padding": "6px",
                                 "border": f"1px solid {BORDER}", "borderRadius": "4px",
                                 "color": TEXT, "background": BG_PAGE}),
            ]),

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

            # Hidden store: column metadata for selected table
            dcc.Store(id="store-columns"),
        ]),

        # ── Main content ──────────────────────────────────────────────────────
        html.Main(style=S["main"], children=[
            html.Div(id="output-warning"),
            html.Div(id="output-table", style=S["card"]),
            html.Div(id="output-chart", style=S["card"]),
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
    Output("date-filter-container", "style"),
    Input("store-columns", "data"),
)
def populate_dropdowns(col_records):
    if not col_records:
        empty = []
        return empty, empty, empty, None, None, None, {"display": "none"}

    cols = pd.DataFrame(col_records)
    dims    = cols[~cols["is_numeric"]]["column_name"].tolist()
    measures = cols[cols["is_numeric"]]["column_name"].tolist()
    has_date = cols["is_date"].any()

    dim_opts     = [{"label": c, "value": c} for c in dims]
    measure_opts = [{"label": c, "value": c} for c in measures]

    # Sensible defaults: all dims on rows, no col pivot, first measure
    default_rows    = dims[:] if dims else []
    default_measure = measures[0] if measures else None
    date_style      = {} if has_date else {"display": "none"}

    return dim_opts, dim_opts, measure_opts, default_rows, None, default_measure, date_style


@callback(
    Output("output-warning", "children"),
    Output("output-table",   "children"),
    Output("output-chart",   "children"),
    Input("btn-run", "n_clicks"),
    State("dd-table",   "value"),
    State("dd-rows",    "value"),
    State("dd-col",     "value"),
    State("dd-measure", "value"),
    State("dd-agg",     "value"),
    State("store-columns", "data"),
    State("date-from",  "value"),
    State("date-to",    "value"),
    prevent_initial_call=True,
)
def run_explorer(_, table, row_dims, col_dim, measure, agg, col_records, date_from, date_to):
    if not table or not row_dims or not measure:
        msg = html.Div("Select a table, at least one row dimension, and a measure.", style=S["hint"])
        return msg, no_update, no_update

    # Find date column (first date-type column in row dims)
    cols     = pd.DataFrame(col_records) if col_records else pd.DataFrame()
    date_col = None
    if not cols.empty:
        date_cols_in_rows = cols[cols["is_date"] & cols["column_name"].isin(row_dims)]["column_name"].tolist()
        date_col = date_cols_in_rows[0] if date_cols_in_rows else None

    try:
        df = run_query(table, row_dims, col_dim, measure, agg,
                       date_col, date_from or None, date_to or None)
    except Exception as e:
        err = html.Div(f"Query error: {e}", style=S["warn"])
        return err, no_update, no_update

    if df.empty:
        return html.Div("No data returned for this selection.", style=S["hint"]), no_update, no_update

    warning = None

    # Pivot if column dimension selected
    if col_dim:
        distinct = df[col_dim].nunique()
        if distinct > MAX_PIVOT_COLS:
            warning = html.Div(
                f"Column dimension '{col_dim}' has {distinct} distinct values — showing top {MAX_PIVOT_COLS} by sum.",
                style=S["warn"],
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

    # ── Chart ─────────────────────────────────────────────────────────────────
    fig = _build_chart(df, row_dims, col_dim, measure, agg, cols)

    return warning or "", table_component, dcc.Graph(figure=fig, config={"displayModeBar": False})


def _build_chart(df: pd.DataFrame, row_dims: list[str], col_dim: str | None,
                 measure: str, agg: str, cols: pd.DataFrame) -> go.Figure:
    fig = go.Figure()

    # Determine x axis: prefer date column, else first row dim
    date_dims = cols[cols["is_date"] & cols["column_name"].isin(row_dims)]["column_name"].tolist() if not cols.empty else []
    x_col     = date_dims[0] if date_dims else row_dims[0]
    is_time   = bool(date_dims)

    if col_dim and col_dim in df.columns:
        # Pivoted: each original col_dim value is now a column
        value_cols = [c for c in df.columns if c not in row_dims]
        for i, vc in enumerate(value_cols):
            trace_df = df[[x_col, vc]].dropna()
            if is_time:
                fig.add_trace(go.Scatter(
                    x=trace_df[x_col], y=trace_df[vc],
                    name=str(vc), mode="lines",
                    line=dict(color=COLORWAY[i % len(COLORWAY)], width=1.5),
                ))
            else:
                fig.add_trace(go.Bar(
                    x=trace_df[x_col], y=trace_df[vc],
                    name=str(vc),
                    marker_color=COLORWAY[i % len(COLORWAY)],
                ))
    else:
        # Flat: single series, optionally grouped by a non-x row dim
        other_dims = [d for d in row_dims if d != x_col]
        if other_dims:
            for i, grp_val in enumerate(sorted(df[other_dims[0]].unique())):
                sub = df[df[other_dims[0]] == grp_val].sort_values(x_col)
                if is_time:
                    fig.add_trace(go.Scatter(
                        x=sub[x_col], y=sub["value"],
                        name=str(grp_val), mode="lines",
                        line=dict(color=COLORWAY[i % len(COLORWAY)], width=1.5),
                    ))
                else:
                    fig.add_trace(go.Bar(
                        x=sub[x_col], y=sub["value"],
                        name=str(grp_val),
                        marker_color=COLORWAY[i % len(COLORWAY)],
                    ))
        else:
            plot_df = df.sort_values(x_col)
            if is_time:
                fig.add_trace(go.Scatter(
                    x=plot_df[x_col], y=plot_df["value"],
                    mode="lines", name=measure,
                    line=dict(color=AZURE_1, width=2),
                ))
            else:
                fig.add_trace(go.Bar(
                    x=plot_df[x_col], y=plot_df["value"],
                    name=measure, marker_color=AZURE_1,
                ))

    fig.update_layout(
        title=f"{agg}({measure})",
        xaxis_title=x_col,
        yaxis_title=measure,
        height=380,
        margin=dict(l=60, r=24, t=48, b=40),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        barmode="group",
    )
    return fig


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    log.info("Explorer starting on port %d — tables: %s", PORT, list_tables())
    app.run(host="0.0.0.0", port=PORT, debug=False)
