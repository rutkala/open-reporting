"""column — Vertical bar chart (Power BI's "Column chart").

Mandatory encoding:
  x:  { dimension: <name> }      — category on x-axis
  y:  { metric:    <name> }      — value on y-axis

Optional:
  color: { dimension: <name> }   — splits into grouped or stacked bars
  options.stack: bool            — stack (true) or group (false) when `color` is set
"""
from dash import dcc, html
import plotly.graph_objects as go

from dbr.semantic import semantic_query_data
from dbr.theme import (
    BG_SURFACE, BAR_CHART_BARGAP, BAR_CHART_HEIGHT,
    CARD_RADIUS, CARD_SHADOW,
)
from dbr.visuals._encoding import (
    apply_reference_lines, postprocess_time_columns,
    dimension_column_name, group_by_from_channels, parse_encoding,
)

SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["type", "encoding"],
    "properties": {
        "type": {"const": "column"},
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
                "reference_lines": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "required": ["value"],
                        "properties": {
                            "value": {"type": "number"},
                            "label": {"type": "string"},
                            "color": {"type": "string"},
                        },
                    },
                },
            },
        },
    },
}

_CARD_STYLE = {
    "background": BG_SURFACE, "borderRadius": CARD_RADIUS, "boxShadow": CARD_SHADOW,
    "padding": "16px", "height": "100%", "boxSizing": "border-box",
}


def column(*, encoding: dict, filter: dict | None = None, options: dict | None = None) -> html.Div:
    enc = parse_encoding(encoding)
    opts = options or {}

    if not (enc.x and enc.x.dimension):
        raise ValueError("column: encoding.x must bind a dimension")
    if not (enc.y and enc.y.metric):
        raise ValueError("column: encoding.y must bind a metric")

    group_by = group_by_from_channels(enc.x, enc.color)
    x_col = dimension_column_name(enc.x)
    metric = enc.y.metric

    df = semantic_query_data(metric, group_by=group_by, filter=filter, order=x_col)
    if df.empty:
        return html.Div("No data", style=_CARD_STYLE)
    df = postprocess_time_columns(df, enc)

    fig = go.Figure()
    if enc.color:
        color_col = dimension_column_name(enc.color)
        for series, sub in df.groupby(color_col):
            fig.add_trace(go.Bar(x=sub[x_col], y=sub[metric], name=str(series)))
        fig.update_layout(barmode="stack" if opts.get("stack") else "group")
    else:
        fig.add_trace(go.Bar(x=df[x_col], y=df[metric]))
    fig.update_layout(
        height=int(str(BAR_CHART_HEIGHT).rstrip("px")),
        bargap=BAR_CHART_BARGAP, xaxis_title="", yaxis_title="",
    )
    apply_reference_lines(fig, opts, axis="y")
    return html.Div(dcc.Graph(figure=fig, config={"displayModeBar": False}), style=_CARD_STYLE)
