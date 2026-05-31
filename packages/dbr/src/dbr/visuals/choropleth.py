"""choropleth — Geographic map with colour-encoded metric values.

Mandatory encoding:
  location: { dimension: <name> }   — ISO 3166-1 alpha-2 codes (e.g. "PL", "DE") or country names
  color:    { metric:    <name> }   — value mapped to colour intensity

Optional:
  options.scope:         str   — plotly geographic scope: "europe" | "world" | "asia" | "africa" |
                                  "north america" | "south america" (default: "europe")
  options.location_mode: str   — "ISO-3166-1-alpha-2" | "country names" | "geojson-id"
                                  (default: "ISO-3166-1-alpha-2")
  options.colorscale:    str   — Plotly colorscale name: "Blues", "RdYlGn", "Oranges", etc.
                                  (default: "Blues")
  options.reverse:       bool  — reverse the colorscale (default: false)
  options.show_labels:   bool  — show metric value labels on each country (default: false)
  options.height:        int   — chart height in px (default: 400)
  options.geojson_path:  str   — absolute path to a GeoJSON file for custom geographies
                                  (e.g. Polish NUTS2 voivodeships). When set, location_mode
                                  is automatically set to "geojson-id".

Typical uses:
  - EU member-state comparison (unemployment, GDP, debt) using ISO alpha-2 codes
  - European regional comparison using NUTS2 codes with custom GeoJSON
  - World-wide indicator maps
"""
import json
from pathlib import Path

from dash import dcc, html
import plotly.graph_objects as go

from dbr.semantic import semantic_query_data
from dbr.theme import BG_SURFACE, CARD_RADIUS, CARD_SHADOW
from dbr.visuals._encoding import (
    postprocess_time_columns,
    dimension_column_name, group_by_from_channels, parse_encoding,
)
from dbr.visuals._render import (
    apply_axis_options, _AXIS_OPTIONS_SCHEMA,
    format_value, _FORMAT_OPTION_SCHEMA,
)

SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["type", "encoding"],
    "properties": {
        "type": {"const": "choropleth"},
        "title":    {"type": "string"},
        "subtitle": {"type": "string"},
        "encoding": {
            "type": "object",
            "required": ["location", "color"],
            "additionalProperties": False,
            "properties": {
                "location": {"type": "object"},
                "color":    {"type": "object"},
            },
        },
        "filter": {"type": "object"},
        "options": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "scope":         {"type": "string"},
                "location_mode": {"type": "string"},
                "colorscale":    {"type": "string"},
                "reverse":       {"type": "boolean"},
                "show_labels":   {"type": "boolean"},
                "height":        {"type": "integer", "minimum": 100, "maximum": 2000},
                "geojson_path":  {"type": "string"},
                **_FORMAT_OPTION_SCHEMA,
            },
        },
    },
}

_CARD_STYLE = {
    "background": BG_SURFACE, "borderRadius": CARD_RADIUS, "boxShadow": CARD_SHADOW,
    "padding": "16px", "height": "100%", "boxSizing": "border-box",
}


def choropleth(*, encoding: dict, filter: dict | None = None, options: dict | None = None) -> html.Div:
    enc  = parse_encoding(encoding)
    opts = options or {}

    raw_enc = encoding or {}
    from dbr.visuals._encoding import parse_channel
    loc_ch = parse_channel(raw_enc.get("location"))
    col_ch = parse_channel(raw_enc.get("color"))

    if not (loc_ch and loc_ch.dimension):
        raise ValueError("choropleth: encoding.location must bind a dimension")
    if not (col_ch and col_ch.metric):
        raise ValueError("choropleth: encoding.color must bind a metric")

    loc_col  = dimension_column_name(loc_ch)
    metric   = col_ch.metric
    group_by = [loc_col]

    df = semantic_query_data(metric, group_by=group_by, filter=filter)
    if df.empty:
        return html.Div("No data", style=_CARD_STYLE)

    scope         = opts.get("scope", "europe")
    colorscale    = opts.get("colorscale", "Blues")
    reverse_cs    = opts.get("reverse", False)
    height        = opts.get("height", 400)
    show_labels   = opts.get("show_labels", False)
    geojson_path  = opts.get("geojson_path")
    location_mode = opts.get("location_mode", "ISO-3166-1-alpha-2")

    if geojson_path:
        gj = json.loads(Path(geojson_path).read_text())
        fig = go.Figure(go.Choropleth(
            geojson=gj,
            locations=df[loc_col].astype(str),
            z=df[metric],
            colorscale=colorscale,
            reversescale=reverse_cs,
            featureidkey="properties.nuts_id",  # adjust per GeoJSON schema
            marker_line_width=0.5,
            marker_line_color="white",
        ))
        fig.update_geos(fitbounds="locations", visible=False)
    else:
        fig = go.Figure(go.Choropleth(
            locations=df[loc_col].astype(str),
            z=df[metric],
            locationmode=location_mode,
            colorscale=colorscale,
            reversescale=reverse_cs,
            marker_line_width=0.5,
            marker_line_color="white",
        ))
        fig.update_geos(
            scope=scope,
            showframe=False,
            showcoastlines=False,
            bgcolor="rgba(0,0,0,0)",
        )

    if show_labels:
        val_fmt = opts.get("value_format")
        fig.add_trace(go.Scattergeo(
            locations=df[loc_col].astype(str),
            locationmode=location_mode if not geojson_path else None,
            text=[format_value(v, val_fmt) for v in df[metric]],
            mode="text",
            textfont=dict(size=9, color="white"),
            showlegend=False,
            hoverinfo="skip",
        ))

    fig.update_layout(
        height=height,
        margin=dict(l=0, r=0, t=0, b=0),
        geo=dict(bgcolor="rgba(0,0,0,0)"),
        paper_bgcolor="rgba(0,0,0,0)",
    )
    return html.Div(dcc.Graph(figure=fig, config={"displayModeBar": False}), style=_CARD_STYLE)
