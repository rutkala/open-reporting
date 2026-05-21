"""area — Area chart (line with filled region below).

Mandatory encoding:
  x:  { dimension: <name>, granularity: <grain> }
  y:  { metric:    <name> }

Optional:
  color:   { dimension: <name> }     — multi-series stacked
  options.opacity:  float 0..1       — area fill opacity
  options.stack:    bool             — stack series (default true when color present)
"""
from dash import dcc, html
import plotly.graph_objects as go

from dbr.semantic import semantic_query_data
from dbr.theme import (
    AREA_CHART_HEIGHT, AREA_CHART_LINE_WIDTH, AREA_CHART_OPACITY,
    BG_SURFACE, CARD_RADIUS, CARD_SHADOW,
)
from dbr.visuals._encoding import (
    dimension_column_name, group_by_from_channels, parse_encoding,
)

SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["type", "encoding"],
    "properties": {
        "type": {"const": "area"},
        "encoding": {
            "type": "object",
            "required": ["x", "y"],
            "additionalProperties": False,
            "properties": {
                "x":     {"type": "object"},
                "y":     {"type": "object"},
                "color": {"type": "object"},
            },
        },
        "filter":  {"type": "object"},
        "options": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "opacity": {"type": "number", "minimum": 0.0, "maximum": 1.0},
                "stack":   {"type": "boolean"},
            },
        },
    },
}

_CARD_STYLE = {
    "background": BG_SURFACE, "borderRadius": CARD_RADIUS, "boxShadow": CARD_SHADOW,
    "padding": "16px", "height": "100%", "boxSizing": "border-box",
}


def area(*, encoding: dict, filter: dict | None = None, options: dict | None = None) -> html.Div:
    enc = parse_encoding(encoding)
    opts = options or {}

    if not (enc.x and enc.x.dimension):
        raise ValueError("area: encoding.x must bind a dimension")
    if not (enc.y and enc.y.metric):
        raise ValueError("area: encoding.y must bind a metric")

    group_by = group_by_from_channels(enc.x, enc.color)
    x_col = dimension_column_name(enc.x)
    metric = enc.y.metric

    df = semantic_query_data(metric, group_by=group_by, filter=filter, order=x_col)
    if df.empty:
        return html.Div("No data", style=_CARD_STYLE)

    opacity = opts.get("opacity", AREA_CHART_OPACITY)
    stack = opts.get("stack", True if enc.color else False)
    stackgroup = "one" if stack else None

    fig = go.Figure()
    if enc.color:
        color_col = dimension_column_name(enc.color)
        for series, sub in df.groupby(color_col):
            fig.add_trace(go.Scatter(
                x=sub[x_col], y=sub[metric], mode="lines",
                fill="tonexty" if stack else "tozeroy",
                stackgroup=stackgroup,
                opacity=opacity, line=dict(width=AREA_CHART_LINE_WIDTH),
                name=str(series),
            ))
    else:
        fig.add_trace(go.Scatter(
            x=df[x_col], y=df[metric], mode="lines",
            fill="tozeroy", opacity=opacity,
            line=dict(width=AREA_CHART_LINE_WIDTH),
        ))
    fig.update_layout(
        height=int(str(AREA_CHART_HEIGHT).rstrip("px")),
        xaxis_title="", yaxis_title="",
    )
    return html.Div(dcc.Graph(figure=fig, config={"displayModeBar": False}), style=_CARD_STYLE)
