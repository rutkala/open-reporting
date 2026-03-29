#!/usr/bin/env python3
"""
Open Reporting — Data Explorer
Two-tab dashboard:
  - Explorer: star-schema pivot over curated.all_indicators
  - DBW HVD:  time-series browser for 85 GUS DBW HVD variables

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
    COLORWAY, NEGATIVE, POSITIVE, SUBTEXT, TEXT,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

FACT_TABLE     = "curated.all_indicators"
MAX_PIVOT_COLS = 60
PORT           = 8051
_PRIMARY       = "__primary__"

# ── Dimension Hierarchies (Explorer tab) ──────────────────────────────────────
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


# ── Explorer tab — data functions ─────────────────────────────────────────────

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


# ── DBW HVD tab — data functions ───────────────────────────────────────────────

def load_dbw_variables() -> list[dict]:
    """Load all 85 DBW variable metadata rows."""
    conn = _db()
    rows = conn.execute(
        "SELECT variable_id, variable_name, section_id, category "
        "FROM raw.dbw_variables ORDER BY category, variable_name"
    ).fetchall()
    conn.close()
    return [
        {
            "variable_id":   r[0],
            "variable_name": r[1] or str(r[0]),
            "section_id":    r[2],
            "category":      r[3] or "Inne",
        }
        for r in rows
    ]


def _build_dbw_variable_opts(variables: list[dict], category: str | None) -> list[dict]:
    filtered = [v for v in variables if category is None or v["category"] == category]
    return [
        {"label": v["variable_name"], "value": str(v["variable_id"])}
        for v in filtered
    ]


def load_dbw_dim_panels(variable_id: int, section_id: int) -> list[dict]:
    """Return active dimension slots for the selected variable+section.

    Returns up to 3 dicts: {slot, col, dim_name, options}.
    A slot is "active" when it has >1 distinct non-zero position value.
    """
    conn = _db()

    counts = conn.execute("""
        SELECT
            COUNT(DISTINCT CASE WHEN dim1_id != 0 THEN dim1_id END),
            COUNT(DISTINCT CASE WHEN dim2_id != 0 THEN dim2_id END),
            COUNT(DISTINCT CASE WHEN dim3_id != 0 THEN dim3_id END)
        FROM raw.dbw_observations
        WHERE variable_id = ? AND section_id = ?
    """, [variable_id, section_id]).fetchone()

    result = []
    for slot_idx, (col, cnt) in enumerate(
        zip(["dim1_id", "dim2_id", "dim3_id"], counts), 1
    ):
        if not cnt or cnt <= 1:
            continue

        opts_rows = conn.execute(f"""
            SELECT DISTINCT o.{col} AS pos_id, p.position_name, p.dim_name
            FROM raw.dbw_observations o
            JOIN raw.dbw_positions p
                ON p.section_id = o.section_id AND p.position_id = o.{col}
            WHERE o.variable_id = ? AND o.section_id = ? AND o.{col} != 0
            ORDER BY p.position_name
        """, [variable_id, section_id]).fetchall()

        if not opts_rows:
            continue

        dim_name = opts_rows[0][2] or f"Wymiar {slot_idx}"
        options  = [{"label": r[1] or str(r[0]), "value": str(r[0])} for r in opts_rows]

        result.append({
            "slot":     slot_idx,
            "col":      col,
            "dim_name": dim_name,
            "options":  options,
        })

    conn.close()
    return result


_VALID_DIM_COLS = frozenset({"dim1_id", "dim2_id", "dim3_id", "dim4_id", "dim5_id", "dim6_id"})


def run_dbw_query(
    variable_id:  int,
    section_id:   int,
    split_col:    str | None,
    filter_cols:  dict[str, list[str]],
    year_from:    str | None,
    year_to:      str | None,
) -> pd.DataFrame:
    """Query DBW observations.

    split_col: dim slot column to split chart lines by (e.g. "dim2_id").
    filter_cols: {col: [pos_id_str]} — restrict to selected position values.
    Returns DataFrame with columns: year, (dim_label if split_col), value.
    """
    if split_col and split_col not in _VALID_DIM_COLS:
        raise ValueError(f"Invalid split_col: {split_col!r}")
    for col in filter_cols:
        if col not in _VALID_DIM_COLS:
            raise ValueError(f"Invalid filter col: {col!r}")

    conn = _db()

    where  = ["o.variable_id = ?", "o.section_id = ?"]
    params: list = [variable_id, section_id]

    for col, vals in filter_cols.items():
        if vals:
            ph = ", ".join(["?"] * len(vals))
            where.append(f"o.{col} IN ({ph})")
            params.extend(int(v) for v in vals)

    if year_from:
        where.append("o.year >= ?")
        params.append(int(year_from))
    if year_to:
        where.append("o.year <= ?")
        params.append(int(year_to))

    where_sql = " AND ".join(where)

    if split_col:
        sql = f"""
            SELECT o.year,
                   COALESCE(p.position_name, o.{split_col}::varchar) AS dim_label,
                   SUM(o.value) AS value
            FROM raw.dbw_observations o
            LEFT JOIN raw.dbw_positions p
                ON p.section_id = o.section_id AND p.position_id = o.{split_col}
            WHERE {where_sql}
            GROUP BY o.year, dim_label
            ORDER BY o.year, dim_label
        """
    else:
        sql = f"""
            SELECT o.year, SUM(o.value) AS value
            FROM raw.dbw_observations o
            WHERE {where_sql}
            GROUP BY o.year
            ORDER BY o.year
        """

    log.info("DBW query: variable=%s section=%s split=%s filter=%s",
             variable_id, section_id, split_col, filter_cols)
    df = conn.execute(sql, params).df()
    conn.close()
    return df


def _compute_dbw_kpis(df: pd.DataFrame) -> dict:
    """Compute KPI values from a DBW observations DataFrame."""
    if df.empty:
        return {}

    by_year = df.groupby("year")["value"].sum().dropna().sort_index()
    if by_year.empty:
        return {}

    latest_year = int(by_year.index[-1])
    latest_val  = float(by_year.iloc[-1])

    yoy_pct = None
    if len(by_year) >= 2:
        prev_val = float(by_year.iloc[-2])
        if prev_val != 0:
            yoy_pct = (latest_val - prev_val) / abs(prev_val) * 100

    return {
        "latest_year": latest_year,
        "latest_val":  latest_val,
        "yoy_pct":     yoy_pct,
        "max_val":     float(by_year.max()),
        "min_val":     float(by_year.min()),
    }


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
    "kpi_row": {
        "display": "flex", "gap": "16px", "marginBottom": "20px", "flexWrap": "wrap",
    },
    "kpi_card": {
        "background": BG_SURFACE, "borderRadius": "6px",
        "boxShadow": "0 1px 4px rgba(0,0,0,0.07), 0 0 1px rgba(0,0,0,0.04)",
        "padding": "16px 20px", "flex": "1", "minWidth": "140px",
    },
    "kpi_label": {
        "fontSize": "10px", "fontWeight": 700, "textTransform": "uppercase",
        "letterSpacing": "0.08em", "color": SUBTEXT, "marginBottom": "8px",
    },
    "kpi_value": {
        "fontSize": "22px", "fontWeight": 700, "lineHeight": "1.1",
    },
    "kpi_sub": {
        "fontSize": "11px", "color": SUBTEXT, "marginTop": "4px",
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

_TAB_STYLE = {
    "padding": "10px 24px",
    "fontSize": "13px",
    "fontWeight": 500,
    "color": SUBTEXT,
    "borderBottom": f"2px solid transparent",
    "background": BG_SURFACE,
}
_TAB_SELECTED_STYLE = {
    **_TAB_STYLE,
    "color": AZURE_1,
    "fontWeight": 700,
    "borderBottom": f"2px solid {AZURE_1}",
}

# ── Pre-load static filter options at startup ──────────────────────────────────
_source_opts = load_sources()
_domain_opts  = load_domains()
_geo_opts     = load_geos()

_dbw_vars        = load_dbw_variables()
_dbw_categories  = sorted({v["category"] for v in _dbw_vars if v["category"]})
_dbw_cat_opts    = [{"label": c, "value": c} for c in _dbw_categories]
_dbw_var_opts    = _build_dbw_variable_opts(_dbw_vars, None)


# ── Layout helpers ─────────────────────────────────────────────────────────────

def _kpi_card(label: str, value_str: str, sub: str = "", value_color: str = TEXT) -> html.Div:
    return html.Div(style=S["kpi_card"], children=[
        html.Div(label,     style=S["kpi_label"]),
        html.Div(value_str, style={**S["kpi_value"], "color": value_color}),
        html.Div(sub,       style=S["kpi_sub"]),
    ])


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

    dcc.Tabs(
        id="main-tabs",
        value="explorer",
        style={
            "background": BG_SURFACE,
            "borderBottom": f"1px solid {BORDER}",
            "flexShrink": 0,
        },
        children=[

            # ── Tab 1: Explorer ────────────────────────────────────────────────
            dcc.Tab(
                label="Explorer",
                value="explorer",
                style=_TAB_STYLE,
                selected_style=_TAB_SELECTED_STYLE,
                children=[
                    dcc.Store(id="store-drill", data={"row": 2, "col": 0, "auto_run": False}),

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
                        html.Span("Open Reporting — wewnętrzny eksplorator danych"),
                    ]),
                ],
            ),

            # ── Tab 2: DBW HVD ─────────────────────────────────────────────────
            dcc.Tab(
                label="DBW HVD",
                value="dbw",
                style=_TAB_STYLE,
                selected_style=_TAB_SELECTED_STYLE,
                children=[
                    dcc.Store(id="dbw-variable-meta"),

                    html.Div(style=S["layout"], children=[

                        html.Aside(style=S["sidebar"], children=[

                            html.Div("Wskaźnik", style={**S["section_header"], "marginTop": 0}),

                            html.Span("Kategoria", style={**S["label"], "marginTop": 0}),
                            dcc.Dropdown(
                                id="dd-dbw-category",
                                options=_dbw_cat_opts,
                                clearable=True,
                                placeholder="Wszystkie kategorie",
                                style=_dd_style,
                            ),

                            html.Span("Wskaźnik", style=S["label"]),
                            dcc.Dropdown(
                                id="dd-dbw-variable",
                                options=_dbw_var_opts,
                                clearable=True,
                                placeholder="Wybierz wskaźnik…",
                                style=_dd_style,
                            ),

                            html.Div("Wymiary", style=S["section_header"]),

                            html.Div(id="dbw-dim-1-container", style={"display": "none"}, children=[
                                html.Span(id="dbw-dim-1-label", style=S["label"]),
                                dcc.Dropdown(id="dbw-dim-1", multi=True,
                                             placeholder="Wszystkie", style=_dd_style),
                            ]),
                            html.Div(id="dbw-dim-2-container", style={"display": "none"}, children=[
                                html.Span(id="dbw-dim-2-label", style=S["label"]),
                                dcc.Dropdown(id="dbw-dim-2", multi=True,
                                             placeholder="Wszystkie", style=_dd_style),
                            ]),
                            html.Div(id="dbw-dim-3-container", style={"display": "none"}, children=[
                                html.Span(id="dbw-dim-3-label", style=S["label"]),
                                dcc.Dropdown(id="dbw-dim-3", multi=True,
                                             placeholder="Wszystkie", style=_dd_style),
                            ]),

                            html.Div("Okres", style=S["section_header"]),

                            html.Div(style=S["period_row"], children=[
                                dcc.Input(id="dbw-year-from", type="text", placeholder="Od roku",
                                          debounce=True, style=S["period_input"]),
                                dcc.Input(id="dbw-year-to", type="text", placeholder="Do roku",
                                          debounce=True, style=S["period_input"]),
                            ]),
                        ]),

                        html.Main(style=S["main"], children=[
                            html.Div(id="dbw-kpi-row", style=S["kpi_row"]),
                            html.Div(id="dbw-chart-area"),
                        ]),
                    ]),

                    html.Footer(style=S["footer"], children=[
                        html.Span(
                            "Źródło: GUS DBW — dane wysokiej wartości (HVD) · dbw.stat.gov.pl"
                        ),
                    ]),
                ],
            ),
        ],
    ),
])


# ── Explorer callbacks ─────────────────────────────────────────────────────────

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
        return html.Div(f"Błąd zapytania: {e}", style=S["warn"]), no_update

    if df.empty:
        return html.Div(
            "Brak danych dla wybranych filtrów.",
            style=S["hint"],
        ), no_update

    row_def = _get_level(row_hier, row_level)
    col_def = _get_level(col_hier, col_level) if col_hier else None

    warning_text = None
    df_flat = df.copy()

    if col_col and col_col in df.columns:
        distinct = df[col_col].nunique()
        if distinct > MAX_PIVOT_COLS:
            warning_text = (
                f"Wymiar kolumn '{col_def['label']}' ma {distinct} wartości — "
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


def _build_explorer_chart(
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


# ── DBW HVD callbacks ──────────────────────────────────────────────────────────

@callback(
    Output("dd-dbw-variable", "options"),
    Output("dd-dbw-variable", "value"),
    Input("dd-dbw-category", "value"),
)
def update_dbw_variable_opts(category):
    return _build_dbw_variable_opts(_dbw_vars, category), None


@callback(
    Output("dbw-dim-1-container", "style"),
    Output("dbw-dim-1-label",     "children"),
    Output("dbw-dim-1",           "options"),
    Output("dbw-dim-1",           "value"),
    Output("dbw-dim-2-container", "style"),
    Output("dbw-dim-2-label",     "children"),
    Output("dbw-dim-2",           "options"),
    Output("dbw-dim-2",           "value"),
    Output("dbw-dim-3-container", "style"),
    Output("dbw-dim-3-label",     "children"),
    Output("dbw-dim-3",           "options"),
    Output("dbw-dim-3",           "value"),
    Output("dbw-variable-meta",   "data"),
    Input("dd-dbw-variable", "value"),
)
def update_dbw_dims(variable_id_str):
    _hide  = {"display": "none"}
    _show  = {}
    _empty = (_hide, "", [], None, _hide, "", [], None, _hide, "", [], None, None)

    if not variable_id_str:
        return _empty

    variable_id = int(variable_id_str)
    meta = next((v for v in _dbw_vars if v["variable_id"] == variable_id), None)
    if not meta or not meta["section_id"]:
        return _empty

    section_id = int(meta["section_id"])
    dims = load_dbw_dim_panels(variable_id, section_id)

    def _slot(idx: int) -> tuple:
        if idx >= len(dims):
            return _hide, "", [], None
        d = dims[idx]
        return _show, d["dim_name"], d["options"], None

    s1, l1, o1, v1 = _slot(0)
    s2, l2, o2, v2 = _slot(1)
    s3, l3, o3, v3 = _slot(2)

    store = {
        "variable_id":   variable_id,
        "section_id":    section_id,
        "variable_name": meta["variable_name"],
        "dims": [
            {"slot": d["slot"], "col": d["col"], "dim_name": d["dim_name"],
             "n_options": len(d["options"])}
            for d in dims
        ],
    }

    return s1, l1, o1, v1, s2, l2, o2, v2, s3, l3, o3, v3, store


@callback(
    Output("dbw-kpi-row",    "children"),
    Output("dbw-chart-area", "children"),
    Input("dbw-variable-meta", "data"),
    Input("dbw-dim-1",         "value"),
    Input("dbw-dim-2",         "value"),
    Input("dbw-dim-3",         "value"),
    Input("dbw-year-from",     "value"),
    Input("dbw-year-to",       "value"),
)
def update_dbw_chart(meta, dim1_vals, dim2_vals, dim3_vals, year_from, year_to):
    if not meta:
        return [], html.Div(
            style=S["empty_state"],
            children=[html.Div("Wybierz wskaźnik z lewego panelu.")],
        )

    variable_id = meta["variable_id"]
    section_id  = meta["section_id"]
    var_name    = meta.get("variable_name", "")
    dims_meta   = meta.get("dims", [])

    slot_vals = {1: dim1_vals or [], 2: dim2_vals or [], 3: dim3_vals or []}
    dim_cols  = {d["slot"]: d["col"] for d in dims_meta}

    # Build WHERE filters (only for slots with explicit selections)
    filter_cols: dict[str, list[str]] = {}
    for slot, vals in slot_vals.items():
        if vals and slot in dim_cols:
            filter_cols[dim_cols[slot]] = vals

    # Determine split dimension: first active dim that has a manageable number of values
    split_col = None
    if dims_meta:
        first = dims_meta[0]
        first_vals = slot_vals.get(first["slot"], [])
        if first_vals:
            split_col = first["col"]
        elif first.get("n_options", 0) <= 15:
            split_col = first["col"]

    try:
        df = run_dbw_query(
            variable_id, section_id,
            split_col, filter_cols,
            year_from or None,
            year_to   or None,
        )
    except Exception as exc:
        return [], html.Div(f"Błąd zapytania: {exc}", style=S["warn"])

    if df.empty:
        return [], html.Div("Brak danych dla wybranych filtrów.", style=S["hint"])

    # ── KPI cards ─────────────────────────────────────────────────────────────
    kpis = _compute_dbw_kpis(df)

    yoy_str   = "—"
    yoy_color = TEXT
    if kpis.get("yoy_pct") is not None:
        yoy_val   = kpis["yoy_pct"]
        sign      = "+" if yoy_val >= 0 else ""
        yoy_str   = f"{sign}{yoy_val:.1f}%"
        yoy_color = POSITIVE if yoy_val >= 0 else NEGATIVE

    kpi_cards = [
        _kpi_card("Ostatnia wartość", _fmt(kpis.get("latest_val")),
                  sub=str(kpis.get("latest_year", ""))),
        _kpi_card("Zmiana r/r", yoy_str, value_color=yoy_color),
        _kpi_card("Maksimum",   _fmt(kpis.get("max_val"))),
        _kpi_card("Minimum",    _fmt(kpis.get("min_val"))),
    ]

    # ── Chart ──────────────────────────────────────────────────────────────────
    fig = go.Figure()

    if split_col and "dim_label" in df.columns:
        labels = sorted(df["dim_label"].dropna().unique())
        for i, label in enumerate(labels):
            sub = df[df["dim_label"] == label].sort_values("year")
            fig.add_trace(go.Scatter(
                x=sub["year"], y=sub["value"],
                name=str(label),
                mode="lines+markers",
                line=dict(color=COLORWAY[i % len(COLORWAY)], width=1.8),
                marker=dict(size=4),
            ))
    else:
        plot_df = df.sort_values("year")
        fig.add_trace(go.Scatter(
            x=plot_df["year"], y=plot_df["value"],
            mode="lines+markers",
            name="wartość",
            line=dict(color=AZURE_1, width=2.5),
            marker=dict(size=5),
        ))

    fig.update_layout(
        title=var_name,
        xaxis_title="Rok",
        yaxis_title="Wartość",
        height=420,
        margin=dict(l=60, r=24, t=56, b=40),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02,
            xanchor="left", x=0, font=dict(size=11),
        ),
    )

    chart_area = html.Div(style=S["card"], children=[
        dcc.Graph(figure=fig, config={"displayModeBar": False}),
    ])

    return kpi_cards, chart_area


# ── Entry point ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    log.info("Explorer starting on port %d", PORT)
    app.run(host="0.0.0.0", port=PORT, debug=False)
