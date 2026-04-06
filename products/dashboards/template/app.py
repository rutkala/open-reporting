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
from products.visuals.components.kpi_card import kpi_standard, kpi_compact
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
    line_clustered_column, line_stacked_column, combo_subplots,
)
from products.visuals.components.waterfall_chart import waterfall_contribution, waterfall_variance
from products.visuals.components.scatter_chart import scatter_basic, scatter_bubble
from products.visuals.components.distribution_chart import histogram, box_plot, violin_plot
from products.visuals.components.special_chart import (
    funnel, treemap, gauge, bullet, ribbon, heatmap_matrix,
)
from products.visuals.components.map_chart import choropleth_map, bubble_map
from products.visuals.components.financial_chart import candlestick
from products.visuals.components.table_chart import table_basic, table_heatmap
from products.visuals.components.pie_chart import pie_chart

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
_df_thmap            = _data.load_table_heatmap()
_groups_cs           = _data.load_clustered_stacked()

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
            html.A("KPI", href="#kpi", style=S["nav-item-active"]),
            html.A("Kolumnowe", href="#column", style=S["nav-item"]),
            html.A("Słupkowe", href="#bar", style=S["nav-item"]),
            html.A("Liniowe", href="#line", style=S["nav-item"]),
            html.A("Obszarowe", href="#area", style=S["nav-item"]),
            html.A("Kombinowane", href="#combo", style=S["nav-item"]),
            html.A("Kaskadowe", href="#waterfall", style=S["nav-item"]),
            html.A("Punktowe", href="#scatter", style=S["nav-item"]),
            html.A("Rozkłady", href="#distribution", style=S["nav-item"]),
            html.A("Specjalne", href="#special", style=S["nav-item"]),
            html.A("Mapy", href="#maps", style=S["nav-item"]),
            html.A("OHLC / świecowe", href="#financial", style=S["nav-item"]),
            html.A("Tabele", href="#table", style=S["nav-item"]),
            html.A("Kołowe", href="#pie", style=S["nav-item"]),
            html.A("Paleta", href="#palette", style=S["nav-item"]),
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
                html.H1("Komponenty wizualne — referencja",
                        style={"fontSize": "20px", "fontWeight": 700, "color": TEXT, "margin": 0}),
                html.P("Wszystkie warianty wykresów z przykładowymi danymi",
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

            # ── KPI cards ────────────────────────────────────────────────────
            html.H2("KPI — karty wskaźników", id="kpi", style={**S["section-heading"], "marginTop": 0}),
            html.P(
                "kpi_standard — duża liczba z trendem i jednostką. "
                "Wariant: kpi_compact (dense, wiele wskaźników w rzędzie).",
                style=S["section-desc"],
            ),

            html.Div(style=S["group"], children=[
                html.Div(style=S["grid-auto"], children=[
                    kpi_standard(m.MEASURES["measure_a"].label,
                                 m.MEASURES["measure_a"].kpi_value(_scalars["measure_a"]),
                                 unit=m.MEASURES["measure_a"].unit,
                                 trend="▲ +0,8", trend_color=POSITIVE),
                    kpi_standard(m.MEASURES["measure_b"].label,
                                 m.MEASURES["measure_b"].kpi_value(_scalars["measure_b"]),
                                 unit=m.MEASURES["measure_b"].unit,
                                 trend="▼ −0,3", trend_color=NEGATIVE),
                    kpi_standard(m.MEASURES["measure_c"].label,
                                 m.MEASURES["measure_c"].kpi_value(_scalars["measure_c"]),
                                 unit=m.MEASURES["measure_c"].unit),
                ]),
            ]),

            # ── Column charts (vertical) ──────────────────────────────────────
            html.H2("Wykresy kolumnowe (pionowe)", id="column", style=S["section-heading"]),
            html.P(
                "clustered_column — pionowe słupki grupowane. "
                "Warianty: stacked_column, pct_stacked_column, bar_diverging (+/−), "
                "clustered_stacked_column (grupy + stosy w pionowych kolumnach).",
                style=S["section-desc"],
            ),

            html.Div(style=S["group"], children=[
                html.Div(style=S["grid-2"], children=[
                    html.Div(style=S["card"], children=[
                        clustered_column(
                            "clustered_column",
                            subtitle="grupowane pionowe — wiele serii",
                            x=_categories,
                            series=[
                                m.MEASURES["measure_a"].to_series(_df_by_cat["val_a"].tolist()),
                                m.MEASURES["measure_b"].to_series(_df_by_cat["val_b"].tolist()),
                                m.MEASURES["measure_c"].to_series(_df_by_cat["val_c"].tolist()),
                            ],
                        ),
                    ]),
                    html.Div(style=S["card"], children=[
                        clustered_stacked_column(
                            "clustered_stacked_column",
                            subtitle="grupy obok siebie, serie skumulowane wewnątrz grupy",
                            x=_categories,
                            groups=_groups_cs,
                        ),
                    ]),
                ]),
            ]),

            # ── Bar charts (horizontal) ───────────────────────────────────────
            html.H2("Wykresy słupkowe (poziome)", id="bar", style=S["section-heading"]),
            html.P(
                "clustered_bar — poziome słupki grupowane; 1 seria → ranking (sortowanie malejąco). "
                "Warianty: stacked_bar, pct_stacked_bar, "
                "clustered_stacked_bar (grupy + stosy w poziomych słupkach).",
                style=S["section-desc"],
            ),

            html.Div(style=S["group"], children=[
                html.Div(style=S["card"], children=[
                    clustered_bar(
                        "clustered_bar",
                        subtitle="ranking — sortowanie malejąco, 1 seria",
                        categories=m.DIMS["label"].values(_df_geo),
                        series=[m.MEASURES["geo_a"].to_series(_df_geo["val_a"].tolist())],
                    ),
                ]),
            ]),

            # ── Line charts ───────────────────────────────────────────────────
            html.H2("Wykresy liniowe", id="line", style=S["section-heading"]),
            html.P(
                "line — trend w czasie, jedna lub wiele serii. "
                "Obsługuje linię referencyjną (reference=).",
                style=S["section-desc"],
            ),

            html.Div(style=S["group"], children=[
                html.Div(style=S["card"], children=[
                    line(
                        "line",
                        subtitle="wiele serii — trend w czasie",
                        x=_years,
                        series=[
                            m.MEASURES["measure_a"].to_series(_df_by_year["val_a"].tolist()),
                            m.MEASURES["measure_b"].to_series(_df_by_year["val_b"].tolist()),
                            m.MEASURES["measure_e"].to_series(_df_by_year["val_e"].tolist()),
                        ],
                        reference={"value": _scalars["measure_b"], "label": "Poziom odniesienia"},
                    ),
                ]),
            ]),

            # ── Area charts ───────────────────────────────────────────────────
            html.H2("Wykresy obszarowe", id="area", style=S["section-heading"]),
            html.P(
                "area — wolumen od zera, wiele serii zachodzących na siebie. "
                "Warianty: stacked_area (skumulowany), pct_stacked_area (100% skumulowany).",
                style=S["section-desc"],
            ),

            html.Div(style=S["group"], children=[
                html.Div(style=S["card"], children=[
                    area(
                        "area",
                        subtitle="wiele serii od zera — wolumen i porównanie",
                        x=_years,
                        series=[
                            m.MEASURES["measure_a"].to_series(_df_by_year["val_a"].tolist()),
                            m.MEASURES["measure_b"].to_series(_df_by_year["val_b"].tolist()),
                            m.MEASURES["measure_c"].to_series(_df_by_year["val_c"].tolist()),
                        ],
                    ),
                ]),
            ]),

            # ── Combo charts ─────────────────────────────────────────────────
            html.H2("Wykresy kombinowane", id="combo", style=S["section-heading"]),
            html.P(
                "combo_subplots — wspólna oś X, osobne panele dla różnych skal (wzorzec IBCS). "
                "Warianty: line_clustered_column, line_stacked_column (tylko dla tej samej skali).",
                style=S["section-desc"],
            ),

            html.Div(style=S["group"], children=[
                html.Div(style=S["card"], children=[
                    combo_subplots(
                        "combo_subplots",
                        subtitle="3 panele — różne skale wymagają osobnych paneli",
                        x=_years,
                        panels=[
                            {"title": m.MEASURES["measure_a"].label, "type": "bar",
                             "series": [m.MEASURES["measure_a"].to_series(_df_by_year["val_a"].tolist())]},
                            {"title": m.MEASURES["measure_b"].label, "type": "bar",
                             "series": [m.MEASURES["measure_b"].to_series(_df_by_year["val_b"].tolist())]},
                            {"title": m.MEASURES["measure_e"].label, "type": "line", "diverging": True,
                             "series": [m.MEASURES["measure_e"].to_series(_df_by_year["val_e"].tolist())]},
                        ],
                    ),
                ]),
            ]),

            # ── Waterfall charts ─────────────────────────────────────────────
            html.H2("Wykresy kaskadowe", id="waterfall", style=S["section-heading"]),
            html.P(
                "waterfall_contribution — jak składniki budują wynik końcowy. "
                "Wariant: waterfall_variance (zmiana wartości między dwoma punktami).",
                style=S["section-desc"],
            ),

            html.Div(style=S["group"], children=[
                html.Div(style=S["card"], children=[
                    waterfall_contribution(
                        "waterfall_contribution",
                        subtitle="składniki wyniku — od punktu startowego do końcowego",
                        categories=_df_wf_c["dim_stage"].tolist(),
                        values=_df_wf_c["val_amount"].tolist(),
                        total_label=_df_wf_c.loc[_df_wf_c["is_total"], "dim_stage"].iloc[0],
                    ),
                ]),
            ]),

            # ── Scatter charts ───────────────────────────────────────────────
            html.H2("Wykresy punktowe", id="scatter", style=S["section-heading"]),
            html.P(
                "scatter_bubble — korelacja X/Y z trzecią zmienną jako rozmiar bąbla. "
                "Wariant: scatter_basic (bez rozmiaru, z opcjonalną linią trendu).",
                style=S["section-desc"],
            ),

            html.Div(style=S["group"], children=[
                html.Div(style=S["card"], children=[
                    scatter_bubble(
                        "scatter_bubble",
                        subtitle="korelacja X/Y — rozmiar bąbla = trzecia zmienna",
                        x=_df_sc["val_x"].tolist(),
                        y=_df_sc["val_y"].tolist(),
                        size=_df_sc["val_size"].tolist(),
                        labels=_df_sc["dim_label"].tolist(),
                    ),
                ]),
            ]),

            # ── Distribution charts ───────────────────────────────────────────
            html.H2("Wykresy rozkładu", id="distribution", style=S["section-heading"]),
            html.P(
                "box_plot — mediana, IQR i outliery wg grup — wzorzec do porównań statystycznych. "
                "Warianty: histogram (częstość wartości), violin_plot (kształt rozkładu).",
                style=S["section-desc"],
            ),

            html.Div(style=S["group"], children=[
                html.Div(style=S["card"], children=[
                    box_plot(
                        "box_plot",
                        subtitle="rozkłady wg grup — mediana, IQR i outliery",
                        data={
                            grp: _df_dist.loc[_df_dist["dim_group"] == grp, "val_obs"].tolist()
                            for grp in _dist_groups
                        },
                    ),
                ]),
            ]),

            # ── Special charts ────────────────────────────────────────────────
            html.H2("Wykresy specjalne", id="special", style=S["section-heading"]),
            html.P(
                "6 odrębnych typów — każdy do innego celu: "
                "funnel (konwersja), treemap (hierarchia), gauge (zakres), "
                "bullet (cel), ribbon (ranking), heatmap_matrix (macierz).",
                style=S["section-desc"],
            ),

            html.Div(style=S["group"], children=[
                html.Div(style=S["grid-2"], children=[
                    html.Div(style=S["card"], children=[
                        funnel(
                            "funnel",
                            subtitle="etapy konwersji — wartości malejące",
                            stages=_df_funnel["dim_stage"].tolist(),
                            values=_df_funnel["val_count"].tolist(),
                        ),
                    ]),
                    html.Div(style=S["card"], children=[
                        treemap(
                            "treemap",
                            subtitle="struktura hierarchiczna — pole = wartość",
                            labels=_df_tree["dim_node"].tolist(),
                            parents=_df_tree["dim_parent"].tolist(),
                            values=_df_tree["val_size"].tolist(),
                        ),
                    ]),
                    html.Div(style=S["card"], children=[
                        gauge(
                            "gauge",
                            subtitle="wartość vs zakres z punktem referencyjnym",
                            value=_gauge["gauge_value"],
                            min_val=0, max_val=_gauge["gauge_max"],
                            reference=_gauge["gauge_target"],
                            suffix=" jedn.",
                        ),
                    ]),
                    html.Div(style=S["card"], children=[
                        bullet(
                            "bullet",
                            subtitle="wartość vs cel — precyzyjne porównanie",
                            value=_gauge["bullet_a_value"],
                            target=_gauge["bullet_a_target"],
                            max_val=_gauge["bullet_a_max"],
                            suffix=" jedn.",
                        ),
                    ]),
                    html.Div(style=S["card"], children=[
                        ribbon(
                            "ribbon",
                            subtitle="zmiany pozycji rankingowej w czasie",
                            x=sorted(_df_ribbon["dim_year"].unique().tolist()),
                            series=[
                                {
                                    "name": entity,
                                    "ranks": _df_ribbon.loc[
                                        _df_ribbon["dim_entity"] == entity
                                    ].sort_values("dim_year")["val_rank"].tolist(),
                                }
                                for entity in _df_ribbon["dim_entity"].unique().tolist()
                            ],
                        ),
                    ]),
                    html.Div(style=S["card"], children=[
                        heatmap_matrix(
                            "heatmap_matrix",
                            subtitle="macierz korelacji — kolor = intensywność",
                            x_labels=_df_hmap["dim_col"].unique().tolist(),
                            y_labels=_df_hmap["dim_row"].unique().tolist(),
                            z_values=[
                                _df_hmap.loc[_df_hmap["dim_row"] == row, "val_z"].tolist()
                                for row in _df_hmap["dim_row"].unique().tolist()
                            ],
                            color_scale="diverging",
                        ),
                    ]),
                ]),
            ]),

            # ── Map charts ────────────────────────────────────────────────────
            html.H2("Mapy", id="maps", style=S["section-heading"]),
            html.P(
                "choropleth_map — regiony wypełnione kolorem (sekwencyjny lub dywergentny). "
                "Wariant: bubble_map (bąbelki w punktach geograficznych).",
                style=S["section-desc"],
            ),

            html.Div(style=S["group"], children=[
                html.Div(style=S["card"], children=[
                    choropleth_map(
                        "choropleth_map",
                        subtitle="regiony wg wartości — skala sekwencyjna",
                        locations=m.DIMS["iso3"].values(_df_geo),
                        values=_df_geo["val_a"].tolist(),
                        hover_labels=m.DIMS["label"].values(_df_geo),
                    ),
                ]),
            ]),

            # ── Financial charts ──────────────────────────────────────────────
            html.H2("Wykresy OHLC / świecowe", id="financial", style=S["section-heading"]),
            html.P(
                "candlestick — dane OHLC (open, high, low, close) dla szeregów czasowych cen.",
                style=S["section-desc"],
            ),

            html.Div(style=S["group"], children=[
                html.Div(style=S["card"], children=[
                    candlestick(
                        "candlestick",
                        subtitle="dane OHLC — świece japonki",
                        dates=m.DIMS["date"].values(_df_ohlc_a),
                        open_=_df_ohlc_a["open"].tolist(),
                        high= _df_ohlc_a["high"].tolist(),
                        low=  _df_ohlc_a["low"].tolist(),
                        close=_df_ohlc_a["close"].tolist(),
                    ),
                ]),
            ]),

            # ── Tables ───────────────────────────────────────────────────────
            html.H2("Tabele", id="table", style=S["section-heading"]),
            html.P(
                "table_basic — precyzja i referencja liczbowa. "
                "Wariant: table_heatmap (kolorowanie komórek wg intensywności).",
                style=S["section-desc"],
            ),

            html.Div(style=S["group"], children=[
                html.Div(style=S["card"], children=[
                    table_basic(
                        "table_basic",
                        subtitle="dane tabelaryczne z wyrównaniem liczb",
                        headers=["Atrybut",
                                 m.MEASURES["measure_a"].label,
                                 m.MEASURES["measure_b"].label,
                                 m.MEASURES["measure_c"].label,
                                 m.MEASURES["measure_d"].label],
                        rows=[
                            [row["dim_attribute"],
                             row["val_a"], row["val_b"],
                             row["val_c"], row["val_d"]]
                            for _, row in _df_table.iterrows()
                        ],
                        number_cols={1, 2, 3, 4},
                    ),
                ]),
            ]),

            # ── Pie charts ───────────────────────────────────────────────────
            html.H2("Wykresy kołowe", id="pie", style=S["section-heading"]),
            html.P(
                "pie_chart (donut=True) — tylko dla 2–5 kategorii z wyraźnymi udziałami. "
                "Preferować słupkowe dla porównań. Wariant: donut=False (pełne koło).",
                style=S["section-desc"],
            ),

            html.Div(style=S["group"], children=[
                html.Div(style=S["card"], children=[
                    pie_chart(
                        "pie_chart",
                        subtitle="donut — udziały procentowe, max 5 kategorii",
                        labels=_categories,
                        values=_df_by_cat["val_a"].tolist(),
                    ),
                ]),
            ]),

            # ── Colour palette reference ──────────────────────────────────────
            html.H2("Paleta wizualna", id="palette", style=S["section-heading"]),
            html.P("Kolory, typografia i ustawienia bazowe motywu Teal.", style=S["section-desc"]),

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
            html.Span("Open Reporting — szablon dashboardu", style=S["footer-text"]),
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
