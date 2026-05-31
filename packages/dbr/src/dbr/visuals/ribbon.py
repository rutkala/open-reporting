"""ribbon — Ribbon / bump chart showing rank changes over time.

Each category gets one line whose y-position represents its rank at each
time period. When a category rises from #3 to #1 its line crosses others —
this crossing is the core information the chart communicates. Sometimes called
a "bump chart" or "slope chart" (for two-point comparisons).

PowerBI equivalent: "Ribbon chart". Tableau equivalent: "Bump chart".

Mandatory encoding:
  x:     { dimension: <name>, granularity: <grain> }  — time or ordered categories
  y:     { metric:    <name> }                          — metric used to compute rank
  color: { dimension: <name> }                          — one line per category value

Optional:
  options.top_n:     int   — show only the top N categories ranked by latest period
                             value (default: all)
  options.inverted:  bool  — rank 1 at the top of the chart (default: true)
  options.markers:   bool  — show data point markers (default: true)
  options.labels:    bool  — label each line at its right endpoint (default: true)
  options.height:    int   — chart height override
  options.y_format:  str   — tickformat for rank axis labels
  options.smooth:    bool  — spline interpolation (default: false)

YAML example (EU unemployment rank among member states over time):

  type: ribbon
  encoding:
    x:     { dimension: metric_time, granularity: year }
    y:     { metric: unemployment_rate }
    color: { dimension: geo }
  options:
    top_n: 10
    inverted: true
    labels: true
"""
from dash import dcc, html
import plotly.graph_objects as go
import pandas as pd

from dbr.semantic import semantic_query_data
from dbr.theme import (
    BG_SURFACE, BAR_CHART_HEIGHT, CARD_RADIUS, CARD_SHADOW, COLORWAY,
    LINE_CHART_LINE_WIDTH, LINE_CHART_MARKER_SIZE, SUBTEXT,
)
from dbr.visuals._encoding import (
    apply_annotations, _ANNOTATIONS_OPTION_SCHEMA,
    postprocess_time_columns,
    dimension_column_name, group_by_from_channels, parse_encoding,
)
from dbr.visuals._render import (
    apply_axis_options, chart_with_optional_table, _AXIS_OPTIONS_SCHEMA,
    format_value, _FORMAT_OPTION_SCHEMA, _TABLE_OPTION_SCHEMA,
)

SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["type", "encoding"],
    "properties": {
        "type": {"const": "ribbon"},
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
                "top_n":    {"type": "integer", "minimum": 2, "maximum": 50},
                "inverted": {"type": "boolean"},
                "markers":  {"type": "boolean"},
                "labels":   {"type": "boolean"},
                "smooth":   {"type": "boolean"},
                "height":   {"type": "integer", "minimum": 100, "maximum": 2000},
                "y_format": {"type": "string"},
                **_AXIS_OPTIONS_SCHEMA,
                **_FORMAT_OPTION_SCHEMA,
                "table": _TABLE_OPTION_SCHEMA,
                "annotations": _ANNOTATIONS_OPTION_SCHEMA,
            },
        },
    },
}

_CARD_STYLE = {
    "background": BG_SURFACE, "borderRadius": CARD_RADIUS, "boxShadow": CARD_SHADOW,
    "padding": "16px", "height": "100%", "boxSizing": "border-box",
}


def ribbon(*, encoding: dict, filter: dict | None = None, options: dict | None = None) -> html.Div:
    enc  = parse_encoding(encoding)
    opts = options or {}

    if not (enc.x and enc.x.dimension):
        raise ValueError("ribbon: encoding.x must bind a dimension")
    if not (enc.y and enc.y.metrics):
        raise ValueError("ribbon: encoding.y must bind a metric")
    if not (enc.color and enc.color.dimension):
        raise ValueError("ribbon: encoding.color must bind a dimension (one line per category)")

    x_col     = dimension_column_name(enc.x)
    color_col = dimension_column_name(enc.color)
    metric    = enc.y.metrics[0]
    group_by  = group_by_from_channels(enc.x, enc.color)

    df = semantic_query_data(metric, group_by=group_by, filter=filter, order=x_col)
    if df.empty:
        return html.Div("No data", style=_CARD_STYLE)
    df = postprocess_time_columns(df, enc)
    df = df.sort_values(x_col)

    # Compute rank per time period (dense rank, ascending = best rank for higher values)
    inverted = opts.get("inverted", True)
    # By default, higher metric value = better rank (rank 1 = largest)
    df["__rank"] = df.groupby(x_col)[metric].rank(
        method="dense", ascending=False  # rank 1 = highest value
    )
    n_cats = df[color_col].nunique()

    # Filter to top_n categories by their latest-period value
    top_n = opts.get("top_n")
    if top_n and top_n < n_cats:
        latest_x = df[x_col].max()
        latest = df[df[x_col] == latest_x].nlargest(top_n, metric)
        top_cats = latest[color_col].tolist()
        df = df[df[color_col].isin(top_cats)]
        n_cats = top_n

    show_markers = opts.get("markers", True)
    show_labels  = opts.get("labels", True)
    smooth       = opts.get("smooth", False)
    height       = opts.get("height", int(str(BAR_CHART_HEIGHT).rstrip("px")))
    mode         = "lines+markers" if show_markers else "lines"

    fig = go.Figure()
    palette = list(COLORWAY)

    for i, (cat, sub) in enumerate(df.groupby(color_col)):
        sub = sub.sort_values(x_col)
        color = palette[i % len(palette)]
        line_shape = "spline" if smooth else "linear"
        fig.add_trace(go.Scatter(
            x=sub[x_col],
            y=sub["__rank"],
            mode=mode,
            name=str(cat),
            line=dict(width=LINE_CHART_LINE_WIDTH, color=color, shape=line_shape),
            marker=dict(size=LINE_CHART_MARKER_SIZE, color=color),
        ))

    # Y-axis: rank 1 at top when inverted=True
    if inverted:
        fig.update_yaxes(
            autorange="reversed",
            dtick=1,
            title="Pozycja",
        )
    else:
        fig.update_yaxes(dtick=1, title="Pozycja")

    # Endpoint labels
    if show_labels:
        fig.update_layout(showlegend=False)
        last_x = df[x_col].max()
        for trace in fig.data:
            x_vals = list(trace.x or [])
            y_vals = list(trace.y or [])
            if not x_vals:
                continue
            # Find last non-null
            last_y = None
            for yv in reversed(y_vals):
                if yv is not None and not (isinstance(yv, float) and pd.isna(yv)):
                    last_y = yv
                    break
            if last_y is not None:
                fig.add_annotation(
                    x=x_vals[-1], y=last_y,
                    text=str(trace.name),
                    xref="x", yref="y",
                    showarrow=False,
                    xanchor="left", xshift=8,
                    font=dict(color=getattr(trace.line, "color", SUBTEXT), size=11),
                )

    if opts.get("y_format"):
        fig.update_layout(yaxis_tickformat=opts["y_format"])

    fig.update_layout(height=height, xaxis_title="")
    apply_axis_options(fig, opts)
    apply_annotations(fig, opts)
    return chart_with_optional_table(fig, df.drop(columns=["__rank"]), opts, _CARD_STYLE)
