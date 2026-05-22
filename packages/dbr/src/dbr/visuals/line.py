"""line — Line chart. Encoding-based, multi-series via `color`.

Mandatory encoding:
  x:  { dimension: <name>, granularity: <grain> }   — time or category
  y:  { metric:    <name> }

Optional:
  color: { dimension: <name> }                       — splits into series
  options.years:     limit history (when x is time)
  options.markers:   show point markers
"""
from dash import dcc, html
import plotly.graph_objects as go

from dbr.semantic import semantic_query_data
from dbr.theme import (
    BG_SURFACE, CARD_RADIUS, CARD_SHADOW,
    LINE_CHART_HEIGHT, LINE_CHART_LINE_WIDTH, LINE_CHART_MARKER_SIZE,
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
        "type": {"const": "line"},
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
                "years":   {"type": "integer", "minimum": 1, "maximum": 100},
                "markers": {"type": "boolean"},
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


def line(*, encoding: dict, filter: dict | None = None, options: dict | None = None) -> html.Div:
    enc = parse_encoding(encoding)
    opts = options or {}

    if not (enc.x and enc.x.dimension):
        raise ValueError("line: encoding.x must bind a dimension")
    if not (enc.y and enc.y.metric):
        raise ValueError("line: encoding.y must bind a metric")

    group_by = group_by_from_channels(enc.x, enc.color)
    x_col = dimension_column_name(enc.x)
    metric = enc.y.metric

    df = semantic_query_data(
        metric, group_by=group_by, filter=filter, order=x_col,
        limit=opts.get("years") * (df_series_count(enc.color) if enc.color else 1) if opts.get("years") else None,
    )
    if df.empty:
        return html.Div("No data", style=_CARD_STYLE)
    df = postprocess_time_columns(df, enc)

    show_markers = opts.get("markers", True)
    mode = "lines+markers" if show_markers else "lines"

    fig = go.Figure()
    if enc.color:
        color_col = dimension_column_name(enc.color)
        for series, sub in df.groupby(color_col):
            fig.add_trace(go.Scatter(
                x=sub[x_col], y=sub[metric], mode=mode, name=str(series),
                line=dict(width=LINE_CHART_LINE_WIDTH),
                marker=dict(size=LINE_CHART_MARKER_SIZE),
            ))
    else:
        fig.add_trace(go.Scatter(
            x=df[x_col], y=df[metric], mode=mode,
            line=dict(width=LINE_CHART_LINE_WIDTH),
            marker=dict(size=LINE_CHART_MARKER_SIZE),
        ))
    fig.update_layout(
        height=int(str(LINE_CHART_HEIGHT).rstrip("px")),
        xaxis_title="", yaxis_title="",
    )
    apply_reference_lines(fig, opts, axis="y")
    return html.Div(dcc.Graph(figure=fig, config={"displayModeBar": False}), style=_CARD_STYLE)


def df_series_count(_color_channel) -> int:
    return 4
