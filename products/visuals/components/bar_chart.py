"""Bar chart — categorical comparison."""
import plotly.graph_objects as go

from products.visuals.lib.theme import COLORWAY
from products.visuals.components import _plotly_layout, _chart


def bar_chart(title, x, series, subtitle="", horizontal=False):
    fig = go.Figure()
    for i, s in enumerate(series):
        if horizontal:
            fig.add_trace(go.Bar(y=x, x=s["y"], name=s["name"], orientation="h",
                                  marker_color=s.get("color", COLORWAY[i % len(COLORWAY)])))
        else:
            fig.add_trace(go.Bar(x=x, y=s["y"], name=s["name"],
                                  marker_color=s.get("color", COLORWAY[i % len(COLORWAY)])))
    kw = {"barmode": "group"}
    if not horizontal:
        kw["yaxis"] = {"rangemode": "tozero"}
    fig.update_layout(_plotly_layout(**kw))
    legend = [(s["name"], s.get("color", COLORWAY[i % len(COLORWAY)])) for i, s in enumerate(series)] if len(series) > 1 else None
    return _chart(title=title, subtitle=subtitle, legend_items=legend, figure=fig)
