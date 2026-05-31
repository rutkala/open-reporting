"""box — Box plot (box-and-whisker) for distribution analysis.

Queries a metric grouped by a category dimension, then renders one box per
category showing median, IQR, and outliers. Useful for comparing distributions
across groups rather than single aggregate values.

Because MetricFlow always returns aggregated values (one row per group), this
visual is most meaningful when used with a fine-grained grouping dimension that
produces many data points — e.g. metric per country per year plotted as boxes
grouped by region.

Mandatory encoding:
  y: { metric:    <name> }        — values for the distribution
  x: { dimension: <name> }        — grouping category (one box per value)

Optional:
  options.points:       "all" | "outliers" | "suspectedoutliers" | false
                        — show underlying data points (default: "outliers")
  options.boxmean:      bool | "sd"  — overlay mean marker (default: false)
  options.orientation:  "v" | "h"    — vertical (default) or horizontal
  options.height:       int          — chart height override
  options.y_format:     str          — Plotly tickformat for value axis
"""
from dash import dcc, html
import plotly.graph_objects as go

from dbr.semantic import semantic_query_data
from dbr.theme import (
    AZURE_1, BG_SURFACE, BAR_CHART_HEIGHT,
    CARD_RADIUS, CARD_SHADOW, COLORWAY,
)
from dbr.visuals._encoding import (
    postprocess_time_columns,
    dimension_column_name, group_by_from_channels, parse_encoding,
)
from dbr.visuals._render import (
    apply_axis_options, chart_with_optional_table,
    format_value, _AXIS_OPTIONS_SCHEMA, _FORMAT_OPTION_SCHEMA, _TABLE_OPTION_SCHEMA,
)

SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["type", "encoding"],
    "properties": {
        "type": {"const": "box"},
        "title":    {"type": "string"},
        "subtitle": {"type": "string"},
        "encoding": {
            "type": "object",
            "required": ["y", "x"],
            "additionalProperties": False,
            "properties": {
                "x": {"type": "object"},
                "y": {"type": "object"},
            },
        },
        "filter": {"type": "object"},
        "options": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "points": {
                    "oneOf": [
                        {"enum": ["all", "outliers", "suspectedoutliers"]},
                        {"type": "boolean", "enum": [False]},
                    ],
                },
                "boxmean":     {"oneOf": [{"type": "boolean"}, {"enum": ["sd"]}]},
                "orientation": {"enum": ["v", "h"]},
                "height":      {"type": "integer", "minimum": 100, "maximum": 2000},
                "y_format":    {"type": "string"},
                "download": {"type": "boolean", "description": "Render a CSV download link below the chart."},
                **_AXIS_OPTIONS_SCHEMA,
                **_FORMAT_OPTION_SCHEMA,
                "table": _TABLE_OPTION_SCHEMA,
            },
        },
    },
}

_CARD_STYLE = {
    "background": BG_SURFACE, "borderRadius": CARD_RADIUS, "boxShadow": CARD_SHADOW,
    "padding": "16px", "height": "100%", "boxSizing": "border-box",
}


def box(*, encoding: dict, filter: dict | None = None, options: dict | None = None) -> html.Div:
    enc  = parse_encoding(encoding)
    opts = options or {}

    if not (enc.y and enc.y.metric):
        raise ValueError("box: encoding.y must bind a metric")
    if not (enc.x and enc.x.dimension):
        raise ValueError("box: encoding.x must bind a dimension")

    metric   = enc.y.metric if isinstance(enc.y.metric, str) else enc.y.metrics[0]
    x_col    = dimension_column_name(enc.x)
    group_by = group_by_from_channels(enc.x)

    df = semantic_query_data(metric, group_by=group_by, filter=filter, order=x_col)
    if df.empty:
        return html.Div("No data", style=_CARD_STYLE)
    df = postprocess_time_columns(df, enc)

    points      = opts.get("points", "outliers")
    boxmean     = opts.get("boxmean", False)
    orientation = opts.get("orientation", "v")
    height      = opts.get("height", int(str(BAR_CHART_HEIGHT).rstrip("px")))

    # One box per category — each category gets its own trace so colours rotate
    fig = go.Figure()
    categories = df[x_col].unique()
    for i, cat in enumerate(categories):
        sub = df[df[x_col] == cat]
        color = list(COLORWAY)[i % len(list(COLORWAY))]
        if orientation == "h":
            fig.add_trace(go.Box(
                x=sub[metric], name=str(cat),
                boxpoints=points, boxmean=boxmean,
                marker_color=color, orientation="h",
            ))
        else:
            fig.add_trace(go.Box(
                y=sub[metric], name=str(cat),
                boxpoints=points, boxmean=boxmean,
                marker_color=color,
            ))

    fig.update_layout(
        height=height, xaxis_title="", yaxis_title="", showlegend=False,
    )
    if opts.get("y_format"):
        axis_key = "xaxis_tickformat" if orientation == "h" else "yaxis_tickformat"
        fig.update_layout(**{axis_key: opts["y_format"]})

    apply_axis_options(fig, opts)
    return chart_with_optional_table(fig, df, opts, _CARD_STYLE)
