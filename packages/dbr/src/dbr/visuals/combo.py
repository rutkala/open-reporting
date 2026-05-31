"""combo — Combination chart: column bars (left y-axis) + line (right y-axis).

Mandatory encoding:
  x:  { dimension: <name>, granularity?: <grain> }  — shared category axis
  y:  { metric: <name> }                             — bar metric (left axis)
  y2: { metric: <name> }                             — line metric (right axis)

Optional:
  options.stack:         bool   — stack bars when multiple y metrics (list) (default: false)
  options.show_markers:  bool   — show point markers on the line (default: true)
  options.bar_color:     str    — palette alias or hex for bars
  options.line_color:    str    — palette alias or hex for line
  options.y_label:       str    — left-axis label
  options.y2_label:      str    — right-axis label
  options.y_format:      str    — Plotly tickformat for left y-axis
  options.y2_format:     str    — Plotly tickformat for right y-axis
  options.height:        int    — chart height override

Classic use: revenue columns + growth-rate line (dual scale), GDP level bars +
inflation line, spending columns + deficit-to-GDP line.
"""
from dash import dcc, html
import plotly.graph_objects as go

from dbr.semantic import metric_label, semantic_query_data
from dbr.theme import (
    AZURE_1, BG_SURFACE, BAR_CHART_BARGAP, BAR_CHART_HEIGHT,
    CARD_RADIUS, CARD_SHADOW, LINE_CHART_LINE_WIDTH, LINE_CHART_MARKER_SIZE, TEAL_1,
)
from dbr.visuals._encoding import (
    apply_annotations, apply_reference_lines, _ANNOTATIONS_OPTION_SCHEMA,
    postprocess_time_columns,
    dimension_column_name, group_by_from_channels, parse_encoding, parse_channel,
    _resolve_color,
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
        "type": {"const": "combo"},
        "title":    {"type": "string"},
        "subtitle": {"type": "string"},
        "encoding": {
            "type": "object",
            "required": ["x", "y", "y2"],
            "additionalProperties": False,
            "properties": {
                "x":  {"type": "object"},
                "y":  {"type": "object"},
                "y2": {"type": "object"},
            },
        },
        "filter": {"type": "object"},
        "options": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "stack":        {"type": "boolean"},
                "show_markers": {"type": "boolean"},
                "bar_color":    {"type": "string"},
                "line_color":   {"type": "string"},
                "y_label":      {"type": "string"},
                "y2_label":     {"type": "string"},
                "y_format":     {"type": "string"},
                "y2_format":    {"type": "string"},
                "height":       {"type": "integer", "minimum": 100, "maximum": 2000},
                "reference_lines": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["value"],
                        "properties": {
                            "value": {"type": "number"},
                            "label": {"type": "string"},
                            "color": {"type": "string"},
                            "axis":  {"enum": ["y", "y2"]},
                        },
                    },
                },
                "download": {"type": "boolean", "description": "Render a CSV download link below the chart."},
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


def combo(*, encoding: dict, filter: dict | None = None, options: dict | None = None) -> html.Div:
    enc   = parse_encoding(encoding)
    opts  = options or {}
    raw_enc = encoding or {}

    if not (enc.x and enc.x.dimension):
        raise ValueError("combo: encoding.x must bind a dimension")
    if not (enc.y and enc.y.metrics):
        raise ValueError("combo: encoding.y must bind a metric (bars)")

    # Parse y2 from raw encoding (Encoding dataclass doesn't have y2 field)
    y2_ch = parse_channel(raw_enc.get("y2"))
    if not (y2_ch and y2_ch.metrics):
        raise ValueError("combo: encoding.y2 must bind a metric (line)")

    x_col      = dimension_column_name(enc.x)
    bar_metric = enc.y.metrics[0]
    line_metric = y2_ch.metrics[0]
    group_by   = group_by_from_channels(enc.x)

    # Query both metrics; merge on the x dimension
    df_bar  = semantic_query_data(bar_metric,  group_by=group_by, filter=filter, order=x_col)
    df_line = semantic_query_data(line_metric, group_by=group_by, filter=filter, order=x_col)
    if df_bar.empty and df_line.empty:
        return html.Div("No data", style=_CARD_STYLE)

    if not df_bar.empty and not df_line.empty:
        df = df_bar.merge(df_line, on=x_col, how="outer").sort_values(x_col)
    elif df_bar.empty:
        df = df_line
    else:
        df = df_bar
    df = postprocess_time_columns(df, enc)

    bar_color  = _resolve_color(opts.get("bar_color"), AZURE_1)
    line_color = _resolve_color(opts.get("line_color"), TEAL_1)
    show_markers = opts.get("show_markers", True)
    mode = "lines+markers" if show_markers else "lines"
    height = opts.get("height", int(str(BAR_CHART_HEIGHT).rstrip("px")))

    fig = go.Figure()

    # Bar trace on y1
    if bar_metric in df.columns:
        fig.add_trace(go.Bar(
            x=df[x_col], y=df[bar_metric],
            name=metric_label(bar_metric),
            marker=dict(color=bar_color),
            yaxis="y",
        ))

    # Line trace on y2
    if line_metric in df.columns:
        fig.add_trace(go.Scatter(
            x=df[x_col], y=df[line_metric],
            name=metric_label(line_metric),
            mode=mode,
            line=dict(width=LINE_CHART_LINE_WIDTH, color=line_color),
            marker=dict(size=LINE_CHART_MARKER_SIZE),
            yaxis="y2",
        ))

    y_label  = opts.get("y_label", "")
    y2_label = opts.get("y2_label", "")
    fig.update_layout(
        height=height,
        bargap=BAR_CHART_BARGAP,
        xaxis=dict(title=""),
        yaxis=dict(title=y_label, tickformat=opts.get("y_format", "")),
        yaxis2=dict(
            title=y2_label,
            overlaying="y",
            side="right",
            tickformat=opts.get("y2_format", ""),
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    # Reference lines — support axis: "y" (left) or "y2" (right)
    for spec in (opts.get("reference_lines") or []):
        if not isinstance(spec, dict) or "value" not in spec:
            continue
        from dbr.visuals._encoding import _resolve_color as rc, NEGATIVE
        color = rc(spec.get("color"))
        label = spec.get("label", "")
        axis  = spec.get("axis", "y")
        yref  = "y" if axis == "y" else "y2"
        fig.add_hline(
            y=spec["value"], line_dash="dash", line_color=color, line_width=1.5,
            annotation_text=label, annotation_position="top right",
            annotation_font=dict(color=color, size=11),
            yref=yref,
        )
    apply_annotations(fig, opts)
    return chart_with_optional_table(fig, df, opts, _CARD_STYLE)
