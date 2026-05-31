"""funnel — Funnel chart. Shows values narrowing across ordered stages.

Mandatory encoding:
  category: { dimension: <name> }  — stage labels (ordered by data, largest first)
  value:    { metric:    <name> }  — value per stage

Optional:
  options.sort:            "value-desc" | "value-asc" | "none" — bar order (default: value-desc)
  options.show_percent:    bool   — show % of total on each segment (default: true)
  options.connector_color: str    — trapezoid connector fill color (default: azure_pale)
  options.height:          int    — chart height override
  options.data_labels:     bool   — show value labels (default: true)

Typical uses: policy pipeline (applications → reviews → approvals), sales funnel,
EU funding absorption rate by stage.
"""
from dash import dcc, html
import plotly.graph_objects as go

from dbr.semantic import semantic_query_data
from dbr.theme import (
    AZURE_1, AZURE_PALE, BG_SURFACE, BAR_CHART_HEIGHT,
    CARD_RADIUS, CARD_SHADOW,
)
from dbr.visuals._encoding import (
    postprocess_time_columns,
    dimension_column_name, group_by_from_channels, parse_encoding,
)

SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["type", "encoding"],
    "properties": {
        "type": {"const": "funnel"},
        "title":    {"type": "string"},
        "subtitle": {"type": "string"},
        "encoding": {
            "type": "object",
            "required": ["category", "value"],
            "additionalProperties": False,
            "properties": {
                "category": {"type": "object"},
                "value":    {"type": "object"},
            },
        },
        "filter": {"type": "object"},
        "options": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "sort":            {"enum": ["value-desc", "value-asc", "none"]},
                "show_percent":    {"type": "boolean"},
                "connector_color": {"type": "string"},
                "height":          {"type": "integer", "minimum": 100, "maximum": 2000},
                "data_labels":     {"type": "boolean"},
            },
        },
    },
}

_CARD_STYLE = {
    "background": BG_SURFACE, "borderRadius": CARD_RADIUS, "boxShadow": CARD_SHADOW,
    "padding": "16px", "height": "100%", "boxSizing": "border-box",
}


def funnel(*, encoding: dict, filter: dict | None = None, options: dict | None = None) -> html.Div:
    enc = parse_encoding(encoding)
    opts = options or {}

    if not (enc.category and enc.category.dimension):
        raise ValueError("funnel: encoding.category must bind a dimension")
    if not (enc.value and enc.value.metric):
        raise ValueError("funnel: encoding.value must bind a metric")

    cat_col = dimension_column_name(enc.category)
    metric  = enc.value.metric
    group_by = group_by_from_channels(enc.category)

    df = semantic_query_data(metric, group_by=group_by, filter=filter)
    if df.empty:
        return html.Div("No data", style=_CARD_STYLE)
    df = postprocess_time_columns(df, enc)

    sort = opts.get("sort", "value-desc")
    if sort == "value-desc":
        df = df.sort_values(metric, ascending=False)
    elif sort == "value-asc":
        df = df.sort_values(metric, ascending=True)

    show_percent = opts.get("show_percent", True)
    data_labels  = opts.get("data_labels", True)
    height       = opts.get("height", int(str(BAR_CHART_HEIGHT).rstrip("px")))

    textinfo = "value+percent initial" if show_percent and data_labels else (
        "value" if data_labels else "none"
    )

    fig = go.Figure(go.Funnel(
        y=df[cat_col].tolist(),
        x=df[metric].tolist(),
        marker=dict(color=AZURE_1),
        connector=dict(fillcolor=AZURE_PALE),
        textinfo=textinfo,
        hovertemplate="%{y}: %{x:.1f}<extra></extra>",
    ))
    fig.update_layout(height=height, showlegend=False)
    return html.Div(dcc.Graph(figure=fig, config={"displayModeBar": False}), style=_CARD_STYLE)
