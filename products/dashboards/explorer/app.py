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
from dash import Dash, Input, Output, State, callback, ctx, dash_table, dcc, html, no_update

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
_PRIMARY       = "__primary__"

# ── Dimension Hierarchies ─────────────────────────────────────────────────────
# Levels ordered coarsest (0) → finest (last).
# default_level: which level opens by default when this hierarchy is selected.
# join: which dimension table alias to LEFT JOIN (None = no extra join needed).

_HIERARCHIES: dict[str, dict] = {
    "period": {
        "label": "Period",
        "default_level": 0,
        "levels": [
            {
                "label": "Year",
                "expr":  "year(ai.period_date)",
                "join":  None,
            },
            {
                "label": "Quarter",
                "expr":  "year(ai.period_date)::varchar || '-Q' || quarter(ai.period_date)::varchar",
                "join":  None,
            },
            {
                "label": "Month",
                "expr":  "strftime(ai.period_date, '%Y-%m')",
                "join":  None,
            },
        ],
    },
    "domain": {
        "label": "Domain",
        "default_level": 2,
        "levels": [
            {"label": "Domain Group",  "expr": "ddd.domain_group", "join": "domain_detail"},
            {"label": "Domain",        "expr": "ddd.domain_name",  "join": "domain_detail"},
            {"label": "Domain Detail", "expr": "ddd.detail_name",  "join": "domain_detail"},
        ],
    },
    "geo": {
        "label": "Geographic Unit",
        "default_level": 0,
        "levels": [
            {"label": "Geographic Unit", "expr": "ai.geo", "join": None},
        ],
    },
    "source": {
        "label": "Source",
        "default_level": 0,
        "levels": [
            {"label": "Source", "expr": "ai.source_id", "join": None},
        ],
    },
}

_HIER_OPTS = [{"label": v["label"], "value": k} for k, v in _HIERARCHIES.items()]


def _get_level(hier_key: str, level: int) -> dict:
    levels = _HIERARCHIES[hier_key]["levels"]
    return levels[max(0, min(level, len(levels) - 1))]


def _col_alias(label: str) -> str:
    """Convert a level label to a safe DataFrame column name."""
    return label.lower().replace(" ", "_")


# ── DuckDB helpers ─────────────────────────────────────────────────────────────

def _db():
    path = os.environ.get("DUCKDB_PATH", "/opt/open-reporting/data/warehouse.duckdb")
    return duckdb.connect(path, read_only=True)


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


def _resolve_agg(agg: str, detail_filter: list[str] | None) -> str:
    """Resolve 'DEFAULT' to the actual aggregation function.

    Queries dim_domain_detail for the default_agg of the filtered indicators.
    If all agree → use that. If mixed or no filter → AVG.
    """
    if agg != "DEFAULT":
        return agg
    if not detail_filter:
        return "AVG"
    conn = _db()
    ph = ", ".join(["?"] * len(detail_filter))
    rows = conn.execute(
        f"SELECT DISTINCT default_agg FROM curated.dim_domain_detail "
        f"WHERE detail_id IN ({ph}) AND default_agg IS NOT NULL",
        detail_filter,
    ).fetchall()
    conn.close()
    distinct = {r[0] for r in rows}
    return distinct.pop() if len(distinct) == 1 else "AVG"


def run_query(
    row_hier:  str,
    row_level: int,
    col_hier:  str | None,
    col_level: int,
    agg: str,
    source_filter: list[str] | None,
    domain_filter: list[str] | None,
    detail_filter: list[str] | None,
    geo_filter:    list[str] | None,
    year_from: str | None,
    year_to:   str | None,
) -> tuple[pd.DataFrame, str, str | None]:
    agg = _resolve_agg(agg, detail_filter)

    row_def = _get_level(row_hier, row_level)
    col_def = _get_level(col_hier, col_level) if col_hier else None

    row_alias = _col_alias(row_def["label"])
    col_alias = _col_alias(col_def["label"]) if col_def else None

    # Determine which dimension table JOINs are required
    needed_joins: set[str] = set()
    for d in [row_def, col_def]:
        if d and d["join"]:
            needed_joins.add(d["join"])

    # Build FROM — always alias fact table as ai
    use_primary = bool(source_filter and _PRIMARY in source_filter)
    joins: list[str] = []
    if use_primary:
        joins.append(
            "JOIN curated.dim_primary_source ps "
            "ON ai.detail_id = ps.detail_id AND ai.source_id = ps.primary_source_id"
        )
    if "domain_detail" in needed_joins:
        joins.append(
            "LEFT JOIN curated.dim_domain_detail ddd ON ai.detail_id = ddd.detail_id"
        )
    from_clause = f"{FACT_TABLE} ai " + " ".join(joins)

    # SELECT: expr AS alias for each dimension, then the aggregate
    select_parts = [f'{row_def["expr"]} AS {row_alias}']
    if col_def and col_alias != row_alias:
        select_parts.append(f'{col_def["expr"]} AS {col_alias}')
    select_parts.append(f"{agg}(ai.value) AS value")

    sql = f"SELECT {', '.join(select_parts)} FROM {from_clause}"

    # WHERE — always use ai. prefix for fact columns
    params: list = []
    conditions: list[str] = []

    if source_filter and not use_primary:
        ph = ", ".join(["?"] * len(source_filter))
        conditions.append(f"ai.source_id IN ({ph})")
        params.extend(source_filter)
    if domain_filter:
        ph = ", ".join(["?"] * len(domain_filter))
        conditions.append(f"ai.domain_id IN ({ph})")
        params.extend(domain_filter)
    if detail_filter:
        ph = ", ".join(["?"] * len(detail_filter))
        conditions.append(f"ai.detail_id IN ({ph})")
        params.extend(detail_filter)
    if geo_filter:
        ph = ", ".join(["?"] * len(geo_filter))
        conditions.append(f"ai.geo IN ({ph})")
        params.extend(geo_filter)
    if year_from:
        conditions.append("ai.period_date >= ?")
        params.append(f"{year_from}-01-01")
    if year_to:
        conditions.append("ai.period_date <= ?")
        params.append(f"{year_to}-12-31")

    if conditions:
        sql += " WHERE " + " AND ".join(conditions)

    # GROUP BY / ORDER BY using original expressions (not aliases)
    group_exprs: list[str] = [row_def["expr"]]
    if col_def and col_alias != row_alias:
        group_exprs.append(col_def["expr"])
    gb = ", ".join(group_exprs)
    sql += f" GROUP BY {gb} ORDER BY {gb}"

    log.info("Explorer query: %s | params: %s", sql, params)
    conn = _db()
    df = conn.execute(sql, params).df()
    conn.close()
    return df, row_alias, col_alias


def pivot_df(df: pd.DataFrame, row_col: str, col_col: str) -> pd.DataFrame:
    distinct = df[col_col].nunique()
    if distinct > MAX_PIVOT_COLS:
        log.warning("Column dimension has %d distinct values — capping at %d", distinct, MAX_PIVOT_COLS)
        top = df.groupby(col_col)["value"].sum().nlargest(MAX_PIVOT_COLS).index
        df = df[df[col_col].isin(top)]

    result = df.pivot_table(
        index=row_col, columns=col_col, values="value", aggfunc="sum"
    ).reset_index()
    # Convert Timestamp column names to ISO strings for JSON serialisation
    result.columns = [
        c.strftime("%Y-%m-%d") if hasattr(c, "strftime") else c
        for c in result.columns
    ]
    return result


# ── App ───────────────────────────────────────────────────────────────────────

app = Dash(
    __name__,
    title="Otwarte Raporty — Explorer",
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
    # Drill bar
    "drill_bar": {
        "display": "flex", "alignItems": "center", "gap": "20px",
        "justifyContent": "flex-end",
        "padding": "8px 14px", "marginBottom": "16px",
        "background": BG_SURFACE, "borderRadius": "6px",
        "border": f"1px solid {BORDER}",
    },
    "drill_axis": {
        "display": "flex", "alignItems": "center", "gap": "6px",
    },
    "drill_axis_label": {
        "fontSize": "10px", "fontWeight": 700, "textTransform": "uppercase",
        "letterSpacing": "0.08em", "color": SUBTEXT, "marginRight": "4px",
    },
    "drill_level_label": {
        "fontSize": "12px", "fontWeight": 600, "color": TEXT,
        "minWidth": "96px", "textAlign": "center",
    },
}

_DRILL_BTN_BASE = {
    "background": "none",
    "border": f"1px solid {BORDER}",
    "borderRadius": "3px",
    "padding": "2px 9px",
    "fontSize": "13px",
    "lineHeight": "18px",
    "cursor": "pointer",
    "color": TEXT,
}

_dd_style = {"fontSize": "13px"}

# Pre-load static filter options at startup
_source_opts = load_sources()
_domain_opts  = load_domains()
_geo_opts     = load_geos()

# ── Layout ────────────────────────────────────────────────────────────────────

app.layout = html.Div(style=S["body"], children=[

    # Stores current drill level per axis.
    # auto_run flag: True when drill buttons trigger the change (auto-reruns query);
    # False when hierarchy dropdown changes (user must click Run to apply).
    dcc.Store(id="store-drill", data={"row": 2, "col": 0, "auto_run": False}),

    html.Header(style=S["header"], children=[
        html.A("Otwarte Raporty", href="/",
               style={"fontSize": "15px", "fontWeight": 600, "color": TEXT,
                      "textDecoration": "none"}),
        html.Span("Explorer", style={"fontSize": "13px", "color": SUBTEXT}),
    ]),

    html.Div(style=S["layout"], children=[

        # ── Sidebar ───────────────────────────────────────────────────────────
        html.Aside(style=S["sidebar"], children=[

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

            html.Div("Pivot", style=S["section_header"]),

            html.Span("Rows", style={**S["label"], "marginTop": 0}),
            dcc.Dropdown(id="dd-row-hier", options=_HIER_OPTS, multi=False,
                         value="domain", clearable=False, style=_dd_style),

            html.Span("Columns  (optional pivot)", style=S["label"]),
            dcc.Dropdown(id="dd-col-hier", options=_HIER_OPTS, multi=False,
                         value="period", style=_dd_style,
                         placeholder="None — flat table"),

            html.Span("Aggregation", style=S["label"]),
            dcc.Dropdown(
                id="dd-agg",
                options=[
                    {"label": "Default (per indicator)", "value": "DEFAULT"},
                    {"label": "Average",                 "value": "AVG"},
                    {"label": "Sum",                     "value": "SUM"},
                    {"label": "Min",                     "value": "MIN"},
                    {"label": "Max",                     "value": "MAX"},
                    {"label": "Count",                   "value": "COUNT"},
                ],
                value="DEFAULT",
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

            # Drill bar — always visible above results
            html.Div(style=S["drill_bar"], children=[
                html.Div(style=S["drill_axis"], children=[
                    html.Span("Rows", style=S["drill_axis_label"]),
                    html.Button("◄", id="btn-row-up",   style=_DRILL_BTN_BASE),
                    html.Span(id="row-level-label",     style=S["drill_level_label"]),
                    html.Button("►", id="btn-row-down", style=_DRILL_BTN_BASE),
                ]),
                html.Span("·", style={"color": BORDER, "fontSize": "18px"}),
                html.Div(style=S["drill_axis"], children=[
                    html.Span("Columns", style=S["drill_axis_label"]),
                    html.Button("◄", id="btn-col-up",   style=_DRILL_BTN_BASE),
                    html.Span(id="col-level-label",     style=S["drill_level_label"]),
                    html.Button("►", id="btn-col-down", style=_DRILL_BTN_BASE),
                ]),
            ]),

            html.Div(id="output-warning"),
            html.Div(id="output-area", children=[
                html.Div(style=S["empty_state"], children=[
                    html.Div("Set filters and click Run.",
                             style={"marginBottom": "8px"}),
                    html.Div(
                        "◄ ► in the drill bar above navigate hierarchy levels — "
                        "results update instantly.",
                        style={"fontSize": "12px", "color": SUBTEXT},
                    ),
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
    Output("store-drill", "data"),
    Input("btn-row-up",   "n_clicks"),
    Input("btn-row-down", "n_clicks"),
    Input("btn-col-up",   "n_clicks"),
    Input("btn-col-down", "n_clicks"),
    Input("dd-row-hier",  "value"),
    Input("dd-col-hier",  "value"),
    State("store-drill",  "data"),
    prevent_initial_call=True,
)
def update_drill(_, __, ___, ____, row_hier, col_hier, drill):
    triggered  = ctx.triggered_id
    row        = drill["row"]
    col        = drill["col"]
    row_max    = len(_HIERARCHIES[row_hier]["levels"]) - 1
    col_max    = len(_HIERARCHIES[col_hier]["levels"]) - 1 if col_hier else 0
    auto_run   = False

    if triggered == "btn-row-up":
        row = max(0, row - 1)
        auto_run = True
    elif triggered == "btn-row-down":
        row = min(row_max, row + 1)
        auto_run = True
    elif triggered == "btn-col-up":
        col = max(0, col - 1)
        auto_run = True
    elif triggered == "btn-col-down":
        col = min(col_max, col + 1)
        auto_run = True
    elif triggered == "dd-row-hier":
        row = _HIERARCHIES[row_hier]["default_level"]
    elif triggered == "dd-col-hier":
        col = _HIERARCHIES[col_hier]["default_level"] if col_hier else 0

    return {"row": min(row, row_max), "col": min(col, col_max), "auto_run": auto_run}


@callback(
    Output("row-level-label", "children"),
    Output("col-level-label", "children"),
    Output("btn-row-up",   "disabled"),
    Output("btn-row-down", "disabled"),
    Output("btn-col-up",   "disabled"),
    Output("btn-col-down", "disabled"),
    Input("store-drill", "data"),
    State("dd-row-hier", "value"),
    State("dd-col-hier", "value"),
)
def update_drill_display(drill, row_hier, col_hier):
    row_level  = drill["row"]
    col_level  = drill["col"]
    row_levels = _HIERARCHIES[row_hier]["levels"]
    col_levels = _HIERARCHIES[col_hier]["levels"] if col_hier else []

    row_label = row_levels[row_level]["label"]
    col_label = col_levels[col_level]["label"] if col_levels else "—"

    return (
        row_label,
        col_label,
        row_level <= 0,
        row_level >= len(row_levels) - 1,
        not col_hier or col_level <= 0,
        not col_hier or col_level >= len(col_levels) - 1,
    )


@callback(
    Output("output-warning", "children"),
    Output("output-area",    "children"),
    Input("btn-run",     "n_clicks"),
    Input("store-drill", "data"),
    State("dd-row-hier", "value"),
    State("dd-col-hier", "value"),
    State("dd-agg",      "value"),
    State("dd-source",   "value"),
    State("dd-domain",   "value"),
    State("dd-detail",   "value"),
    State("dd-geo",      "value"),
    State("year-from",   "value"),
    State("year-to",     "value"),
    prevent_initial_call=True,
)
def run_explorer(_, drill, row_hier, col_hier, agg,
                 source_filter, domain_filter, detail_filter, geo_filter,
                 year_from, year_to):
    # Drill store changes only auto-run when triggered by drill buttons
    if ctx.triggered_id == "store-drill" and not drill.get("auto_run", False):
        return no_update, no_update

    row_level = drill["row"]
    col_level = drill["col"]

    try:
        df, row_col, col_col = run_query(
            row_hier,  row_level,
            col_hier,  col_level,
            agg,
            source_filter or None,
            domain_filter or None,
            detail_filter or None,
            geo_filter    or None,
            year_from     or None,
            year_to       or None,
        )
    except Exception as e:
        return html.Div(f"Query error: {e}", style=S["warn"]), no_update

    if df.empty:
        return html.Div("No data returned. Try adjusting your filters.", style=S["hint"]), no_update

    row_def = _get_level(row_hier, row_level)
    col_def = _get_level(col_hier, col_level) if col_hier else None

    warning_text = None
    df_flat = df.copy()

    if col_col and col_col in df.columns:
        distinct = df[col_col].nunique()
        if distinct > MAX_PIVOT_COLS:
            warning_text = (
                f"Column dimension '{col_def['label']}' has {distinct} distinct values — "
                f"showing top {MAX_PIVOT_COLS} by sum."
            )
        df = pivot_df(df, row_col, col_col)

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

    fig = _build_chart(
        df_flat, row_col, col_col,
        row_def["label"],
        col_def["label"] if col_def else None,
        agg,
    )

    output = [
        html.Div(style=S["card"], children=[table_component]),
        html.Div(style=S["card"], children=[
            dcc.Graph(figure=fig, config={"displayModeBar": False}),
        ]),
    ]

    warning = html.Div(warning_text, style=S["warn"]) if warning_text else ""
    return warning, output


def _build_chart(
    df_flat:   pd.DataFrame,
    row_col:   str,
    col_col:   str | None,
    row_label: str,
    col_label: str | None,
    agg: str,
) -> go.Figure:
    fig = go.Figure()

    if col_col and col_col in df_flat.columns:
        for i, sv in enumerate(sorted(df_flat[row_col].unique())):
            sub = df_flat[df_flat[row_col] == sv].sort_values(col_col)
            fig.add_trace(go.Scatter(
                x=sub[col_col], y=sub["value"],
                name=str(sv),
                mode="lines+markers",
                line=dict(color=COLORWAY[i % len(COLORWAY)], width=1.5),
                marker=dict(size=4),
            ))
        x_label = col_label or col_col
    else:
        y_col = "value" if "value" in df_flat.columns else df_flat.select_dtypes("number").columns[0]
        plot_df = df_flat.sort_values(row_col)
        fig.add_trace(go.Scatter(
            x=plot_df[row_col], y=plot_df[y_col],
            mode="lines+markers", name="value",
            line=dict(color=AZURE_1, width=2), marker=dict(size=5),
        ))
        x_label = row_label

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
