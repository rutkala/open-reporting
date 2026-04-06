"""
Line and area chart variants — Power BI naming convention.
KB reference: team/analytics/visualization/charts/line.md

Rules applied:
  - line_shape="linear" — no smoothing (KB: straight lines = accurate)
  - line.width=2 minimum (KB: 2–3px)
  - Area fill opacity 0.25 — visible without occlusion
  - Area/stacked area always starts at zero (KB requirement)

y_measure (optional Measure):
  When provided, sets y-axis title, tickformat and ticksuffix on all variants.
"""
import plotly.graph_objects as go

from products.visuals.lib.theme import COLORWAY, SLATE_1, SUBTEXT
from products.visuals.components import PLOT_H, _plotly_layout, _chart


def _rgba(hex_color: str, alpha: float) -> str:
    r, g, b = int(hex_color[1:3], 16), int(hex_color[3:5], 16), int(hex_color[5:7], 16)
    return f"rgba({r},{g},{b},{alpha})"


def _legend(series):
    return (
        [(s["name"], s.get("color", COLORWAY[i % len(COLORWAY)])) for i, s in enumerate(series)]
        if len(series) > 1 else None
    )


def line(title, x, series, subtitle="", markers=True, reference=None, y_measure=None):
    """
    Line chart — single or multi-series trend over time.

    Args:
        series:    list of {"name": str, "y": list, "color": str (optional)}
        markers:   show data point markers (recommended for clarity)
        reference: {"value": float, "label": str} — horizontal reference line
        y_measure: when provided, sets y-axis title, tickformat and ticksuffix
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
    layout = _plotly_layout()
    if y_measure is not None:
        y_measure.apply_to_yaxis(layout["yaxis"])
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
    return _chart(title=title, subtitle=subtitle, legend_items=_legend(series), figure=fig)


def area(title, x, series, subtitle="", opacity=0.25, y_measure=None):
    """
    Area chart — emphasises volume/magnitude.
    Multiple series = overlapping areas (use stacked_area for part-to-whole).
    Always starts at zero (KB requirement).

    Args:
        series:    list of {"name": str, "y": list, "color": str (optional)}
        opacity:   fill opacity 0–1 (default 0.25)
        y_measure: when provided, sets y-axis title, tickformat and ticksuffix
    """
    fig = go.Figure()
    for i, s in enumerate(series):
        color = s.get("color", COLORWAY[i % len(COLORWAY)])
        fig.add_trace(go.Scatter(
            x=x, y=s["y"], name=s["name"], mode="lines",
            fill="tozeroy",
            fillcolor=_rgba(color, opacity),
            line=dict(color=color, width=2, shape="linear"),
        ))
    layout = _plotly_layout(yaxis={"rangemode": "tozero"})
    if y_measure is not None:
        y_measure.apply_to_yaxis(layout["yaxis"])
    fig.update_layout(layout)
    return _chart(title=title, subtitle=subtitle, legend_items=_legend(series), figure=fig)


def stacked_area(title, x, series, subtitle="", y_measure=None):
    """
    Stacked area chart — part-to-whole over time.
    Most important segment first (rendered at bottom, per KB).

    Args:
        series:    list of {"name": str, "y": list, "color": str (optional)}
        y_measure: when provided, sets y-axis title, tickformat and ticksuffix
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
    layout = _plotly_layout(yaxis={"rangemode": "tozero"})
    if y_measure is not None:
        y_measure.apply_to_yaxis(layout["yaxis"])
    fig.update_layout(layout)
    return _chart(title=title, subtitle=subtitle, legend_items=_legend(series), figure=fig)


def pct_stacked_area(title, x, series, subtitle="", y_measure=None):
    """
    100% normalised stacked area — composition over time, total always = 100%.

    Args:
        series:    list of {"name": str, "y": list, "color": str (optional)}
        y_measure: when provided, sets y-axis title, tickformat and ticksuffix
                   (note: 100% stacked axes are always %, y_measure overrides)
    """
    fig = go.Figure()
    for i, s in enumerate(series):
        color = s.get("color", COLORWAY[i % len(COLORWAY)])
        fig.add_trace(go.Scatter(
            x=x, y=s["y"], name=s["name"], mode="lines",
            stackgroup="one",
            groupnorm="percent",
            fillcolor=_rgba(color, 0.6),
            line=dict(color=color, width=1.5, shape="linear"),
        ))
    layout = _plotly_layout(yaxis={"rangemode": "tozero", "ticksuffix": "%", "range": [0, 100]})
    if y_measure is not None:
        y_measure.apply_to_yaxis(layout["yaxis"])
    fig.update_layout(layout)
    return _chart(title=title, subtitle=subtitle, legend_items=_legend(series), figure=fig)
