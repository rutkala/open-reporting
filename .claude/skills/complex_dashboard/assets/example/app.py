#!/usr/bin/env python3
"""Single-page example — proves the skill helpers compose into a working
dashboard.

Two sections, one KPI row each, two charts (line + clustered column).
Synthetic data — no warehouse access. Demonstrates:

- ``make_app(...)``                                          → specs/deploy/app_init.md
- ``S`` dict + grids + cards                                 → specs/layout/styles.md
- ``build_page_layout(...)``                                 → specs/page_layout.md
- ``build_sidebar`` / ``build_header`` / ``build_footer``    → specs/layout/, specs/controls/
- ``register_toggle_callback``                               → specs/controls/navigation/
- ``DIMS`` / ``MEASURES``                                    → ./measures.py
- ``load_by_year`` / ``load_by_region`` / ``load_scalars``   → ./data_loaders.py
- ``kpi_row`` + ``kpi_standard`` + ``line`` + ``clustered_column``
                                                             → products/visuals/components/

Run:
    PYTHONPATH=/opt/open-reporting:/opt/open-reporting/.claude/skills \\
    python3 .claude/skills/complex_dashboard/assets/example/app.py

Then open http://localhost:8060/example/.
"""
from dash import html

from complex_dashboard.assets.runtime import (
    S,
    build_page_layout, register_toggle_callback,
    register_healthcheck,
    make_app,
)
from complex_dashboard.assets.components.bar_chart import clustered_column
from complex_dashboard.assets.components.kpi_card import kpi_row, kpi_standard
from complex_dashboard.assets.components.line_chart import line
from complex_dashboard.assets.theme import POSITIVE

from complex_dashboard.assets.example.data_loaders import (
    load_by_region, load_by_year, load_scalars,
)
from complex_dashboard.assets.example.measures import DIMS, MEASURES


PORT = 8060

app = make_app(
    domain="example",
    title="Przykład — complex_dashboard",
    module_name=__name__,
)
register_healthcheck(app)


_SECTIONS = [
    ("Bezrobocie",   "unemployment"),
    ("Zatrudnienie", "employment"),
]

_year_df   = load_by_year()
_region_df = load_by_region()
_scalars   = load_scalars()


_content = [
    # ── Section 1 — Bezrobocie ──────────────────────────────────────────────
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
            value=MEASURES["unemployment"].kpi_value(_scalars["unemployment"]),
            unit=MEASURES["unemployment"].plotly_ticksuffix,
            trend="▼ -0.7 pp od 2018",
            trend_color=POSITIVE,
        ),
    ]),
    html.Div(style=S["card"], children=[
        line(
            "Stopa bezrobocia spadła do 5,1% w 2024",
            subtitle="Źródło: dane syntetyczne — przykład skill",
            x=DIMS["year"].values(_year_df),
            series=[MEASURES["unemployment"].to_series(_year_df["val_unemployment"].tolist())],
            y_measure=MEASURES["unemployment"],
        ),
    ]),

    # ── Section 2 — Zatrudnienie ────────────────────────────────────────────
    html.H2("Zatrudnienie według województwa", id="employment", style=S["section-heading"]),
    html.P(
        "Liczba pracujących, w tysiącach osób — top 5 województw.",
        style=S["section-desc"],
    ),
    kpi_row([
        kpi_standard(
            label=MEASURES["employment"].label,
            value=MEASURES["employment"].kpi_value(_scalars["employment"]),
            unit=MEASURES["employment"].plotly_ticksuffix,
            trend="▲ +1 010 tys. od 2018",
            trend_color=POSITIVE,
        ),
    ]),
    html.Div(style=S["card"], children=[
        clustered_column(
            "Mazowieckie zdecydowanie przed pozostałymi regionami",
            subtitle="Źródło: dane syntetyczne — przykład skill",
            x=DIMS["region"].values(_region_df),
            series=[MEASURES["employment"].to_series(_region_df["val_employment"].tolist())],
            y_measure=MEASURES["employment"],
        ),
    ]),
]


app.layout = build_page_layout(
    domain="example",
    title="Przykład — complex_dashboard",
    subtitle="Dane syntetyczne 2018–2024",
    sections=_SECTIONS,
    content=_content,
    footer_name="Przykład — complex_dashboard",
    footer_source="dane syntetyczne",
    footer_updated="2018–2024",
)


register_toggle_callback(app)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=False)
