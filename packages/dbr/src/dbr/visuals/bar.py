"""bar — Horizontal bar chart.

Mandatory encoding:
  x:  { metric:    <name> }     — value on x-axis
  y:  { dimension: <name> }     — category on y-axis

Optional:
  color:     { dimension: <name> }  — splits into grouped or stacked bars
  options.stack:            bool    — stack (true) or group (false) when `color` is set
  options.sort:             "value-asc" | "value-desc" | "category"
  options.highlight:                — color one row distinctly (single-series only)
    value:   <category value>       — exact match against the y-dim column
    color:   <alias|hex>            — default azure_1
    other:   <alias|hex>            — default slate_2
  options.reference_lines:          — vertical dashed lines at given x values
    - { value: <number>, label: <str>, color: <alias|hex> }
"""
from dash import dcc, html
import plotly.graph_objects as go

from dbr.semantic import semantic_query_data
from dbr.theme import (
    AZURE_1, BG_SURFACE, BAR_CHART_BARGAP, BAR_CHART_HEIGHT,
    CARD_RADIUS, CARD_SHADOW, SLATE_1,
)
from dbr.visuals._encoding import (
    apply_reference_lines, postprocess_time_columns,
    dimension_column_name, group_by_from_channels, parse_encoding,
    _resolve_color,
)
from dbr.visuals._render import chart_with_optional_table, _TABLE_OPTION_SCHEMA

SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["type", "encoding"],
    "properties": {
        "type": {"const": "bar"},
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
                "stack": {"type": "boolean"},
                "sort":  {"enum": ["value-asc", "value-desc", "category"]},
                "highlight": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["value"],
                    "properties": {
                        "value": {},
                        "color": {"type": "string"},
                        "other": {"type": "string"},
                    },
                },
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
                "table": _TABLE_OPTION_SCHEMA,
            },
        },
    },
}

_CARD_STYLE = {
    "background": BG_SURFACE, "borderRadius": CARD_RADIUS, "boxShadow": CARD_SHADOW,
    "padding": "16px", "height": "100%", "boxSizing": "border-box",
}


def bar(*, encoding: dict, filter: dict | None = None, options: dict | None = None) -> html.Div:
    enc = parse_encoding(encoding)
    opts = options or {}

    if not (enc.x and enc.x.metric):
        raise ValueError("bar: encoding.x must bind a metric (use `column` for vertical bars)")
    if not (enc.y and enc.y.dimension):
        raise ValueError("bar: encoding.y must bind a dimension")

    group_by = group_by_from_channels(enc.y, enc.color)
    y_col = dimension_column_name(enc.y)
    metric = enc.x.metric

    df = semantic_query_data(metric, group_by=group_by, filter=filter, order=y_col)
    if df.empty:
        return html.Div("No data", style=_CARD_STYLE)
    df = postprocess_time_columns(df, enc)

    sort = opts.get("sort")
    if sort == "value-asc":
        df = df.sort_values(metric, ascending=True)
    elif sort == "value-desc":
        df = df.sort_values(metric, ascending=False)
    elif sort == "category":
        df = df.sort_values(y_col)

    fig = go.Figure()
    if enc.color:
        color_col = dimension_column_name(enc.color)
        for series, sub in df.groupby(color_col):
            fig.add_trace(go.Bar(x=sub[metric], y=sub[y_col], orientation="h", name=str(series)))
        fig.update_layout(barmode="stack" if opts.get("stack") else "group")
    else:
        marker_color = None
        hi = opts.get("highlight")
        if hi:
            target = hi["value"]
            color_hit = _resolve_color(hi.get("color"), AZURE_1)
            color_miss = _resolve_color(hi.get("other"), SLATE_1)
            marker_color = [color_hit if v == target else color_miss for v in df[y_col]]
        fig.add_trace(go.Bar(
            x=df[metric], y=df[y_col], orientation="h",
            marker=dict(color=marker_color) if marker_color else None,
            showlegend=False,
        ))
    fig.update_layout(
        height=int(str(BAR_CHART_HEIGHT).rstrip("px")),
        bargap=BAR_CHART_BARGAP, xaxis_title="", yaxis_title="",
    )
    apply_reference_lines(fig, opts, axis="x")
    return chart_with_optional_table(fig, df, opts, _CARD_STYLE)
