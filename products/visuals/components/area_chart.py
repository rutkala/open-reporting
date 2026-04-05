"""Area chart — composition / volume over time."""
import plotly.graph_objects as go

from products.visuals.lib.theme import COLORWAY
from products.visuals.components import _plotly_layout, _chart


def _hex_to_rgba(hex_color, alpha=0.2):
    r = int(hex_color[1:3], 16)
    g = int(hex_color[3:5], 16)
    b = int(hex_color[5:7], 16)
    return f"rgba({r}, {g}, {b}, {alpha})"


def area_chart(title, x, series, subtitle="", stacked=False):
    fig = go.Figure()
    for i, s in enumerate(series):
        color = s.get("color", COLORWAY[i % len(COLORWAY)])
        fig.add_trace(go.Scatter(
            x=x, y=s["y"], name=s["name"], mode="lines",
            fill="tonexty" if i > 0 else "tozeroy",
            fillcolor=_hex_to_rgba(color),
            line=dict(color=color, width=1.5),
        ))
    fig.update_layout(_plotly_layout())
    legend = [(s["name"], s.get("color", COLORWAY[i % len(COLORWAY)])) for i, s in enumerate(series)] if len(series) > 1 else None
    return _chart(title=title, subtitle=subtitle, legend_items=legend, figure=fig)
