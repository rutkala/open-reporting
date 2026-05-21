"""bar — Horizontal bar chart.

Mandatory encoding:
  x:  { metric:    <name> }     — value on x-axis
  y:  { dimension: <name> }     — category on y-axis

Optional:
  color: { dimension: <name> }  — splits into grouped or stacked bars
  options.stack: bool           — stack (true) or group (false) when `color` is set
"""
from dash import dcc, html
import plotly.graph_objects as go

from dbr.semantic import semantic_query_data
from dbr.theme import (
    BG_SURFACE, BAR_CHART_BARGAP, BAR_CHART_HEIGHT,
    CARD_RADIUS, CARD_SHADOW,
)
from dbr.visuals._encoding import (
    dimension_column_name, group_by_from_channels, parse_encoding,
)

SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["type", "encoding"],
    "properties": {
        "type": {"const": "bar"},
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
                "stack": {"type": "boolean"},
            },
        },
    },
}

_CARD_STYLE = {
    "background": BG_SURFACE, "borderRadius": CARD_RADIUS, "boxShadow": CARD_SHADOW,
    "padding": "16px", "height": "100%", "boxSizing": "border-box",
}


def bar(*, encoding: dict, filter: dict | None = None, options: dict | None = None) -> html.Div:
    enc = parse_encoding(encoding)
    opts = options or {}

    if not (enc.x and enc.x.metric):
        raise ValueError("bar: encoding.x must bind a metric (use `column` for vertical bars)")
    if not (enc.y and enc.y.dimension):
        raise ValueError("bar: encoding.y must bind a dimension")

    group_by = group_by_from_channels(enc.y, enc.color)
    y_col = dimension_column_name(enc.y)
    metric = enc.x.metric

    df = semantic_query_data(metric, group_by=group_by, filter=filter, order=y_col)
    if df.empty:
        return html.Div("No data", style=_CARD_STYLE)

    fig = go.Figure()
    if enc.color:
        color_col = dimension_column_name(enc.color)
        for series, sub in df.groupby(color_col):
            fig.add_trace(go.Bar(x=sub[metric], y=sub[y_col], orientation="h", name=str(series)))
        fig.update_layout(barmode="stack" if opts.get("stack") else "group")
    else:
        fig.add_trace(go.Bar(x=df[metric], y=df[y_col], orientation="h"))
    fig.update_layout(
        height=int(str(BAR_CHART_HEIGHT).rstrip("px")),
        bargap=BAR_CHART_BARGAP, xaxis_title="", yaxis_title="",
    )
    return html.Div(dcc.Graph(figure=fig, config={"displayModeBar": False}), style=_CARD_STYLE)
