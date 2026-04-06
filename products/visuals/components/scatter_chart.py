"""
Scatter and bubble chart variants.
KB reference: team/analytics/visualization/charts/scatter.md

Rules applied:
- Axes do NOT force zero (KB: scatter is exempt from zero-baseline rule)
- Bubble size mapped proportionally (KB: area encoding, not radius)
- Opacity 0.7 to handle overlapping points (KB: 60–80%)
- Optional trendline in scatter_basic
"""
import plotly.graph_objects as go
import numpy as np

from products.visuals.lib.theme import COLORWAY, AZURE_1, SLATE_1, SUBTEXT, TEXT, BORDER, GRID, ZERO_LINE
from products.visuals.components import PLOT_H, MARGIN_L, MARGIN_R, MARGIN_T, MARGIN_B, _chart
from products.visuals.lib.theme import FONT_FAMILY

_SCATTER_LAYOUT = {
    "template": "teal",
    "height": PLOT_H,
    "margin_l": MARGIN_L,
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(0,0,0,0)",
    "showlegend": False,
    "hovermode": "closest",
}


def _base_layout(**kw):
    return {
        "template": "teal",
        "height": PLOT_H,
        "margin": dict(l=MARGIN_L, r=MARGIN_R, t=MARGIN_T, b=MARGIN_B),
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": dict(family=FONT_FAMILY, color=TEXT, size=12),
        "xaxis": dict(showgrid=True, gridcolor=GRID, showline=True, linecolor=BORDER,
                      tickfont=dict(size=11, color=SUBTEXT), zerolinecolor=ZERO_LINE),
        "yaxis": dict(showgrid=True, gridcolor=GRID, showline=True, linecolor=BORDER,
                      tickfont=dict(size=11, color=SUBTEXT), zerolinecolor=ZERO_LINE),
        "showlegend": False,
        "hovermode": "closest",
        **kw,
    }


def scatter_basic(title, x, y, subtitle="", labels=None, trendline=False):
    """
    Basic scatter plot — correlation between two continuous variables.

    Args:
        labels:    list of point labels (shown in hover, optional)
        trendline: if True, add a linear regression line
    """
    hover = labels if labels else [f"({xi}, {yi})" for xi, yi in zip(x, y)]
    fig = go.Figure(go.Scatter(
        x=x, y=y,
        mode="markers",
        marker=dict(color=AZURE_1, size=8, opacity=0.7,
                    line=dict(color="white", width=1)),
        text=hover,
        hovertemplate="%{text}<extra></extra>",
    ))

    if trendline:
        xn, yn = np.array(x, dtype=float), np.array(y, dtype=float)
        m, b = np.polyfit(xn, yn, 1)
        x_range = [float(xn.min()), float(xn.max())]
        y_range = [m * x_range[0] + b, m * x_range[1] + b]
        fig.add_trace(go.Scatter(
            x=x_range, y=y_range, mode="lines",
            line=dict(color=SLATE_1, width=1.5, dash="dash"),
            hoverinfo="skip",
        ))

    fig.update_layout(_base_layout())
    return _chart(title=title, subtitle=subtitle, figure=fig)


def scatter_bubble(title, x, y, size, subtitle="", labels=None, color_values=None):
    """
    Bubble chart — three variables encoded as x, y, and bubble size.
    Size is mapped to area (proportional encoding per KB).

    Args:
        size:         list of values for bubble size (proportional to area)
        labels:       list of point labels for hover
        color_values: optional list of numeric values for colour encoding
    """
    # Normalise size to area (not radius) — KB requirement
    import math
    max_size = max(abs(s) for s in size) if size else 1
    scaled = [math.sqrt(abs(s) / max_size) * 40 + 6 for s in size]

    hover = labels if labels else [f"({xi}, {yi}, size={si})" for xi, yi, si in zip(x, y, size)]

    if color_values:
        marker = dict(
            size=scaled,
            color=color_values,
            colorscale=[[0, "#D6E4F4"], [0.5, AZURE_1], [1, "#2D5A8E"]],
            opacity=0.7,
            line=dict(color="white", width=1),
        )
    else:
        marker = dict(
            size=scaled, color=AZURE_1, opacity=0.7,
            line=dict(color="white", width=1),
        )

    fig = go.Figure(go.Scatter(
        x=x, y=y, mode="markers",
        marker=marker,
        text=hover,
        hovertemplate="%{text}<extra></extra>",
    ))

    fig.update_layout(_base_layout())
    return _chart(title=title, subtitle=subtitle, figure=fig)
