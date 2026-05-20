"""Area chart — line_chart with a filled area under the curve.

Same data binding as line_chart (semantic_query_history). Useful when you
want to emphasise magnitude or cumulative shape over time rather than the
exact trajectory.

YAML usage:

    type:   area_chart
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
    AREA_CHART_HEIGHT,
    AREA_CHART_HISTORY_YEARS,
    AREA_CHART_LINE_WIDTH,
    AREA_CHART_OPACITY,
    BG_SURFACE,
    CARD_RADIUS,
    CARD_SHADOW,
)

DEFAULTS = {
    "years": AREA_CHART_HISTORY_YEARS,
}

SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["type", "metric"],
    "properties": {
        "type":   {"const": "area_chart"},
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


def area_chart(metric: str, *, filter: dict | None = None, **overrides) -> html.Div:
    """Render ``metric`` as an area chart over the last ``years`` periods."""
    cfg = {**DEFAULTS, **overrides}
    history = semantic_query_history(metric, filter=filter, n=cfg["years"])

    if not history:
        return html.Div("No data", style=_CARD_STYLE)

    history = list(reversed(history))

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=[r.period for r in history],
        y=[r.value  for r in history],
        mode="lines",
        fill="tozeroy",
        opacity=AREA_CHART_OPACITY,
        line=dict(width=AREA_CHART_LINE_WIDTH),
        name=history[0].label,
        hovertemplate="%{x}: %{y}<extra></extra>",
    ))
    fig.update_layout(
        title=history[0].label,
        xaxis_title="",
        yaxis_title=history[0].unit_str or "",
        height=int(str(AREA_CHART_HEIGHT).rstrip("px")),
    )

    return html.Div(
        style=_CARD_STYLE,
        children=dcc.Graph(figure=fig, config={"displayModeBar": False}),
    )
