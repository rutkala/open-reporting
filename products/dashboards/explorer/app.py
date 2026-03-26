#!/usr/bin/env python3
"""
Open Reporting — Data Explorer
Star-schema explorer over curated.all_indicators + common dimensions.
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

FACT_TABLE     = "curated.all_indicators"
MAX_PIVOT_COLS = 60
PORT           = 8051

# Columns available as pivot row/column dimensions
_PIVOT_DIMS = [
    {"label": "Domain Detail",   "value": "detail_id"},
    {"label": "Period Date",     "value": "period_date"},
    {"label": "Geographic Unit", "value": "geo"},
    {"label": "Source",          "value": "source_id"},
    {"label": "Domain",          "value": "domain_id"},
]


# ── DuckDB helpers ────────────────────────────────────────────────────────────

def _db():
    path = os.environ.get("DUCKDB_PATH", "/opt/open-reporting/data/warehouse.duckdb")
    return duckdb.connect(path, read_only=True)


_PRIMARY = "__primary__"   # sentinel value for the "primary source only" virtual option


def load_sources() -> list[dict]:
    conn = _db()
    rows = conn.execute(
        "SELECT s.source_id, s.source_name "
        "FROM curated.dim_source s "
        "WHERE EXISTS (SELECT 1 FROM curated.all_indicators ai WHERE ai.source_id = s.source_id) "
        "ORDER BY s.source_name"
    ).fetchall()
    conn.close()
    source_opts = [{"label": r[1], "value": r[0]} for r in rows]
    # Prepend the virtual "Primary" option
    return [{"label": "Primary source", "value": _PRIMARY}] + source_opts


def load_domains() -> list[dict]:
    conn = _db()
    rows = conn.execute(
        "SELECT DISTINCT domain_id, domain_name "
        "FROM curated.dim_domain_detail "
        "ORDER BY domain_name"
    ).fetchall()
    conn.close()
    return [{"label": r[1], "value": r[0]} for r in rows]


def load_details(domain_ids: list[str] | None) -> list[dict]:
    conn = _db()
    if domain_ids:
        ph = ", ".join(["?"] * len(domain_ids))
        rows = conn.execute(
            f"SELECT detail_id, detail_name FROM curated.dim_domain_detail "
            f"WHERE domain_id IN ({ph}) ORDER BY detail_name",
            domain_ids,
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT detail_id, detail_name FROM curated.dim_domain_detail ORDER BY detail_name"
        ).fetchall()
    conn.close()
    return [{"label": f"{r[1]}  ({r[0]})", "value": r[0]} for r in rows]


def load_geos() -> list[dict]:
    conn = _db()
    rows = conn.execute(
        "SELECT g.geo, g.geo_name "
        "FROM curated.dim_geo g "
        "WHERE EXISTS (SELECT 1 FROM curated.all_indicators ai WHERE ai.geo = g.geo) "
        "ORDER BY g.geo_name"
    ).fetchall()
    conn.close()
    return [{"label": r[1], "value": r[0]} for r in rows]


def run_query(
    row_dims: list[str],
    col_dim: str | None,
    agg: str,
    source_filter: list[str] | None,
    domain_filter: list[str] | None,
    detail_filter: list[str] | None,
    geo_filter: list[str] | None,
    year_from: str | None,
    year_to: str | None,
) -> pd.DataFrame:
    group_cols = list(row_dims)
    if col_dim and col_dim not in group_cols:
        group_cols.append(col_dim)

    select_parts = [f'"{c}"' for c in group_cols]
    select_parts.append(f'{agg}("value") AS value')

    use_primary = source_filter and _PRIMARY in source_filter
    # When "Primary source" is selected, join dim_primary_source to get one row per indicator
    from_clause = FACT_TABLE
    if use_primary:
        from_clause = (
            f"{FACT_TABLE} ai "
            f"JOIN curated.dim_primary_source ps "
            f"ON ai.detail_id = ps.detail_id AND ai.source_id = ps.primary_source_id"
        )
        # Prefix all column refs with ai. to avoid ambiguity after the join
        select_parts = [f'ai."{c}"' for c in group_cols]
        select_parts.append(f'{agg}(ai."value") AS value')

    sql = f'SELECT {", ".join(select_parts)} FROM {from_clause}'
    params: list = []
    conditions: list[str] = []

    if source_filter and not use_primary:
        ph = ", ".join(["?"] * len(source_filter))
        conditions.append(f'"source_id" IN ({ph})')
        params.extend(source_filter)

    # When joining dim_primary_source, prefix columns with ai. to avoid ambiguity
    col = (lambda c: f'ai."{c}"') if use_primary else (lambda c: f'"{c}"')

    if domain_filter:
        ph = ", ".join(["?"] * len(domain_filter))
        conditions.append(f'{col("domain_id")} IN ({ph})')
        params.extend(domain_filter)

    if detail_filter:
        ph = ", ".join(["?"] * len(detail_filter))
        conditions.append(f'{col("detail_id")} IN ({ph})')
        params.extend(detail_filter)

    if geo_filter:
        ph = ", ".join(["?"] * len(geo_filter))
        conditions.append(f'{col("geo")} IN ({ph})')
        params.extend(geo_filter)

    if year_from:
        conditions.append(f'{col("period_date")} >= ?')
        params.append(f"{year_from}-01-01")

    if year_to:
        conditions.append(f'{col("period_date")} <= ?')
        params.append(f"{year_to}-12-31")

    if conditions:
        sql += " WHERE " + " AND ".join(conditions)

    if group_cols:
        gb = ", ".join(col(c) for c in group_cols)
        sql += f' GROUP BY {gb} ORDER BY {gb}'

    log.info("Explorer query: %s | params: %s", sql, params)
    conn = _db()
    df = conn.execute(sql, params).df()
    conn.close()
    return df


def pivot_df(df: pd.DataFrame, row_dims: list[str], col_dim: str) -> pd.DataFrame:
    distinct = df[col_dim].nunique()
    if distinct > MAX_PIVOT_COLS:
        log.warning("Column dimension has %d distinct values — capping at %d", distinct, MAX_PIVOT_COLS)
        top = df.groupby(col_dim)["value"].sum().nlargest(MAX_PIVOT_COLS).index
        df = df[df[col_dim].isin(top)]

    index = row_dims[0] if len(row_dims) == 1 else row_dims
    result = df.pivot_table(index=index, columns=col_dim, values="value", aggfunc="sum").reset_index()
    # Convert Timestamp column names to ISO strings for JSON serialisation
    result.columns = [
        c.strftime("%Y-%m-%d") if hasattr(c, "strftime") else c
        for c in result.columns
    ]
    return result


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
        "width": "280px", "flexShrink": 0,
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
    "period_row": {"display": "flex", "gap": "8px"},
    "period_input": {
        "flex": 1, "fontSize": "12px", "padding": "6px",
        "border": f"1px solid {BORDER}", "borderRadius": "4px",
        "color": TEXT, "background": BG_PAGE,
    },
}

_dd_style = {"fontSize": "13px"}

# Pre-load static filter options at startup
_source_opts = load_sources()
_domain_opts  = load_domains()
_geo_opts     = load_geos()

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

            # — Filters —
            html.Div("Filters", style={**S["section_header"], "marginTop": 0}),

            html.Span("Source", style={**S["label"], "marginTop": 0}),
            dcc.Dropdown(id="dd-source", options=_source_opts, multi=True,
                         value=[_PRIMARY], style=_dd_style),

            html.Span("Domain", style=S["label"]),
            dcc.Dropdown(id="dd-domain", options=_domain_opts, multi=True,
                         style=_dd_style, placeholder="All domains"),

            html.Span("Domain Detail", style=S["label"]),
            dcc.Dropdown(id="dd-detail", multi=True,
                         style=_dd_style, placeholder="All indicators"),

            html.Span("Geographic Unit", style=S["label"]),
            dcc.Dropdown(id="dd-geo", options=_geo_opts, multi=True,
                         style=_dd_style, placeholder="All geographies"),

            html.Span("Period", style=S["label"]),
            html.Div(style=S["period_row"], children=[
                dcc.Input(id="year-from", type="text", placeholder="From year",
                          debounce=True, style=S["period_input"]),
                dcc.Input(id="year-to", type="text", placeholder="To year",
                          debounce=True, style=S["period_input"]),
            ]),

            # — Pivot —
            html.Div("Pivot", style=S["section_header"]),

            html.Span("Rows", style={**S["label"], "marginTop": 0}),
            dcc.Dropdown(id="dd-rows", options=_PIVOT_DIMS, multi=True,
                         value=["detail_id"], style=_dd_style),

            html.Span("Columns  (optional pivot)", style=S["label"]),
            dcc.Dropdown(id="dd-col", options=_PIVOT_DIMS, multi=False,
                         value="period_date", style=_dd_style,
                         placeholder="None — flat table"),

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
                value="AVG",
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
        ]),

        # ── Main content ──────────────────────────────────────────────────────
        html.Main(style=S["main"], children=[
            html.Div(id="output-warning"),
            html.Div(id="output-area", children=[
                html.Div(style=S["empty_state"], children=[
                    html.Div("Set filters and click Run.",
                             style={"marginBottom": "8px"}),
                    html.Div("Rows → Y-axis / table index  ·  Columns → pivot dimension  ·  Values → aggregated measure",
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
    Output("dd-detail", "options"),
    Input("dd-domain", "value"),
)
def update_detail_options(domain_vals):
    return load_details(domain_vals or None)


@callback(
    Output("output-warning", "children"),
    Output("output-area",    "children"),
    Input("btn-run", "n_clicks"),
    State("dd-rows",   "value"),
    State("dd-col",    "value"),
    State("dd-agg",    "value"),
    State("dd-source", "value"),
    State("dd-domain", "value"),
    State("dd-detail", "value"),
    State("dd-geo",    "value"),
    State("year-from", "value"),
    State("year-to",   "value"),
    prevent_initial_call=True,
)
def run_explorer(_, row_dims, col_dim, agg,
                 source_filter, domain_filter, detail_filter, geo_filter,
                 year_from, year_to):
    if not row_dims:
        return html.Div("Select at least one Row dimension.", style=S["hint"]), no_update

    try:
        df = run_query(
            row_dims, col_dim, agg,
            source_filter  or None,
            domain_filter  or None,
            detail_filter  or None,
            geo_filter     or None,
            year_from      or None,
            year_to        or None,
        )
    except Exception as e:
        return html.Div(f"Query error: {e}", style=S["warn"]), no_update

    if df.empty:
        return html.Div("No data returned. Try adjusting your filters.", style=S["hint"]), no_update

    warning_text = None
    df_flat = df.copy()

    if col_dim:
        distinct = df[col_dim].nunique()
        if distinct > MAX_PIVOT_COLS:
            warning_text = (
                f"Column dimension '{col_dim}' has {distinct} distinct values — "
                f"showing top {MAX_PIVOT_COLS} by sum."
            )
        df = pivot_df(df, row_dims, col_dim)

    # ── Table ──────────────────────────────────────────────────────────────────
    table_component = dash_table.DataTable(
        data=df.head(500).to_dict("records"),
        columns=[{"name": str(c), "id": str(c)} for c in df.columns],
        page_size=20,
        sort_action="native",
        filter_action="native",
        style_table={"overflowX": "auto"},
        style_header={
            "backgroundColor": BG_PAGE, "fontWeight": 600,
            "fontSize": "12px", "color": SUBTEXT,
            "border": f"1px solid {BORDER}",
            "textTransform": "uppercase", "letterSpacing": "0.06em",
        },
        style_cell={
            "backgroundColor": BG_SURFACE, "color": TEXT,
            "fontSize": "13px", "border": f"1px solid {BORDER}",
            "padding": "8px 12px",
            "fontFamily": "Inter, 'Segoe UI', system-ui, sans-serif",
        },
        style_data_conditional=[
            {"if": {"row_index": "odd"}, "backgroundColor": BG_PAGE},
        ],
    )

    fig = _build_chart(df_flat, row_dims, col_dim, agg)

    output = [
        html.Div(style=S["card"], children=[table_component]),
        html.Div(style=S["card"], children=[
            dcc.Graph(figure=fig, config={"displayModeBar": False}),
        ]),
    ]

    warning = html.Div(warning_text, style=S["warn"]) if warning_text else ""
    return warning, output


def _build_chart(df_flat: pd.DataFrame, row_dims: list[str],
                 col_dim: str | None, agg: str) -> go.Figure:
    fig = go.Figure()

    if col_dim and col_dim in df_flat.columns:
        series_dim  = row_dims[0] if row_dims else None
        series_vals = sorted(df_flat[series_dim].unique()) if series_dim else [None]

        for i, sv in enumerate(series_vals):
            sub = df_flat[df_flat[series_dim] == sv].sort_values(col_dim) if series_dim else df_flat
            fig.add_trace(go.Scatter(
                x=sub[col_dim], y=sub["value"],
                name=str(sv) if sv is not None else "value",
                mode="lines+markers",
                line=dict(color=COLORWAY[i % len(COLORWAY)], width=1.5),
                marker=dict(size=4),
            ))
        x_label = col_dim
    else:
        x_col  = row_dims[0] if row_dims else df_flat.columns[0]
        y_col  = "value" if "value" in df_flat.columns else df_flat.select_dtypes("number").columns[0]
        others = [d for d in row_dims if d != x_col]

        if others:
            for i, grp_val in enumerate(sorted(df_flat[others[0]].unique())):
                sub = df_flat[df_flat[others[0]] == grp_val].sort_values(x_col)
                fig.add_trace(go.Scatter(
                    x=sub[x_col], y=sub[y_col], name=str(grp_val),
                    mode="lines+markers",
                    line=dict(color=COLORWAY[i % len(COLORWAY)], width=1.5),
                    marker=dict(size=4),
                ))
        else:
            plot_df = df_flat.sort_values(x_col)
            fig.add_trace(go.Scatter(
                x=plot_df[x_col], y=plot_df[y_col],
                mode="lines+markers", name="value",
                line=dict(color=AZURE_1, width=2), marker=dict(size=5),
            ))
        x_label = x_col

    fig.update_layout(
        title=f"{agg}(value)",
        xaxis_title=x_label, yaxis_title="value",
        height=400,
        margin=dict(l=60, r=24, t=48, b=40),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02,
                    xanchor="left", x=0, font=dict(size=11)),
    )
    return fig


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    log.info("Explorer starting on port %d", PORT)
    app.run(host="0.0.0.0", port=PORT, debug=False)
