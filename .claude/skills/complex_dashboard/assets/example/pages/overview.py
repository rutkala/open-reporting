"""Multi-page example — overview page (path='/').

Lives at the dashboard root. Carries the headline KPI and the
time-series chart. Synthetic data, no warehouse access — exercises
the same DIMS / MEASURES / load_* shape a real dashboard uses.
"""
import dash
from dash import html

import pandas as pd

from complex_dashboard.assets.runtime import S
from products.visuals.components.kpi_card import kpi_row, kpi_standard
from products.visuals.components.line_chart import line
from products.visuals.lib.semantic import Dimension, Measure
from products.visuals.lib.theme import POSITIVE


dash.register_page(
    __name__,
    path="/",
    name="Przegląd",
    title="Przykład — przegląd",
    order=0,
)


_df = pd.DataFrame({
    "dim_year":         [2018, 2019, 2020, 2021, 2022, 2023, 2024],
    "val_unemployment": [5.8,  5.2,  6.3,  5.4,  4.9,  5.0,  5.1],
})

_YEAR = Dimension("year", "Rok", "dim_year")
_UNEMPL = Measure(
    "unemployment", "Stopa bezrobocia", "val_unemployment",
    unit="%", format_type="percent", decimals=1,
)


def layout():
    latest = float(_df["val_unemployment"].iloc[-1])
    return html.Div([
        html.H2(
            "Stopa bezrobocia w czasie",
            id="overview",
            style={**S["section-heading"], "marginTop": 0},
        ),
        html.P(
            "Stopa bezrobocia w Polsce wg danych syntetycznych.",
            style=S["section-desc"],
        ),
        kpi_row([
            kpi_standard(
                label=_UNEMPL.label,
                value=_UNEMPL.kpi_value(latest),
                unit=_UNEMPL.plotly_ticksuffix,
                trend="▼ -0.7 pp od 2018",
                trend_color=POSITIVE,
            ),
        ]),
        html.Div(style=S["card"], children=[
            line(
                "Stopa bezrobocia spadła do 5,1% w 2024",
                subtitle="Źródło: dane syntetyczne — przykład skill",
                x=_YEAR.values(_df),
                series=[_UNEMPL.to_series(_df["val_unemployment"].tolist())],
                y_measure=_UNEMPL,
            ),
        ]),
    ])
