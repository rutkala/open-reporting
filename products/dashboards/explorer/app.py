#!/usr/bin/env python3
"""
Open Reporting — Data Explorer
Unified dashboard querying curated.all_indicators for all sources.

Run: PYTHONPATH=/opt/open-reporting DUCKDB_PATH=/opt/open-reporting/data/warehouse.duckdb \
     python3 products/dashboards/explorer/app.py
"""
import logging
import os

import duckdb
import pandas as pd
import plotly.graph_objects as go
from dash import ALL, Dash, Input, Output, State, callback, ctx, dash_table, dcc, html, no_update

import complex_dashboard.assets.theme as _theme  # noqa: F401 — registers nordic template
from complex_dashboard.assets.theme import (
    AZURE_1, AZURE_3, BG_PAGE, BG_SURFACE, BORDER,
    COLORWAY, SUBTEXT, TEXT, WARNING,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

FACT_TABLE     = "curated.all_indicators"
MAX_PIVOT_COLS = 60
PORT           = int(os.environ.get("OR_PORT", 8051))
_PRIMARY       = "__primary__"

# ── Semantic dimension columns ─────────────────────────────────────────────────
# All 24 named dim columns in curated.all_indicators — Polish labels for UI.

_DIM_LABELS: dict[str, str] = {
    "dim_sex":                  "Płeć",
    "dim_age_group":            "Grupa wiekowa",
    "dim_type_of_locality":     "Typ obszaru",
    "dim_nace_sector":          "Sektor NACE",
    "dim_employment_status":    "Status zatrudnienia",
    "dim_education_level":      "Poziom wykształcenia",
    "dim_prodcom_product":      "Produkt PRODCOM",
    "dim_hicp_category":        "Kategoria HICP",
    "dim_pollutant_type":       "Rodzaj zanieczyszczenia",
    "dim_waste_category":       "Kategoria odpadów",
    "dim_healthcare_function":  "Funkcja ochrony zdrowia",
    "dim_health_provider":      "Dostawca usług zdrowotnych",
    "dim_health_financing":     "Finansowanie zdrowia",
    "dim_govt_sector":          "Sektor rządowy",
    "dim_institutional_sector": "Sektor instytucjonalny",
    "dim_asset_classification": "Klasyfikacja aktywów",
    "dim_tourist_origin":       "Kraj turysty",
    "dim_trip_direction":       "Kierunek podróży",
    "dim_trip_duration":        "Czas trwania podróży",
    "dim_quintile_group":       "Kwintyl dochodowy",
    "dim_citizenship":          "Obywatelstwo",
    "dim_resources_uses":       "Zasoby / Zastosowania",
    "dim_transport_mode":       "Środek transportu",
    "dim_accommodation_type":   "Rodzaj zakwaterowania",
}

_DIM_COLS = list(_DIM_LABELS.keys())

# ── Dimension Hierarchies ──────────────────────────────────────────────────────
# Levels ordered coarsest (0) → finest (last).
# default_level: which level opens by default when this hierarchy is selected.

_HIERARCHIES: dict[str, dict] = {
    "period": {
        "label": "Okres",
        "default_level": 0,
        "levels": [
            {"label": "Rok",     "expr": "year(ai.period_date)",                                              "join": None},
            {"label": "Kwartal", "expr": "year(ai.period_date)::varchar || '-Q' || quarter(ai.period_date)::varchar", "join": None},
            {"label": "Miesiac", "expr": "strftime(ai.period_date, '%Y-%m')",                                 "join": None},
        ],
    },
    "domain": {
        "label": "Domena",
        "default_level": 2,
        "levels": [
            {"label": "Grupa_domen",     "expr": "ddd.domain_group", "join": "domain_detail"},
            {"label": "Domena",          "expr": "ddd.domain_name",  "join": "domain_detail"},
            {"label": "Szczegol_domeny", "expr": "ddd.detail_name",  "join": "domain_detail"},
        ],
    },
    "geo": {
        "label": "Jednostka geograficzna",
        "default_level": 0,
        "levels": [
            {"label": "Jednostka_geo", "expr": "ai.geo", "join": None},
        ],
    },
    "source": {
        "label": "Źródło",
        "default_level": 0,
        "levels": [
            {"label": "Zrodlo", "expr": "ai.source_id", "join": None},
        ],
    },
}

# Display labels for the drill bar (Polish, separate from internal alias labels)
_HIER_LEVEL_DISPLAY: dict[str, list[str]] = {
    "period": ["Rok", "Kwartał", "Miesiąc"],
    "domain": ["Grupa domen", "Domena", "Szczegół domeny"],
    "geo":    ["Jednostka geograficzna"],
    "source": ["Źródło"],
}

_HIER_OPTS = [{"label": v["label"], "value": k} for k, v in _HIERARCHIES.items()]


def _get_level(hier_key: str, level: int) -> dict:
    levels = _HIERARCHIES[hier_key]["levels"]
    return levels[max(0, min(level, len(levels) - 1))]


def _display_label(hier_key: str, level: int) -> str:
    labels = _HIER_LEVEL_DISPLAY.get(hier_key, [])
    return labels[max(0, min(level, len(labels) - 1))] if labels else "—"


# ── DuckDB helper ──────────────────────────────────────────────────────────────

def _db():
    path = os.environ.get("DUCKDB_PATH", "/opt/open-reporting/data/warehouse.duckdb")
    return duckdb.connect(path, read_only=True)


# ── Data loading functions ─────────────────────────────────────────────────────

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
    return [{"label": "Główne źródło", "value": _PRIMARY}] + source_opts


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


def load_available_dims(detail_filter: list[str] | None) -> list[dict]:
    """Return dim columns that have non-null values for the selected indicators.

    Uses DuckDB UNPIVOT to find populated dims in one query.
    Returns list of {col, label, options} in _DIM_COLS canonical order.
    Returns empty list when no detail_filter is provided.
    """
    if not detail_filter:
        return []

    col_list = ", ".join(_DIM_COLS)
    ph       = ", ".join(["?"] * len(detail_filter))

    sql = f"""
        SELECT col, val
        FROM (
            UNPIVOT (
                SELECT {col_list}
                FROM {FACT_TABLE}
                WHERE detail_id IN ({ph})
            )
            ON {col_list}
            INTO NAME col VALUE val
        )
        WHERE val IS NOT NULL
        GROUP BY col, val
        ORDER BY col, val
    """

    conn = _db()
    rows = conn.execute(sql, detail_filter).fetchall()
    conn.close()

    by_col: dict[str, list[str]] = {}
    for col, val in rows:
        by_col.setdefault(col, []).append(val)

    result = []
    for col in _DIM_COLS:
        if col in by_col:
            result.append({
                "col":     col,
                "label":   _DIM_LABELS[col],
                "options": [{"label": v, "value": v} for v in by_col[col]],
            })
    return result


def _resolve_agg(agg: str, detail_filter: list[str] | None) -> str:
    """Resolve 'DEFAULT' to the actual aggregation function."""
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
    row_hier:      str,
    row_level:     int,
    col_hier:      str | None,
    col_level:     int,
    agg:           str,
    source_filter: list[str] | None,
    domain_filter: list[str] | None,
    detail_filter: list[str] | None,
    geo_filter:    list[str] | None,
    year_from:     str | None,
    year_to:       str | None,
    dim_filters:   dict[str, list[str]] | None = None,
) -> tuple[pd.DataFrame, str, str | None]:
    agg = _resolve_agg(agg, detail_filter)

    row_def = _get_level(row_hier, row_level)
    col_def = _get_level(col_hier, col_level) if col_hier else None

    row_alias = row_def["label"].lower()
    col_alias = col_def["label"].lower() if col_def else None

    needed_joins: set[str] = set()
    for d in [row_def, col_def]:
        if d and d["join"]:
            needed_joins.add(d["join"])

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

    select_parts = [f'{row_def["expr"]} AS {row_alias}']
    if col_def and col_alias != row_alias:
        select_parts.append(f'{col_def["expr"]} AS {col_alias}')
    select_parts.append(f"{agg}(ai.value) AS value")

    sql = f"SELECT {', '.join(select_parts)} FROM {from_clause}"

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
    if dim_filters:
        for col, vals in dim_filters.items():
            if vals and col in _DIM_LABELS:
                ph = ", ".join(["?"] * len(vals))
                conditions.append(f"ai.{col} IN ({ph})")
                params.extend(vals)

    if conditions:
        sql += " WHERE " + " AND ".join(conditions)

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
    result.columns = [
        c.strftime("%Y-%m-%d") if hasattr(c, "strftime") else c
        for c in result.columns
    ]
    return result


# ── App ────────────────────────────────────────────────────────────────────────

app = Dash(
    __name__,
    title="Otwarte Raporty — Explorer",
    suppress_callback_exceptions=True,
    requests_pathname_prefix="/explorer/",
    routes_pathname_prefix="/explorer/",
)

# ── Styles ─────────────────────────────────────────────────────────────────────

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
        "fontSize": "12px", "color": WARNING,
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
        "minWidth": "120px", "textAlign": "center",
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

# ── Pre-load static filter options at startup ──────────────────────────────────
_source_opts = load_sources()
_domain_opts  = load_domains()
_geo_opts     = load_geos()


# ── Helpers ────────────────────────────────────────────────────────────────────

def _fmt(v: float | None) -> str:
    if v is None:
        return "—"
    if abs(v) >= 1_000_000_000:
        return f"{v / 1_000_000_000:.2f} mld"
    if abs(v) >= 1_000_000:
        return f"{v / 1_000_000:.2f} mln"
    if abs(v) >= 1_000:
        return f"{v:,.0f}".replace(",", "\u202f")
    return f"{v:.2f}"


# ── Layout ─────────────────────────────────────────────────────────────────────

app.layout = html.Div(style=S["body"], children=[

    html.Header(style=S["header"], children=[
        html.A("Otwarte Raporty", href="/",
               style={"fontSize": "15px", "fontWeight": 600, "color": TEXT,
                      "textDecoration": "none"}),
        html.Span("Explorer", style={"fontSize": "13px", "color": SUBTEXT}),
    ]),

    dcc.Store(id="store-drill",       data={"row": 2, "col": 0, "auto_run": False}),
    dcc.Store(id="store-dim-filters", data={}),

    html.Div(style=S["layout"], children=[

        html.Aside(style=S["sidebar"], children=[

            html.Div("Filtry", style={**S["section_header"], "marginTop": 0}),

            html.Span("Źródło", style={**S["label"], "marginTop": 0}),
            dcc.Dropdown(id="dd-source", options=_source_opts, multi=True,
                         value=[_PRIMARY], style=_dd_style),

            html.Span("Domena", style=S["label"]),
            dcc.Dropdown(id="dd-domain", options=_domain_opts, multi=True,
                         style=_dd_style, placeholder="Wszystkie domeny"),

            html.Span("Szczegół domeny", style=S["label"]),
            dcc.Dropdown(id="dd-detail", multi=True,
                         style=_dd_style, placeholder="Wszystkie wskaźniki"),

            html.Span("Jednostka geograficzna", style=S["label"]),
            dcc.Dropdown(id="dd-geo", options=_geo_opts, multi=True,
                         style=_dd_style, placeholder="Wszystkie obszary"),

            html.Span("Okres", style=S["label"]),
            html.Div(style=S["period_row"], children=[
                dcc.Input(id="year-from", type="text", placeholder="Od roku",
                          debounce=True, style=S["period_input"]),
                dcc.Input(id="year-to", type="text", placeholder="Do roku",
                          debounce=True, style=S["period_input"]),
            ]),

            # Dynamic dimension filters — rendered by update_dim_filters callback
            html.Div(id="dim-filters-container"),

            html.Div("Pivot", style=S["section_header"]),

            html.Span("Wiersze", style={**S["label"], "marginTop": 0}),
            dcc.Dropdown(id="dd-row-hier", options=_HIER_OPTS, multi=False,
                         value="domain", clearable=False, style=_dd_style),

            html.Span("Kolumny (opcjonalny pivot)", style=S["label"]),
            dcc.Dropdown(id="dd-col-hier", options=_HIER_OPTS, multi=False,
                         value="period", style=_dd_style,
                         placeholder="Brak — płaska tabela"),

            html.Span("Agregacja", style=S["label"]),
            dcc.Dropdown(
                id="dd-agg",
                options=[
                    {"label": "Domyślna (wg wskaźnika)", "value": "DEFAULT"},
                    {"label": "Średnia",                 "value": "AVG"},
                    {"label": "Suma",                    "value": "SUM"},
                    {"label": "Minimum",                 "value": "MIN"},
                    {"label": "Maksimum",                "value": "MAX"},
                    {"label": "Liczba",                  "value": "COUNT"},
                ],
                value="DEFAULT",
                clearable=False,
                style=_dd_style,
            ),

            html.Div(style={"marginTop": "20px"}, children=[
                html.Button("Uruchom", id="btn-run",
                            style={
                                "width": "100%", "padding": "8px",
                                "background": AZURE_1, "color": "#fff",
                                "border": "none", "borderRadius": "4px",
                                "fontSize": "13px", "fontWeight": 600,
                                "cursor": "pointer",
                            }),
            ]),
        ]),

        html.Main(style=S["main"], children=[

            html.Div(style=S["drill_bar"], children=[
                html.Div(style=S["drill_axis"], children=[
                    html.Span("Wiersze", style=S["drill_axis_label"]),
                    html.Button("◄", id="btn-row-up",   style=_DRILL_BTN_BASE),
                    html.Span(id="row-level-label",     style=S["drill_level_label"]),
                    html.Button("►", id="btn-row-down", style=_DRILL_BTN_BASE),
                ]),
                html.Span("·", style={"color": BORDER, "fontSize": "18px"}),
                html.Div(style=S["drill_axis"], children=[
                    html.Span("Kolumny", style=S["drill_axis_label"]),
                    html.Button("◄", id="btn-col-up",   style=_DRILL_BTN_BASE),
                    html.Span(id="col-level-label",     style=S["drill_level_label"]),
                    html.Button("►", id="btn-col-down", style=_DRILL_BTN_BASE),
                ]),
            ]),

            html.Div(id="output-warning"),
            html.Div(id="output-area", children=[
                html.Div(style=S["empty_state"], children=[
                    html.Div("Ustaw filtry i kliknij Uruchom.",
                             style={"marginBottom": "8px"}),
                    html.Div(
                        "Przyciski ◄ ► na pasku powyżej umożliwiają nawigację "
                        "po poziomach hierarchii — wyniki aktualizują się natychmiast.",
                        style={"fontSize": "12px", "color": SUBTEXT},
                    ),
                ]),
            ]),
        ]),
    ]),

    html.Footer(style=S["footer"], children=[
        html.Span(
            "Open Reporting — eksplorator danych · Źródła: Eurostat, NBP, GUS DBW HVD"
        ),
    ]),
])


# ── Callbacks ──────────────────────────────────────────────────────────────────

@callback(
    Output("dd-detail", "options"),
    Input("dd-domain", "value"),
)
def update_detail_options(domain_vals):
    return load_details(domain_vals or None)


@callback(
    Output("dim-filters-container", "children"),
    Input("dd-detail", "value"),
)
def update_dim_filters(detail_vals):
    """Render dimension filter dropdowns for dims populated in selected indicators."""
    if not detail_vals:
        return []

    dims = load_available_dims(detail_vals)
    if not dims:
        return []

    children = [html.Div("Wymiary", style=S["section_header"])]
    for d in dims:
        children.append(
            html.Span(d["label"], style={**S["label"], "marginTop": "10px"})
        )
        children.append(
            dcc.Dropdown(
                id={"type": "dim-filter", "col": d["col"]},
                options=d["options"],
                multi=True,
                placeholder="Wszystkie",
                style=_dd_style,
            )
        )
    return children


@callback(
    Output("store-dim-filters", "data"),
    Input({"type": "dim-filter", "col": ALL}, "value"),
    prevent_initial_call=True,
)
def sync_dim_filter_store(values):
    """Sync all active dim filter dropdowns into a flat dict store."""
    result = {}
    for inp in ctx.inputs_list[0]:
        col = inp["id"]["col"]
        val = inp.get("value") or []
        if val:
            result[col] = val
    return result


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
    triggered = ctx.triggered_id
    row       = drill["row"]
    col       = drill["col"]
    row_max   = len(_HIERARCHIES[row_hier]["levels"]) - 1
    col_max   = len(_HIERARCHIES[col_hier]["levels"]) - 1 if col_hier else 0
    auto_run  = False

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

    row_label = _display_label(row_hier, row_level)
    col_label = _display_label(col_hier, col_level) if col_hier else "—"

    return (
        row_label,
        col_label,
        row_level <= 0,
        row_level >= len(row_levels) - 1,
        not col_hier or col_level <= 0,
        not col_hier or col_level >= len(col_levels) - 1,
    )


@callback(
    Output("output-warning",   "children"),
    Output("output-area",      "children"),
    Input("btn-run",           "n_clicks"),
    Input("store-drill",       "data"),
    State("dd-row-hier",       "value"),
    State("dd-col-hier",       "value"),
    State("dd-agg",            "value"),
    State("dd-source",         "value"),
    State("dd-domain",         "value"),
    State("dd-detail",         "value"),
    State("dd-geo",            "value"),
    State("year-from",         "value"),
    State("year-to",           "value"),
    State("store-dim-filters", "data"),
    prevent_initial_call=True,
)
def run_explorer(_, drill, row_hier, col_hier, agg,
                 source_filter, domain_filter, detail_filter, geo_filter,
                 year_from, year_to, dim_filters):
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
            dim_filters   or None,
        )
    except Exception as e:
        return html.Div(f"Błąd zapytania: {e}", style=S["warn"]), no_update

    if df.empty:
        return html.Div("Brak danych dla wybranych filtrów.", style=S["hint"]), no_update

    row_def = _get_level(row_hier, row_level)
    col_def = _get_level(col_hier, col_level) if col_hier else None

    warning_text = None
    df_flat = df.copy()

    if col_col and col_col in df.columns:
        distinct = df[col_col].nunique()
        if distinct > MAX_PIVOT_COLS:
            warning_text = (
                f"Wymiar kolumn '{_display_label(col_hier, col_level)}' ma {distinct} wartości — "
                f"pokazuję top {MAX_PIVOT_COLS} wg sumy."
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

    fig = _build_explorer_chart(
        df_flat, row_col, col_col,
        _display_label(row_hier, row_level),
        _display_label(col_hier, col_level) if col_def else None,
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


def _build_explorer_chart(
    df_flat:   pd.DataFrame,
    row_col:   str,
    col_col:   str | None,
    row_label: str,
    col_label: str | None,
    agg:       str,
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
            mode="lines+markers", name="wartość",
            line=dict(color=AZURE_1, width=2), marker=dict(size=5),
        ))
        x_label = row_label

    fig.update_layout(
        title=f"{agg}(wartość)",
        xaxis_title=x_label, yaxis_title="wartość",
        height=400,
        margin=dict(l=60, r=24, t=48, b=40),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02,
                    xanchor="left", x=0, font=dict(size=11)),
    )
    return fig


# ── Entry point ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=PORT)
