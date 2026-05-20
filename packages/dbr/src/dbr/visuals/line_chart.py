"""Line chart — time series of a metric over the last N periods.

Uses ``semantic_query_history`` to pull the last N years of a metric and
renders a Plotly line+marker trace. The 'teal' Plotly template (registered
by ``theme``) handles all colours, fonts, and axis styling automatically.

YAML usage:

    type:   line_chart
    metric: fiscal_balance
    filter:
      geo: PL
    # optional behaviour overrides:
    # years: 10
"""
from dash import dcc, html
import plotly.graph_objects as go

from dbr.semantic import semantic_query_history
from dbr.theme import (
    BG_SURFACE,
    CARD_RADIUS,
    CARD_SHADOW,
    LINE_CHART_HEIGHT,
    LINE_CHART_HISTORY_YEARS,
    LINE_CHART_LINE_WIDTH,
    LINE_CHART_MARKER_SIZE,
)

DEFAULTS = {
    "years": LINE_CHART_HISTORY_YEARS,
}

SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["type", "metric"],
    "properties": {
        "type":   {"const": "line_chart"},
        "metric": {"type": "string"},
        "filter": {"type": "object"},
        "years":  {"type": "integer", "minimum": 1, "maximum": 100},
    },
}

_CARD_STYLE = {
    "background":   BG_SURFACE,
    "borderRadius": CARD_RADIUS,
    "boxShadow":    CARD_SHADOW,
    "padding":      "16px",
    "height":       "100%",
    "boxSizing":    "border-box",
}


def line_chart(metric: str, *, filter: dict | None = None, **overrides) -> html.Div:
    """Render a line chart of ``metric`` over the last ``years`` periods.

    Picks up the metric's label and unit from the semantic-layer metadata
    so the chart title and y-axis are filled in automatically.
    """
    cfg = {**DEFAULTS, **overrides}
    history = semantic_query_history(metric, filter=filter, n=cfg["years"])

    if not history:
        return html.Div("No data", style=_CARD_STYLE)

    # Reverse to chronological order (semantic_query_history returns newest-first)
    history = list(reversed(history))

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=[r.period for r in history],
        y=[r.value  for r in history],
        mode="lines+markers",
        line=dict(width=LINE_CHART_LINE_WIDTH),
        marker=dict(size=LINE_CHART_MARKER_SIZE),
        name=history[0].label,
        hovertemplate="%{x}: %{y}<extra></extra>",
    ))
    fig.update_layout(
        title=history[0].label,
        xaxis_title="",
        yaxis_title=history[0].unit_str or "",
        height=int(str(LINE_CHART_HEIGHT).rstrip("px")),
    )

    return html.Div(
        style=_CARD_STYLE,
        children=dcc.Graph(figure=fig, config={"displayModeBar": False}),
    )
