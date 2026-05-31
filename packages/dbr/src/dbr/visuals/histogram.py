"""histogram — Distribution chart (histogram of metric values across dimension values).

Queries a metric grouped by a dimension, then plots the distribution of the
resulting aggregated values — e.g. "Histogram of unemployment rates across
27 EU countries" shows how values cluster, not time evolution.

Mandatory encoding:
  x: { metric: <name> }         — the metric whose distribution to show
  color: { dimension: <name> }  — group-by dimension (one data point per value)

Optional:
  options.nbins:        int     — number of histogram bins (Plotly auto if absent)
  options.cumulative:   bool    — cumulative distribution (default: false)
  options.orientation:  "v"|"h" — vertical (default) or horizontal bars
  options.height:       int     — chart height override
  options.y_format:     str     — y-axis tick format
  options.x_format:     str     — x-axis tick format
"""
from dash import dcc, html
import plotly.graph_objects as go

from dbr.semantic import semantic_query_data
from dbr.theme import (
    AZURE_1, BG_SURFACE, BAR_CHART_HEIGHT,
    CARD_RADIUS, CARD_SHADOW,
)
from dbr.visuals._encoding import (
    dimension_column_name, group_by_from_channels, parse_encoding,
)
from dbr.visuals._render import chart_with_optional_table, _TABLE_OPTION_SCHEMA

SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["type", "encoding"],
    "properties": {
        "type": {"const": "histogram"},
        "title":    {"type": "string"},
        "subtitle": {"type": "string"},
        "encoding": {
            "type": "object",
            "required": ["x", "color"],
            "additionalProperties": False,
            "properties": {
                "x":     {"type": "object"},
                "color": {"type": "object"},
            },
        },
        "filter": {"type": "object"},
        "options": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "nbins":       {"type": "integer", "minimum": 2, "maximum": 200},
                "cumulative":  {"type": "boolean"},
                "orientation": {"enum": ["v", "h"]},
                "height":      {"type": "integer", "minimum": 100, "maximum": 2000},
                "y_format":    {"type": "string"},
                "x_format":    {"type": "string"},
                "download": {"type": "boolean", "description": "Render a CSV download link below the chart."},
                "table": _TABLE_OPTION_SCHEMA,
            },
        },
    },
}

_CARD_STYLE = {
    "background": BG_SURFACE, "borderRadius": CARD_RADIUS, "boxShadow": CARD_SHADOW,
    "padding": "16px", "height": "100%", "boxSizing": "border-box",
}


def histogram(*, encoding: dict, filter: dict | None = None, options: dict | None = None) -> html.Div:
    enc = parse_encoding(encoding)
    opts = options or {}

    if not (enc.x and enc.x.metric):
        raise ValueError("histogram: encoding.x must bind a metric")
    if not (enc.color and enc.color.dimension):
        raise ValueError("histogram: encoding.color must bind a dimension (one value per category)")

    metric   = enc.x.metric
    group_by = group_by_from_channels(enc.color)

    df = semantic_query_data(metric, group_by=group_by, filter=filter)
    if df.empty:
        return html.Div("No data", style=_CARD_STYLE)

    nbins       = opts.get("nbins")
    cumulative  = opts.get("cumulative", False)
    orientation = opts.get("orientation", "v")
    height      = opts.get("height", int(str(BAR_CHART_HEIGHT).rstrip("px")))

    values = df[metric]
    hist_kwargs = dict(
        marker=dict(color=AZURE_1),
        cumulative=dict(enabled=cumulative),
    )
    if nbins:
        hist_kwargs["nbinsx" if orientation == "v" else "nbinsy"] = nbins

    if orientation == "h":
        fig = go.Figure(go.Histogram(y=values, orientation="h", **hist_kwargs))
    else:
        fig = go.Figure(go.Histogram(x=values, **hist_kwargs))

    fig.update_layout(height=height, xaxis_title="", yaxis_title="", showlegend=False)
    if opts.get("y_format"):
        fig.update_layout(yaxis_tickformat=opts["y_format"])
    if opts.get("x_format"):
        fig.update_layout(xaxis_tickformat=opts["x_format"])

    return chart_with_optional_table(fig, df, opts, _CARD_STYLE)
