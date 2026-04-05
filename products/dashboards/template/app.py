#!/usr/bin/env python3
"""
Open Reporting — Template Dashboard
Reusable scaffold for new domain dashboards.
Copy this directory, rename, and customise for your domain.

Run:
    PYTHONPATH=/opt/open-reporting \
    DUCKDB_PATH=/opt/open-reporting/data/warehouse.duckdb \
    python3 products/dashboards/template/app.py
"""
import logging

from dash import Dash, Input, Output, State, callback, dcc, html

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

from products.visuals.components.line_chart import line_chart
from products.visuals.components.bar_chart import bar_chart
from products.visuals.components.area_chart import area_chart
from products.visuals.components.pie_chart import pie_chart
from products.visuals.components.kpi_card import kpi_card

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

PORT = 8055

# ── Helpers ────────────────────────────────────────────────────────────────────

def _color_swatch(name: str, color: str) -> html.Div:
    """Render a color swatch with label."""
    return html.Div(style={
        "display": "flex", "flexDirection": "column", "alignItems": "center",
        "gap": "6px", "minWidth": "80px",
    }, children=[
        html.Div(style={
            "width": "48px", "height": "48px",
            "borderRadius": "8px",
            "backgroundColor": color,
            "border": f"1px solid {BORDER}",
            "boxShadow": "0 1px 3px rgba(0,0,0,0.06)",
        }),
        html.Span(name, style={
            "fontSize": "10px", "color": SUBTEXT, "fontFamily": "monospace",
        }),
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

SIDEBAR_W = "240px"
SIDEBAR_COLLAPSED = "44px"
GAP = "4px"
RADIUS = "10px"

S = {
    "body": {
        "fontFamily": "Inter, 'Segoe UI', system-ui, sans-serif",
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
        "height": "68px",
        "boxSizing": "border-box",
        "display": "flex",
        "alignItems": "center",
    },
    "sidebar-divider": {
        "margin": "0 16px",
        "border": "none",
        "borderTop": f"1px solid {BORDER}",
    },
    "logo": {
        "height": "32px",
        "width": "auto",
    },
    "sidebar-nav": {
        "flex": 1, "padding": "16px 0", "overflowY": "auto",
        "whiteSpace": "nowrap", "overflow": "hidden",
    },
    "nav-item": {
        "display": "block", "padding": "8px 20px",
        "fontSize": "13px", "color": SUBTEXT, "textDecoration": "none",
        "cursor": "pointer",
    },
    "nav-item-active": {
        "display": "block", "padding": "8px 20px",
        "fontSize": "13px", "color": TEXT, "textDecoration": "none",
        "borderLeft": f"3px solid {TEXT}",
        "backgroundColor": f"{BORDER}40",
        "cursor": "pointer",
    },
    "toggle-btn": {
        "position": "absolute",
        "top": "28px",
        "right": "10px",
        "width": "24px",
        "height": "24px",
        "background": "none",
        "border": "none",
        "cursor": "pointer",
        "padding": 0,
        "display": "flex", "alignItems": "center", "justifyContent": "center",
        "zIndex": 100,
    },
    "toggle-icon": {
        "width": "20px",
        "height": "20px",
        "opacity": 0.5,
    },
    "main": {
        "flex": 1, "minWidth": 0,
        "overflowY": "auto", "overflowX": "hidden", "height": f"calc(100vh - {GAP} * 2)",
        "boxSizing": "border-box",
        "display": "flex", "flexDirection": "column",
    },
    "main-header": {
        "padding": "0 32px",
        "flexShrink": 0,
        "display": "flex",
        "alignItems": "center",
        "justifyContent": "space-between",
        "height": "68px",
    },
    "header-actions": {
        "display": "flex",
        "alignItems": "center",
        "gap": "8px",
    },
    "header-btn": {
        "width": "32px",
        "height": "32px",
        "background": "none",
        "border": f"1px solid {BORDER}",
        "borderRadius": "6px",
        "cursor": "pointer",
        "display": "flex",
        "alignItems": "center",
        "justifyContent": "center",
        "color": SUBTEXT,
        "padding": 0,
    },
    "header-icon": {
        "width": "16px",
        "height": "16px",
    },
    "main-divider": {
        "margin": "0 32px",
        "border": "none",
        "borderTop": f"1px solid {BORDER}",
    },
    "main-footer": {
        "padding": "0 32px",
        "flexShrink": 0,
        "display": "flex",
        "alignItems": "center",
        "justifyContent": "space-between",
        "height": "48px",
    },
    "footer-divider": {
        "margin": "0 32px",
        "border": "none",
        "borderTop": f"1px solid {BORDER}",
    },
    "footer-text": {
        "fontSize": "12px",
        "color": SUBTEXT,
    },
    "main-content-area": {
        "flex": 1, "padding": "28px 32px 0",
        "overflowY": "auto",
        "width": "100%",
        "boxSizing": "border-box",
    },
    "chart-group": {
        "marginBottom": "32px", "width": "100%",
    },
    "chart-group-title": {
        "fontSize": "14px", "fontWeight": 600, "color": TEXT,
        "marginBottom": "16px",
    },
    "chart-grid-2": {
        "display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "20px",
        "alignItems": "start",
    },
    "chart-grid-3": {
        "display": "grid", "gridTemplateColumns": "1fr 1fr 1fr", "gap": "20px",
        "alignItems": "start",
    },
    "chart-grid-auto": {
        "display": "grid",
        "gridTemplateColumns": "repeat(auto-fit, minmax(200px, 1fr))",
        "gap": "16px",
        "maxWidth": "100%",
    },
    "chart-card": {
        "background": BG_SURFACE,
        "border": f"1px solid {BORDER}",
        "borderRadius": "8px",
        "padding": "16px",
        "overflow": "hidden",
        "minWidth": 0,
    },
}

# ── Layout ────────────────────────────────────────────────────────────────────

app.layout = html.Div(style=S["body"], children=[

    html.Aside(id="sidebar", style=S["sidebar"], children=[

        html.Div(id="sidebar-logo", style=S["sidebar-logo"], children=[
            html.A(
                html.Img(id="sidebar-logo-img", src="/template/assets/images/logo.svg",
                         style=S["logo"]),
                href="/",
            ),
        ]),

        html.Hr(id="sidebar-divider", style=S["sidebar-divider"]),

        html.Nav(id="sidebar-nav", style=S["sidebar-nav"], children=[
            html.A("Placeholder nav 1", href="#", style=S["nav-item-active"]),
            html.A("Placeholder nav 2", href="#", style=S["nav-item"]),
            html.A("Placeholder nav 3", href="#", style=S["nav-item"]),
        ]),

        html.Button(id="btn-toggle", style=S["toggle-btn"], children=[
            html.Img(id="toggle-icon", src="/template/assets/images/sidebar.svg",
                     style=S["toggle-icon"]),
        ]),
    ]),

    html.Main(id="main-content", style=S["main"], children=[

        html.Div(id="main-header", style=S["main-header"], children=[
            html.Div(children=[
                html.H1("Dashboard title",
                        style={"fontSize": "20px", "fontWeight": 700, "color": TEXT, "margin": 0}),
                html.P("Dashboard subtitle — description or data source info",
                       style={"fontSize": "13px", "color": SUBTEXT, "margin": "4px 0 0"}),
            ]),
            html.Div(style=S["header-actions"], children=[
                html.Button(
                    html.Img(src="/template/assets/images/settings.svg",
                             style=S["header-icon"]),
                    id="btn-settings",
                    style=S["header-btn"],
                    title="Ustawienia",
                ),
                html.Button(
                    html.Img(src="/template/assets/images/user.svg",
                             style=S["header-icon"]),
                    id="btn-user",
                    style=S["header-btn"],
                    title="Użytkownik",
                ),
            ]),
        ]),

        html.Hr(style=S["main-divider"]),

        html.Div(id="main-content-area", style=S["main-content-area"], children=[

            # KPI row
            html.Div(style=S["chart-group"], children=[
                html.Div("KPI — kluczowe wskaźniki", style=S["chart-group-title"]),
                html.Div(style=S["chart-grid-auto"], children=[
                    kpi_card("Miara 1", "1 234,5", unit="mln", trend="▲ +5,2%"),
                    kpi_card("Miara 2", "56,7%", trend="▼ −1,3 pp"),
                    kpi_card("Miara 3", "890", unit="tys.", trend="▲ +12,1%"),
                    kpi_card("Miara 4", "2024"),
                ]),
            ]),

            # Line charts row
            html.Div(style=S["chart-group"], children=[
                html.Div("Wykresy liniowe", style=S["chart-group-title"]),
                html.Div(style=S["chart-grid-2"], children=[
                    html.Div(style=S["chart-card"], children=[
                        line_chart("Trend 1",
                                   subtitle="Dane przykładowe — szereg czasowy",
                                   x=[2019, 2020, 2021, 2022, 2023, 2024],
                                   series=[
                                       {"name": "Seria A", "y": [450, 420, 480, 510, 540, 580]},
                                       {"name": "Seria B", "y": [320, 300, 340, 360, 390, 410]},
                                   ]),
                    ]),
                    html.Div(style=S["chart-card"], children=[
                        line_chart("Trend 2",
                                   subtitle="Dane przykładowe — pojedyncza seria",
                                   x=[2019, 2020, 2021, 2022, 2023, 2024],
                                   series=[
                                       {"name": "Seria C", "y": [85, 92, 98, 102, 108, 115]},
                                   ]),
                    ]),
                ]),
            ]),

            # Bar charts row
            html.Div(style=S["chart-group"], children=[
                html.Div("Wykresy słupkowe", style=S["chart-group-title"]),
                html.Div(style=S["chart-grid-2"], children=[
                    html.Div(style=S["chart-card"], children=[
                        bar_chart("Porównanie 1",
                                  subtitle="Dane przykładowe — grupy kategorii",
                                  x=["Kat. A", "Kat. B", "Kat. C", "Kat. D"],
                                  series=[
                                      {"name": "2023", "y": [68, 55, 42, 38]},
                                      {"name": "2024", "y": [72, 62, 45, 40]},
                                  ]),
                    ]),
                    html.Div(style=S["chart-card"], children=[
                        bar_chart("Porównanie 2",
                                  subtitle="Dane przykładowe — jedna seria",
                                  x=["Kat. A", "Kat. B", "Kat. C", "Kat. D"],
                                  series=[
                                      {"name": "Wartość", "y": [180, 320, 250, 450]},
                                  ]),
                    ]),
                ]),
            ]),

            # Area charts row
            html.Div(style=S["chart-group"], children=[
                html.Div("Wykresy powierzchniowe", style=S["chart-group-title"]),
                html.Div(style=S["chart-grid-2"], children=[
                    html.Div(style=S["chart-card"], children=[
                        area_chart("Struktura 1",
                                   subtitle="Dane przykładowe — nakładanie powierzchni",
                                   x=[2019, 2020, 2021, 2022, 2023, 2024],
                                   series=[
                                       {"name": "Składnik A", "y": [65, 62, 68, 70, 72, 75]},
                                       {"name": "Składnik B", "y": [40, 45, 50, 55, 60, 65]},
                                       {"name": "Składnik C", "y": [35, 38, 40, 42, 44, 47]},
                                   ]),
                    ]),
                    html.Div(style=S["chart-card"], children=[
                        area_chart("Struktura 2",
                                   subtitle="Dane przykładowe — pojedyncza seria",
                                   x=[2019, 2020, 2021, 2022, 2023, 2024],
                                   series=[
                                       {"name": "Wartość", "y": [950, 1080, 1120, 1150, 1180, 1200]},
                                   ]),
                    ]),
                ]),
            ]),

            # Pie charts row
            html.Div(style=S["chart-group"], children=[
                html.Div("Wykresy kołowe", style=S["chart-group-title"]),
                html.Div(style=S["chart-grid-3"], children=[
                    html.Div(style=S["chart-card"], children=[
                        pie_chart("Udział 1",
                                  subtitle="Dane przykładowe — wykres pierścieniowy",
                                  labels=["A", "B", "C", "D", "E"],
                                  values=[28, 18, 32, 14, 8]),
                    ]),
                    html.Div(style=S["chart-card"], children=[
                        pie_chart("Udział 2",
                                  subtitle="Dane przykładowe — trzy kategorie",
                                  labels=["X", "Y", "Z"],
                                  values=[55, 25, 20]),
                    ]),
                    html.Div(style=S["chart-card"], children=[
                        pie_chart("Udział 3",
                                  subtitle="Dane przykładowe — wykres kołowy",
                                  labels=["P", "Q", "R", "S", "T"],
                                  values=[30, 25, 20, 15, 10],
                                  donut=False),
                    ]),
                ]),
            ]),

            # ── Visual settings reference ─────────────────────────────────
            html.Div(style={**S["chart-group"], "marginTop": "48px"}, children=[
                html.Div("Paleta wizualna — ustawienia motywu", style={
                    **S["chart-group-title"],
                    "fontSize": "16px",
                    "fontWeight": "700",
                    "marginBottom": "24px",
                }),

                # Background colors
                html.Div(style={"marginBottom": "32px"}, children=[
                    html.Div("Kolory tła", style={
                        "fontSize": "13px", "fontWeight": "600", "color": TEXT,
                        "marginBottom": "12px",
                    }),
                    html.Div(style={"display": "flex", "gap": "16px", "flexWrap": "wrap"}, children=[
                        _color_swatch("BG_PAGE", BG_PAGE),
                        _color_swatch("BG_SURFACE", BG_SURFACE),
                        _color_swatch("BORDER", BORDER),
                        _color_swatch("GRID", GRID),
                        _color_swatch("ZERO_LINE", ZERO_LINE),
                    ]),
                ]),

                # Text colors
                html.Div(style={"marginBottom": "32px"}, children=[
                    html.Div("Kolory tekstu", style={
                        "fontSize": "13px", "fontWeight": "600", "color": TEXT,
                        "marginBottom": "12px",
                    }),
                    html.Div(style={"display": "flex", "gap": "16px", "flexWrap": "wrap"}, children=[
                        _color_swatch("TEXT", TEXT),
                        _color_swatch("SUBTEXT", SUBTEXT),
                        _color_swatch("MUTED", MUTED),
                    ]),
                ]),

                # Teal accent colors
                html.Div(style={"marginBottom": "32px"}, children=[
                    html.Div("Kolory akcentów (Teal — zielonkawy)", style={
                        "fontSize": "13px", "fontWeight": "600", "color": TEXT,
                        "marginBottom": "12px",
                    }),
                    html.Div(style={"display": "flex", "gap": "16px", "flexWrap": "wrap"}, children=[
                        _color_swatch("TEAL_1", TEAL_1),
                        _color_swatch("TEAL_2", TEAL_2),
                        _color_swatch("TEAL_3", TEAL_3),
                        _color_swatch("TEAL_4", TEAL_4),
                        _color_swatch("TEAL_PALE", TEAL_PALE),
                    ]),
                ]),

                # Azure accent colors
                html.Div(style={"marginBottom": "32px"}, children=[
                    html.Div("Kolory akcentów (Azure — niebieski)", style={
                        "fontSize": "13px", "fontWeight": "600", "color": TEXT,
                        "marginBottom": "12px",
                    }),
                    html.Div(style={"display": "flex", "gap": "16px", "flexWrap": "wrap"}, children=[
                        _color_swatch("AZURE_1", AZURE_1),
                        _color_swatch("AZURE_2", AZURE_2),
                        _color_swatch("AZURE_3", AZURE_3),
                        _color_swatch("AZURE_4", AZURE_4),
                        _color_swatch("AZURE_PALE", AZURE_PALE),
                    ]),
                ]),

                # Slate accent colors
                html.Div(style={"marginBottom": "32px"}, children=[
                    html.Div("Kolory akcentów (Slate — szary)", style={
                        "fontSize": "13px", "fontWeight": "600", "color": TEXT,
                        "marginBottom": "12px",
                    }),
                    html.Div(style={"display": "flex", "gap": "16px", "flexWrap": "wrap"}, children=[
                        _color_swatch("SLATE_1", SLATE_1),
                        _color_swatch("SLATE_2", SLATE_2),
                        _color_swatch("SLATE_3", SLATE_3),
                        _color_swatch("SLATE_4", SLATE_4),
                    ]),
                ]),

                # Semantic colors
                html.Div(style={"marginBottom": "32px"}, children=[
                    html.Div("Kolory semantyczne", style={
                        "fontSize": "13px", "fontWeight": "600", "color": TEXT,
                        "marginBottom": "12px",
                    }),
                    html.Div(style={"display": "flex", "gap": "16px", "flexWrap": "wrap"}, children=[
                        _color_swatch("POSITIVE", POSITIVE),
                        _color_swatch("NEGATIVE", NEGATIVE),
                        _color_swatch("WARNING", WARNING),
                    ]),
                ]),

                # Colorway
                html.Div(style={"marginBottom": "32px"}, children=[
                    html.Div("COLORWAY — domyślna paleta wykresów", style={
                        "fontSize": "13px", "fontWeight": "600", "color": TEXT,
                        "marginBottom": "12px",
                    }),
                    html.Div(style={"display": "flex", "gap": "12px", "flexWrap": "wrap"}, children=[
                        _color_swatch(f"COLORWAY[{i}]", c) for i, c in enumerate(COLORWAY)
                    ]),
                ]),

                # Typography
                html.Div(style={"marginBottom": "32px"}, children=[
                    html.Div("Typografia", style={
                        "fontSize": "13px", "fontWeight": "600", "color": TEXT,
                        "marginBottom": "12px",
                    }),
                    html.Div(style={"display": "flex", "flexDirection": "column", "gap": "8px"}, children=[
                        html.Div(children=[
                            html.Span("Rodzina: ", style={"color": SUBTEXT, "fontSize": "12px"}),
                            html.Span(FONT_FAMILY, style={"color": TEXT, "fontSize": "12px", "fontFamily": FONT_FAMILY}),
                        ]),
                        html.Div(children=[
                            html.Span("Tytuł dashboardu: ", style={"color": SUBTEXT, "fontSize": "12px"}),
                            html.Span("20px / 700 (bold)", style={"fontSize": "20px", "fontWeight": 700, "color": TEXT}),
                        ]),
                        html.Div(children=[
                            html.Span("Podtytuł: ", style={"color": SUBTEXT, "fontSize": "12px"}),
                            html.Span("13px / normal / SUBTEXT", style={"fontSize": "13px", "color": SUBTEXT}),
                        ]),
                        html.Div(children=[
                            html.Span("Nagłówek grupy wykresów: ", style={"color": SUBTEXT, "fontSize": "12px"}),
                            html.Span("14px / 600 (semibold)", style={"fontSize": "14px", "fontWeight": 600, "color": TEXT}),
                        ]),
                        html.Div(children=[
                            html.Span("Tytuł wykresu: ", style={"color": SUBTEXT, "fontSize": "12px"}),
                            html.Span("14px / 600", style={"fontSize": "14px", "fontWeight": 600, "color": TEXT}),
                        ]),
                        html.Div(children=[
                            html.Span("Podtytuł wykresu: ", style={"color": SUBTEXT, "fontSize": "12px"}),
                            html.Span("12px / SUBTEXT", style={"fontSize": "12px", "color": SUBTEXT}),
                        ]),
                        html.Div(children=[
                            html.Span("Legenda: ", style={"color": SUBTEXT, "fontSize": "12px"}),
                            html.Span("11px / SUBTEXT", style={"fontSize": "11px", "color": SUBTEXT}),
                        ]),
                        html.Div(children=[
                            html.Span("Etykiety osi: ", style={"color": SUBTEXT, "fontSize": "12px"}),
                            html.Span("11px / SUBTEXT", style={"fontSize": "11px", "color": SUBTEXT}),
                        ]),
                        html.Div(children=[
                            html.Span("Stopka: ", style={"color": SUBTEXT, "fontSize": "12px"}),
                            html.Span("12px / SUBTEXT", style={"fontSize": "12px", "color": SUBTEXT}),
                        ]),
                    ]),
                ]),

                # Chart settings
                html.Div(style={"marginBottom": "32px"}, children=[
                    html.Div("Ustawienia wykresów", style={
                        "fontSize": "13px", "fontWeight": "600", "color": TEXT,
                        "marginBottom": "12px",
                    }),
                    html.Div(style={"display": "flex", "flexDirection": "column", "gap": "6px"}, children=[
                        html.Span("Wysokość wykresu: 320px", style={"fontSize": "12px", "color": TEXT}),
                        html.Span("Hover mode: x unified", style={"fontSize": "12px", "color": TEXT}),
                        html.Span("Siatka: tylko oś Y (GRID)", style={"fontSize": "12px", "color": TEXT}),
                        html.Span("Wykresy słupkowe: zaczynają się od zera", style={"fontSize": "12px", "color": TEXT}),
                        html.Span("Tło wykresu: przezroczyste", style={"fontSize": "12px", "color": TEXT}),
                        html.Span("Grubość linii: 2px", style={"fontSize": "12px", "color": TEXT}),
                    ]),
                ]),
            ]),
        ]),

        html.Hr(style=S["footer-divider"]),

        html.Footer(style=S["main-footer"], children=[
            html.Span("Open Reporting — szablon dashboardu", style=S["footer-text"]),
            html.A("open-reporting.dev", href="https://open-reporting.dev",
                   style={**S["footer-text"], "textDecoration": "none"}),
        ]),
    ]),
])

# ── Callbacks ─────────────────────────────────────────────────────────────────

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

    btn_open = dict(S["toggle-btn"])
    btn_open["right"] = "10px"
    btn_open["transform"] = "none"

    btn_closed = dict(S["toggle-btn"])
    btn_closed["right"] = "50%"
    btn_closed["transform"] = "translateX(50%)"

    if is_expanded:
        sb = dict(sidebar_style)
        sb["width"] = SIDEBAR_COLLAPSED
        return (
            sb,
            btn_closed,
            {"display": "none"},
            {"display": "none"},
            {"display": "none"},
        )
    else:
        return (
            S["sidebar"],
            btn_open,
            S["sidebar-logo"],
            S["sidebar-nav"],
            S["logo"],
        )

# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    log.info("Starting Template dashboard on port %d", PORT)
    app.run(host="0.0.0.0", port=PORT, debug=False)
