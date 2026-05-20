#!/usr/bin/env python3
"""Visual-component showroom — built from the skill's runtime helpers.

Single source of truth for the "every-chart, every-control" reference
dashboard. The synthetic data + measures live in ``data_loaders.py`` and
``measures.py``; the page assembly here pulls them together into the 41
sections shown in ``_SECTIONS``.

Two callers:

- ``products/dashboards/template/app.py`` — runs this on port 8055
  under ``/template/``.
- ``assets/example/app.py`` — runs this on port 8060 under
  ``/example/``.

Both end up identical except for URL prefix and port — that is the
point. The showroom proves that any domain dashboard built on the
skill picks up the same theme, layout, components, and behaviour.
"""
from __future__ import annotations

from pathlib import Path

from dash import Dash, html

import complex_dashboard.assets.theme as _theme  # noqa: F401 — registers 'teal' template
from complex_dashboard.assets.theme import (
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
from complex_dashboard.assets.components.kpi_card import kpi_row, kpi_standard, kpi_compact
from complex_dashboard.assets.components.bar_chart import (
    clustered_column, stacked_column, pct_stacked_column,
    clustered_bar, stacked_bar, pct_stacked_bar,
    clustered_stacked_column, clustered_stacked_bar,
)
from complex_dashboard.assets.components.line_chart import (
    line, area, stacked_area, pct_stacked_area,
)
from complex_dashboard.assets.components.combo_chart import (
    line_clustered_column, line_stacked_column, line_pct_stacked_column,
)
from complex_dashboard.assets.components.waterfall_chart import waterfall_contribution, waterfall_variance
from complex_dashboard.assets.components.scatter_chart import scatter_bubble
from complex_dashboard.assets.components.distribution_chart import histogram, box_plot
from complex_dashboard.assets.components.special_chart import (
    funnel, treemap, gauge, bullet, ribbon, heatmap_matrix,
)
from complex_dashboard.assets.components.map_chart import choropleth_map, bubble_map
from complex_dashboard.assets.components.financial_chart import candlestick
from complex_dashboard.assets.components.table_chart import table_basic, table_matrix, data_list
from complex_dashboard.assets.components.pie_chart import pie_chart
from complex_dashboard.assets.components.slicer import (
    dropdown_slicer, list_slicer, range_slicer, date_range_slicer, tile_slicer,
)

from complex_dashboard.assets.example import data_loaders as _data
from complex_dashboard.assets.example import measures as m


# ── Sidebar nav ───────────────────────────────────────────────────────────────
# (label, anchor_id) — anchor_id=None renders a non-clickable section separator.
SECTIONS: list[tuple[str, str | None]] = [
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


def _build_content() -> list:
    """Return the showroom's section list (41 entries — see ``SECTIONS``)."""
    df_by_cat    = _data.load_by_category()
    df_by_year   = _data.load_by_year()
    df_by_period = _data.load_by_period()
    scalars      = _data.load_scalars()

    df_geo              = _data.load_geo()
    df_ohlc_a, _df_ohlc_b = _data.load_ohlc()
    df_sc               = _data.load_scatter()
    df_dist             = _data.load_distribution()
    df_wf_c, df_wf_v    = _data.load_waterfall()
    df_funnel           = _data.load_funnel()
    df_tree             = _data.load_treemap()
    df_ribbon           = _data.load_ribbon()
    df_hmap             = _data.load_heatmap()
    gauge_data          = _data.load_gauge()
    df_table            = _data.load_table()
    groups_cs           = _data.load_clustered_stacked()
    matrix              = _data.load_matrix()
    list_items          = _data.load_data_list()

    years       = m.DIMS["year"].values(df_by_year)
    categories  = m.DIMS["category"].values(df_by_cat)
    periods     = m.DIMS["period"].values(df_by_period)
    dist_groups = m.DIMS["group"].values(df_dist)

    return [

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
                    value=m.MEASURES["measure_a"].kpi_value(scalars["measure_a"]),
                    unit=m.MEASURES["measure_a"].plotly_ticksuffix,
                    subtitle="Average 2018–2024",
                    reference_value=m.MEASURES["measure_a"].kpi_value(50.0),
                    reference_label="Target",
                    trend="▲ +0.8",
                    trend_color=POSITIVE,
                ),
                kpi_standard(
                    label=m.MEASURES["measure_b"].label,
                    value=m.MEASURES["measure_b"].kpi_value(scalars["measure_b"]),
                    unit=m.MEASURES["measure_b"].plotly_ticksuffix,
                    reference_value=m.MEASURES["measure_b"].kpi_value(40.0),
                    reference_label="Prior year",
                ),
                kpi_standard(
                    label=m.MEASURES["measure_a_pct"].label,
                    value=m.MEASURES["measure_a_pct"].kpi_value(scalars["measure_a_pct"]),
                    unit=m.MEASURES["measure_a_pct"].plotly_ticksuffix,
                    trend="▼ -1.2",
                    trend_color=NEGATIVE,
                ),
                kpi_standard(
                    label=m.MEASURES["measure_a_cum"].label,
                    value=m.MEASURES["measure_a_cum"].kpi_value(scalars["measure_a_cum"]),
                    unit=m.MEASURES["measure_a_cum"].plotly_ticksuffix,
                    subtitle="All years combined",
                ),
            ]),
        ]),
        html.Div(style=S["group"], children=[
            kpi_row([
                kpi_compact(
                    label=m.MEASURES["measure_a"].label,
                    value=m.MEASURES["measure_a"].kpi_value(scalars["measure_a"]),
                    unit=m.MEASURES["measure_a"].plotly_ticksuffix,
                    trend="▲ +0.8", trend_color=POSITIVE,
                ),
                kpi_compact(
                    label=m.MEASURES["measure_b"].label,
                    value=m.MEASURES["measure_b"].kpi_value(scalars["measure_b"]),
                    unit=m.MEASURES["measure_b"].plotly_ticksuffix,
                ),
                kpi_compact(
                    label=m.MEASURES["measure_c"].label,
                    value=m.MEASURES["measure_c"].kpi_value(scalars["measure_c"]),
                    unit=m.MEASURES["measure_c"].plotly_ticksuffix,
                ),
                kpi_compact(
                    label=m.MEASURES["measure_d"].label,
                    value=m.MEASURES["measure_d"].kpi_value(scalars["measure_d"]),
                    unit=m.MEASURES["measure_d"].plotly_ticksuffix,
                ),
                kpi_compact(
                    label=m.MEASURES["measure_a_pct"].label,
                    value=m.MEASURES["measure_a_pct"].kpi_value(scalars["measure_a_pct"]),
                    unit=m.MEASURES["measure_a_pct"].plotly_ticksuffix,
                    trend="▼ -1.2", trend_color=NEGATIVE,
                ),
            ], min_width="140px", gap="12px"),
        ]),
        html.Div(style=S["group"], children=[
            kpi_row([
                kpi_standard(
                    label=m.MEASURES["measure_a"].label,
                    value=m.MEASURES["measure_a"].kpi_value(scalars["measure_a"]),
                    unit=m.MEASURES["measure_a"].plotly_ticksuffix,
                    badge=("✓ Target", POSITIVE),
                    value_color=POSITIVE,
                ),
                kpi_standard(
                    label=m.MEASURES["measure_b"].label,
                    value=m.MEASURES["measure_b"].kpi_value(scalars["measure_b"]),
                    unit=m.MEASURES["measure_b"].plotly_ticksuffix,
                    badge=("✗ Limit", NEGATIVE),
                    value_color=NEGATIVE,
                ),
                kpi_standard(
                    label=m.MEASURES["measure_c"].label,
                    value=m.MEASURES["measure_c"].kpi_value(scalars["measure_c"]),
                    unit=m.MEASURES["measure_c"].plotly_ticksuffix,
                    badge=("Watch", WARNING),
                    value_color=WARNING,
                ),
            ]),
        ]),

        # ── 1. Clustered column ───────────────────────────────────────────
        html.H2("Clustered column", id="col-clustered", style=S["section-heading"]),
        html.P("clustered_column — grouped vertical bars, compare multiple series side by side.", style=S["section-desc"]),
        html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
            clustered_column("Clustered column", subtitle="sample data",
                x=categories,
                series=[
                    m.MEASURES["measure_a"].to_series(df_by_cat["val_a"].tolist()),
                    m.MEASURES["measure_b"].to_series(df_by_cat["val_b"].tolist()),
                    m.MEASURES["measure_c"].to_series(df_by_cat["val_c"].tolist()),
                ],
                y_measure=m.MEASURES["measure_a"]),
        ])]),

        # ── 2. Stacked column ─────────────────────────────────────────────
        html.H2("Stacked column", id="col-stacked", style=S["section-heading"]),
        html.P("stacked_column — vertical bars stacked, shows total and composition.", style=S["section-desc"]),
        html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
            stacked_column("Stacked column", subtitle="Sample data 2018–2024",
                x=years,
                series=[
                    m.MEASURES["measure_a"].to_series(df_by_year["val_a"].tolist()),
                    m.MEASURES["measure_b"].to_series(df_by_year["val_b"].tolist()),
                    m.MEASURES["measure_c"].to_series(df_by_year["val_c"].tolist()),
                    m.MEASURES["measure_d"].to_series(df_by_year["val_d"].tolist()),
                ],
                y_measure=m.MEASURES["measure_a"]),
        ])]),

        # ── 3. 100% stacked column ────────────────────────────────────────
        html.H2("100% stacked column", id="col-pct", style=S["section-heading"]),
        html.P("pct_stacked_column — normalised to 100%, shows composition only.", style=S["section-desc"]),
        html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
            pct_stacked_column("100% stacked column", subtitle="sample data",
                x=categories,
                series=[
                    m.MEASURES["measure_a"].to_series(df_by_cat["val_a"].tolist()),
                    m.MEASURES["measure_b"].to_series(df_by_cat["val_b"].tolist()),
                    m.MEASURES["measure_c"].to_series(df_by_cat["val_c"].tolist()),
                ],
                y_measure=m.MEASURES["measure_a"]),
        ])]),

        # ── 4. Clustered + stacked column ─────────────────────────────────
        html.H2("Clustered + stacked column", id="col-cs", style=S["section-heading"]),
        html.P("clustered_stacked_column — groups side by side, series stacked within each group.", style=S["section-desc"]),
        html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
            clustered_stacked_column("Clustered + stacked column", subtitle="sample data",
                x=categories, groups=groups_cs,
                y_measure=m.MEASURES["measure_a"]),
        ])]),

        # ── 5. Clustered bar ──────────────────────────────────────────────
        html.H2("Clustered bar", id="bar-clustered", style=S["section-heading"]),
        html.P("clustered_bar — horizontal grouped bars; single series sorts descending (ranking).", style=S["section-desc"]),
        html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
            clustered_bar("Clustered bar", subtitle="sample data — sorted descending",
                categories=m.DIMS["label"].values(df_geo),
                series=[m.MEASURES["geo_a"].to_series(df_geo["val_a"].tolist())],
                y_measure=m.MEASURES["geo_a"]),
        ])]),

        # ── 6. Stacked bar ────────────────────────────────────────────────
        html.H2("Stacked bar", id="bar-stacked", style=S["section-heading"]),
        html.P("stacked_bar — horizontal stacked bars, shows total and composition.", style=S["section-desc"]),
        html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
            stacked_bar("Stacked bar", subtitle="sample data",
                categories=categories,
                series=[
                    m.MEASURES["measure_a"].to_series(df_by_cat["val_a"].tolist()),
                    m.MEASURES["measure_b"].to_series(df_by_cat["val_b"].tolist()),
                    m.MEASURES["measure_c"].to_series(df_by_cat["val_c"].tolist()),
                ],
                y_measure=m.MEASURES["measure_a"]),
        ])]),

        # ── 7. 100% stacked bar ───────────────────────────────────────────
        html.H2("100% stacked bar", id="bar-pct", style=S["section-heading"]),
        html.P("pct_stacked_bar — normalised to 100%, horizontal, composition only.", style=S["section-desc"]),
        html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
            pct_stacked_bar("100% stacked bar", subtitle="sample data",
                categories=categories,
                series=[
                    m.MEASURES["measure_a"].to_series(df_by_cat["val_a"].tolist()),
                    m.MEASURES["measure_b"].to_series(df_by_cat["val_b"].tolist()),
                    m.MEASURES["measure_c"].to_series(df_by_cat["val_c"].tolist()),
                ]),
        ])]),

        # ── 8. Clustered + stacked bar ────────────────────────────────────
        html.H2("Clustered + stacked bar", id="bar-cs", style=S["section-heading"]),
        html.P("clustered_stacked_bar — horizontal variant of clustered+stacked.", style=S["section-desc"]),
        html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
            clustered_stacked_bar("Clustered + stacked bar", subtitle="sample data",
                categories=categories, groups=groups_cs,
                y_measure=m.MEASURES["measure_a"]),
        ])]),

        # ── 9. Line ───────────────────────────────────────────────────────
        html.H2("Line", id="line", style=S["section-heading"]),
        html.P("line — trends over time, one or multiple series. Supports reference line.", style=S["section-desc"]),
        html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
            line("Line", subtitle="Sample data 2018–2024",
                x=years,
                series=[
                    m.MEASURES["measure_a"].to_series(df_by_year["val_a"].tolist()),
                    m.MEASURES["measure_b"].to_series(df_by_year["val_b"].tolist()),
                    m.MEASURES["measure_e"].to_series(df_by_year["val_e"].tolist()),
                ],
                reference={"value": scalars["measure_b"], "label": "Reference"},
                y_measure=m.MEASURES["measure_a"]),
        ])]),

        # ── 10. Clustered area ────────────────────────────────────────────
        html.H2("Clustered area", id="area-clustered", style=S["section-heading"]),
        html.P("area — all series fill from zero, overlapping with transparency. Shows volume.", style=S["section-desc"]),
        html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
            area("Clustered area", subtitle="Sample data 2018–2024",
                x=years,
                series=[
                    m.MEASURES["measure_a"].to_series(df_by_year["val_a"].tolist()),
                    m.MEASURES["measure_b"].to_series(df_by_year["val_b"].tolist()),
                    m.MEASURES["measure_c"].to_series(df_by_year["val_c"].tolist()),
                ],
                y_measure=m.MEASURES["measure_a"]),
        ])]),

        # ── 11. Stacked area ──────────────────────────────────────────────
        html.H2("Stacked area", id="area-stacked", style=S["section-heading"]),
        html.P("stacked_area — areas stacked cumulatively, shows total and composition over time.", style=S["section-desc"]),
        html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
            stacked_area("Stacked area", subtitle="Sample data 2018–2024",
                x=years,
                series=[
                    m.MEASURES["measure_a"].to_series(df_by_year["val_a"].tolist()),
                    m.MEASURES["measure_b"].to_series(df_by_year["val_b"].tolist()),
                    m.MEASURES["measure_c"].to_series(df_by_year["val_c"].tolist()),
                    m.MEASURES["measure_d"].to_series(df_by_year["val_d"].tolist()),
                ],
                y_measure=m.MEASURES["measure_a"]),
        ])]),

        # ── 12. 100% stacked area ─────────────────────────────────────────
        html.H2("100% stacked area", id="area-pct", style=S["section-heading"]),
        html.P("pct_stacked_area — normalised to 100%, composition over time only.", style=S["section-desc"]),
        html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
            pct_stacked_area("100% stacked area", subtitle="Sample data 2018–2024",
                x=years,
                series=[
                    m.MEASURES["measure_a"].to_series(df_by_year["val_a"].tolist()),
                    m.MEASURES["measure_b"].to_series(df_by_year["val_b"].tolist()),
                    m.MEASURES["measure_c"].to_series(df_by_year["val_c"].tolist()),
                    m.MEASURES["measure_d"].to_series(df_by_year["val_d"].tolist()),
                ]),
        ])]),

        # ── 13. Line + clustered column ───────────────────────────────────
        html.H2("Line + clustered column", id="combo-lc", style=S["section-heading"]),
        html.P("line_clustered_column — line and grouped bars on a shared axis. Same scale only.", style=S["section-desc"]),
        html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
            line_clustered_column("Line + clustered column", subtitle="Sample data 2018–2024 — shared scale",
                x=years,
                bar_series=[m.MEASURES["measure_a"].to_series(df_by_year["val_a"].tolist())],
                line_series=[m.MEASURES["measure_b"].to_series(df_by_year["val_b"].tolist())],
                y_measure=m.MEASURES["measure_a"]),
        ])]),

        # ── 14. Line + stacked column ─────────────────────────────────────
        html.H2("Line + stacked column", id="combo-ls", style=S["section-heading"]),
        html.P("line_stacked_column — stacked bars show components, line shows aggregate or rate.", style=S["section-desc"]),
        html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
            line_stacked_column("Line + stacked column", subtitle="Sample data 2018–2024",
                x=years,
                bar_series=[
                    m.MEASURES["measure_a"].to_series(df_by_year["val_a"].tolist()),
                    m.MEASURES["measure_c"].to_series(df_by_year["val_c"].tolist()),
                    m.MEASURES["measure_d"].to_series(df_by_year["val_d"].tolist()),
                ],
                line_series=[m.MEASURES["measure_b"].to_series(df_by_year["val_b"].tolist())],
                y_measure=m.MEASURES["measure_a"]),
        ])]),

        # ── 15. Line + 100% stacked column ───────────────────────────────
        html.H2("Line + 100% stacked column", id="combo-lp", style=S["section-heading"]),
        html.P("line_pct_stacked_column — 100% normalised bars with a rate or % line overlay.", style=S["section-desc"]),
        html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
            line_pct_stacked_column("Line + 100% stacked column", subtitle="Sample data 2018–2024",
                x=years,
                bar_series=[
                    m.MEASURES["measure_a"].to_series(df_by_year["val_a"].tolist()),
                    m.MEASURES["measure_b"].to_series(df_by_year["val_b"].tolist()),
                    m.MEASURES["measure_c"].to_series(df_by_year["val_c"].tolist()),
                ],
                line_series=[m.MEASURES["measure_e"].to_series(df_by_year["val_e"].tolist())],
                y_measure=m.MEASURES["measure_a"]),
        ])]),

        # ── 16. Scatter / Bubble ──────────────────────────────────────────
        html.H2("Scatter / Bubble", id="scatter", style=S["section-heading"]),
        html.P("scatter_bubble — X/Y correlation with bubble size as third variable. Variant: scatter_basic (no size).", style=S["section-desc"]),
        html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
            scatter_bubble("Scatter / Bubble", subtitle="sample data",
                x=df_sc["val_x"].tolist(),
                y=df_sc["val_y"].tolist(),
                size=df_sc["val_size"].tolist(),
                labels=df_sc["dim_label"].tolist(),
                x_measure=m.MEASURES["measure_a"],
                y_measure=m.MEASURES["measure_b"]),
        ])]),

        # ── 17. Pie / Donut ───────────────────────────────────────────────
        html.H2("Pie / Donut", id="pie", style=S["section-heading"]),
        html.P("pie_chart — part-to-whole for 2–5 categories. Donut by default; pie via donut=False.", style=S["section-desc"]),
        html.Div(style=S["group"], children=[html.Div(style={"maxWidth": "360px"}, children=[
            html.Div(style=S["card"], children=[
                pie_chart("Pie / Donut", subtitle="sample data — donut variant",
                    labels=categories, values=df_by_cat["val_a"].tolist()),
            ]),
        ])]),

        # ── 18. Treemap ───────────────────────────────────────────────────
        html.H2("Treemap", id="treemap", style=S["section-heading"]),
        html.P("treemap — hierarchical part-to-whole, rectangle size = value.", style=S["section-desc"]),
        html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
            treemap("Treemap", subtitle="sample data",
                labels=df_tree["dim_node"].tolist(),
                parents=df_tree["dim_parent"].tolist(),
                values=df_tree["val_size"].tolist()),
        ])]),

        # ── 19. Funnel ────────────────────────────────────────────────────
        html.H2("Funnel", id="funnel", style=S["section-heading"]),
        html.P("funnel — sequential stages with drop-off, conversion tracking.", style=S["section-desc"]),
        html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
            funnel("Funnel", subtitle="sample data",
                stages=df_funnel["dim_stage"].tolist(),
                values=df_funnel["val_count"].tolist()),
        ])]),

        # ── 20. Waterfall — contribution ──────────────────────────────────
        html.H2("Waterfall — contribution", id="waterfall-contribution", style=S["section-heading"]),
        html.P("waterfall_contribution — components building a total; bars show additive decomposition of the final result.", style=S["section-desc"]),
        html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
            waterfall_contribution("Waterfall — contribution", subtitle="sample data",
                categories=df_wf_c["dim_stage"].tolist(),
                values=df_wf_c["val_amount"].tolist(),
                total_label=df_wf_c.loc[df_wf_c["is_total"], "dim_stage"].iloc[0],
                y_measure=m.MEASURES["measure_a"]),
        ])]),

        # ── 21. Waterfall — variance ──────────────────────────────────────
        html.H2("Waterfall — variance", id="waterfall-variance", style=S["section-heading"]),
        html.P("waterfall_variance — bridge between two absolute values; explains how a base becomes the final value.", style=S["section-desc"]),
        html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
            waterfall_variance("Waterfall — variance", subtitle="sample data",
                categories=df_wf_v["dim_stage"].tolist(),
                values=df_wf_v["val_amount"].tolist(),
                y_measure=m.MEASURES["measure_a"]),
        ])]),

        # ── 22. Histogram ─────────────────────────────────────────────────
        html.H2("Histogram", id="histogram", style=S["section-heading"]),
        html.P("histogram — frequency distribution of a single numeric variable.", style=S["section-desc"]),
        html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
            histogram("Histogram", subtitle="sample data",
                x=df_dist["val_obs"].tolist(),
                x_label=m.MEASURES["measure_a"].axis_label,
                y_measure=m.MEASURES["measure_a"]),
        ])]),

        # ── 23. Box plot ──────────────────────────────────────────────────
        html.H2("Box plot", id="boxplot", style=S["section-heading"]),
        html.P("box_plot — median, IQR and outliers by group. Use for distribution comparisons.", style=S["section-desc"]),
        html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
            box_plot("Box plot", subtitle="sample data",
                data={grp: df_dist.loc[df_dist["dim_group"] == grp, "val_obs"].tolist()
                      for grp in dist_groups},
                y_measure=m.MEASURES["measure_a"]),
        ])]),

        # ── 24. Gauge ─────────────────────────────────────────────────────
        html.H2("Gauge", id="gauge", style=S["section-heading"]),
        html.P("gauge — single value measured against a range with a reference point.", style=S["section-desc"]),
        html.Div(style=S["group"], children=[html.Div(style={"maxWidth": "360px"}, children=[
            html.Div(style=S["card"], children=[
                gauge("Gauge", subtitle="sample data",
                    value=gauge_data["gauge_value"],
                    min_val=0, max_val=gauge_data["gauge_max"],
                    reference=gauge_data["gauge_target"],
                    y_measure=m.MEASURES["measure_a"]),
            ]),
        ])]),

        # ── 25. Bullet ────────────────────────────────────────────────────
        html.H2("Bullet", id="bullet", style=S["section-heading"]),
        html.P("bullet — value vs target with a background range. Precise goal tracking.", style=S["section-desc"]),
        html.Div(style=S["group"], children=[html.Div(style={"maxWidth": "360px"}, children=[
            html.Div(style=S["card"], children=[
                bullet("Bullet", subtitle="sample data",
                    value=gauge_data["bullet_a_value"],
                    target=gauge_data["bullet_a_target"],
                    max_val=gauge_data["bullet_a_max"],
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
                      for _, row in df_table.iterrows()],
                number_cols={1, 2, 3, 4}),
        ])]),

        # ── 27. Matrix / Pivot ────────────────────────────────────────────
        html.H2("Matrix / Pivot table", id="matrix", style=S["section-heading"]),
        html.P("table_matrix — row dimension × column dimension, values at intersections.", style=S["section-desc"]),
        html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
            table_matrix("Matrix / Pivot table", subtitle="sample data",
                row_labels=matrix["row_labels"],
                col_labels=matrix["col_labels"],
                values=matrix["values"],
                row_dim="Category"),
        ])]),

        # ── 28. Data list ─────────────────────────────────────────────────
        html.H2("Data list", id="datalist", style=S["section-heading"]),
        html.P("data_list — scrollable list of labelled items with optional values.", style=S["section-desc"]),
        html.Div(style=S["group"], children=[html.Div(style={"maxWidth": "360px"}, children=[
            data_list("Data list", subtitle="sample data", items=list_items),
        ])]),

        # ── 29. Heatmap ───────────────────────────────────────────────────
        html.H2("Heatmap", id="heatmap", style=S["section-heading"]),
        html.P("heatmap_matrix — matrix of values coloured by intensity, diverging or sequential.", style=S["section-desc"]),
        html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
            heatmap_matrix("Heatmap", subtitle="sample data — diverging colour scale",
                x_labels=df_hmap["dim_col"].unique().tolist(),
                y_labels=df_hmap["dim_row"].unique().tolist(),
                z_values=[df_hmap.loc[df_hmap["dim_row"] == row, "val_z"].tolist()
                           for row in df_hmap["dim_row"].unique().tolist()],
                color_scale="diverging"),
        ])]),

        # ── 30. Choropleth map ────────────────────────────────────────────
        html.H2("Choropleth map", id="choropleth", style=S["section-heading"]),
        html.P("choropleth_map — geographic regions filled by value, sequential or diverging colour scale.", style=S["section-desc"]),
        html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
            choropleth_map("Choropleth map", subtitle="sample data — sequential scale",
                locations=m.DIMS["iso3"].values(df_geo),
                values=df_geo["val_a"].tolist(),
                hover_labels=m.DIMS["label"].values(df_geo)),
        ])]),

        # ── 31. Bubble map ────────────────────────────────────────────────
        html.H2("Bubble map", id="bubblemap", style=S["section-heading"]),
        html.P("bubble_map — geographic points sized by value.", style=S["section-desc"]),
        html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
            bubble_map("Bubble map", subtitle="sample data",
                lat=df_geo["dim_lat"].tolist(),
                lon=df_geo["dim_lon"].tolist(),
                size=df_geo["val_a"].tolist(),
                labels=m.DIMS["label"].values(df_geo)),
        ])]),

        # ── 32. Ribbon ────────────────────────────────────────────────────
        html.H2("Ribbon", id="ribbon", style=S["section-heading"]),
        html.P("ribbon — rank changes over time, highest rank always on top.", style=S["section-desc"]),
        html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
            ribbon("Ribbon", subtitle="sample data",
                x=sorted(df_ribbon["dim_year"].unique().tolist()),
                series=[{"name": entity,
                         "ranks": df_ribbon.loc[df_ribbon["dim_entity"] == entity
                                  ].sort_values("dim_year")["val_rank"].tolist()}
                        for entity in df_ribbon["dim_entity"].unique().tolist()]),
        ])]),

        # ── 33. Candlestick ───────────────────────────────────────────────
        html.H2("Candlestick", id="candlestick", style=S["section-heading"]),
        html.P("candlestick — OHLC financial data (open, high, low, close) over time.", style=S["section-desc"]),
        html.Div(style=S["group"], children=[html.Div(style=S["card"], children=[
            candlestick("Candlestick", subtitle="sample OHLC data",
                dates=m.DIMS["date"].values(df_ohlc_a),
                open_=df_ohlc_a["open"].tolist(),
                high= df_ohlc_a["high"].tolist(),
                low=  df_ohlc_a["low"].tolist(),
                close=df_ohlc_a["close"].tolist(),
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
            dropdown_slicer("Category", options=categories, value=categories[0]),
        ])]),

        # ── 35. List slicer ───────────────────────────────────────────────
        html.H2("List slicer", id="slicer-list", style=S["section-heading"]),
        html.P("list_slicer — checklist (multi=True) or radio (multi=False).", style=S["section-desc"]),
        html.Div(style=S["group"], children=[html.Div(style={"maxWidth": "320px"}, children=[
            list_slicer("Period", options=periods, value=periods[:2], multi=True),
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
            tile_slicer("Period", options=periods, value=periods[0]),
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


def build_showroom_app(
    *,
    domain: str,
    title: str = "Visual components — reference",
    subtitle: str = "One example per chart family — sample data",
    footer_name: str = "Open Reporting — visual components showroom",
    footer_source: str = "dane przykładowe",
    footer_updated: str = "referencja komponentów",
    module_name: str = __name__,
) -> Dash:
    """Return a fully wired showroom Dash app served under ``/{domain}/``.

    The Dash instance has its assets folder pinned at ``example/assets/``
    so the SVG icons used by ``build_sidebar`` (logo, sidebar, settings,
    user) resolve regardless of where the calling ``app.py`` lives.
    """
    app = make_app(
        domain=domain,
        title=title,
        module_name=module_name,
        assets_folder=str((Path(__file__).parent / "assets").resolve()),
    )

    app.layout = build_page_layout(
        domain=domain,
        title=title,
        subtitle=subtitle,
        sections=SECTIONS,
        content=_build_content(),
        footer_name=footer_name,
        footer_source=footer_source,
        footer_updated=footer_updated,
    )

    register_toggle_callback(app)
    return app
