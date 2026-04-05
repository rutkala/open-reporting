"""
Line and area chart variants.
KB reference: team/analytics/visualization/charts/line.md

Rules applied:
- line_shape="linear" enforced — no smoothing (KB: straight lines = accurate)
- line.width=2 minimum (KB: 2–3px)
- Area fill opacity 0.25 — visible without occlusion
- Area always starts at zero (KB: 0 baseline required)
- Max 3–4 lines recommended (enforced by convention, not code)
"""
import plotly.graph_objects as go

from products.visuals.lib.theme import COLORWAY, SLATE_1, SUBTEXT
from products.visuals.components import PLOT_H, _plotly_layout, _chart


def _rgba(hex_color: str, alpha: float) -> str:
    r = int(hex_color[1:3], 16)
    g = int(hex_color[3:5], 16)
    b = int(hex_color[5:7], 16)
    return f"rgba({r},{g},{b},{alpha})"


def line_single(title, x, y, name="", subtitle="", markers=True, reference=None):
    """
    Single-series line chart — trend over time.

    Args:
        y:         list of numeric values
        name:      series name (for hover tooltip)
        markers:   show data point markers (recommended for clarity)
        reference: {"value": float, "label": str} — horizontal reference line
    """
    color = COLORWAY[0]
    fig = go.Figure(go.Scatter(
        x=x, y=y, name=name, mode="lines+markers" if markers else "lines",
        line=dict(color=color, width=2, shape="linear"),
        marker=dict(size=5, color=color),
    ))

    layout = _plotly_layout()
    if reference:
        layout["shapes"] = [dict(
            type="line", x0=x[0], x1=x[-1],
            y0=reference["value"], y1=reference["value"],
            line=dict(color=SLATE_1, width=1.5, dash="dash"),
        )]
        layout["annotations"] = [dict(
            x=x[-1], y=reference["value"],
            text=reference.get("label", ""), showarrow=False,
            font=dict(size=11, color=SLATE_1), xanchor="right", yanchor="bottom",
        )]
    fig.update_layout(layout)
    return _chart(title=title, subtitle=subtitle, figure=fig)


def line_multi(title, x, series, subtitle="", markers=True):
    """
    Multi-series line chart — up to 4 lines for comparison.

    Args:
        series: list of {"name": str, "y": list, "color": str (optional)}
        markers: show data point markers
    """
    fig = go.Figure()
    for i, s in enumerate(series):
        color = s.get("color", COLORWAY[i % len(COLORWAY)])
        fig.add_trace(go.Scatter(
            x=x, y=s["y"], name=s["name"],
            mode="lines+markers" if markers else "lines",
            line=dict(color=color, width=2, shape="linear"),
            marker=dict(size=5, color=color),
        ))
    fig.update_layout(_plotly_layout())

    legend = [(s["name"], s.get("color", COLORWAY[i % len(COLORWAY)])) for i, s in enumerate(series)]
    return _chart(title=title, subtitle=subtitle, legend_items=legend, figure=fig)


def line_area(title, x, y, name="", subtitle="", opacity=0.25):
    """
    Single-series area chart — emphasises volume/magnitude.
    Always starts at zero (KB requirement).

    Args:
        opacity: fill opacity 0–1 (default 0.25)
    """
    color = COLORWAY[0]
    fig = go.Figure(go.Scatter(
        x=x, y=y, name=name, mode="lines",
        fill="tozeroy",
        fillcolor=_rgba(color, opacity),
        line=dict(color=color, width=2, shape="linear"),
    ))
    fig.update_layout(_plotly_layout(yaxis={"rangemode": "tozero"}))
    return _chart(title=title, subtitle=subtitle, figure=fig)


def line_area_stacked(title, x, series, subtitle=""):
    """
    Stacked area chart — part-to-whole over time.
    Most important segment should be first in series list (rendered at bottom).

    Args:
        series: list of {"name": str, "y": list, "color": str (optional)}
    """
    fig = go.Figure()
    for i, s in enumerate(series):
        color = s.get("color", COLORWAY[i % len(COLORWAY)])
        fig.add_trace(go.Scatter(
            x=x, y=s["y"], name=s["name"], mode="lines",
            stackgroup="one",
            fillcolor=_rgba(color, 0.6),
            line=dict(color=color, width=1.5, shape="linear"),
        ))
    fig.update_layout(_plotly_layout(yaxis={"rangemode": "tozero"}))

    legend = [(s["name"], s.get("color", COLORWAY[i % len(COLORWAY)])) for i, s in enumerate(series)]
    return _chart(title=title, subtitle=subtitle, legend_items=legend, figure=fig)
