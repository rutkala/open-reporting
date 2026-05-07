#!/usr/bin/env python3
"""
End-to-end example — proves the skill helpers compose into a working
dashboard.

Two sections, one KPI row, two charts (line + clustered column).
Uses synthetic data — no warehouse access. Demonstrates:

- ``make_app(...)``                                        → deploy/app.md
- ``S`` dict + grids + cards                               → pages/layout/styles.md
- ``build_sidebar`` / ``build_header`` / ``build_footer``  → pages/layout/, pages/controls/
- ``register_toggle_callback``                             → pages/controls/navigation/
- ``Dimension`` / ``Measure`` / ``DIMS`` / ``MEASURES``    → data/measures_template.py
- ``kpi_row``, ``kpi_standard``, ``line``, ``clustered_column``
                                                           → products/visuals/components/

Run:
    PYTHONPATH=/opt/open-reporting:/opt/open-reporting/.claude/skills \\
    python3 .claude/skills/complex_dashboard/assets/example_app.py

Then open http://localhost:8060/example/
"""
from dash import html
import pandas as pd

from products.visuals.components.bar_chart import clustered_column
from products.visuals.components.kpi_card import kpi_row, kpi_standard
from products.visuals.components.line_chart import line
from products.visuals.lib.semantic import Dimension, Measure
from products.visuals.lib.theme import POSITIVE

from complex_dashboard.assets.pages.controls.navigation.sidebar_nav import (
    build_sidebar, register_toggle_callback,
)
from complex_dashboard.assets.pages.layout.footer import build_footer
from complex_dashboard.assets.pages.layout.header import build_header
from complex_dashboard.assets.pages.layout.styles import S
from complex_dashboard.assets.deploy.app_init import make_app


# ── Synthetic data ──────────────────────────────────────────────────────────
_df = pd.DataFrame({
    "dim_year":         [2018, 2019, 2020, 2021, 2022, 2023, 2024],
    "val_unemployment": [5.8,  5.2,  6.3,  5.4,  4.9,  5.0,  5.1],
    "val_employment":   [16_400, 16_550, 16_320, 16_700, 17_050, 17_280, 17_410],
})

DIMS = {"year": Dimension("year", "Rok", "dim_year")}
MEASURES = {
    "unemployment": Measure(
        "unemployment", "Stopa bezrobocia", "val_unemployment",
        unit="%", format_type="percent", decimals=1,
    ),
    "employment": Measure(
        "employment", "Zatrudnienie", "val_employment",
        unit="tys.", format_type="number", scale="K", decimals=0,
    ),
}


# ── App init ────────────────────────────────────────────────────────────────
PORT = 8060
app = make_app(
    domain="example",
    title="Przykład — complex_dashboard",
    module_name=__name__,
)


# ── Layout ──────────────────────────────────────────────────────────────────
_SECTIONS = [
    ("Bezrobocie", "unemployment"),
    ("Zatrudnienie", "employment"),
]

_x = DIMS["year"].values(_df)
_unempl_latest = float(_df["val_unemployment"].iloc[-1])
_empl_latest   = float(_df["val_employment"].iloc[-1])

app.layout = html.Div(style=S["body"], children=[
    build_sidebar(domain="example", sections=_SECTIONS),

    html.Main(style=S["main"], children=[
        *build_header(
            title="Przykład — complex_dashboard",
            subtitle="Dane syntetyczne 2018–2024",
            domain="example",
        ),

        html.Div(style=S["main-content-area"], children=[

            # ── Section 1 — Bezrobocie ───────────────────────────────────
            html.H2(
                "Stopa bezrobocia w czasie",
                id="unemployment",
                style={**S["section-heading"], "marginTop": 0},
            ),
            html.P(
                "Stopa bezrobocia w Polsce wg danych syntetycznych.",
                style=S["section-desc"],
            ),
            kpi_row([
                kpi_standard(
                    label=MEASURES["unemployment"].label,
                    value=MEASURES["unemployment"].kpi_value(_unempl_latest),
                    unit=MEASURES["unemployment"].plotly_ticksuffix,
                    trend="▼ -0.7 pp od 2018",
                    trend_color=POSITIVE,
                ),
            ]),
            html.Div(style=S["card"], children=[
                line(
                    "Stopa bezrobocia spadła do 5,1% w 2024",
                    subtitle="Źródło: dane syntetyczne — przykład skill",
                    x=_x,
                    series=[MEASURES["unemployment"].to_series(_df["val_unemployment"].tolist())],
                    y_measure=MEASURES["unemployment"],
                ),
            ]),

            # ── Section 2 — Zatrudnienie ─────────────────────────────────
            html.H2("Zatrudnienie ogółem", id="employment", style=S["section-heading"]),
            html.P(
                "Liczba pracujących, w tysiącach osób.",
                style=S["section-desc"],
            ),
            kpi_row([
                kpi_standard(
                    label=MEASURES["employment"].label,
                    value=MEASURES["employment"].kpi_value(_empl_latest),
                    unit=MEASURES["employment"].plotly_ticksuffix,
                    trend="▲ +1 010 tys. od 2018",
                    trend_color=POSITIVE,
                ),
            ]),
            html.Div(style=S["card"], children=[
                clustered_column(
                    "Zatrudnienie rośnie konsekwentnie po 2020",
                    subtitle="Źródło: dane syntetyczne — przykład skill",
                    x=[str(y) for y in _x],
                    series=[MEASURES["employment"].to_series(_df["val_employment"].tolist())],
                    y_measure=MEASURES["employment"],
                ),
            ]),
        ]),

        *build_footer(name="Przykład — complex_dashboard"),
    ]),
])


# ── Callbacks ───────────────────────────────────────────────────────────────
register_toggle_callback(app)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=False)
