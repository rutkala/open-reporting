"""
Distribution chart variants.
KB reference: team/analytics/visualization/charts/scatter.md (distribution section)

histogram  — frequency distribution of a single variable
box_plot   — distribution summary: median, IQR, outliers
violin_plot — distribution shape + box summary
"""
import plotly.graph_objects as go

from products.visuals.lib.theme import (
    COLORWAY, AZURE_1, AZURE_PALE, BORDER, GRID, SUBTEXT, TEXT, ZERO_LINE, FONT_FAMILY,
)
from products.visuals.components import PLOT_H, MARGIN_L, MARGIN_R, MARGIN_T, MARGIN_B, _chart


def _rgba(hex_color: str, alpha: float = 0.25) -> str:
    """Convert #RRGGBB to rgba(R,G,B,alpha) — go.Box/Violin reject 8-digit hex."""
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"


def _base_layout(**kw):
    return {
        "template": "teal",
        "height": PLOT_H,
        "margin": dict(l=MARGIN_L, r=MARGIN_R, t=MARGIN_T, b=MARGIN_B),
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": dict(family=FONT_FAMILY, color=TEXT, size=12),
        "xaxis": dict(showgrid=False, showline=True, linecolor=BORDER,
                      tickfont=dict(size=11, color=SUBTEXT), zerolinecolor=ZERO_LINE),
        "yaxis": dict(showgrid=True, gridcolor=GRID, showline=False,
                      tickfont=dict(size=11, color=SUBTEXT), zerolinecolor=ZERO_LINE),
        "showlegend": False,
        "hovermode": "x",
        **kw,
    }


def histogram(title, x, subtitle="", nbins=None, color=None, x_label=""):
    """
    Frequency distribution of a single continuous variable.

    Args:
        x:      list of numeric values
        nbins:  number of bins (auto if None)
        color:  bar colour (default AZURE_1)
        x_label: x-axis label
    """
    bar_color = color or AZURE_1
    fig = go.Figure(go.Histogram(
        x=x,
        nbinsx=nbins,
        marker_color=bar_color,
        marker_line=dict(color="white", width=0.5),
        opacity=0.85,
        hovertemplate="Zakres: %{x}<br>Liczba: %{y}<extra></extra>",
    ))
    layout = _base_layout()
    if x_label:
        layout["xaxis"]["title"] = dict(text=x_label, font=dict(size=11, color=SUBTEXT))
    layout["yaxis"]["title"] = dict(text="Liczba", font=dict(size=11, color=SUBTEXT))
    fig.update_layout(layout)
    return _chart(title=title, subtitle=subtitle, figure=fig)


def box_plot(title, data, subtitle="", show_points=True):
    """
    Box plot — distribution summary: median, IQR, whiskers, outliers.

    Args:
        data:        dict of {label: [values]} or list of {"name": str, "y": list}
        show_points: overlay individual data points (jittered)
    """
    if isinstance(data, dict):
        items = [{"name": k, "y": v} for k, v in data.items()]
    else:
        items = data

    fig = go.Figure()
    for i, item in enumerate(items):
        color = item.get("color", COLORWAY[i % len(COLORWAY)])
        fig.add_trace(go.Box(
            y=item["y"], name=item["name"],
            marker_color=color,
            line_color=color,
            fillcolor=_rgba(color, 0.25),
            boxpoints="all" if show_points else "outliers",
            jitter=0.3,
            pointpos=0,
            marker=dict(size=4, opacity=0.5),
        ))

    layout = _base_layout()
    layout["xaxis"].update(showgrid=False, showline=False)
    layout["yaxis"].update(showgrid=True)
    layout["hovermode"] = "closest"
    if len(items) > 1:
        layout["showlegend"] = False
    fig.update_layout(layout)

    legend = [(item["name"], item.get("color", COLORWAY[i % len(COLORWAY)])) for i, item in enumerate(items)] if len(items) > 1 else None
    return _chart(title=title, subtitle=subtitle, legend_items=legend, figure=fig)


def violin_plot(title, data, subtitle="", show_box=True):
    """
    Violin plot — distribution shape with optional embedded box.

    Args:
        data:     dict of {label: [values]} or list of {"name": str, "y": list}
        show_box: embed box plot inside violin
    """
    if isinstance(data, dict):
        items = [{"name": k, "y": v} for k, v in data.items()]
    else:
        items = data

    fig = go.Figure()
    for i, item in enumerate(items):
        color = item.get("color", COLORWAY[i % len(COLORWAY)])
        fig.add_trace(go.Violin(
            y=item["y"], name=item["name"],
            line_color=color,
            fillcolor=_rgba(color, 0.25),
            box_visible=show_box,
            meanline_visible=True,
            meanline_color=color,
            points="outliers",
            marker=dict(size=4, opacity=0.5, color=color),
        ))

    layout = _base_layout()
    layout["xaxis"].update(showgrid=False, showline=False)
    layout["hovermode"] = "closest"
    fig.update_layout(layout)

    legend = [(item["name"], item.get("color", COLORWAY[i % len(COLORWAY)])) for i, item in enumerate(items)] if len(items) > 1 else None
    return _chart(title=title, subtitle=subtitle, legend_items=legend, figure=fig)
