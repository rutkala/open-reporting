"""heatmap — Matrix heatmap. Color encodes a metric across two dimension axes.

Mandatory encoding:
  x:     { dimension: <name>, granularity?: <grain> }  — x categories
  y:     { dimension: <name>, granularity?: <grain> }  — y categories
  color: { metric: <name> }                            — value → fill colour

Optional:
  options.colorscale:   str   — Plotly colorscale name: "Blues", "RdYlGn", "Oranges", etc.
                                Default: "Blues". Use "RdYlGn" for good/bad polarity.
  options.show_values:  bool  — render the numeric value inside each cell (default: false)
  options.value_format: str   — Python format spec for cell labels, e.g. ".1f", ".0%" (default: ".1f")
  options.height:       int   — chart height override
  options.reverse:      bool  — reverse the colorscale direction (default: false)

Typical uses: cross-tab patterns (year × month seasonality), EU country × indicator
comparison matrix, correlation tables.
"""
import pandas as pd
from dash import dcc, html
import plotly.graph_objects as go

from dbr.semantic import semantic_query_data
from dbr.theme import BG_SURFACE, BAR_CHART_HEIGHT, CARD_RADIUS, CARD_SHADOW
from dbr.visuals._encoding import (
    postprocess_time_columns,
    dimension_column_name, group_by_from_channels, parse_encoding,
)

SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["type", "encoding"],
    "properties": {
        "type": {"const": "heatmap"},
        "title":    {"type": "string"},
        "subtitle": {"type": "string"},
        "encoding": {
            "type": "object",
            "required": ["x", "y", "color"],
            "additionalProperties": False,
            "properties": {
                "x":     {"type": "object"},
                "y":     {"type": "object"},
                "color": {"type": "object"},
            },
        },
        "filter": {"type": "object"},
        "options": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "colorscale":   {"type": "string"},
                "show_values":  {"type": "boolean"},
                "value_format": {"type": "string"},
                "height":       {"type": "integer", "minimum": 100, "maximum": 2000},
                "reverse":      {"type": "boolean"},
            },
        },
    },
}

_CARD_STYLE = {
    "background": BG_SURFACE, "borderRadius": CARD_RADIUS, "boxShadow": CARD_SHADOW,
    "padding": "16px", "height": "100%", "boxSizing": "border-box",
}


def heatmap(*, encoding: dict, filter: dict | None = None, options: dict | None = None) -> html.Div:
    enc = parse_encoding(encoding)
    opts = options or {}

    if not (enc.x and enc.x.dimension):
        raise ValueError("heatmap: encoding.x must bind a dimension")
    if not (enc.y and enc.y.dimension):
        raise ValueError("heatmap: encoding.y must bind a dimension")
    if not (enc.color and enc.color.metric):
        raise ValueError("heatmap: encoding.color must bind a metric")

    x_col  = dimension_column_name(enc.x)
    y_col  = dimension_column_name(enc.y)
    metric = enc.color.metric

    group_by = group_by_from_channels(enc.x, enc.y)
    df = semantic_query_data(metric, group_by=group_by, filter=filter)
    if df.empty:
        return html.Div("No data", style=_CARD_STYLE)
    df = postprocess_time_columns(df, enc)

    # Pivot to matrix
    matrix = df.pivot_table(index=y_col, columns=x_col, values=metric, aggfunc="first")
    z      = matrix.values.tolist()
    x_vals = [str(v) for v in matrix.columns.tolist()]
    y_vals = [str(v) for v in matrix.index.tolist()]

    colorscale  = opts.get("colorscale", "Blues")
    reverse_cs  = opts.get("reverse", False)
    show_values = opts.get("show_values", False)
    val_fmt     = opts.get("value_format", ".1f")
    height      = opts.get("height", int(str(BAR_CHART_HEIGHT).rstrip("px")))

    text = None
    if show_values:
        text = [[f"{v:{val_fmt}}" if pd.notna(v) else "" for v in row] for row in z]

    fig = go.Figure(go.Heatmap(
        x=x_vals, y=y_vals, z=z,
        colorscale=colorscale,
        reversescale=reverse_cs,
        text=text,
        texttemplate="%{text}" if show_values else "",
        hovertemplate="%{y} / %{x}: %{z}<extra></extra>",
    ))
    fig.update_layout(height=height, xaxis_title="", yaxis_title="")
    return html.Div(dcc.Graph(figure=fig, config={"displayModeBar": False}), style=_CARD_STYLE)
