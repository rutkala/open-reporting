"""Bar chart — same time-series data as line_chart, rendered as bars.

Uses ``semantic_query_history`` to pull the last N periods of a metric and
renders a Plotly Bar trace. The 'teal' Plotly template (registered by
``theme``) handles colours, fonts, and axis styling.

YAML usage:

    type:   bar_chart
    metric: fiscal_balance
    filter:
      geo: PL
    # Optional behaviour overrides:
    # years: 10
"""
from dash import dcc, html
import plotly.graph_objects as go

from dbr.semantic import semantic_query_history
from dbr.theme import (
    BAR_CHART_BARGAP,
    BAR_CHART_HEIGHT,
    BAR_CHART_HISTORY_YEARS,
    BG_SURFACE,
    CARD_RADIUS,
    CARD_SHADOW,
)

DEFAULTS = {
    "years": BAR_CHART_HISTORY_YEARS,
}

SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["type", "metric"],
    "properties": {
        "type":   {"const": "bar_chart"},
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


def bar_chart(metric: str, *, filter: dict | None = None, **overrides) -> html.Div:
    """Render ``metric`` as a bar chart over the last ``years`` periods."""
    cfg = {**DEFAULTS, **overrides}
    history = semantic_query_history(metric, filter=filter, n=cfg["years"])

    if not history:
        return html.Div("No data", style=_CARD_STYLE)

    history = list(reversed(history))  # newest-first → chronological

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=[r.period for r in history],
        y=[r.value  for r in history],
        name=history[0].label,
        hovertemplate="%{x}: %{y}<extra></extra>",
    ))
    fig.update_layout(
        title=history[0].label,
        xaxis_title="",
        yaxis_title=history[0].unit_str or "",
        height=int(str(BAR_CHART_HEIGHT).rstrip("px")),
        bargap=BAR_CHART_BARGAP,
    )

    return html.Div(
        style=_CARD_STYLE,
        children=dcc.Graph(figure=fig, config={"displayModeBar": False}),
    )
