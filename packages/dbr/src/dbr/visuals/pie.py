"""pie — Pie / Donut chart.

Mandatory encoding:
  category: { dimension: <name> }   — which slice
  value:    { metric:    <name> }   — slice size

Optional:
  options.hole_size:  float 0..0.9  — 0 = pie, >0 = donut
"""
from dash import dcc, html
import plotly.graph_objects as go

from dbr.semantic import semantic_query_data
from dbr.theme import BG_SURFACE, CARD_RADIUS, CARD_SHADOW
from dbr.visuals._encoding import (
    dimension_column_name, group_by_from_channels, parse_encoding,
)

SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["type", "encoding"],
    "properties": {
        "type": {"const": "pie"},
        "encoding": {
            "type": "object",
            "required": ["category", "value"],
            "additionalProperties": False,
            "properties": {
                "category": {"type": "object"},
                "value":    {"type": "object"},
            },
        },
        "filter":  {"type": "object"},
        "options": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "hole_size": {"type": "number", "minimum": 0.0, "maximum": 0.9},
            },
        },
    },
}

_CARD_STYLE = {
    "background": BG_SURFACE, "borderRadius": CARD_RADIUS, "boxShadow": CARD_SHADOW,
    "padding": "16px", "height": "100%", "boxSizing": "border-box",
}


def pie(*, encoding: dict, filter: dict | None = None, options: dict | None = None) -> html.Div:
    enc = parse_encoding(encoding)
    opts = options or {}

    if not (enc.category and enc.category.dimension):
        raise ValueError("pie: encoding.category must bind a dimension")
    if not (enc.value and enc.value.metric):
        raise ValueError("pie: encoding.value must bind a metric")

    group_by = group_by_from_channels(enc.category)
    cat_col = dimension_column_name(enc.category)
    metric = enc.value.metric

    df = semantic_query_data(metric, group_by=group_by, filter=filter)
    if df.empty:
        return html.Div("No data", style=_CARD_STYLE)

    fig = go.Figure(go.Pie(
        labels=df[cat_col], values=df[metric],
        hole=opts.get("hole_size", 0.0),
        textinfo="label+percent",
    ))
    fig.update_layout(height=300)
    return html.Div(dcc.Graph(figure=fig, config={"displayModeBar": False}), style=_CARD_STYLE)
