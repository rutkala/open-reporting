"""treemap — Hierarchical treemap (area = proportional to metric).

One dimension:
  encoding:
    category: { dimension: <name> }   — leaf labels
    value:    { metric:    <name> }   — tile area

Two-level hierarchy:
  encoding:
    category: { dimension: <leaf_dim>  }
    parent:   { dimension: <group_dim> }
    value:    { metric: <name> }

Optional:
  options.colorscale:   str    — Plotly colorscale; values mapped to colour. Default: "Blues".
  options.show_values:  bool   — show metric value inside tile (default: true)
  options.height:       int    — chart height override
  options.maxdepth:     int    — max depth displayed initially (default: 2)

Typical uses: government spending composition by COFOG, emissions by sector,
export basket by product category.
"""
from dash import dcc, html
import plotly.graph_objects as go

from dbr.semantic import semantic_query_data
from dbr.theme import BG_SURFACE, BAR_CHART_HEIGHT, CARD_RADIUS, CARD_SHADOW
from dbr.visuals._encoding import (
    postprocess_time_columns,
    dimension_column_name, group_by_from_channels, parse_encoding,
)

SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["type", "encoding"],
    "properties": {
        "type": {"const": "treemap"},
        "title":    {"type": "string"},
        "subtitle": {"type": "string"},
        "encoding": {
            "type": "object",
            "required": ["category", "value"],
            "additionalProperties": False,
            "properties": {
                "category": {"type": "object"},
                "parent":   {"type": "object"},
                "value":    {"type": "object"},
            },
        },
        "filter": {"type": "object"},
        "options": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "colorscale":  {"type": "string"},
                "show_values": {"type": "boolean"},
                "height":      {"type": "integer", "minimum": 100, "maximum": 2000},
                "maxdepth":    {"type": "integer", "minimum": 1, "maximum": 5},
            },
        },
    },
}

_CARD_STYLE = {
    "background": BG_SURFACE, "borderRadius": CARD_RADIUS, "boxShadow": CARD_SHADOW,
    "padding": "16px", "height": "100%", "boxSizing": "border-box",
}


def treemap(*, encoding: dict, filter: dict | None = None, options: dict | None = None) -> html.Div:
    enc = parse_encoding(encoding)
    opts = options or {}

    if not (enc.category and enc.category.dimension):
        raise ValueError("treemap: encoding.category must bind a dimension")
    if not (enc.value and enc.value.metric):
        raise ValueError("treemap: encoding.value must bind a metric")

    cat_col  = dimension_column_name(enc.category)
    metric   = enc.value.metric
    has_parent = enc.category is not None and hasattr(enc, "value")

    group_by = group_by_from_channels(enc.category)

    # Check for parent dimension (two-level hierarchy)
    parent_dim = None
    parent_col = None
    raw_enc = encoding or {}
    if "parent" in raw_enc:
        from dbr.visuals._encoding import parse_channel
        parent_ch  = parse_channel(raw_enc["parent"])
        if parent_ch and parent_ch.dimension:
            parent_col = dimension_column_name(parent_ch)
            group_by   = group_by_from_channels(enc.category, parent_ch)

    df = semantic_query_data(metric, group_by=group_by, filter=filter)
    if df.empty:
        return html.Div("No data", style=_CARD_STYLE)
    df = postprocess_time_columns(df, enc)

    colorscale  = opts.get("colorscale", "Blues")
    show_values = opts.get("show_values", True)
    height      = opts.get("height", int(str(BAR_CHART_HEIGHT).rstrip("px")))
    maxdepth    = opts.get("maxdepth", 2)

    if parent_col and parent_col in df.columns:
        # Two-level: group tiles under parent categories
        # Build id, label, parent, value arrays
        groups = df[parent_col].unique().tolist()
        group_vals = df.groupby(parent_col)[metric].sum()
        ids     = [""] + [str(g) for g in groups] + [f"{row[parent_col]}|{row[cat_col]}" for _, row in df.iterrows()]
        labels  = ["Total"] + [str(g) for g in groups] + [str(row[cat_col]) for _, row in df.iterrows()]
        parents = [""] + [""] * len(groups) + [str(row[parent_col]) for _, row in df.iterrows()]
        values  = [df[metric].sum()] + [group_vals.get(g, 0) for g in groups] + df[metric].tolist()
    else:
        ids     = [str(v) for v in df[cat_col]]
        labels  = ids
        parents = [""] * len(ids)
        values  = df[metric].tolist()

    text_templ = "%{label}<br>%{value:.1f}" if show_values else "%{label}"

    fig = go.Figure(go.Treemap(
        ids=ids, labels=labels, parents=parents, values=values,
        texttemplate=text_templ,
        marker=dict(colorscale=colorscale, showscale=True),
        maxdepth=maxdepth,
        hovertemplate="%{label}: %{value:.1f}<extra></extra>",
    ))
    fig.update_layout(height=height, margin=dict(l=0, r=0, t=0, b=0))
    return html.Div(dcc.Graph(figure=fig, config={"displayModeBar": False}), style=_CARD_STYLE)
