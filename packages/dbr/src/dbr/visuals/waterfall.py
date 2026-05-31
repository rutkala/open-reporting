"""waterfall — Waterfall / bridge chart.

Mandatory encoding:
  x: { dimension: <name> }   — categories (bars) on x-axis
  y: { metric:    <name> }   — values (positive = up, negative = down)

Optional:
  options.totals:            list of category names rendered as total bars (full-height)
  options.increasing_color:  hex or palette alias (default: positive/blue)
  options.decreasing_color:  hex or palette alias (default: negative/orange)
  options.total_color:       hex or palette alias for total bars (default: slate_1)
  options.connector_visible: bool — show connector lines between bars (default: true)
  options.data_labels:       bool — show value label on each bar
  options.height:            int  — chart height override

Classic use: budget bridge (revenue → spending → balance), cumulative cash flow,
variance decomposition (plan vs. actual by component).
"""
from dash import dcc, html
import plotly.graph_objects as go

from dbr.semantic import semantic_query_data
from dbr.theme import (
    AZURE_1, BG_SURFACE, BAR_CHART_BARGAP, BAR_CHART_HEIGHT,
    CARD_RADIUS, CARD_SHADOW, NEGATIVE, POSITIVE, SLATE_1,
)
from dbr.visuals._encoding import (
    apply_annotations, _ANNOTATIONS_OPTION_SCHEMA,
    postprocess_time_columns,
    dimension_column_name, group_by_from_channels, parse_encoding,
    _resolve_color,
)
from dbr.visuals._render import chart_with_optional_table, _TABLE_OPTION_SCHEMA

SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["type", "encoding"],
    "properties": {
        "type": {"const": "waterfall"},
        "title":    {"type": "string"},
        "subtitle": {"type": "string"},
        "encoding": {
            "type": "object",
            "required": ["x", "y"],
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
                "totals": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Category names to render as totals (full-height accumulation bars).",
                },
                "increasing_color": {"type": "string"},
                "decreasing_color": {"type": "string"},
                "total_color":      {"type": "string"},
                "connector_visible": {"type": "boolean"},
                "data_labels": {"type": "boolean"},
                "height":      {"type": "integer", "minimum": 100, "maximum": 2000},
                "y_format":    {"type": "string"},
                "download": {"type": "boolean", "description": "Render a CSV download link below the chart."},
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


def waterfall(*, encoding: dict, filter: dict | None = None, options: dict | None = None) -> html.Div:
    enc = parse_encoding(encoding)
    opts = options or {}

    if not (enc.x and enc.x.dimension):
        raise ValueError("waterfall: encoding.x must bind a dimension")
    metrics = enc.y.metrics if enc.y else []
    if not metrics:
        raise ValueError("waterfall: encoding.y must bind a metric")

    x_col = dimension_column_name(enc.x)
    metric = metrics[0]

    df = semantic_query_data(metric, group_by=group_by_from_channels(enc.x), filter=filter, order=x_col)
    if df.empty:
        return html.Div("No data", style=_CARD_STYLE)
    df = postprocess_time_columns(df, enc)

    totals_set = set(str(t) for t in (opts.get("totals") or []))
    measure = ["total" if str(v) in totals_set else "relative" for v in df[x_col]]

    inc_color = _resolve_color(opts.get("increasing_color"), POSITIVE)
    dec_color = _resolve_color(opts.get("decreasing_color"), NEGATIVE)
    tot_color = _resolve_color(opts.get("total_color"), SLATE_1)

    connector_visible = opts.get("connector_visible", True)

    text = [f"{v:.1f}" for v in df[metric]] if opts.get("data_labels") else None

    fig = go.Figure(go.Waterfall(
        x=df[x_col].tolist(),
        y=df[metric].tolist(),
        measure=measure,
        text=text,
        textposition="outside" if text else "none",
        increasing=dict(marker=dict(color=inc_color)),
        decreasing=dict(marker=dict(color=dec_color)),
        totals=dict(marker=dict(color=tot_color)),
        connector=dict(visible=connector_visible),
    ))
    height = opts.get("height", int(str(BAR_CHART_HEIGHT).rstrip("px")))
    fig.update_layout(height=height, xaxis_title="", yaxis_title="", showlegend=False)
    if opts.get("y_format"):
        fig.update_layout(yaxis_tickformat=opts["y_format"])
    apply_annotations(fig, opts)
    return chart_with_optional_table(fig, df, opts, _CARD_STYLE)
