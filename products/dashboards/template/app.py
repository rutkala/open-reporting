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
from products.visuals.components.bar_chart import bar_grouped, bar_stacked, bar_horizontal, bar_diverging
from products.visuals.components.line_chart import line_single, line_multi, line_area, line_area_stacked
from products.visuals.components.combo_chart import combo_bar_line, combo_subplots
from products.visuals.components.waterfall_chart import waterfall_contribution, waterfall_variance
from products.visuals.components.scatter_chart import scatter_basic, scatter_bubble
from products.visuals.components.table_chart import table_basic, table_heatmap
from products.visuals.components.pie_chart import pie_chart

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

PORT = 8055

# ── Sample data ───────────────────────────────────────────────────────────────
YEARS = [2018, 2019, 2020, 2021, 2022, 2023, 2024]
CATS  = ["Polska", "Niemcy", "Francja", "Włochy", "Czechy"]

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
            html.A("Wykresy słupkowe", href="#bar", style=S["nav-item"]),
            html.A("Wykresy liniowe", href="#line", style=S["nav-item"]),
            html.A("Kombinowane", href="#combo", style=S["nav-item"]),
            html.A("Kaskadowe", href="#waterfall", style=S["nav-item"]),
            html.A("Punktowe", href="#scatter", style=S["nav-item"]),
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
                    kpi_standard("Dochody budżetu", "47,2", unit="% PKB",
                                 trend="▲ +0,8 pp", trend_color=POSITIVE),
                    kpi_standard("Wydatki budżetu", "50,4", unit="% PKB",
                                 trend="▼ −0,3 pp", trend_color=NEGATIVE),
                    kpi_standard("Saldo fiskalne", "−3,2", unit="% PKB",
                                 trend="▲ +0,5 pp", trend_color=POSITIVE),
                    kpi_standard("Dług publiczny", "54,1", unit="% PKB"),
                ]),
            ]),

            html.Div(style=S["group"], children=[
                html.Div("kpi_compact", style=S["group-title"]),
                html.Div(style=S["grid-auto"], children=[
                    kpi_compact("Inflacja CPI", "4,7%", trend="▼ −0,3 pp"),
                    kpi_compact("Stopa bezrobocia", "2,9%"),
                    kpi_compact("Wzrost PKB", "3,1%", trend="▲ +0,6 pp", trend_color=POSITIVE),
                    kpi_compact("Eksport", "1 234 mld", trend="▲ +8,4%", trend_color=POSITIVE),
                    kpi_compact("Import", "1 189 mld"),
                    kpi_compact("Saldo handlowe", "+45 mld", trend_color=POSITIVE),
                ]),
            ]),

            # ── Bar charts ───────────────────────────────────────────────────
            html.H2("Wykresy słupkowe", id="bar", style=S["section-heading"]),
            html.P("Cztery warianty: grupowany, skumulowany, poziomy (ranking), dywergentny.",
                   style=S["section-desc"]),

            html.Div(style=S["group"], children=[
                html.Div("bar_grouped — porównanie wielu serii", style=S["group-title"]),
                html.Div(style=S["grid-2"], children=[
                    html.Div(style=S["card"], children=[
                        bar_grouped(
                            "Dochody i wydatki wg krajów",
                            subtitle="% PKB, 2024",
                            x=CATS,
                            series=[
                                {"name": "Dochody", "y": [47.2, 45.8, 52.3, 48.1, 43.6]},
                                {"name": "Wydatki", "y": [50.4, 47.5, 55.8, 51.2, 45.1]},
                            ],
                        ),
                    ]),
                    html.Div(style=S["card"], children=[
                        bar_grouped(
                            "Wykonanie budżetu",
                            subtitle="mld zł, plan vs wykonanie",
                            x=["Q1", "Q2", "Q3", "Q4"],
                            series=[
                                {"name": "Plan", "y": [280, 310, 295, 340]},
                                {"name": "Wykonanie", "y": [265, 325, 288, 352]},
                            ],
                            show_labels=True,
                            reference={"value": 300, "label": "Cel roczny /4"},
                        ),
                    ]),
                ]),
            ]),

            html.Div(style=S["group"], children=[
                html.Div("bar_stacked — skumulowany (absolutny i procentowy)", style=S["group-title"]),
                html.Div(style=S["grid-2"], children=[
                    html.Div(style=S["card"], children=[
                        bar_stacked(
                            "Struktura wydatków",
                            subtitle="mld zł, 2020–2024",
                            x=[2020, 2021, 2022, 2023, 2024],
                            series=[
                                {"name": "Świadczenia społeczne", "y": [320, 335, 355, 370, 390]},
                                {"name": "Inwestycje publiczne",  "y": [140, 155, 162, 170, 180]},
                                {"name": "Obsługa długu",        "y": [45, 48, 52, 60, 68]},
                                {"name": "Pozostałe",            "y": [95, 102, 108, 115, 122]},
                            ],
                        ),
                    ]),
                    html.Div(style=S["card"], children=[
                        bar_stacked(
                            "Udział składników — 100%",
                            subtitle="struktura procentowa, 2024",
                            x=CATS,
                            series=[
                                {"name": "Transfery",    "y": [52, 48, 55, 50, 45]},
                                {"name": "Inwestycje",  "y": [20, 22, 19, 21, 23]},
                                {"name": "Pozostałe",   "y": [28, 30, 26, 29, 32]},
                            ],
                            pct=True,
                        ),
                    ]),
                ]),
            ]),

            html.Div(style=S["group"], children=[
                html.Div("bar_horizontal — ranking i długie etykiety", style=S["group-title"]),
                html.Div(style=S["grid-2"], children=[
                    html.Div(style=S["card"], children=[
                        bar_horizontal(
                            "Kraje wg długu publicznego",
                            subtitle="% PKB, 2024 — posortowane malejąco",
                            categories=["Grecja", "Włochy", "Portugalia", "Francja", "Belgia",
                                        "Hiszpania", "Austria", "Polska", "Czechy", "Szwecja"],
                            values=[163, 137, 112, 109, 105, 103, 82, 54, 44, 32],
                        ),
                    ]),
                    html.Div(style=S["card"], children=[
                        bar_horizontal(
                            "Wzrost PKB per capita",
                            subtitle="%, 2023 — ranking krajów UE",
                            categories=CATS + ["Węgry", "Rumunia"],
                            values=[3.1, 1.8, 2.4, 1.2, 4.2, 2.8, 5.1],
                        ),
                    ]),
                ]),
            ]),

            html.Div(style=S["group"], children=[
                html.Div("bar_diverging — wartości dodatnie i ujemne od zera", style=S["group-title"]),
                html.Div(style=S["grid-2"], children=[
                    html.Div(style=S["card"], children=[
                        bar_diverging(
                            "Saldo fiskalne wg krajów",
                            subtitle="% PKB, 2024 — zielony = nadwyżka",
                            x=["Dania", "Szwecja", "Holandia", "Austria", "Polska",
                               "Francja", "Włochy", "Grecja"],
                            values=[3.2, 0.6, -0.3, -2.1, -5.1, -5.5, -7.2, -1.6],
                        ),
                    ]),
                    html.Div(style=S["card"], children=[
                        bar_diverging(
                            "Odchylenie od planu budżetowego",
                            subtitle="mld zł, Q1–Q4 2024",
                            x=["Q1", "Q2", "Q3", "Q4"],
                            values=[12.5, -8.3, 3.1, -5.2],
                            show_labels=True,
                        ),
                    ]),
                ]),
            ]),

            # ── Line charts ──────────────────────────────────────────────────
            html.H2("Wykresy liniowe", id="line", style=S["section-heading"]),
            html.P("Cztery warianty: pojedyncza seria, wiele serii, powierzchnia, skumulowana powierzchnia.",
                   style=S["section-desc"]),

            html.Div(style=S["group"], children=[
                html.Div("line_single / line_multi", style=S["group-title"]),
                html.Div(style=S["grid-2"], children=[
                    html.Div(style=S["card"], children=[
                        line_single(
                            "Dług publiczny Polski",
                            subtitle="% PKB, 2018–2024",
                            x=YEARS, name="% PKB",
                            y=[48.9, 45.7, 57.1, 53.8, 51.4, 49.7, 54.1],
                            reference={"value": 60, "label": "Limit SGP 60%"},
                        ),
                    ]),
                    html.Div(style=S["card"], children=[
                        line_multi(
                            "Dochody i wydatki",
                            subtitle="% PKB, porównanie 2018–2024",
                            x=YEARS,
                            series=[
                                {"name": "Dochody",  "y": [41.5, 42.3, 41.8, 43.2, 44.6, 46.1, 47.2]},
                                {"name": "Wydatki",  "y": [43.2, 44.0, 48.7, 46.5, 47.8, 49.3, 50.4]},
                                {"name": "Saldo",    "y": [-1.7, -1.7, -6.9, -3.3, -3.2, -3.2, -3.2]},
                            ],
                        ),
                    ]),
                ]),
            ]),

            html.Div(style=S["group"], children=[
                html.Div("line_area / line_area_stacked", style=S["group-title"]),
                html.Div(style=S["grid-2"], children=[
                    html.Div(style=S["card"], children=[
                        line_area(
                            "Dochody podatkowe",
                            subtitle="mld zł, 2018–2024 — podkreślenie wolumenu",
                            x=YEARS, name="mld zł",
                            y=[380, 410, 395, 445, 520, 580, 615],
                        ),
                    ]),
                    html.Div(style=S["card"], children=[
                        line_area_stacked(
                            "Struktura dochodów",
                            subtitle="mld zł — składniki skumulowane",
                            x=YEARS,
                            series=[
                                {"name": "VAT",    "y": [180, 195, 185, 215, 250, 278, 295]},
                                {"name": "PIT",    "y": [85, 90, 88, 100, 115, 128, 135]},
                                {"name": "CIT",    "y": [45, 52, 48, 58, 72, 85, 92]},
                                {"name": "Akcyza", "y": [70, 73, 74, 72, 83, 89, 93]},
                            ],
                        ),
                    ]),
                ]),
            ]),

            # ── Combo charts ─────────────────────────────────────────────────
            html.H2("Wykresy kombinowane", id="combo", style=S["section-heading"]),
            html.P("combo_bar_line: dla danych na tej samej skali. combo_subplots: dla różnych skal (wzorzec IBCS).",
                   style=S["section-desc"]),

            html.Div(style=S["group"], children=[
                html.Div("combo_bar_line — słupki i linia na wspólnej osi", style=S["group-title"]),
                html.Div(style=S["grid-2"], children=[
                    html.Div(style=S["card"], children=[
                        combo_bar_line(
                            "Wykonanie vs plan",
                            subtitle="mld zł — ta sama skala, wspólna oś",
                            x=[2020, 2021, 2022, 2023, 2024],
                            bar_series=[{"name": "Wykonanie", "y": [395, 445, 520, 580, 615]}],
                            line_series=[{"name": "Plan",     "y": [400, 430, 510, 560, 600]}],
                        ),
                    ]),
                    html.Div(style=S["card"], children=[
                        combo_bar_line(
                            "Dochody: bieżący vs poprzedni rok",
                            subtitle="mld zł — porównanie roczne",
                            x=["Q1", "Q2", "Q3", "Q4"],
                            bar_series=[{"name": "2024", "y": [148, 158, 155, 154]}],
                            line_series=[{"name": "2023", "y": [138, 148, 145, 149]}],
                        ),
                    ]),
                ]),
            ]),

            html.Div(style=S["group"], children=[
                html.Div("combo_subplots — panele ze wspólną osią X (wzorzec fiskalny IBCS)", style=S["group-title"]),
                html.Div(style=S["grid-2"], children=[
                    html.Div(style=S["card"], children=[
                        combo_subplots(
                            "Dochody / Wydatki / Saldo",
                            subtitle="mld zł, 2018–2024 — różne skale wymagają paneli",
                            x=YEARS,
                            panels=[
                                {"title": "Dochody (mld zł)", "type": "bar",
                                 "series": [{"name": "Dochody", "y": [380, 410, 395, 445, 520, 580, 615]}]},
                                {"title": "Wydatki (mld zł)", "type": "bar",
                                 "series": [{"name": "Wydatki", "y": [410, 440, 470, 488, 565, 630, 665]}]},
                                {"title": "Saldo (mld zł)", "type": "line", "diverging": True,
                                 "series": [{"name": "Saldo", "y": [-30, -30, -75, -43, -45, -50, -50]}]},
                            ],
                        ),
                    ]),
                    html.Div(style=S["card"], children=[
                        combo_subplots(
                            "Inflacja i stopy procentowe",
                            subtitle="% — dwie miary, różne skale",
                            x=YEARS,
                            panels=[
                                {"title": "Inflacja CPI (%)", "type": "line",
                                 "series": [{"name": "CPI", "y": [1.2, 2.3, 3.4, 5.1, 14.4, 11.5, 4.7]}]},
                                {"title": "Stopa NBP (%)", "type": "line",
                                 "series": [{"name": "NBP", "y": [1.5, 1.5, 0.1, 0.1, 6.75, 5.75, 5.75]}]},
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
                            "Struktura salda fiskalnego",
                            subtitle="mld zł, 2024 — jak składniki tworzą wynik",
                            categories=["VAT", "PIT", "CIT", "Akcyza", "Świadczenia", "Inwestycje", "Pozostałe", "Razem"],
                            values=[295, 135, 92, 93, -390, -180, -95, -50],
                            total_label="Razem",
                        ),
                    ]),
                    html.Div(style=S["card"], children=[
                        waterfall_variance(
                            "Zmiana długu 2023→2024",
                            subtitle="mld zł — co zmieniło poziom długu",
                            categories=["Dług 2023", "Nowe emisje", "Spłaty", "Kurs walut", "Inne", "Dług 2024"],
                            values=[1240, 180, -140, 35, 15, 1330],
                            base_label="Dług 2023",
                            final_label="Dług 2024",
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
                            "Dług a deficyt",
                            subtitle="% PKB, kraje UE — korelacja",
                            x=[32, 44, 54, 82, 103, 105, 109, 112, 137, 163],
                            y=[-0.3, -3.2, -5.1, -2.1, -3.4, -4.8, -5.5, -3.1, -7.2, -1.6],
                            labels=["Szwecja", "Czechy", "Polska", "Austria", "Belgia",
                                    "Hiszpania", "Francja", "Portugalia", "Włochy", "Grecja"],
                            trendline=True,
                        ),
                    ]),
                    html.Div(style=S["card"], children=[
                        scatter_bubble(
                            "PKB, dług i populacja",
                            subtitle="kraje UE — rozmiar = populacja",
                            x=[32, 44, 54, 82, 103, 109, 137],
                            y=[3.1, 4.2, 3.1, 1.2, 1.8, 2.4, 0.8],
                            size=[38, 10, 38, 9, 11, 68, 60],
                            labels=["Szwecja", "Czechy", "Polska", "Austria",
                                    "Belgia", "Francja", "Włochy"],
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
                            "Wskaźniki fiskalne",
                            subtitle="% PKB, 2024",
                            headers=["Kraj", "Dochody", "Wydatki", "Saldo", "Dług"],
                            rows=[
                                ["Polska",    47.2, 50.4, -3.2, 54.1],
                                ["Niemcy",    45.8, 47.5, -1.7, 63.2],
                                ["Francja",   52.3, 55.8, -5.5, 109.1],
                                ["Włochy",    48.1, 51.2, -7.2, 137.3],
                                ["Czechy",    43.6, 45.1, -1.6, 44.1],
                                ["Węgry",     44.2, 49.1, -4.9, 73.4],
                            ],
                            number_cols={1, 2, 3, 4},
                        ),
                    ]),
                    html.Div(style=S["card"], children=[
                        table_heatmap(
                            "Wzrost PKB — mapa ciepła",
                            subtitle="%, 2019–2024 — kolor = intensywność wzrostu",
                            headers=["Kraj", "2019", "2020", "2021", "2022", "2023", "2024"],
                            rows=[
                                ["Polska",    4.5, -2.5, 5.9, 5.3, 0.1, 3.1],
                                ["Niemcy",    1.0, -4.6, 3.1, 1.9, -0.3, 0.2],
                                ["Francja",   1.8, -7.9, 6.4, 2.6, 0.9, 1.1],
                                ["Włochy",    0.5, -8.9, 7.2, 3.7, 0.9, 0.7],
                                ["Czechy",    3.0, -5.5, 3.5, 2.4, 0.0, 1.5],
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
                        pie_chart("Struktura dochodów",
                                  subtitle="donut — max 5 kategorii",
                                  labels=["VAT", "PIT", "CIT", "Akcyza", "Pozostałe"],
                                  values=[295, 135, 92, 93, 60]),
                    ]),
                    html.Div(style=S["card"], children=[
                        pie_chart("Struktura wydatków",
                                  subtitle="donut — trzy kategorie",
                                  labels=["Świadczenia", "Inwestycje", "Pozostałe"],
                                  values=[390, 180, 95]),
                    ]),
                    html.Div(style=S["card"], children=[
                        pie_chart("Dług wg walut",
                                  subtitle="kołowy (bez środka)",
                                  labels=["PLN", "EUR", "USD", "Inne"],
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
                    html.Div(label, style={"fontSize": "13px", "fontWeight": "600", "color": TEXT, "marginBottom": "12px"}),
                    html.Div(style={"display": "flex", "gap": "16px", "flexWrap": "wrap"}, children=[
                        _color_swatch(n, c) for n, c in swatches
                    ]),
                ])
                for label, swatches in [
                    ("Tło i powierzchnie",     [("BG_PAGE", BG_PAGE), ("BG_SURFACE", BG_SURFACE), ("BORDER", BORDER), ("GRID", GRID), ("ZERO_LINE", ZERO_LINE)]),
                    ("Tekst",                  [("TEXT", TEXT), ("SUBTEXT", SUBTEXT), ("MUTED", MUTED)]),
                    ("Teal (zielonkawy)",       [("TEAL_1", TEAL_1), ("TEAL_2", TEAL_2), ("TEAL_3", TEAL_3), ("TEAL_4", TEAL_4), ("TEAL_PALE", TEAL_PALE)]),
                    ("Azure (niebieski)",       [("AZURE_1", AZURE_1), ("AZURE_2", AZURE_2), ("AZURE_3", AZURE_3), ("AZURE_4", AZURE_4), ("AZURE_PALE", AZURE_PALE)]),
                    ("Slate (szary)",           [("SLATE_1", SLATE_1), ("SLATE_2", SLATE_2), ("SLATE_3", SLATE_3), ("SLATE_4", SLATE_4)]),
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
