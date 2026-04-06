"""Pie / donut chart — part-to-whole."""
import plotly.graph_objects as go

from products.visuals.lib.theme import COLORWAY
from products.visuals.components import _plotly_layout, _chart


def pie_chart(title, labels, values, subtitle="", donut=True):
    fig = go.Figure(go.Pie(
        labels=labels, values=values, hole=0.5 if donut else 0,
        marker=dict(colors=COLORWAY[:len(labels)]),
        textinfo="label+percent", textfont=dict(size=11),
    ))
    fig.update_layout(_plotly_layout())
    legend = [(labels[i], COLORWAY[i % len(COLORWAY)]) for i in range(len(labels))]
    return _chart(title=title, subtitle=subtitle, legend_items=legend, figure=fig)
