#!/usr/bin/env python3
"""
Open Reporting — Template Dashboard
Developer reference: every chart component variant displayed with sample data.

Copy this directory, rename, and customise for your domain.

Run:
    PYTHONPATH=/opt/open-reporting \
    DUCKDB_PATH=/opt/open-reporting/data/warehouse.duckdb \
    python3 products/dashboards/template/app.py
"""
import logging

from dash import Dash, Input, Output, State, callback, html

import products.visuals.lib.theme as _theme  # noqa: F401 — registers 'teal' template
from products.visuals.lib.theme import (
    BG_PAGE, BG_SURFACE, BORDER,
    COLORWAY, GRID, MUTED, NEGATIVE, POSITIVE,
    SUBTEXT, TEXT, WARNING, ZERO_LINE,
    FONT_FAMILY,
    TEAL_1, TEAL_2, TEAL_3, TEAL_4, TEAL_PALE,
    AZURE_1, AZURE_2, AZURE_3, AZURE_4, AZURE_PALE,
    SLATE_1, SLATE_2, SLATE_3, SLATE_4,
)

# ── Chart components ──────────────────────────────────────────────────────────
from products.visuals.components.kpi_card import kpi_row, kpi_standard, kpi_compact
from products.visuals.components.bar_chart import (
    clustered_column, stacked_column, pct_stacked_column,
    clustered_bar, stacked_bar, pct_stacked_bar,
    bar_diverging,
    clustered_stacked_column, clustered_stacked_bar,
)
from products.visuals.components.line_chart import (
    line, area, stacked_area, pct_stacked_area,
)
from products.visuals.components.combo_chart import (
    line_clustered_column, line_stacked_column, line_pct_stacked_column,
)
from products.visuals.components.waterfall_chart import waterfall_contribution, waterfall_variance
from products.visuals.components.scatter_chart import scatter_bubble
from products.visuals.components.distribution_chart import histogram, box_plot
from products.visuals.components.special_chart import (
    funnel, treemap, gauge, bullet, ribbon, heatmap_matrix,
)
from products.visuals.components.map_chart import choropleth_map, bubble_map
from products.visuals.components.financial_chart import candlestick
from products.visuals.components.table_chart import table_basic, table_matrix, data_list
from products.visuals.components.pie_chart import pie_chart
from products.visuals.components.slicer import (
    dropdown_slicer, list_slicer, range_slicer, date_range_slicer, tile_slicer,
)

import products.dashboards.template.data as _data
import products.dashboards.template.measures as m

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

PORT = 8055

# ── Data (loaded once at startup — swap data.py to connect to warehouse) ──────
# Pre-aggregated views — consumed directly by chart calls
_df_by_cat    = _data.load_by_category()
_df_by_year   = _data.load_by_year()
_df_by_period = _data.load_by_period()
_scalars      = _data.load_scalars()

# Specialised datasets — already chart-ready (no aggregation needed)
_df_geo              = _data.load_geo()
_df_ohlc_a, _df_ohlc_b = _data.load_ohlc()
_df_sc               = _data.load_scatter()
_df_dist             = _data.load_distribution()
_df_wf_c, _df_wf_v  = _data.load_waterfall()
_df_funnel           = _data.load_funnel()
_df_tree             = _data.load_treemap()
_df_ribbon           = _data.load_ribbon()
_df_hmap             = _data.load_heatmap()
_gauge               = _data.load_gauge()
_df_table            = _data.load_table()
_groups_cs           = _data.load_clustered_stacked()
_matrix              = _data.load_matrix()
_list_items          = _data.load_data_list()

# ── Convenience shortcuts ─────────────────────────────────────────────────────
_years       = m.DIMS["year"].values(_df_by_year)
_categories  = m.DIMS["category"].values(_df_by_cat)
_periods     = m.DIMS["period"].values(_df_by_period)
_dist_groups = m.DIMS["group"].values(_df_dist)

# ── Helpers ───────────────────────────────────────────────────────────────────

def _color_swatch(name: str, color: str) -> html.Div:
    return html.Div(style={
        "display": "flex", "flexDirection": "column", "alignItems": "center",
        "gap": "6px", "minWidth": "80px",
    }, children=[
        html.Div(style={
            "width": "48px", "height": "48px", "borderRadius": "8px",
            "backgroundColor": color, "border": f"1px solid {BORDER}",
            "boxShadow": "0 1px 3px rgba(0,0,0,0.06)",
        }),
        html.Span(name, style={"fontSize": "10px", "color": SUBTEXT, "fontFamily": "monospace"}),
    ])

# ── App ───────────────────────────────────────────────────────────────────────

app = Dash(
    __name__,
    title="Template — Open Reporting",
    suppress_callback_exceptions=True,
    requests_pathname_prefix="/template/",
    routes_pathname_prefix="/template/",
    index_string="""<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            html, body { margin: 0; padding: 0; height: 100vh; }
            #react-entry-point { height: 100%; }
            .js-plotly-plot .plotly { width: 100% !important; }
            .js-plotly-plot .plotly .main-svg { width: 100% !important; }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>""",
)

# ── Styles ────────────────────────────────────────────────────────────────────

SIDEBAR_W         = "240px"
SIDEBAR_COLLAPSED = "44px"
GAP    = "4px"
RADIUS = "10px"

S = {
    "body": {
        "fontFamily": FONT_FAMILY,
        "background": BG_PAGE, "color": TEXT,
        "height": "100vh", "display": "flex", "margin": 0,
        "padding": f"{GAP} 0 {GAP} {GAP}",
        "boxSizing": "border-box",
        "overflow": "hidden",
    },
    "sidebar": {
        "width": SIDEBAR_W, "flexShrink": 0,
        "background": BG_SURFACE,
        "borderRadius": RADIUS,
        "boxShadow": "0 2px 8px rgba(0,0,0,0.06), 0 0 1px rgba(0,0,0,0.08)",
        "display": "flex", "flexDirection": "column",
        "height": f"calc(100vh - {GAP} * 2)",
        "overflow": "hidden",
        "transition": "width 0.25s ease",
        "position": "relative",
    },
    "sidebar-logo": {
        "padding": "20px 20px 16px",
        "whiteSpace": "nowrap", "overflow": "hidden",
        "height": "68px", "boxSizing": "border-box",
        "display": "flex", "alignItems": "center",
    },
    "sidebar-divider": {"margin": "0 16px", "border": "none", "borderTop": f"1px solid {BORDER}"},
    "logo": {"height": "32px", "width": "auto"},
    "sidebar-nav": {"flex": 1, "padding": "16px 0", "overflowY": "auto", "whiteSpace": "nowrap", "overflow": "hidden"},
    "nav-item": {
        "display": "block", "padding": "8px 20px",
        "fontSize": "13px", "color": SUBTEXT, "textDecoration": "none", "cursor": "pointer",
    },
    "nav-item-active": {
        "display": "block", "padding": "8px 20px",
        "fontSize": "13px", "color": TEXT, "textDecoration": "none",
        "borderLeft": f"3px solid {TEXT}", "backgroundColor": f"{BORDER}40", "cursor": "pointer",
    },
    "toggle-btn": {
        "position": "absolute", "top": "28px", "right": "10px",
        "width": "24px", "height": "24px",
        "background": "none", "border": "none", "cursor": "pointer", "padding": 0,
        "display": "flex", "alignItems": "center", "justifyContent": "center", "zIndex": 100,
    },
    "toggle-icon": {"width": "20px", "height": "20px", "opacity": 0.5},
    "main": {
        "flex": 1, "minWidth": 0,
        "overflowY": "auto", "overflowX": "hidden",
        "height": f"calc(100vh - {GAP} * 2)",
        "boxSizing": "border-box",
        "display": "flex", "flexDirection": "column",
    },
    "main-header": {
        "padding": "0 32px", "flexShrink": 0,
        "display": "flex", "alignItems": "center", "justifyContent": "space-between",
        "height": "68px",
    },
    "header-actions": {"display": "flex", "alignItems": "center", "gap": "8px"},
    "header-btn": {
        "width": "32px", "height": "32px",
        "background": "none", "border": f"1px solid {BORDER}", "borderRadius": "6px",
        "cursor": "pointer", "display": "flex", "alignItems": "center", "justifyContent": "center",
        "color": SUBTEXT, "padding": 0,
    },
    "header-icon": {"width": "16px", "height": "16px"},
    "main-divider": {"margin": "0 32px", "border": "none", "borderTop": f"1px solid {BORDER}"},
    "footer-divider": {"margin": "0 32px", "border": "none", "borderTop": f"1px solid {BORDER}"},
    "main-footer": {
        "padding": "0 32px", "flexShrink": 0,
        "display": "flex", "alignItems": "center", "justifyContent": "space-between",
        "height": "48px",
    },
    "footer-text": {"fontSize": "12px", "color": SUBTEXT},
    "main-content-area": {
        "flex": 1, "padding": "28px 32px 32px",
        "overflowY": "auto", "width": "100%", "boxSizing": "border-box",
    },
    "section-heading": {
        "fontSize": "18px", "fontWeight": "700", "color": TEXT,
        "marginBottom": "6px", "marginTop": "48px",
    },
    "section-desc": {"fontSize": "13px", "color": SUBTEXT, "marginBottom": "24px"},
    "group": {"marginBottom": "28px", "width": "100%"},
    "group-title": {"fontSize": "13px", "fontWeight": 600, "color": SUBTEXT, "marginBottom": "12px"},
    "grid-2": {"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "20px", "alignItems": "start"},
    "grid-3": {"display": "grid", "gridTemplateColumns": "1fr 1fr 1fr", "gap": "20px", "alignItems": "start"},
    "grid-4": {"display": "grid", "gridTemplateColumns": "repeat(4, 1fr)", "gap": "16px", "alignItems": "start"},
    "grid-auto": {
        "display": "grid", "gridTemplateColumns": "repeat(auto-fit, minmax(180px, 1fr))",
        "gap": "16px", "maxWidth": "100%",
    },
    "card": {
        "background": BG_SURFACE, "border": f"1px solid {BORDER}",
        "borderRadius": "8px", "padding": "16px", "overflow": "hidden", "minWidth": 0,
    },
}

# ── Layout ────────────────────────────────────────────────────────────────────

app.layout = html.Div(style=S["body"], children=[

    # ── Sidebar ───────────────────────────────────────────────────────────────
    html.Aside(id="sidebar", style=S["sidebar"], children=[
        html.Div(id="sidebar-logo", style=S["sidebar-logo"], children=[
            html.A(html.Img(id="sidebar-logo-img",
                            src="/template/assets/images/logo.svg", style=S["logo"]),
                   href="/"),
        ]),
        html.Hr(id="sidebar-divider", style=S["sidebar-divider"]),
        html.Nav(id="sidebar-nav", style=S["sidebar-nav"], children=[
            html.A("KPI card", href="#kpi", style=S["nav-item-active"]),
            html.A("Clustered column", href="#col-clustered", style=S["nav-item"]),
            html.A("Stacked column", href="#col-stacked", style=S["nav-item"]),
            html.A("100% stacked column", href="#col-pct", style=S["nav-item"]),
            html.A("Clustered+stacked column", href="#col-cs", style=S["nav-item"]),
            html.A("Clustered bar", href="#bar-clustered", style=S["nav-item"]),
            html.A("Stacked bar", href="#bar-stacked", style=S["nav-item"]),
            html.A("100% stacked bar", href="#bar-pct", style=S["nav-item"]),
            html.A("Clustered+stacked bar", href="#bar-cs", style=S["nav-item"]),
            html.A("Line", href="#line", style=S["nav-item"]),
            html.A("Clustered area", href="#area-clustered", style=S["nav-item"]),
            html.A("Stacked area", href="#area-stacked", style=S["nav-item"]),
            html.A("100% stacked area", href="#area-pct", style=S["nav-item"]),
            html.A("Line + clustered column", href="#combo-lc", style=S["nav-item"]),
            html.A("Line + stacked column", href="#combo-ls", style=S["nav-item"]),
            html.A("Line + 100% stacked column", href="#combo-lp", style=S["nav-item"]),
            html.A("Scatter / Bubble", href="#scatter", style=S["nav-item"]),
            html.A("Pie / Donut", href="#pie", style=S["nav-item"]),
            html.A("Treemap", href="#treemap", style=S["nav-item"]),
            html.A("Funnel", href="#funnel", style=S["nav-item"]),
            html.A("Waterfall — contribution", href="#waterfall-contribution", style=S["nav-item"]),
            html.A("Waterfall — variance", href="#waterfall-variance", style=S["nav-item"]),
            html.A("Histogram", href="#histogram", style=S["nav-item"]),
            html.A("Box plot", href="#boxplot", style=S["nav-item"]),
            html.A("Gauge", href="#gauge", style=S["nav-item"]),
            html.A("Bullet", href="#bullet", style=S["nav-item"]),
            html.A("Table", href="#table", style=S["nav-item"]),
            html.A("Matrix / Pivot", href="#matrix", style=S["nav-item"]),
            html.A("Data list", href="#datalist", style=S["nav-item"]),
            html.A("Heatmap", href="#heatmap", style=S["nav-item"]),
            html.A("Choropleth map", href="#choropleth", style=S["nav-item"]),
            html.A("Bubble map", href="#bubblemap", style=S["nav-item"]),
            html.A("Ribbon", href="#ribbon", style=S["nav-item"]),
            html.A("Candlestick", href="#candlestick", style=S["nav-item"]),
            html.A("— UI / Filters —", href="#slicers",
                   style={**S["nav-item"], "color": SUBTEXT, "fontSize": "11px",
                          "marginTop": "8px", "pointerEvents": "none"}),
            html.A("Dropdown slicer", href="#slicer-dropdown", style=S["nav-item"]),
            html.A("List slicer", href="#slicer-list", style=S["nav-item"]),
            html.A("Range slicer", href="#slicer-range", style=S["nav-item"]),
            html.A("Date range slicer", href="#slicer-date", style=S["nav-item"]),
            html.A("Tile slicer", href="#slicer-tile", style=S["nav-item"]),
            html.A("Colour palette", href="#palette", style=S["nav-item"]),
        ]),
        html.Button(id="btn-toggle", style=S["toggle-btn"], children=[
            html.Img(id="toggle-icon", src="/template/assets/images/sidebar.svg",
                     style=S["toggle-icon"]),
        ]),
    ]),

    # ── Main ─────────────────────────────────────────────────────────────────
    html.Main(id="main-content", style=S["main"], children=[

        html.Div(id="main-header", style=S["main-header"], children=[
            html.Div(children=[
                html.H1("Visual components — reference",
                        style={"fontSize": "20px", "fontWeight": 700, "color": TEXT, "margin": 0}),
                html.P("One example per chart family — sample data",
                       style={"fontSize": "13px", "color": SUBTEXT, "margin": "4px 0 0"}),
            ]),
            html.Div(style=S["header-actions"], children=[
                html.Button(html.Img(src="/template/assets/images/settings.svg",
                                     style=S["header-icon"]),
                            id="btn-settings", style=S["header-btn"]),
                html.Button(html.Img(src="/template/assets/images/user.svg",
                                     style=S["header-icon"]),
                            id="btn-user", style=S["header-btn"]),
            ]),
        ]),

        html.Hr(style=S["main-divider"]),

        html.Div(id="main-content-area", style=S["main-content-area"], children=[

            # ── KPI card ─────────────────────────────────────────────────────
            html.H2("KPI card", id="kpi", style={**S["section-heading"], "marginTop": 0}),
            html.P("kpi_standard + kpi_row — multi-card row, equal height, responsive wrap. "
                   "Format driven by Measure (format_type, scale, decimals, currency_symbol). "
                   "kpi_compact variant for dense layouts.",
                   style=S["section-desc"]),
            html.Div(style=S["group"], children=[
                kpi_row([
                    kpi_standard(
                        label=m.MEASURES["measure_a"].label,
                        value=m.MEASURES["measure_a"].kpi_value(_scalars["measure_a"]),
                        unit=m.MEASURES["measure_a"].plotly_ticksuffix,
                        subtitle="Average 2018–2024",
                        reference_value=m.MEASURES["measure_a"].kpi_value(50.0),
                        reference_label="Target",
                        trend="▲ +0.8",
                        trend_color=POSITIVE,
                    ),
                    kpi_standard(
                        label=m.MEASURES["measure_b"].label,
                        value=m.MEASURES["measure_b"].kpi_value(_scalars["measure_b"]),
                        unit=m.MEASURES["measure_b"].plotly_ticksuffix,
                        reference_value=m.MEASURES["measure_b"].kpi_value(40.0),
                        reference_label="Prior year",
                    ),
                    kpi_standard(
                        label=m.MEASURES["measure_a_pct"].label,
                        value=m.MEASURES["measure_a_pct"].kpi_value(_scalars["measure_a_pct"]),
                        unit=m.MEASURES["measure_a_pct"].plotly_ticksuffix,
                        trend="▼ -1.2",
                        trend_color=NEGATIVE,
                    ),
                    kpi_standard(
                        label=m.MEASURES["measure_a_cum"].label,
                        value=m.MEASURES["measure_a_cum"].kpi_value(_scalars["measure_a_cum"]),
                        unit=m.MEASURES["measure_a_cum"].plotly_ticksuffix,
                        subtitle="All years combined",
                    ),
                ]),
            ]),
            html.Div(style=S["group"], children=[
                kpi_row([
                    kpi_compact(
                        label=m.MEASURES["measure_a"].label,
                        value=m.MEASURES["measure_a"].kpi_value(_scalars["measure_a"]),
                        unit=m.MEASURES["measure_a"].plotly_ticksuffix,
                        trend="▲ +0.8", trend_color=POSITIVE,
                    ),
                    kpi_compact(
                        label=m.MEASURES["measure_b"].label,
                        value=m.MEASURES["measure_b"].kpi_value(_scalars["measure_b"]),
                        unit=m.MEASURES["measure_b"].plotly_ticksuffix,
                    ),
                    kpi_compact(
                        label=m.MEASURES["measure_c"].label,
                        value=m.MEASURES["measure_c"].kpi_value(_scalars["measure_c"]),
                        unit=m.MEASURES["measure_c"].plotly_ticksuffix,
                    ),
                    kpi_compact(
                        label=m.MEASURES["measure_d"].label,
                        value=m.MEASURES["measure_d"].kpi_value(_scalars["measure_d"]),
                        unit=m.MEASURES["measure_d"].plotly_ticksuffix,
                    ),
                    kpi_compact(
                        label=m.MEASURES["measure_a_pct"].label,
                        value=m.MEASURES["measure_a_pct"].kpi_value(_scalars["measure_a_pct"]),
                        unit=m.MEASURES["measure_a_pct"].plotly_ticksuffix,
                        trend="▼ -1.2", trend_color=NEGATIVE,
                    ),
                ], min_width="140px", gap="12px"),
            ]),

            # ── 1. Clustered column ───────────────────────────────────────────
            html.H2("Clustered column", id="col-clustered", style=S["section-heading"]),
            html.P("clustered_column — grouped vertical bars, compare multiple series side by side.", style=S["section-desc"]),
            html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
                clustered_column("Clustered column", subtitle="sample data",
                    x=_categories,
                    series=[
                        {"name": "Measure A", "y": _df_by_cat["val_a"].tolist()},
                        {"name": "Measure B", "y": _df_by_cat["val_b"].tolist()},
                        {"name": "Measure C", "y": _df_by_cat["val_c"].tolist()},
                    ]),
            ])]),

            # ── 2. Stacked column ─────────────────────────────────────────────
            html.H2("Stacked column", id="col-stacked", style=S["section-heading"]),
            html.P("stacked_column — vertical bars stacked, shows total and composition.", style=S["section-desc"]),
            html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
                stacked_column("Stacked column", subtitle="sample data",
                    x=_years,
                    series=[
                        {"name": "Measure A", "y": _df_by_year["val_a"].tolist()},
                        {"name": "Measure B", "y": _df_by_year["val_b"].tolist()},
                        {"name": "Measure C", "y": _df_by_year["val_c"].tolist()},
                        {"name": "Measure D", "y": _df_by_year["val_d"].tolist()},
                    ]),
            ])]),

            # ── 3. 100% stacked column ────────────────────────────────────────
            html.H2("100% stacked column", id="col-pct", style=S["section-heading"]),
            html.P("pct_stacked_column — normalised to 100%, shows composition only.", style=S["section-desc"]),
            html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
                pct_stacked_column("100% stacked column", subtitle="sample data",
                    x=_categories,
                    series=[
                        {"name": "Measure A", "y": _df_by_cat["val_a"].tolist()},
                        {"name": "Measure B", "y": _df_by_cat["val_b"].tolist()},
                        {"name": "Measure C", "y": _df_by_cat["val_c"].tolist()},
                    ]),
            ])]),

            # ── 4. Clustered + stacked column ─────────────────────────────────
            html.H2("Clustered + stacked column", id="col-cs", style=S["section-heading"]),
            html.P("clustered_stacked_column — groups side by side, series stacked within each group.", style=S["section-desc"]),
            html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
                clustered_stacked_column("Clustered + stacked column", subtitle="sample data",
                    x=_categories, groups=_groups_cs),
            ])]),

            # ── 5. Clustered bar ──────────────────────────────────────────────
            html.H2("Clustered bar", id="bar-clustered", style=S["section-heading"]),
            html.P("clustered_bar — horizontal grouped bars; single series sorts descending (ranking).", style=S["section-desc"]),
            html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
                clustered_bar("Clustered bar", subtitle="sample data — sorted descending",
                    categories=m.DIMS["label"].values(_df_geo),
                    series=[{"name": "Measure A", "y": _df_geo["val_a"].tolist()}]),
            ])]),

            # ── 6. Stacked bar ────────────────────────────────────────────────
            html.H2("Stacked bar", id="bar-stacked", style=S["section-heading"]),
            html.P("stacked_bar — horizontal stacked bars, shows total and composition.", style=S["section-desc"]),
            html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
                stacked_bar("Stacked bar", subtitle="sample data",
                    categories=_categories,
                    series=[
                        {"name": "Measure A", "y": _df_by_cat["val_a"].tolist()},
                        {"name": "Measure B", "y": _df_by_cat["val_b"].tolist()},
                        {"name": "Measure C", "y": _df_by_cat["val_c"].tolist()},
                    ]),
            ])]),

            # ── 7. 100% stacked bar ───────────────────────────────────────────
            html.H2("100% stacked bar", id="bar-pct", style=S["section-heading"]),
            html.P("pct_stacked_bar — normalised to 100%, horizontal, composition only.", style=S["section-desc"]),
            html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
                pct_stacked_bar("100% stacked bar", subtitle="sample data",
                    categories=_categories,
                    series=[
                        {"name": "Measure A", "y": _df_by_cat["val_a"].tolist()},
                        {"name": "Measure B", "y": _df_by_cat["val_b"].tolist()},
                        {"name": "Measure C", "y": _df_by_cat["val_c"].tolist()},
                    ]),
            ])]),

            # ── 8. Clustered + stacked bar ────────────────────────────────────
            html.H2("Clustered + stacked bar", id="bar-cs", style=S["section-heading"]),
            html.P("clustered_stacked_bar — horizontal variant of clustered+stacked.", style=S["section-desc"]),
            html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
                clustered_stacked_bar("Clustered + stacked bar", subtitle="sample data",
                    categories=_categories, groups=_groups_cs),
            ])]),

            # ── 9. Line ───────────────────────────────────────────────────────
            html.H2("Line", id="line", style=S["section-heading"]),
            html.P("line — trends over time, one or multiple series. Supports reference line.", style=S["section-desc"]),
            html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
                line("Line", subtitle="sample data",
                    x=_years,
                    series=[
                        {"name": "Measure A", "y": _df_by_year["val_a"].tolist()},
                        {"name": "Measure B", "y": _df_by_year["val_b"].tolist()},
                        {"name": "Measure E", "y": _df_by_year["val_e"].tolist()},
                    ],
                    reference={"value": _scalars["measure_b"], "label": "Reference"}),
            ])]),

            # ── 10. Clustered area ────────────────────────────────────────────
            html.H2("Clustered area", id="area-clustered", style=S["section-heading"]),
            html.P("area — all series fill from zero, overlapping with transparency. Shows volume.", style=S["section-desc"]),
            html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
                area("Clustered area", subtitle="sample data",
                    x=_years,
                    series=[
                        {"name": "Measure A", "y": _df_by_year["val_a"].tolist()},
                        {"name": "Measure B", "y": _df_by_year["val_b"].tolist()},
                        {"name": "Measure C", "y": _df_by_year["val_c"].tolist()},
                    ]),
            ])]),

            # ── 11. Stacked area ──────────────────────────────────────────────
            html.H2("Stacked area", id="area-stacked", style=S["section-heading"]),
            html.P("stacked_area — areas stacked cumulatively, shows total and composition over time.", style=S["section-desc"]),
            html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
                stacked_area("Stacked area", subtitle="sample data",
                    x=_years,
                    series=[
                        {"name": "Measure A", "y": _df_by_year["val_a"].tolist()},
                        {"name": "Measure B", "y": _df_by_year["val_b"].tolist()},
                        {"name": "Measure C", "y": _df_by_year["val_c"].tolist()},
                        {"name": "Measure D", "y": _df_by_year["val_d"].tolist()},
                    ]),
            ])]),

            # ── 12. 100% stacked area ─────────────────────────────────────────
            html.H2("100% stacked area", id="area-pct", style=S["section-heading"]),
            html.P("pct_stacked_area — normalised to 100%, composition over time only.", style=S["section-desc"]),
            html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
                pct_stacked_area("100% stacked area", subtitle="sample data",
                    x=_years,
                    series=[
                        {"name": "Measure A", "y": _df_by_year["val_a"].tolist()},
                        {"name": "Measure B", "y": _df_by_year["val_b"].tolist()},
                        {"name": "Measure C", "y": _df_by_year["val_c"].tolist()},
                        {"name": "Measure D", "y": _df_by_year["val_d"].tolist()},
                    ]),
            ])]),

            # ── 13. Line + clustered column ───────────────────────────────────
            html.H2("Line + clustered column", id="combo-lc", style=S["section-heading"]),
            html.P("line_clustered_column — line and grouped bars on a shared axis. Same scale only.", style=S["section-desc"]),
            html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
                line_clustered_column("Line + clustered column", subtitle="sample data — same scale",
                    x=_years,
                    bar_series=[{"name": "Measure A", "y": _df_by_year["val_a"].tolist()}],
                    line_series=[{"name": "Measure B", "y": _df_by_year["val_b"].tolist()}]),
            ])]),

            # ── 14. Line + stacked column ─────────────────────────────────────
            html.H2("Line + stacked column", id="combo-ls", style=S["section-heading"]),
            html.P("line_stacked_column — stacked bars show components, line shows aggregate or rate.", style=S["section-desc"]),
            html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
                line_stacked_column("Line + stacked column", subtitle="sample data",
                    x=_years,
                    bar_series=[
                        {"name": "Measure A", "y": _df_by_year["val_a"].tolist()},
                        {"name": "Measure C", "y": _df_by_year["val_c"].tolist()},
                        {"name": "Measure D", "y": _df_by_year["val_d"].tolist()},
                    ],
                    line_series=[{"name": "Measure B", "y": _df_by_year["val_b"].tolist()}]),
            ])]),

            # ── 15. Line + 100% stacked column ───────────────────────────────
            html.H2("Line + 100% stacked column", id="combo-lp", style=S["section-heading"]),
            html.P("line_pct_stacked_column — 100% normalised bars with a rate or % line overlay.", style=S["section-desc"]),
            html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
                line_pct_stacked_column("Line + 100% stacked column", subtitle="sample data",
                    x=_years,
                    bar_series=[
                        {"name": "Measure A", "y": _df_by_year["val_a"].tolist()},
                        {"name": "Measure B", "y": _df_by_year["val_b"].tolist()},
                        {"name": "Measure C", "y": _df_by_year["val_c"].tolist()},
                    ],
                    line_series=[{"name": "Measure E", "y": _df_by_year["val_e"].tolist()}]),
            ])]),

            # ── 16. Scatter / Bubble ──────────────────────────────────────────
            html.H2("Scatter / Bubble", id="scatter", style=S["section-heading"]),
            html.P("scatter_bubble — X/Y correlation with bubble size as third variable. Variant: scatter_basic (no size).", style=S["section-desc"]),
            html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
                scatter_bubble("Scatter / Bubble", subtitle="sample data",
                    x=_df_sc["val_x"].tolist(),
                    y=_df_sc["val_y"].tolist(),
                    size=_df_sc["val_size"].tolist(),
                    labels=_df_sc["dim_label"].tolist()),
            ])]),

            # ── 17. Pie / Donut ───────────────────────────────────────────────
            html.H2("Pie / Donut", id="pie", style=S["section-heading"]),
            html.P("pie_chart — part-to-whole for 2–5 categories. Donut by default; pie via donut=False.", style=S["section-desc"]),
            html.Div(style=S["group"], children=[html.Div(style={"maxWidth": "360px"}, children=[
                html.Div(style=S["card"], children=[
                    pie_chart("Pie / Donut", subtitle="sample data — donut variant",
                        labels=_categories, values=_df_by_cat["val_a"].tolist()),
                ]),
            ])]),

            # ── 18. Treemap ───────────────────────────────────────────────────
            html.H2("Treemap", id="treemap", style=S["section-heading"]),
            html.P("treemap — hierarchical part-to-whole, rectangle size = value.", style=S["section-desc"]),
            html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
                treemap("Treemap", subtitle="sample data",
                    labels=_df_tree["dim_node"].tolist(),
                    parents=_df_tree["dim_parent"].tolist(),
                    values=_df_tree["val_size"].tolist()),
            ])]),

            # ── 19. Funnel ────────────────────────────────────────────────────
            html.H2("Funnel", id="funnel", style=S["section-heading"]),
            html.P("funnel — sequential stages with drop-off, conversion tracking.", style=S["section-desc"]),
            html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
                funnel("Funnel", subtitle="sample data",
                    stages=_df_funnel["dim_stage"].tolist(),
                    values=_df_funnel["val_count"].tolist()),
            ])]),

            # ── 20. Waterfall — contribution ──────────────────────────────────
            html.H2("Waterfall — contribution", id="waterfall-contribution", style=S["section-heading"]),
            html.P("waterfall_contribution — components building a total; bars show additive decomposition of the final result.", style=S["section-desc"]),
            html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
                waterfall_contribution("Waterfall — contribution", subtitle="sample data",
                    categories=_df_wf_c["dim_stage"].tolist(),
                    values=_df_wf_c["val_amount"].tolist(),
                    total_label=_df_wf_c.loc[_df_wf_c["is_total"], "dim_stage"].iloc[0]),
            ])]),

            # ── 21. Waterfall — variance ──────────────────────────────────────
            html.H2("Waterfall — variance", id="waterfall-variance", style=S["section-heading"]),
            html.P("waterfall_variance — bridge between two absolute values; explains how a base becomes the final value.", style=S["section-desc"]),
            html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
                waterfall_variance("Waterfall — variance", subtitle="sample data",
                    categories=_df_wf_v["dim_stage"].tolist(),
                    values=_df_wf_v["val_amount"].tolist()),
            ])]),

            # ── 22. Histogram ─────────────────────────────────────────────────
            html.H2("Histogram", id="histogram", style=S["section-heading"]),
            html.P("histogram — frequency distribution of a single numeric variable.", style=S["section-desc"]),
            html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
                histogram("Histogram", subtitle="sample data",
                    x=_df_dist["val_obs"].tolist(),
                    x_label="Observed value"),
            ])]),

            # ── 23. Box plot ──────────────────────────────────────────────────
            html.H2("Box plot", id="boxplot", style=S["section-heading"]),
            html.P("box_plot — median, IQR and outliers by group. Use for distribution comparisons.", style=S["section-desc"]),
            html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
                box_plot("Box plot", subtitle="sample data",
                    data={grp: _df_dist.loc[_df_dist["dim_group"] == grp, "val_obs"].tolist()
                          for grp in _dist_groups}),
            ])]),

            # ── 24. Gauge ─────────────────────────────────────────────────────
            html.H2("Gauge", id="gauge", style=S["section-heading"]),
            html.P("gauge — single value measured against a range with a reference point.", style=S["section-desc"]),
            html.Div(style=S["group"], children=[html.Div(style={"maxWidth": "360px"}, children=[
                html.Div(style=S["card"], children=[
                    gauge("Gauge", subtitle="sample data",
                        value=_gauge["gauge_value"],
                        min_val=0, max_val=_gauge["gauge_max"],
                        reference=_gauge["gauge_target"],
                        suffix=" units"),
                ]),
            ])]),

            # ── 25. Bullet ────────────────────────────────────────────────────
            html.H2("Bullet", id="bullet", style=S["section-heading"]),
            html.P("bullet — value vs target with a background range. Precise goal tracking.", style=S["section-desc"]),
            html.Div(style=S["group"], children=[html.Div(style={"maxWidth": "360px"}, children=[
                html.Div(style=S["card"], children=[
                    bullet("Bullet", subtitle="sample data",
                        value=_gauge["bullet_a_value"],
                        target=_gauge["bullet_a_target"],
                        max_val=_gauge["bullet_a_max"],
                        suffix=" units"),
                ]),
            ])]),

            # ── 26. Table ─────────────────────────────────────────────────────
            html.H2("Table", id="table", style=S["section-heading"]),
            html.P("table_basic — exact values in rows and columns, numbers right-aligned.", style=S["section-desc"]),
            html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
                table_basic("Table", subtitle="sample data",
                    headers=["Attribute", "Measure A", "Measure B", "Measure C", "Measure D"],
                    rows=[[row["dim_attribute"], row["val_a"], row["val_b"],
                           row["val_c"], row["val_d"]]
                          for _, row in _df_table.iterrows()],
                    number_cols={1, 2, 3, 4}),
            ])]),

            # ── 27. Matrix / Pivot ────────────────────────────────────────────
            html.H2("Matrix / Pivot table", id="matrix", style=S["section-heading"]),
            html.P("table_matrix — row dimension × column dimension, values at intersections.", style=S["section-desc"]),
            html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
                table_matrix("Matrix / Pivot table", subtitle="sample data",
                    row_labels=_matrix["row_labels"],
                    col_labels=_matrix["col_labels"],
                    values=_matrix["values"],
                    row_dim="Category"),
            ])]),

            # ── 28. Data list ─────────────────────────────────────────────────
            html.H2("Data list", id="datalist", style=S["section-heading"]),
            html.P("data_list — scrollable list of labelled items with optional values.", style=S["section-desc"]),
            html.Div(style=S["group"], children=[html.Div(style={"maxWidth": "360px"}, children=[
                data_list("Data list", subtitle="sample data", items=_list_items),
            ])]),

            # ── 29. Heatmap ───────────────────────────────────────────────────
            html.H2("Heatmap", id="heatmap", style=S["section-heading"]),
            html.P("heatmap_matrix — matrix of values coloured by intensity, diverging or sequential.", style=S["section-desc"]),
            html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
                heatmap_matrix("Heatmap", subtitle="sample data — diverging colour scale",
                    x_labels=_df_hmap["dim_col"].unique().tolist(),
                    y_labels=_df_hmap["dim_row"].unique().tolist(),
                    z_values=[_df_hmap.loc[_df_hmap["dim_row"] == row, "val_z"].tolist()
                               for row in _df_hmap["dim_row"].unique().tolist()],
                    color_scale="diverging"),
            ])]),

            # ── 30. Choropleth map ────────────────────────────────────────────
            html.H2("Choropleth map", id="choropleth", style=S["section-heading"]),
            html.P("choropleth_map — geographic regions filled by value, sequential or diverging colour scale.", style=S["section-desc"]),
            html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
                choropleth_map("Choropleth map", subtitle="sample data — sequential scale",
                    locations=m.DIMS["iso3"].values(_df_geo),
                    values=_df_geo["val_a"].tolist(),
                    hover_labels=m.DIMS["label"].values(_df_geo)),
            ])]),

            # ── 31. Bubble map ────────────────────────────────────────────────
            html.H2("Bubble map", id="bubblemap", style=S["section-heading"]),
            html.P("bubble_map — geographic points sized by value.", style=S["section-desc"]),
            html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
                bubble_map("Bubble map", subtitle="sample data",
                    lat=_df_geo["dim_lat"].tolist(),
                    lon=_df_geo["dim_lon"].tolist(),
                    size=_df_geo["val_a"].tolist(),
                    labels=m.DIMS["label"].values(_df_geo)),
            ])]),

            # ── 32. Ribbon ────────────────────────────────────────────────────
            html.H2("Ribbon", id="ribbon", style=S["section-heading"]),
            html.P("ribbon — rank changes over time, highest rank always on top.", style=S["section-desc"]),
            html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
                ribbon("Ribbon", subtitle="sample data",
                    x=sorted(_df_ribbon["dim_year"].unique().tolist()),
                    series=[{"name": entity,
                             "ranks": _df_ribbon.loc[_df_ribbon["dim_entity"] == entity
                                      ].sort_values("dim_year")["val_rank"].tolist()}
                            for entity in _df_ribbon["dim_entity"].unique().tolist()]),
            ])]),

            # ── 33. Candlestick ───────────────────────────────────────────────
            html.H2("Candlestick", id="candlestick", style=S["section-heading"]),
            html.P("candlestick — OHLC financial data (open, high, low, close) over time.", style=S["section-desc"]),
            html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
                candlestick("Candlestick", subtitle="sample OHLC data",
                    dates=m.DIMS["date"].values(_df_ohlc_a),
                    open_=_df_ohlc_a["open"].tolist(),
                    high= _df_ohlc_a["high"].tolist(),
                    low=  _df_ohlc_a["low"].tolist(),
                    close=_df_ohlc_a["close"].tolist()),
            ])]),

            # ── UI / Filter components ────────────────────────────────────────
            html.H2("UI / Filter components", id="slicers",
                    style={**S["section-heading"], "marginTop": "64px"}),
            html.P("Interactive filter controls. Connect to callbacks in the host app.", style=S["section-desc"]),

            # ── 34. Dropdown slicer ───────────────────────────────────────────
            html.H2("Dropdown slicer", id="slicer-dropdown", style=S["section-heading"]),
            html.P("dropdown_slicer — single select from a collapsed list.", style=S["section-desc"]),
            html.Div(style=S["group"], children=[html.Div(style={"maxWidth": "320px"}, children=[
                dropdown_slicer("Category", options=_categories, value=_categories[0]),
            ])]),

            # ── 35. List slicer ───────────────────────────────────────────────
            html.H2("List slicer", id="slicer-list", style=S["section-heading"]),
            html.P("list_slicer — checklist (multi=True) or radio (multi=False).", style=S["section-desc"]),
            html.Div(style=S["group"], children=[html.Div(style={"maxWidth": "320px"}, children=[
                list_slicer("Period", options=_periods, value=_periods[:2], multi=True),
            ])]),

            # ── 36. Range slicer ──────────────────────────────────────────────
            html.H2("Range slicer", id="slicer-range", style=S["section-heading"]),
            html.P("range_slicer — dual-handle numeric range slider.", style=S["section-desc"]),
            html.Div(style=S["group"], children=[html.Div(style={"maxWidth": "480px"}, children=[
                range_slicer("Value range", min_val=0, max_val=100, value=[20, 80]),
            ])]),

            # ── 37. Date range slicer ─────────────────────────────────────────
            html.H2("Date range slicer", id="slicer-date", style=S["section-heading"]),
            html.P("date_range_slicer — start and end date picker.", style=S["section-desc"]),
            html.Div(style=S["group"], children=[html.Div(style={"maxWidth": "480px"}, children=[
                date_range_slicer("Date range", start_date="2024-01-01", end_date="2024-12-31"),
            ])]),

            # ── 38. Tile slicer ───────────────────────────────────────────────
            html.H2("Tile slicer", id="slicer-tile", style=S["section-heading"]),
            html.P("tile_slicer — clickable button tiles, single or multi-select.", style=S["section-desc"]),
            html.Div(style=S["group"], children=[html.Div(style={"maxWidth": "480px"}, children=[
                tile_slicer("Period", options=_periods, value=_periods[0]),
            ])]),

            # ── Colour palette reference ──────────────────────────────────────
            html.H2("Colour palette", id="palette", style=S["section-heading"]),
            html.P("Colours, typography and base settings of the Teal theme.", style=S["section-desc"]),

            *[
                html.Div(style={"marginBottom": "28px"}, children=[
                    html.Div(label, style={"fontSize": "13px", "fontWeight": "600",
                                           "color": TEXT, "marginBottom": "12px"}),
                    html.Div(style={"display": "flex", "gap": "16px", "flexWrap": "wrap"}, children=[
                        _color_swatch(n, c) for n, c in swatches
                    ]),
                ])
                for label, swatches in [
                    ("Tło i powierzchnie",     [("BG_PAGE", BG_PAGE), ("BG_SURFACE", BG_SURFACE),
                                                ("BORDER", BORDER), ("GRID", GRID), ("ZERO_LINE", ZERO_LINE)]),
                    ("Tekst",                  [("TEXT", TEXT), ("SUBTEXT", SUBTEXT), ("MUTED", MUTED)]),
                    ("Teal (zielonkawy)",       [("TEAL_1", TEAL_1), ("TEAL_2", TEAL_2),
                                                ("TEAL_3", TEAL_3), ("TEAL_4", TEAL_4), ("TEAL_PALE", TEAL_PALE)]),
                    ("Azure (niebieski)",       [("AZURE_1", AZURE_1), ("AZURE_2", AZURE_2),
                                                ("AZURE_3", AZURE_3), ("AZURE_4", AZURE_4), ("AZURE_PALE", AZURE_PALE)]),
                    ("Slate (szary)",           [("SLATE_1", SLATE_1), ("SLATE_2", SLATE_2),
                                                ("SLATE_3", SLATE_3), ("SLATE_4", SLATE_4)]),
                    ("Semantyczne",             [("POSITIVE", POSITIVE), ("NEGATIVE", NEGATIVE), ("WARNING", WARNING)]),
                    ("COLORWAY — kolejność",    [(f"[{i}]", c) for i, c in enumerate(COLORWAY)]),
                ]
            ],
        ]),

        html.Hr(style=S["footer-divider"]),

        html.Footer(style=S["main-footer"], children=[
            html.Span("Open Reporting — visual components template", style=S["footer-text"]),
            html.A("open-reporting.dev", href="https://open-reporting.dev",
                   style={**S["footer-text"], "textDecoration": "none"}),
        ]),
    ]),
])

# ── Sidebar toggle callback ───────────────────────────────────────────────────

@callback(
    Output("sidebar", "style"),
    Output("btn-toggle", "style"),
    Output("sidebar-logo", "style"),
    Output("sidebar-nav", "style"),
    Output("sidebar-logo-img", "style"),
    Input("btn-toggle", "n_clicks"),
    State("sidebar", "style"),
    prevent_initial_call=True,
)
def toggle_sidebar(n_clicks, sidebar_style):
    is_expanded = sidebar_style.get("width", SIDEBAR_W) == SIDEBAR_W

    btn_open   = {**S["toggle-btn"], "right": "10px", "transform": "none"}
    btn_closed = {**S["toggle-btn"], "right": "50%", "transform": "translateX(50%)"}

    if is_expanded:
        return ({**sidebar_style, "width": SIDEBAR_COLLAPSED},
                btn_closed, {"display": "none"}, {"display": "none"}, {"display": "none"})
    else:
        return (S["sidebar"], btn_open, S["sidebar-logo"], S["sidebar-nav"], S["logo"])

# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    log.info("Starting Template dashboard on port %d", PORT)
    app.run(host="0.0.0.0", port=PORT, debug=False)
