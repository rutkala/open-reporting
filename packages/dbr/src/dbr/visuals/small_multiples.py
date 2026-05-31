"""small_multiples — Trellis / facet chart grid.

Repeats the same chart (line or bar) for each value of a facet dimension, laying
the panels out in a grid. Makes it easy to compare patterns across many categories
simultaneously without overlapping series.

Mandatory encoding:
  x:     { dimension: <name>, granularity?: <grain> }  — shared x-axis
  y:     { metric:    <name> }                          — y-axis metric
  facet: { dimension: <name> }                          — split-by dimension (one panel per value)

Optional:
  options.cols:         int  — number of columns in the grid (default: 3)
  options.shared_y:     bool — all panels share the same y-axis range (default: true)
  options.chart_type:   "line" | "bar" | "area"  — panel chart type (default: "line")
  options.height:       int  — total figure height (default: 600)
  options.facet_limit:  int  — max panels to render (default: 12)
  options.markers:      bool — show markers on line panels (default: false)
  options.color:        str  — palette alias or hex for bars/lines

Typical uses:
  - Unemployment rate over time for each EU country (one line panel per country)
  - Government spending by COFOG function over time
  - Regional GDP trends for Polish voivodeships
"""
from dash import dcc, html
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from dbr.semantic import semantic_query_data
from dbr.theme import (
    AZURE_1, BG_SURFACE, BAR_CHART_BARGAP,
    CARD_RADIUS, CARD_SHADOW, LINE_CHART_LINE_WIDTH, SUBTEXT, TEXT,
)
from dbr.visuals._encoding import (
    postprocess_time_columns,
    dimension_column_name, group_by_from_channels, parse_encoding, parse_channel,
    _resolve_color,
)

SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["type", "encoding"],
    "properties": {
        "type": {"const": "small_multiples"},
        "title":    {"type": "string"},
        "subtitle": {"type": "string"},
        "encoding": {
            "type": "object",
            "required": ["x", "y", "facet"],
            "additionalProperties": False,
            "properties": {
                "x":     {"type": "object"},
                "y":     {"type": "object"},
                "facet": {"type": "object"},
            },
        },
        "filter": {"type": "object"},
        "options": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "cols":        {"type": "integer", "minimum": 1, "maximum": 6},
                "shared_y":    {"type": "boolean"},
                "chart_type":  {"enum": ["line", "bar", "area"]},
                "height":      {"type": "integer", "minimum": 100, "maximum": 3000},
                "facet_limit": {"type": "integer", "minimum": 1, "maximum": 50},
                "markers":     {"type": "boolean"},
                "color":       {"type": "string"},
            },
        },
    },
}

_CARD_STYLE = {
    "background": BG_SURFACE, "borderRadius": CARD_RADIUS, "boxShadow": CARD_SHADOW,
    "padding": "16px", "height": "100%", "boxSizing": "border-box",
}


def small_multiples(*, encoding: dict, filter: dict | None = None, options: dict | None = None) -> html.Div:
    enc  = parse_encoding(encoding)
    opts = options or {}
    raw_enc = encoding or {}

    if not (enc.x and enc.x.dimension):
        raise ValueError("small_multiples: encoding.x must bind a dimension")
    if not (enc.y and enc.y.metrics):
        raise ValueError("small_multiples: encoding.y must bind a metric")

    facet_ch = parse_channel(raw_enc.get("facet"))
    if not (facet_ch and facet_ch.dimension):
        raise ValueError("small_multiples: encoding.facet must bind a dimension")

    x_col     = dimension_column_name(enc.x)
    facet_col = dimension_column_name(facet_ch)
    metric    = enc.y.metrics[0]
    group_by  = group_by_from_channels(enc.x, facet_ch)

    df = semantic_query_data(metric, group_by=group_by, filter=filter, order=x_col)
    if df.empty:
        return html.Div("No data", style=_CARD_STYLE)
    df = postprocess_time_columns(df, enc)

    facet_vals = df[facet_col].unique().tolist()
    facet_limit = opts.get("facet_limit", 12)
    facet_vals = facet_vals[:facet_limit]

    cols    = opts.get("cols", 3)
    rows    = (len(facet_vals) + cols - 1) // cols
    height  = opts.get("height", max(600, rows * 200))
    shared_y = opts.get("shared_y", True)
    chart_type = opts.get("chart_type", "line")
    show_markers = opts.get("markers", False)
    color = _resolve_color(opts.get("color"), AZURE_1)

    fig = make_subplots(
        rows=rows, cols=cols,
        shared_yaxes=shared_y,
        shared_xaxes=True,
        subplot_titles=[str(v) for v in facet_vals],
        vertical_spacing=0.12,
        horizontal_spacing=0.06,
    )

    for i, val in enumerate(facet_vals):
        sub = df[df[facet_col] == val].sort_values(x_col)
        row = i // cols + 1
        col = i % cols + 1
        if chart_type == "bar":
            fig.add_trace(go.Bar(
                x=sub[x_col], y=sub[metric],
                marker=dict(color=color),
                showlegend=False,
            ), row=row, col=col)
        elif chart_type == "area":
            fig.add_trace(go.Scatter(
                x=sub[x_col], y=sub[metric],
                fill="tozeroy", mode="lines",
                line=dict(color=color, width=LINE_CHART_LINE_WIDTH),
                showlegend=False,
            ), row=row, col=col)
        else:  # line
            mode = "lines+markers" if show_markers else "lines"
            fig.add_trace(go.Scatter(
                x=sub[x_col], y=sub[metric],
                mode=mode,
                line=dict(color=color, width=LINE_CHART_LINE_WIDTH),
                showlegend=False,
            ), row=row, col=col)

    fig.update_annotations(font_size=11, font_color=SUBTEXT)
    fig.update_layout(
        height=height,
        showlegend=False,
        bargap=BAR_CHART_BARGAP,
    )
    return html.Div(dcc.Graph(figure=fig, config={"displayModeBar": False}), style=_CARD_STYLE)
