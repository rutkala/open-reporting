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

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

PORT = 8055

# ── Sample data (generic placeholders — replace with domain data) ─────────────
YEARS    = [2018, 2019, 2020, 2021, 2022, 2023, 2024]
QUARTERS = ["Q1", "Q2", "Q3", "Q4"]
CATS     = ["Kat. A", "Kat. B", "Kat. C", "Kat. D", "Kat. E"]
CATS_8   = ["Kat. A", "Kat. B", "Kat. C", "Kat. D",
            "Kat. E", "Kat. F", "Kat. G", "Kat. H"]

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
            html.A("Kolumnowe i słupkowe", href="#bar", style=S["nav-item"]),
            html.A("Liniowe i obszarowe", href="#line", style=S["nav-item"]),
            html.A("Kombinowane", href="#combo", style=S["nav-item"]),
            html.A("Kaskadowe", href="#waterfall", style=S["nav-item"]),
            html.A("Punktowe", href="#scatter", style=S["nav-item"]),
            html.A("Rozkłady", href="#distribution", style=S["nav-item"]),
            html.A("Specjalne", href="#special", style=S["nav-item"]),
            html.A("Mapy", href="#maps", style=S["nav-item"]),
            html.A("Finansowe", href="#financial", style=S["nav-item"]),
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
            html.P("Dwa warianty: standardowy (duża liczba) i kompaktowy (dense rows).",
                   style=S["section-desc"]),

            html.Div(style=S["group"], children=[
                html.Div("kpi_standard", style=S["group-title"]),
                html.Div(style=S["grid-auto"], children=[
                    kpi_standard("Wskaźnik A", "47,2", unit="jedn.",
                                 trend="▲ +0,8", trend_color=POSITIVE),
                    kpi_standard("Wskaźnik B", "50,4", unit="jedn.",
                                 trend="▼ −0,3", trend_color=NEGATIVE),
                    kpi_standard("Wskaźnik C", "−3,2", unit="jedn.",
                                 trend="▲ +0,5", trend_color=POSITIVE),
                    kpi_standard("Wskaźnik D", "54,1", unit="jedn."),
                ]),
            ]),

            html.Div(style=S["group"], children=[
                html.Div("kpi_compact", style=S["group-title"]),
                html.Div(style=S["grid-auto"], children=[
                    kpi_compact("Miara A", "4,7", trend="▼ −0,3"),
                    kpi_compact("Miara B", "2,9"),
                    kpi_compact("Miara C", "3,1", trend="▲ +0,6", trend_color=POSITIVE),
                    kpi_compact("Miara D", "1 234", trend="▲ +8,4%", trend_color=POSITIVE),
                    kpi_compact("Miara E", "1 189"),
                    kpi_compact("Miara F", "+45", trend_color=POSITIVE),
                ]),
            ]),

            # ── Column & Bar charts ───────────────────────────────────────────
            html.H2("Wykresy kolumnowe i słupkowe", id="bar", style=S["section-heading"]),
            html.P(
                "Kolumnowe = pionowe, słupkowe = poziome. "
                "Grupowane / skumulowane / 100% skumulowane. "
                "Dywergentne dla wartości +/−.",
                style=S["section-desc"],
            ),

            html.Div(style=S["group"], children=[
                html.Div("clustered_column — grupowane pionowe", style=S["group-title"]),
                html.Div(style=S["grid-2"], children=[
                    html.Div(style=S["card"], children=[
                        clustered_column(
                            "Tytuł wykresu",
                            subtitle="dane przykładowe",
                            x=CATS,
                            series=[
                                {"name": "Seria A", "y": [47.2, 45.8, 52.3, 48.1, 43.6]},
                                {"name": "Seria B", "y": [50.4, 47.5, 55.8, 51.2, 45.1]},
                            ],
                        ),
                    ]),
                    html.Div(style=S["card"], children=[
                        clustered_column(
                            "Tytuł wykresu (z etykietami i linią ref.)",
                            subtitle="dane przykładowe",
                            x=QUARTERS,
                            series=[
                                {"name": "Plan",      "y": [280, 310, 295, 340]},
                                {"name": "Wykonanie", "y": [265, 325, 288, 352]},
                            ],
                            show_labels=True,
                            reference={"value": 300, "label": "Poziom odniesienia"},
                        ),
                    ]),
                ]),
            ]),

            html.Div(style=S["group"], children=[
                html.Div("stacked_column / pct_stacked_column — skumulowane pionowe", style=S["group-title"]),
                html.Div(style=S["grid-2"], children=[
                    html.Div(style=S["card"], children=[
                        stacked_column(
                            "Tytuł wykresu",
                            subtitle="dane przykładowe, 2020–2024",
                            x=[2020, 2021, 2022, 2023, 2024],
                            series=[
                                {"name": "Seria A", "y": [320, 335, 355, 370, 390]},
                                {"name": "Seria B", "y": [140, 155, 162, 170, 180]},
                                {"name": "Seria C", "y": [45, 48, 52, 60, 68]},
                                {"name": "Seria D", "y": [95, 102, 108, 115, 122]},
                            ],
                        ),
                    ]),
                    html.Div(style=S["card"], children=[
                        pct_stacked_column(
                            "Tytuł wykresu — udział 100%",
                            subtitle="dane przykładowe",
                            x=CATS,
                            series=[
                                {"name": "Seria A", "y": [52, 48, 55, 50, 45]},
                                {"name": "Seria B", "y": [20, 22, 19, 21, 23]},
                                {"name": "Seria C", "y": [28, 30, 26, 29, 32]},
                            ],
                        ),
                    ]),
                ]),
            ]),

            html.Div(style=S["group"], children=[
                html.Div("clustered_bar / stacked_bar — poziome", style=S["group-title"]),
                html.Div(style=S["grid-2"], children=[
                    html.Div(style=S["card"], children=[
                        clustered_bar(
                            "Tytuł wykresu — ranking",
                            subtitle="dane przykładowe, posortowane malejąco",
                            categories=CATS_8,
                            series=[{"name": "Seria A", "y": [163, 137, 112, 109, 105, 103, 82, 54]}],
                        ),
                    ]),
                    html.Div(style=S["card"], children=[
                        stacked_bar(
                            "Tytuł wykresu — skumulowany poziomy",
                            subtitle="dane przykładowe",
                            categories=CATS,
                            series=[
                                {"name": "Seria A", "y": [180, 420, 390, 310, 95]},
                                {"name": "Seria B", "y": [295, 380, 420, 280, 110]},
                                {"name": "Seria C", "y": [120, 290, 310, 220, 75]},
                            ],
                        ),
                    ]),
                ]),
            ]),

            html.Div(style=S["group"], children=[
                html.Div("pct_stacked_bar / bar_diverging — 100% poziomy i dywergentny", style=S["group-title"]),
                html.Div(style=S["grid-2"], children=[
                    html.Div(style=S["card"], children=[
                        pct_stacked_bar(
                            "Tytuł wykresu — udział 100% poziomy",
                            subtitle="dane przykładowe",
                            categories=CATS,
                            series=[
                                {"name": "Seria A", "y": [180, 420, 390, 310, 95]},
                                {"name": "Seria B", "y": [295, 380, 420, 280, 110]},
                                {"name": "Seria C", "y": [120, 290, 310, 220, 75]},
                            ],
                        ),
                    ]),
                    html.Div(style=S["card"], children=[
                        bar_diverging(
                            "Tytuł wykresu — wartości +/−",
                            subtitle="dane przykładowe",
                            x=CATS_8,
                            values=[3.2, 0.6, -0.3, -2.1, -5.1, -5.5, -7.2, -1.6],
                        ),
                    ]),
                ]),
            ]),

            # ── Line & Area charts ────────────────────────────────────────────
            html.H2("Wykresy liniowe i obszarowe", id="line", style=S["section-heading"]),
            html.P(
                "line: jedna lub wiele serii. area: wolumen. stacked_area: skumulowany. "
                "pct_stacked_area: 100% skumulowany.",
                style=S["section-desc"],
            ),

            html.Div(style=S["group"], children=[
                html.Div("line — jedna i wiele serii", style=S["group-title"]),
                html.Div(style=S["grid-2"], children=[
                    html.Div(style=S["card"], children=[
                        line(
                            "Tytuł wykresu (z linią ref.)",
                            subtitle="dane przykładowe, 2018–2024",
                            x=YEARS,
                            series=[{"name": "Seria A", "y": [48.9, 45.7, 57.1, 53.8, 51.4, 49.7, 54.1]}],
                            reference={"value": 60, "label": "Poziom odniesienia"},
                        ),
                    ]),
                    html.Div(style=S["card"], children=[
                        line(
                            "Tytuł wykresu — wiele serii",
                            subtitle="dane przykładowe, 2018–2024",
                            x=YEARS,
                            series=[
                                {"name": "Seria A", "y": [41.5, 42.3, 41.8, 43.2, 44.6, 46.1, 47.2]},
                                {"name": "Seria B", "y": [43.2, 44.0, 48.7, 46.5, 47.8, 49.3, 50.4]},
                                {"name": "Seria C", "y": [-1.7, -1.7, -6.9, -3.3, -3.2, -3.2, -3.2]},
                            ],
                        ),
                    ]),
                ]),
            ]),

            html.Div(style=S["group"], children=[
                html.Div("area / stacked_area / pct_stacked_area", style=S["group-title"]),
                html.Div(style=S["grid-3"], children=[
                    html.Div(style=S["card"], children=[
                        area(
                            "Tytuł wykresu",
                            subtitle="dane przykładowe, 2018–2024",
                            x=YEARS,
                            series=[{"name": "Seria A", "y": [380, 410, 395, 445, 520, 580, 615]}],
                        ),
                    ]),
                    html.Div(style=S["card"], children=[
                        stacked_area(
                            "Tytuł wykresu — skumulowany",
                            subtitle="dane przykładowe, 2018–2024",
                            x=YEARS,
                            series=[
                                {"name": "Seria A", "y": [180, 195, 185, 215, 250, 278, 295]},
                                {"name": "Seria B", "y": [85, 90, 88, 100, 115, 128, 135]},
                                {"name": "Seria C", "y": [45, 52, 48, 58, 72, 85, 92]},
                                {"name": "Seria D", "y": [70, 73, 74, 72, 83, 89, 93]},
                            ],
                        ),
                    ]),
                    html.Div(style=S["card"], children=[
                        pct_stacked_area(
                            "Tytuł wykresu — udział 100%",
                            subtitle="dane przykładowe, 2018–2024",
                            x=YEARS,
                            series=[
                                {"name": "Seria A", "y": [180, 195, 185, 215, 250, 278, 295]},
                                {"name": "Seria B", "y": [85, 90, 88, 100, 115, 128, 135]},
                                {"name": "Seria C", "y": [45, 52, 48, 58, 72, 85, 92]},
                                {"name": "Seria D", "y": [70, 73, 74, 72, 83, 89, 93]},
                            ],
                        ),
                    ]),
                ]),
            ]),

            # ── Combo charts ─────────────────────────────────────────────────
            html.H2("Wykresy kombinowane", id="combo", style=S["section-heading"]),
            html.P(
                "line_clustered_column / line_stacked_column: tylko dla danych na tej samej skali. "
                "combo_subplots: panele dla różnych skal (wzorzec IBCS).",
                style=S["section-desc"],
            ),

            html.Div(style=S["group"], children=[
                html.Div("line_clustered_column / line_stacked_column", style=S["group-title"]),
                html.Div(style=S["grid-2"], children=[
                    html.Div(style=S["card"], children=[
                        line_clustered_column(
                            "Tytuł wykresu",
                            subtitle="dane przykładowe — ta sama skala, wspólna oś",
                            x=[2020, 2021, 2022, 2023, 2024],
                            bar_series=[{"name": "Seria A (słupki)", "y": [395, 445, 520, 580, 615]}],
                            line_series=[{"name": "Seria B (linia)", "y": [400, 430, 510, 560, 600]}],
                        ),
                    ]),
                    html.Div(style=S["card"], children=[
                        line_stacked_column(
                            "Tytuł wykresu — składniki + suma",
                            subtitle="dane przykładowe",
                            x=[2020, 2021, 2022, 2023, 2024],
                            bar_series=[
                                {"name": "Seria A", "y": [185, 215, 250, 278, 295]},
                                {"name": "Seria B", "y": [88, 100, 115, 128, 135]},
                                {"name": "Seria C", "y": [48, 58, 72, 85, 92]},
                            ],
                            line_series=[{"name": "Razem", "y": [321, 373, 437, 491, 522]}],
                        ),
                    ]),
                ]),
            ]),

            html.Div(style=S["group"], children=[
                html.Div("combo_subplots — panele ze wspólną osią X", style=S["group-title"]),
                html.Div(style=S["grid-2"], children=[
                    html.Div(style=S["card"], children=[
                        combo_subplots(
                            "Tytuł wykresu — 3 panele",
                            subtitle="dane przykładowe — różne skale wymagają paneli",
                            x=YEARS,
                            panels=[
                                {"title": "Miara A", "type": "bar",
                                 "series": [{"name": "Seria A", "y": [380, 410, 395, 445, 520, 580, 615]}]},
                                {"title": "Miara B", "type": "bar",
                                 "series": [{"name": "Seria B", "y": [410, 440, 470, 488, 565, 630, 665]}]},
                                {"title": "Miara C (dywerg.)", "type": "line", "diverging": True,
                                 "series": [{"name": "Seria C", "y": [-30, -30, -75, -43, -45, -50, -50]}]},
                            ],
                        ),
                    ]),
                    html.Div(style=S["card"], children=[
                        combo_subplots(
                            "Tytuł wykresu — 2 panele",
                            subtitle="dane przykładowe",
                            x=YEARS,
                            panels=[
                                {"title": "Miara A", "type": "line",
                                 "series": [{"name": "Seria A", "y": [1.2, 2.3, 3.4, 5.1, 14.4, 11.5, 4.7]}]},
                                {"title": "Miara B", "type": "line",
                                 "series": [{"name": "Seria B", "y": [1.5, 1.5, 0.1, 0.1, 6.75, 5.75, 5.75]}]},
                            ],
                        ),
                    ]),
                ]),
            ]),

            # ── Waterfall charts ─────────────────────────────────────────────
            html.H2("Wykresy kaskadowe", id="waterfall", style=S["section-heading"]),
            html.P("Jak wartość początkowa staje się końcową przez kolejne składniki.",
                   style=S["section-desc"]),

            html.Div(style=S["group"], children=[
                html.Div("waterfall_contribution / waterfall_variance", style=S["group-title"]),
                html.Div(style=S["grid-2"], children=[
                    html.Div(style=S["card"], children=[
                        waterfall_contribution(
                            "Tytuł wykresu — składniki wyniku",
                            subtitle="dane przykładowe",
                            categories=["Składnik A", "Składnik B", "Składnik C", "Składnik D",
                                        "Korekta A", "Korekta B", "Korekta C", "Wynik"],
                            values=[295, 135, 92, 93, -390, -180, -95, -50],
                            total_label="Wynik",
                        ),
                    ]),
                    html.Div(style=S["card"], children=[
                        waterfall_variance(
                            "Tytuł wykresu — zmiana wartości",
                            subtitle="dane przykładowe",
                            categories=["Start", "Wzrost A", "Spadek A",
                                        "Wzrost B", "Korekta", "Koniec"],
                            values=[1240, 180, -140, 35, 15, 1330],
                            base_label="Start",
                            final_label="Koniec",
                        ),
                    ]),
                ]),
            ]),

            # ── Scatter charts ───────────────────────────────────────────────
            html.H2("Wykresy punktowe", id="scatter", style=S["section-heading"]),
            html.P("Korelacje i rozkłady. Bubble: trzecia zmienna przez rozmiar punktu.",
                   style=S["section-desc"]),

            html.Div(style=S["group"], children=[
                html.Div("scatter_basic / scatter_bubble", style=S["group-title"]),
                html.Div(style=S["grid-2"], children=[
                    html.Div(style=S["card"], children=[
                        scatter_basic(
                            "Tytuł wykresu — korelacja X i Y",
                            subtitle="dane przykładowe",
                            x=[32, 44, 54, 82, 103, 105, 109, 112, 137, 163],
                            y=[-0.3, -3.2, -5.1, -2.1, -3.4, -4.8, -5.5, -3.1, -7.2, -1.6],
                            labels=[f"Obs. {i}" for i in range(1, 11)],
                            trendline=True,
                        ),
                    ]),
                    html.Div(style=S["card"], children=[
                        scatter_bubble(
                            "Tytuł wykresu — rozmiar bąbla = trzecia zmienna",
                            subtitle="dane przykładowe",
                            x=[32, 44, 54, 82, 103, 109, 137],
                            y=[3.1, 4.2, 3.1, 1.2, 1.8, 2.4, 0.8],
                            size=[38, 10, 38, 9, 11, 68, 60],
                            labels=[f"Obs. {i}" for i in range(1, 8)],
                        ),
                    ]),
                ]),
            ]),

            # ── Distribution charts ───────────────────────────────────────────
            html.H2("Wykresy rozkładu", id="distribution", style=S["section-heading"]),
            html.P("histogram: rozkład jednej zmiennej. box_plot: mediana + IQR + outliery. "
                   "violin_plot: kształt rozkładu.",
                   style=S["section-desc"]),

            html.Div(style=S["group"], children=[
                html.Div("histogram — częstość wartości", style=S["group-title"]),
                html.Div(style=S["grid-2"], children=[
                    html.Div(style=S["card"], children=[
                        histogram(
                            "Tytuł wykresu — rozkład",
                            subtitle="dane przykładowe",
                            x=[-7.2, -5.5, -5.1, -4.9, -4.8, -3.4, -3.2, -3.2,
                               -2.1, -1.7, -1.6, -0.3, 0.6, 3.2],
                            x_label="Zmienna X",
                            nbins=8,
                        ),
                    ]),
                    html.Div(style=S["card"], children=[
                        histogram(
                            "Tytuł wykresu — rozkład (więcej obserwacji)",
                            subtitle="dane przykładowe",
                            x=[-8.9, -7.9, -5.5, -4.6, -2.5, 0.0, 0.1, 0.2, 0.5, 0.7,
                               0.9, 0.9, 1.0, 1.1, 1.5, 1.8, 1.9, 2.4, 2.6, 3.0,
                               3.1, 3.1, 3.5, 3.7, 4.5, 5.3, 5.9, 6.4, 7.2],
                            x_label="Zmienna X",
                        ),
                    ]),
                ]),
            ]),

            html.Div(style=S["group"], children=[
                html.Div("box_plot / violin_plot — porównanie rozkładów", style=S["group-title"]),
                html.Div(style=S["grid-2"], children=[
                    html.Div(style=S["card"], children=[
                        box_plot(
                            "Tytuł wykresu — rozkłady wg grup",
                            subtitle="dane przykładowe — mediana, IQR i outliery",
                            data={
                                "Grupa A": [1.2, 3.4, 5.9, 4.0, 2.1, 6.2, 3.8, 1.0, 0.5, 4.5],
                                "Grupa B": [1.5, 2.3, 4.7, 3.1, 0.8, 2.9, 3.6, 1.4, 2.0, 3.0],
                                "Grupa C": [-8.9, 5.9, 5.3, 0.1, 3.1],
                            },
                        ),
                    ]),
                    html.Div(style=S["card"], children=[
                        violin_plot(
                            "Tytuł wykresu — kształt rozkładu",
                            subtitle="dane przykładowe",
                            data={
                                "Seria A": [20, 22, 18, 25, 19, 23, 21, 24, 17, 26, 20, 22],
                                "Seria B": [28, 30, 27, 32, 29, 31, 28, 33, 27, 30, 29, 31],
                                "Seria C": [12, 14, 11, 15, 13, 12, 14, 16, 11, 13, 14, 12],
                            },
                        ),
                    ]),
                ]),
            ]),

            # ── Special charts ────────────────────────────────────────────────
            html.H2("Wykresy specjalne", id="special", style=S["section-heading"]),
            html.P("funnel, treemap, gauge, bullet, ribbon (ranking), heatmap_matrix.",
                   style=S["section-desc"]),

            html.Div(style=S["group"], children=[
                html.Div("funnel / treemap", style=S["group-title"]),
                html.Div(style=S["grid-2"], children=[
                    html.Div(style=S["card"], children=[
                        funnel(
                            "Tytuł wykresu — lejek konwersji",
                            subtitle="dane przykładowe",
                            stages=["Etap 1", "Etap 2", "Etap 3", "Etap 4", "Etap 5"],
                            values=[12400, 8900, 6200, 4800, 4100],
                        ),
                    ]),
                    html.Div(style=S["card"], children=[
                        treemap(
                            "Tytuł wykresu — struktura hierarchiczna",
                            subtitle="dane przykładowe — pole = wartość",
                            labels=["Razem", "Grupa A", "Grupa B",
                                    "A1", "A2", "B1", "B2", "B3"],
                            parents=["", "Razem", "Razem",
                                     "Grupa A", "Grupa A", "Grupa B", "Grupa B", "Grupa B"],
                            values=[0, 615, 665, 295, 135, 390, 180, 68],
                        ),
                    ]),
                ]),
            ]),

            html.Div(style=S["group"], children=[
                html.Div("gauge / bullet — wskaźniki vs cel", style=S["group-title"]),
                html.Div(style=S["grid-3"], children=[
                    html.Div(style=S["card"], children=[
                        gauge(
                            "Tytuł — wskaźnik vs zakres",
                            subtitle="dane przykładowe",
                            value=78,
                            min_val=0, max_val=100,
                            reference=80,
                            suffix="%",
                        ),
                    ]),
                    html.Div(style=S["card"], children=[
                        bullet(
                            "Tytuł — wartość vs cel",
                            subtitle="dane przykładowe",
                            value=615,
                            target=600,
                            max_val=750,
                            suffix=" jedn.",
                        ),
                    ]),
                    html.Div(style=S["card"], children=[
                        bullet(
                            "Tytuł — wartość vs cel (ujemna)",
                            subtitle="dane przykładowe",
                            value=-3.2,
                            target=-3.0,
                            min_val=-8.0,
                            max_val=0,
                            suffix=" jedn.",
                        ),
                    ]),
                ]),
            ]),

            html.Div(style=S["group"], children=[
                html.Div("ribbon — zmiany rankingowe w czasie", style=S["group-title"]),
                html.Div(style=S["grid-2"], children=[
                    html.Div(style=S["card"], children=[
                        ribbon(
                            "Tytuł wykresu — zmiany pozycji rankingowej",
                            subtitle="dane przykładowe, 2020–2024",
                            x=[2020, 2021, 2022, 2023, 2024],
                            series=[
                                {"name": "Podmiot A", "ranks": [1, 1, 1, 1, 1]},
                                {"name": "Podmiot B", "ranks": [2, 2, 2, 2, 2]},
                                {"name": "Podmiot C", "ranks": [3, 3, 3, 3, 3]},
                                {"name": "Podmiot D", "ranks": [4, 4, 4, 4, 4]},
                                {"name": "Podmiot E", "ranks": [8, 7, 6, 6, 5]},
                            ],
                        ),
                    ]),
                    html.Div(style=S["card"], children=[
                        heatmap_matrix(
                            "Tytuł wykresu — macierz korelacji",
                            subtitle="dane przykładowe",
                            x_labels=["Zmienna A", "Zmienna B", "Zmienna C", "Zmienna D"],
                            y_labels=["Zmienna A", "Zmienna B", "Zmienna C", "Zmienna D"],
                            z_values=[
                                [1.00,  0.82, -0.41, -0.23],
                                [0.82,  1.00, -0.78,  0.15],
                                [-0.41, -0.78, 1.00, -0.56],
                                [-0.23,  0.15, -0.56, 1.00],
                            ],
                            color_scale="diverging",
                        ),
                    ]),
                ]),
            ]),

            # ── Map charts ────────────────────────────────────────────────────
            html.H2("Mapy", id="maps", style=S["section-heading"]),
            html.P("choropleth_map: regiony wypełnione kolorem. bubble_map: bąbelki w punktach geograficznych.",
                   style=S["section-desc"]),

            html.Div(style=S["group"], children=[
                html.Div("choropleth_map — choropleta europejska", style=S["group-title"]),
                html.Div(style=S["grid-2"], children=[
                    html.Div(style=S["card"], children=[
                        choropleth_map(
                            "Tytuł mapy — miara A wg kraju",
                            subtitle="dane przykładowe — skala sekwencyjna",
                            locations=["POL", "DEU", "FRA", "ITA", "CZE", "GRC",
                                       "ESP", "PRT", "AUT", "BEL", "SWE", "DNK"],
                            values=[54.1, 63.2, 109.1, 137.3, 44.1, 163.0,
                                    103.0, 112.0, 82.0, 105.0, 32.0, 29.0],
                            hover_labels=[f"Region {chr(65+i)}" for i in range(12)],
                        ),
                    ]),
                    html.Div(style=S["card"], children=[
                        choropleth_map(
                            "Tytuł mapy — miara B wg kraju (dywergentna)",
                            subtitle="dane przykładowe — zielony = wartości dodatnie",
                            locations=["POL", "DEU", "FRA", "ITA", "CZE", "GRC",
                                       "ESP", "PRT", "AUT", "SWE", "DNK"],
                            values=[-5.1, -1.7, -5.5, -7.2, -1.6, -1.6,
                                    -3.4, -3.1, -2.1, 0.6, 3.2],
                            hover_labels=[f"Region {chr(65+i)}" for i in range(11)],
                            color_scale="diverging",
                        ),
                    ]),
                ]),
            ]),

            html.Div(style=S["group"], children=[
                html.Div("bubble_map — bąbelki geograficzne", style=S["group-title"]),
                html.Div(style=S["grid-2"], children=[
                    html.Div(style=S["card"], children=[
                        bubble_map(
                            "Tytuł mapy — bąbel = miara A",
                            subtitle="dane przykładowe",
                            lat=[52.2, 51.2, 46.2, 41.9, 50.1, 40.4, 38.7, 47.5, 50.8, 59.3, 55.7],
                            lon=[21.0, 10.4, 2.2, 12.5, 15.5, -3.7, -9.1, 14.6, 4.4, 18.1, 12.6],
                            size=[680, 4200, 2800, 2100, 290, 1500, 270, 470, 560, 580, 400],
                            labels=[f"Region {chr(65+i)}" for i in range(11)],
                        ),
                    ]),
                    html.Div(style=S["card"], children=[
                        bubble_map(
                            "Tytuł mapy — bąbel = miara B",
                            subtitle="dane przykładowe",
                            lat=[52.2, 51.2, 46.2, 41.9, 50.1, 40.4, 47.5, 59.3],
                            lon=[21.0, 10.4, 2.2, 12.5, 15.5, -3.7, 14.6, 18.1],
                            size=[3.1, 0.2, 1.1, 0.7, 1.5, 3.2, 0.8, 2.6],
                            labels=[f"Region {chr(65+i)}" for i in range(8)],
                        ),
                    ]),
                ]),
            ]),

            # ── Financial charts ──────────────────────────────────────────────
            html.H2("Wykresy finansowe", id="financial", style=S["section-heading"]),
            html.P("candlestick: dane OHLC — cena akcji lub obligacji w czasie.",
                   style=S["section-desc"]),

            html.Div(style=S["group"], children=[
                html.Div("candlestick — OHLC", style=S["group-title"]),
                html.Div(style=S["grid-2"], children=[
                    html.Div(style=S["card"], children=[
                        candlestick(
                            "Tytuł wykresu — instrument A",
                            subtitle="dane przykładowe OHLC",
                            dates=["2024-01", "2024-02", "2024-03", "2024-04",
                                   "2024-05", "2024-06", "2024-07", "2024-08",
                                   "2024-09", "2024-10", "2024-11", "2024-12"],
                            open_=[5.65, 5.52, 5.41, 5.38, 5.45, 5.55, 5.48, 5.30,
                                   5.22, 5.35, 5.55, 5.70],
                            high= [5.75, 5.65, 5.55, 5.52, 5.60, 5.68, 5.58, 5.45,
                                   5.40, 5.65, 5.72, 5.88],
                            low=  [5.48, 5.38, 5.30, 5.25, 5.35, 5.42, 5.32, 5.18,
                                   5.10, 5.22, 5.42, 5.58],
                            close=[5.52, 5.41, 5.38, 5.45, 5.55, 5.48, 5.30, 5.22,
                                   5.35, 5.55, 5.70, 5.80],
                        ),
                    ]),
                    html.Div(style=S["card"], children=[
                        candlestick(
                            "Tytuł wykresu — instrument B",
                            subtitle="dane przykładowe OHLC",
                            dates=["2024-01", "2024-02", "2024-03", "2024-04",
                                   "2024-05", "2024-06", "2024-07", "2024-08",
                                   "2024-09", "2024-10", "2024-11", "2024-12"],
                            open_=[4.35, 4.32, 4.29, 4.31, 4.28, 4.25, 4.22, 4.27,
                                   4.30, 4.33, 4.28, 4.25],
                            high= [4.38, 4.36, 4.34, 4.35, 4.32, 4.30, 4.28, 4.33,
                                   4.36, 4.38, 4.35, 4.30],
                            low=  [4.30, 4.28, 4.26, 4.27, 4.24, 4.21, 4.18, 4.23,
                                   4.26, 4.29, 4.24, 4.21],
                            close=[4.32, 4.29, 4.31, 4.28, 4.25, 4.22, 4.27, 4.30,
                                   4.33, 4.28, 4.25, 4.22],
                        ),
                    ]),
                ]),
            ]),

            # ── Tables ───────────────────────────────────────────────────────
            html.H2("Tabele", id="table", style=S["section-heading"]),
            html.P("table_basic: precyzja i referencja. table_heatmap: wzorce wizualne + wartości.",
                   style=S["section-desc"]),

            html.Div(style=S["group"], children=[
                html.Div("table_basic / table_heatmap", style=S["group-title"]),
                html.Div(style=S["grid-2"], children=[
                    html.Div(style=S["card"], children=[
                        table_basic(
                            "Tytuł tabeli",
                            subtitle="dane przykładowe",
                            headers=["Atrybut", "Miara A", "Miara B", "Miara C", "Miara D"],
                            rows=[
                                ["Wiersz A", 47.2, 50.4, -3.2, 54.1],
                                ["Wiersz B", 45.8, 47.5, -1.7, 63.2],
                                ["Wiersz C", 52.3, 55.8, -5.5, 109.1],
                                ["Wiersz D", 48.1, 51.2, -7.2, 137.3],
                                ["Wiersz E", 43.6, 45.1, -1.6, 44.1],
                                ["Wiersz F", 44.2, 49.1, -4.9, 73.4],
                            ],
                            number_cols={1, 2, 3, 4},
                        ),
                    ]),
                    html.Div(style=S["card"], children=[
                        table_heatmap(
                            "Tytuł tabeli — mapa ciepła",
                            subtitle="dane przykładowe — kolor = intensywność",
                            headers=["Atrybut", "Rok 1", "Rok 2", "Rok 3", "Rok 4", "Rok 5", "Rok 6"],
                            rows=[
                                ["Wiersz A", 4.5, -2.5, 5.9, 5.3, 0.1, 3.1],
                                ["Wiersz B", 1.0, -4.6, 3.1, 1.9, -0.3, 0.2],
                                ["Wiersz C", 1.8, -7.9, 6.4, 2.6, 0.9, 1.1],
                                ["Wiersz D", 0.5, -8.9, 7.2, 3.7, 0.9, 0.7],
                                ["Wiersz E", 3.0, -5.5, 3.5, 2.4, 0.0, 1.5],
                            ],
                            number_cols={1, 2, 3, 4, 5, 6},
                            diverging=True,
                        ),
                    ]),
                ]),
            ]),

            # ── Pie charts ───────────────────────────────────────────────────
            html.H2("Wykresy kołowe", id="pie", style=S["section-heading"]),
            html.P("Stosować tylko dla 2–5 kategorii z wyraźnymi udziałami. Preferować słupkowe dla porównań.",
                   style=S["section-desc"]),

            html.Div(style=S["group"], children=[
                html.Div("pie_chart — donut i kołowy", style=S["group-title"]),
                html.Div(style=S["grid-3"], children=[
                    html.Div(style=S["card"], children=[
                        pie_chart("Tytuł — struktura (5 kategorii)",
                                  subtitle="donut — max 5 kategorii",
                                  labels=["Kat. A", "Kat. B", "Kat. C", "Kat. D", "Kat. E"],
                                  values=[295, 135, 92, 93, 60]),
                    ]),
                    html.Div(style=S["card"], children=[
                        pie_chart("Tytuł — struktura (3 kategorie)",
                                  subtitle="donut — trzy kategorie",
                                  labels=["Kat. A", "Kat. B", "Kat. C"],
                                  values=[390, 180, 95]),
                    ]),
                    html.Div(style=S["card"], children=[
                        pie_chart("Tytuł — kołowy (bez środka)",
                                  subtitle="pie — cztery kategorie",
                                  labels=["Kat. A", "Kat. B", "Kat. C", "Kat. D"],
                                  values=[68, 22, 7, 3],
                                  donut=False),
                    ]),
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
