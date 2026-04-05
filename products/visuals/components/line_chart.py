"""Line chart — trends over time."""
import plotly.graph_objects as go

from products.visuals.lib.theme import COLORWAY
from products.visuals.components import _plotly_layout, _chart


def line_chart(title, x, series, subtitle=""):
    fig = go.Figure()
    for i, s in enumerate(series):
        fig.add_trace(go.Scatter(
            x=x, y=s["y"], name=s["name"], mode="lines",
            line=dict(color=s.get("color", COLORWAY[i % len(COLORWAY)]), width=2),
        ))
    legend = [(s["name"], s.get("color", COLORWAY[i % len(COLORWAY)])) for i, s in enumerate(series)] if len(series) > 1 else None
    return _chart(title=title, subtitle=subtitle, legend_items=legend, figure=fig)
