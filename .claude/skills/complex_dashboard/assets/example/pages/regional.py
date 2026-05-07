"""Multi-page example — regional page (path='/regional').

Second URL of the example app. Demonstrates that page modules can
carry their own data shape and visual components without touching the
overview page.
"""
import dash
from dash import html

import pandas as pd

from complex_dashboard.assets.runtime import S
from products.visuals.components.bar_chart import clustered_column
from products.visuals.lib.semantic import Dimension, Measure


dash.register_page(
    __name__,
    path="/regional",
    name="Regiony",
    title="Przykład — regiony",
    order=1,
)


_df = pd.DataFrame({
    "dim_region":     ["Mazowieckie", "Śląskie", "Małopolskie", "Wielkopolskie", "Pomorskie"],
    "val_employment": [3_010, 1_840, 1_420, 1_490, 920],
})

_REGION = Dimension("region", "Województwo", "dim_region")
_EMPL = Measure(
    "employment", "Zatrudnienie", "val_employment",
    unit="tys.", format_type="number", scale="K", decimals=0,
)


def layout():
    return html.Div([
        html.H2(
            "Zatrudnienie według województwa",
            id="regional",
            style={**S["section-heading"], "marginTop": 0},
        ),
        html.P(
            "Liczba pracujących, w tysiącach osób — top 5 województw.",
            style=S["section-desc"],
        ),
        html.Div(style=S["card"], children=[
            clustered_column(
                "Mazowieckie zdecydowanie przed pozostałymi regionami",
                subtitle="Źródło: dane syntetyczne — przykład skill",
                x=_REGION.values(_df),
                series=[_EMPL.to_series(_df["val_employment"].tolist())],
                y_measure=_EMPL,
            ),
        ]),
    ])
