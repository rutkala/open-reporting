#!/usr/bin/env python3
"""
Open Reporting — Template Dashboard
Developer reference: every chart component variant displayed with sample data.

Maintained showroom of the ``complex_dashboard`` skill — the page shell
(sidebar + header + footer + toggle) is rendered by the skill's
``runtime`` helpers, so any change to the skill is reflected here
automatically.

Copy this directory, rename, and customise for your domain.

Run:
    PYTHONPATH=/opt/open-reporting:/opt/open-reporting/.claude/skills \
    DUCKDB_PATH=/opt/open-reporting/data/warehouse.duckdb \
    python3 products/dashboards/template/app.py
"""
import logging

from dash import html

import products.visuals.lib.theme as _theme  # noqa: F401 — registers 'teal' template
from products.visuals.lib.theme import (
    BG_PAGE, BG_SURFACE, BORDER,
    COLORWAY, GRID, MUTED, NEGATIVE, POSITIVE,
    SUBTEXT, TEXT, WARNING, ZERO_LINE,
    TEAL_1, TEAL_2, TEAL_3, TEAL_4, TEAL_PALE,
    AZURE_1, AZURE_2, AZURE_3, AZURE_4, AZURE_PALE,
    SLATE_1, SLATE_2, SLATE_3, SLATE_4,
)

from complex_dashboard.assets.runtime import (
    S,
    build_page_layout,
    make_app,
    register_toggle_callback,
)

# ── Chart components ──────────────────────────────────────────────────────────
from products.visuals.components.kpi_card import kpi_row, kpi_standard, kpi_compact
from products.visuals.components.bar_chart import (
    clustered_column, stacked_column, pct_stacked_column,
    clustered_bar, stacked_bar, pct_stacked_bar,
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

app = make_app(domain="template", title="Template", module_name=__name__)

# ── Sidebar nav ───────────────────────────────────────────────────────────────
# (label, anchor_id) — anchor_id=None renders a non-clickable section separator.

_SECTIONS: list[tuple[str, str | None]] = [
    ("KPI card",                    "kpi"),
    ("Clustered column",            "col-clustered"),
    ("Stacked column",              "col-stacked"),
    ("100% stacked column",         "col-pct"),
    ("Clustered+stacked column",    "col-cs"),
    ("Clustered bar",               "bar-clustered"),
    ("Stacked bar",                 "bar-stacked"),
    ("100% stacked bar",            "bar-pct"),
    ("Clustered+stacked bar",       "bar-cs"),
    ("Line",                        "line"),
    ("Clustered area",              "area-clustered"),
    ("Stacked area",                "area-stacked"),
    ("100% stacked area",           "area-pct"),
    ("Line + clustered column",     "combo-lc"),
    ("Line + stacked column",       "combo-ls"),
    ("Line + 100% stacked column",  "combo-lp"),
    ("Scatter / Bubble",            "scatter"),
    ("Pie / Donut",                 "pie"),
    ("Treemap",                     "treemap"),
    ("Funnel",                      "funnel"),
    ("Waterfall — contribution",    "waterfall-contribution"),
    ("Waterfall — variance",        "waterfall-variance"),
    ("Histogram",                   "histogram"),
    ("Box plot",                    "boxplot"),
    ("Gauge",                       "gauge"),
    ("Bullet",                      "bullet"),
    ("Table",                       "table"),
    ("Matrix / Pivot",              "matrix"),
    ("Data list",                   "datalist"),
    ("Heatmap",                     "heatmap"),
    ("Choropleth map",              "choropleth"),
    ("Bubble map",                  "bubblemap"),
    ("Ribbon",                      "ribbon"),
    ("Candlestick",                 "candlestick"),
    ("— UI / Filters —",            None),
    ("Dropdown slicer",             "slicer-dropdown"),
    ("List slicer",                 "slicer-list"),
    ("Range slicer",                "slicer-range"),
    ("Date range slicer",           "slicer-date"),
    ("Tile slicer",                 "slicer-tile"),
    ("Colour palette",              "palette"),
]

# ── Page content (chart sections) ─────────────────────────────────────────────

_content = [

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
                        m.MEASURES["measure_a"].to_series(_df_by_cat["val_a"].tolist()),
                        m.MEASURES["measure_b"].to_series(_df_by_cat["val_b"].tolist()),
                        m.MEASURES["measure_c"].to_series(_df_by_cat["val_c"].tolist()),
                    ],
                    y_measure=m.MEASURES["measure_a"]),
            ])]),

            # ── 2. Stacked column ─────────────────────────────────────────────
            html.H2("Stacked column", id="col-stacked", style=S["section-heading"]),
            html.P("stacked_column — vertical bars stacked, shows total and composition.", style=S["section-desc"]),
            html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
                stacked_column("Stacked column", subtitle="Sample data 2018–2024",
                    x=_years,
                    series=[
                        m.MEASURES["measure_a"].to_series(_df_by_year["val_a"].tolist()),
                        m.MEASURES["measure_b"].to_series(_df_by_year["val_b"].tolist()),
                        m.MEASURES["measure_c"].to_series(_df_by_year["val_c"].tolist()),
                        m.MEASURES["measure_d"].to_series(_df_by_year["val_d"].tolist()),
                    ],
                    y_measure=m.MEASURES["measure_a"]),
            ])]),

            # ── 3. 100% stacked column ────────────────────────────────────────
            html.H2("100% stacked column", id="col-pct", style=S["section-heading"]),
            html.P("pct_stacked_column — normalised to 100%, shows composition only.", style=S["section-desc"]),
            html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
                pct_stacked_column("100% stacked column", subtitle="sample data",
                    x=_categories,
                    series=[
                        m.MEASURES["measure_a"].to_series(_df_by_cat["val_a"].tolist()),
                        m.MEASURES["measure_b"].to_series(_df_by_cat["val_b"].tolist()),
                        m.MEASURES["measure_c"].to_series(_df_by_cat["val_c"].tolist()),
                    ],
                    y_measure=m.MEASURES["measure_a"]),
            ])]),

            # ── 4. Clustered + stacked column ─────────────────────────────────
            html.H2("Clustered + stacked column", id="col-cs", style=S["section-heading"]),
            html.P("clustered_stacked_column — groups side by side, series stacked within each group.", style=S["section-desc"]),
            html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
                clustered_stacked_column("Clustered + stacked column", subtitle="sample data",
                    x=_categories, groups=_groups_cs,
                    y_measure=m.MEASURES["measure_a"]),
            ])]),

            # ── 5. Clustered bar ──────────────────────────────────────────────
            html.H2("Clustered bar", id="bar-clustered", style=S["section-heading"]),
            html.P("clustered_bar — horizontal grouped bars; single series sorts descending (ranking).", style=S["section-desc"]),
            html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
                clustered_bar("Clustered bar", subtitle="sample data — sorted descending",
                    categories=m.DIMS["label"].values(_df_geo),
                    series=[m.MEASURES["geo_a"].to_series(_df_geo["val_a"].tolist())],
                    y_measure=m.MEASURES["geo_a"]),
            ])]),

            # ── 6. Stacked bar ────────────────────────────────────────────────
            html.H2("Stacked bar", id="bar-stacked", style=S["section-heading"]),
            html.P("stacked_bar — horizontal stacked bars, shows total and composition.", style=S["section-desc"]),
            html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
                stacked_bar("Stacked bar", subtitle="sample data",
                    categories=_categories,
                    series=[
                        m.MEASURES["measure_a"].to_series(_df_by_cat["val_a"].tolist()),
                        m.MEASURES["measure_b"].to_series(_df_by_cat["val_b"].tolist()),
                        m.MEASURES["measure_c"].to_series(_df_by_cat["val_c"].tolist()),
                    ],
                    y_measure=m.MEASURES["measure_a"]),
            ])]),

            # ── 7. 100% stacked bar ───────────────────────────────────────────
            html.H2("100% stacked bar", id="bar-pct", style=S["section-heading"]),
            html.P("pct_stacked_bar — normalised to 100%, horizontal, composition only.", style=S["section-desc"]),
            html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
                pct_stacked_bar("100% stacked bar", subtitle="sample data",
                    categories=_categories,
                    series=[
                        m.MEASURES["measure_a"].to_series(_df_by_cat["val_a"].tolist()),
                        m.MEASURES["measure_b"].to_series(_df_by_cat["val_b"].tolist()),
                        m.MEASURES["measure_c"].to_series(_df_by_cat["val_c"].tolist()),
                    ]),
            ])]),

            # ── 8. Clustered + stacked bar ────────────────────────────────────
            html.H2("Clustered + stacked bar", id="bar-cs", style=S["section-heading"]),
            html.P("clustered_stacked_bar — horizontal variant of clustered+stacked.", style=S["section-desc"]),
            html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
                clustered_stacked_bar("Clustered + stacked bar", subtitle="sample data",
                    categories=_categories, groups=_groups_cs,
                    y_measure=m.MEASURES["measure_a"]),
            ])]),

            # ── 9. Line ───────────────────────────────────────────────────────
            html.H2("Line", id="line", style=S["section-heading"]),
            html.P("line — trends over time, one or multiple series. Supports reference line.", style=S["section-desc"]),
            html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
                line("Line", subtitle="Sample data 2018–2024",
                    x=_years,
                    series=[
                        m.MEASURES["measure_a"].to_series(_df_by_year["val_a"].tolist()),
                        m.MEASURES["measure_b"].to_series(_df_by_year["val_b"].tolist()),
                        m.MEASURES["measure_e"].to_series(_df_by_year["val_e"].tolist()),
                    ],
                    reference={"value": _scalars["measure_b"], "label": "Reference"},
                    y_measure=m.MEASURES["measure_a"]),
            ])]),

            # ── 10. Clustered area ────────────────────────────────────────────
            html.H2("Clustered area", id="area-clustered", style=S["section-heading"]),
            html.P("area — all series fill from zero, overlapping with transparency. Shows volume.", style=S["section-desc"]),
            html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
                area("Clustered area", subtitle="Sample data 2018–2024",
                    x=_years,
                    series=[
                        m.MEASURES["measure_a"].to_series(_df_by_year["val_a"].tolist()),
                        m.MEASURES["measure_b"].to_series(_df_by_year["val_b"].tolist()),
                        m.MEASURES["measure_c"].to_series(_df_by_year["val_c"].tolist()),
                    ],
                    y_measure=m.MEASURES["measure_a"]),
            ])]),

            # ── 11. Stacked area ──────────────────────────────────────────────
            html.H2("Stacked area", id="area-stacked", style=S["section-heading"]),
            html.P("stacked_area — areas stacked cumulatively, shows total and composition over time.", style=S["section-desc"]),
            html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
                stacked_area("Stacked area", subtitle="Sample data 2018–2024",
                    x=_years,
                    series=[
                        m.MEASURES["measure_a"].to_series(_df_by_year["val_a"].tolist()),
                        m.MEASURES["measure_b"].to_series(_df_by_year["val_b"].tolist()),
                        m.MEASURES["measure_c"].to_series(_df_by_year["val_c"].tolist()),
                        m.MEASURES["measure_d"].to_series(_df_by_year["val_d"].tolist()),
                    ],
                    y_measure=m.MEASURES["measure_a"]),
            ])]),

            # ── 12. 100% stacked area ─────────────────────────────────────────
            html.H2("100% stacked area", id="area-pct", style=S["section-heading"]),
            html.P("pct_stacked_area — normalised to 100%, composition over time only.", style=S["section-desc"]),
            html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
                pct_stacked_area("100% stacked area", subtitle="Sample data 2018–2024",
                    x=_years,
                    series=[
                        m.MEASURES["measure_a"].to_series(_df_by_year["val_a"].tolist()),
                        m.MEASURES["measure_b"].to_series(_df_by_year["val_b"].tolist()),
                        m.MEASURES["measure_c"].to_series(_df_by_year["val_c"].tolist()),
                        m.MEASURES["measure_d"].to_series(_df_by_year["val_d"].tolist()),
                    ]),
            ])]),

            # ── 13. Line + clustered column ───────────────────────────────────
            html.H2("Line + clustered column", id="combo-lc", style=S["section-heading"]),
            html.P("line_clustered_column — line and grouped bars on a shared axis. Same scale only.", style=S["section-desc"]),
            html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
                line_clustered_column("Line + clustered column", subtitle="Sample data 2018–2024 — shared scale",
                    x=_years,
                    bar_series=[m.MEASURES["measure_a"].to_series(_df_by_year["val_a"].tolist())],
                    line_series=[m.MEASURES["measure_b"].to_series(_df_by_year["val_b"].tolist())],
                    y_measure=m.MEASURES["measure_a"]),
            ])]),

            # ── 14. Line + stacked column ─────────────────────────────────────
            html.H2("Line + stacked column", id="combo-ls", style=S["section-heading"]),
            html.P("line_stacked_column — stacked bars show components, line shows aggregate or rate.", style=S["section-desc"]),
            html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
                line_stacked_column("Line + stacked column", subtitle="Sample data 2018–2024",
                    x=_years,
                    bar_series=[
                        m.MEASURES["measure_a"].to_series(_df_by_year["val_a"].tolist()),
                        m.MEASURES["measure_c"].to_series(_df_by_year["val_c"].tolist()),
                        m.MEASURES["measure_d"].to_series(_df_by_year["val_d"].tolist()),
                    ],
                    line_series=[m.MEASURES["measure_b"].to_series(_df_by_year["val_b"].tolist())],
                    y_measure=m.MEASURES["measure_a"]),
            ])]),

            # ── 15. Line + 100% stacked column ───────────────────────────────
            html.H2("Line + 100% stacked column", id="combo-lp", style=S["section-heading"]),
            html.P("line_pct_stacked_column — 100% normalised bars with a rate or % line overlay.", style=S["section-desc"]),
            html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
                line_pct_stacked_column("Line + 100% stacked column", subtitle="Sample data 2018–2024",
                    x=_years,
                    bar_series=[
                        m.MEASURES["measure_a"].to_series(_df_by_year["val_a"].tolist()),
                        m.MEASURES["measure_b"].to_series(_df_by_year["val_b"].tolist()),
                        m.MEASURES["measure_c"].to_series(_df_by_year["val_c"].tolist()),
                    ],
                    line_series=[m.MEASURES["measure_e"].to_series(_df_by_year["val_e"].tolist())],
                    y_measure=m.MEASURES["measure_a"]),
            ])]),

            # ── 16. Scatter / Bubble ──────────────────────────────────────────
            html.H2("Scatter / Bubble", id="scatter", style=S["section-heading"]),
            html.P("scatter_bubble — X/Y correlation with bubble size as third variable. Variant: scatter_basic (no size).", style=S["section-desc"]),
            html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
                scatter_bubble("Scatter / Bubble", subtitle="sample data",
                    x=_df_sc["val_x"].tolist(),
                    y=_df_sc["val_y"].tolist(),
                    size=_df_sc["val_size"].tolist(),
                    labels=_df_sc["dim_label"].tolist(),
                    x_measure=m.MEASURES["measure_a"],
                    y_measure=m.MEASURES["measure_b"]),
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
                    total_label=_df_wf_c.loc[_df_wf_c["is_total"], "dim_stage"].iloc[0],
                    y_measure=m.MEASURES["measure_a"]),
            ])]),

            # ── 21. Waterfall — variance ──────────────────────────────────────
            html.H2("Waterfall — variance", id="waterfall-variance", style=S["section-heading"]),
            html.P("waterfall_variance — bridge between two absolute values; explains how a base becomes the final value.", style=S["section-desc"]),
            html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
                waterfall_variance("Waterfall — variance", subtitle="sample data",
                    categories=_df_wf_v["dim_stage"].tolist(),
                    values=_df_wf_v["val_amount"].tolist(),
                    y_measure=m.MEASURES["measure_a"]),
            ])]),

            # ── 22. Histogram ─────────────────────────────────────────────────
            html.H2("Histogram", id="histogram", style=S["section-heading"]),
            html.P("histogram — frequency distribution of a single numeric variable.", style=S["section-desc"]),
            html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
                histogram("Histogram", subtitle="sample data",
                    x=_df_dist["val_obs"].tolist(),
                    x_label=m.MEASURES["measure_a"].axis_label,
                    y_measure=m.MEASURES["measure_a"]),
            ])]),

            # ── 23. Box plot ──────────────────────────────────────────────────
            html.H2("Box plot", id="boxplot", style=S["section-heading"]),
            html.P("box_plot — median, IQR and outliers by group. Use for distribution comparisons.", style=S["section-desc"]),
            html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
                box_plot("Box plot", subtitle="sample data",
                    data={grp: _df_dist.loc[_df_dist["dim_group"] == grp, "val_obs"].tolist()
                          for grp in _dist_groups},
                    y_measure=m.MEASURES["measure_a"]),
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
                        y_measure=m.MEASURES["measure_a"]),
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
                        y_measure=m.MEASURES["measure_a"]),
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
                    close=_df_ohlc_a["close"].tolist(),
                    y_measure=m.MEASURES["measure_a"]),
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
                    ("Background & surfaces",  [("BG_PAGE", BG_PAGE), ("BG_SURFACE", BG_SURFACE),
                                                ("BORDER", BORDER), ("GRID", GRID), ("ZERO_LINE", ZERO_LINE)]),
                    ("Text",                   [("TEXT", TEXT), ("SUBTEXT", SUBTEXT), ("MUTED", MUTED)]),
                    ("Teal",                   [("TEAL_1", TEAL_1), ("TEAL_2", TEAL_2),
                                                ("TEAL_3", TEAL_3), ("TEAL_4", TEAL_4), ("TEAL_PALE", TEAL_PALE)]),
                    ("Azure",                  [("AZURE_1", AZURE_1), ("AZURE_2", AZURE_2),
                                                ("AZURE_3", AZURE_3), ("AZURE_4", AZURE_4), ("AZURE_PALE", AZURE_PALE)]),
                    ("Slate",                  [("SLATE_1", SLATE_1), ("SLATE_2", SLATE_2),
                                                ("SLATE_3", SLATE_3), ("SLATE_4", SLATE_4)]),
                    ("Semantic",               [("POSITIVE", POSITIVE), ("NEGATIVE", NEGATIVE), ("WARNING", WARNING)]),
                    ("COLORWAY — order",       [(f"[{i}]", c) for i, c in enumerate(COLORWAY)]),
                ]
            ],
]

# ── Page assembly ─────────────────────────────────────────────────────────────

app.layout = build_page_layout(
    domain="template",
    title="Visual components — reference",
    subtitle="One example per chart family — sample data",
    sections=_SECTIONS,
    content=_content,
    footer_name="Open Reporting — visual components template",
    footer_source="dane przykładowe",
    footer_updated="referencja komponentów",
)

register_toggle_callback(app)

# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    log.info("Starting Template dashboard on port %d", PORT)
    app.run(host="0.0.0.0", port=PORT, debug=False)
