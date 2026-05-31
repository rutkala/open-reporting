"""scatter — Scatter / Bubble chart.

Mandatory encoding:
  x: { metric: <name> }    — value on x-axis
  y: { metric: <name> }    — value on y-axis

Optional:
  color: { dimension: <name> }     — colour by category
  size:  { metric:    <name> }     — bubble size (turns scatter into bubble chart)

The grouping dimensions come from `color` (if present); the two metrics
are queried jointly. For a scatter you typically need at least one
shared dimension (e.g., a per-country point) — that's the `color` channel.
"""
from dash import dcc, html
import plotly.graph_objects as go

from dbr.semantic import semantic_query_data
from dbr.theme import BG_SURFACE, CARD_RADIUS, CARD_SHADOW
from dbr.visuals._encoding import (
    apply_annotations, _ANNOTATIONS_OPTION_SCHEMA,
    dimension_column_name, group_by_from_channels, parse_encoding,
)
from dbr.visuals._render import chart_with_optional_table, _TABLE_OPTION_SCHEMA

SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["type", "encoding"],
    "properties": {
        "type": {"const": "scatter"},
        "encoding": {
            "type": "object",
            "required": ["x", "y"],
            "additionalProperties": False,
            "properties": {
                "x":     {"type": "object"},
                "y":     {"type": "object"},
                "color": {"type": "object"},
                "size":  {"type": "object"},
            },
        },
        "title":    {"type": "string"},
        "subtitle": {"type": "string"},
        "filter":  {"type": "object"},
        "options": {"type": "object", "additionalProperties": True},
    },
}

_CARD_STYLE = {
    "background": BG_SURFACE, "borderRadius": CARD_RADIUS, "boxShadow": CARD_SHADOW,
    "padding": "16px", "height": "100%", "boxSizing": "border-box",
}


def scatter(*, encoding: dict, filter: dict | None = None, options: dict | None = None) -> html.Div:
    enc = parse_encoding(encoding)
    opts = options or {}

    if not (enc.x and enc.x.metric):
        raise ValueError("scatter: encoding.x must bind a metric")
    if not (enc.y and enc.y.metric):
        raise ValueError("scatter: encoding.y must bind a metric")

    # For scatter we usually want one point per category — the `color` channel
    # provides that dimension. Without `color`, we'd be plotting one point per
    # (cross-product of all dimensions), which usually isn't what's wanted.
    group_by = group_by_from_channels(enc.color)
    if not group_by:
        raise ValueError("scatter: encoding needs a `color` channel (dimension) — one point per category")

    color_col = dimension_column_name(enc.color)

    # Query each metric separately and merge — MetricFlow doesn't return two
    # metrics in one call unless we ask explicitly. For now we query the x-metric
    # and y-metric individually and merge on the color dimension.
    df_x = semantic_query_data(enc.x.metric, group_by=group_by, filter=filter)
    df_y = semantic_query_data(enc.y.metric, group_by=group_by, filter=filter)
    if df_x.empty or df_y.empty:
        return html.Div("No data", style=_CARD_STYLE)

    df = df_x.merge(df_y, on=color_col, how="inner")
    if enc.size and enc.size.metric:
        df_s = semantic_query_data(enc.size.metric, group_by=group_by, filter=filter)
        df = df.merge(df_s, on=color_col, how="inner")
        size_values = df[enc.size.metric]
    else:
        size_values = None

    fig = go.Figure(go.Scatter(
        x=df[enc.x.metric], y=df[enc.y.metric], mode="markers+text",
        text=df[color_col], textposition="top center",
        marker=dict(size=size_values if size_values is not None else 12,
                    sizemode="area", sizeref=2.0 * size_values.max() / 40**2 if size_values is not None else None),
    ))
    fig.update_layout(
        height=400, xaxis_title=enc.x.metric, yaxis_title=enc.y.metric,
    )
    apply_annotations(fig, opts)
    return chart_with_optional_table(fig, df, opts, _CARD_STYLE)
