"""choropleth — Geographic map with colour-encoded metric values.

Mandatory encoding:
  location: { dimension: <name> }   — the geo CODE column. ISO 3166-1 alpha-2
                                      (e.g. "PL", "DE") for country maps, or NUTS
                                      codes (e.g. "PL21") for the bundled regional maps.
  color:    { metric:    <name> }   — value mapped to colour intensity

Optional:
  options.scope:         str   — plotly geographic scope for built-in country maps:
                                  "europe" | "world" | "asia" | "africa" |
                                  "north america" | "south america" (default: "europe").
                                  Ignored when a geojson map is selected.
  options.location_mode: str   — "ISO-3166-1-alpha-2" | "country names"
                                  (default: "ISO-3166-1-alpha-2"). Ignored for geojson maps.
  options.geojson:       str   — bundled geography name → renders a custom-shape map keyed
                                  on the `geo` code. Available: "europe_countries" (EU/EFTA
                                  country shapes, matched on NUTS level-0 code incl. EL/UK)
                                  and "poland_nuts2" (17 voivodeships). Both are Eurostat
                                  GISCO NUTS 2021, locations matched on NUTS_ID.
  options.geojson_path:  str   — absolute path to a custom GeoJSON file (advanced; overrides
                                  `geojson`). featureidkey defaults to properties.NUTS_ID.
  options.feature_id_key: str  — override the GeoJSON feature key used to match `location`
                                  values (default resolved per bundled map).
  options.colorscale:    str   — Plotly colorscale name: "Blues", "RdYlGn", "Teal", … (default: "Blues")
  options.reverse:       bool  — reverse the colorscale (default: false)
  options.color_midpoint: num  — anchor the colour scale midpoint (z=zmid); use 0 with a
                                  diverging scale for balance/change metrics (default: none)
  options.show_labels:   bool  — show metric value labels on each region (default: false;
                                  country/ISO maps only)
  options.height:        int   — chart height in px (default: 400)

Typical uses:
  - EU member-state comparison (deficit, debt, unemployment) — geojson: europe_countries,
    location bound to the country `geo` code (Eurostat alpha-2, incl. EL/UK).
  - Polish voivodeship comparison — geojson: poland_nuts2, location bound to the NUTS2 `geo` code.
  - World-wide indicator maps — scope: world + ISO-3 / country-name locations.

Note: Plotly's built-in scope maps (no geojson) only match ISO-3 alpha-3 codes or country
names, not Eurostat alpha-2 — so EU maps use the bundled europe_countries geojson instead.
"""
import json
import logging
from pathlib import Path

from dash import html
import plotly.graph_objects as go

logger = logging.getLogger(__name__)

from dbr.semantic import semantic_query_data
from dbr.theme import BG_SURFACE, CARD_RADIUS, CARD_SHADOW
from dbr.visuals._encoding import (
    dimension_column_name, parse_channel,
)
from dbr.visuals._render import format_value, chart_with_optional_table, _FORMAT_OPTION_SCHEMA

# Bundled geographies shipped under dbr/data/. Each maps a friendly name to its
# GeoJSON file and the feature property key whose value equals our `geo` code.
_DATA_DIR = Path(__file__).resolve().parent.parent / "data"
# Each bundled geography: GeoJSON path, the feature property key matching our `geo`
# code, and the default map framing. GISCO NUTS 2021 shapes are keyed by NUTS_ID, which
# equals our `geo` codes 1:1 (Eurostat 2-letter country codes incl. EL/UK at level 0;
# PL21… at level 2). `view` is update_geos kwargs; None → fit to the drawn locations.
_BUNDLED_GEOJSON = {
    "europe_countries": (
        _DATA_DIR / "europe_countries.geojson", "properties.NUTS_ID",
        # Clip to continental Europe so outlying territories (Canaries, Cyprus) don't
        # blow out the bounds and shrink the map.
        {"lonaxis_range": [-12, 34], "lataxis_range": [34, 71], "projection_type": "mercator"},
    ),
    "poland_nuts2": (
        _DATA_DIR / "poland_nuts2.geojson", "properties.NUTS_ID", None,
    ),
}

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
                "scope":          {"type": "string"},
                "location_mode":  {"type": "string"},
                "geojson":        {"type": "string", "enum": list(_BUNDLED_GEOJSON)},
                "geojson_path":   {"type": "string"},
                "feature_id_key": {"type": "string"},
                "colorscale":     {"type": "string"},
                "reverse":        {"type": "boolean"},
                "color_midpoint": {"type": "number"},
                "show_labels":    {"type": "boolean"},
                "height":         {"type": "integer", "minimum": 100, "maximum": 2000},
                **_FORMAT_OPTION_SCHEMA,
            },
        },
    },
}

_CARD_STYLE = {
    "background": BG_SURFACE, "borderRadius": CARD_RADIUS, "boxShadow": CARD_SHADOW,
    "padding": "16px", "height": "100%", "boxSizing": "border-box",
}


def _resolve_geojson(opts: dict):
    """Return (geojson_dict, feature_id_key, view) or (None, None, None) for scope maps.

    `view` is a dict of update_geos kwargs framing the map, or None to fit the
    drawn locations.
    """
    name = opts.get("geojson")
    path = opts.get("geojson_path")
    fik  = opts.get("feature_id_key")
    if name:
        if name not in _BUNDLED_GEOJSON:
            raise ValueError(f"choropleth: unknown bundled geojson {name!r}; "
                             f"available: {sorted(_BUNDLED_GEOJSON)}")
        gj_path, default_fik, view = _BUNDLED_GEOJSON[name]
        return json.loads(gj_path.read_text(encoding="utf-8")), (fik or default_fik), view
    if path:
        return json.loads(Path(path).read_text(encoding="utf-8")), (fik or "properties.NUTS_ID"), None
    return None, None, None


def choropleth(*, encoding: dict, filter: dict | None = None, options: dict | None = None) -> html.Div:
    opts = options or {}
    raw_enc = encoding or {}

    loc_ch = parse_channel(raw_enc.get("location"))
    col_ch = parse_channel(raw_enc.get("color"))
    if not (loc_ch and loc_ch.dimension):
        raise ValueError("choropleth: encoding.location must bind a dimension")
    if not (col_ch and col_ch.metric):
        raise ValueError("choropleth: encoding.color must bind a metric")

    loc_col = dimension_column_name(loc_ch)
    metric  = col_ch.metric

    df = semantic_query_data(metric, group_by=[loc_col], filter=filter)
    if df.empty:
        return html.Div("No data", style=_CARD_STYLE)

    colorscale    = opts.get("colorscale", "Blues")
    reverse_cs    = opts.get("reverse", False)
    show_labels   = opts.get("show_labels", False)
    zmid          = opts.get("color_midpoint")
    val_fmt       = opts.get("value_format")

    locations = df[loc_col].astype(str)
    z         = df[metric]
    hover     = [f"{loc}: {format_value(v, val_fmt)}" for loc, v in zip(locations, z)]

    geojson, feature_id_key, view = _resolve_geojson(opts)

    common = dict(
        locations=locations, z=z,
        colorscale=colorscale, reversescale=reverse_cs,
        marker_line_width=0.5, marker_line_color="white",
        hovertext=hover, hoverinfo="text",
        colorbar=dict(thickness=12, len=0.8, outlinewidth=0),
    )
    if zmid is not None:
        common["zmid"] = zmid

    if geojson is not None:
        # Plotly silently drops locations with no matching feature — warn so an author
        # binding `location: geo` without a member filter can see the gap (e.g. aggregate
        # codes like EU27_2020 / EA20, or non-NUTS GUS codes).
        key = feature_id_key.split(".", 1)[-1] if feature_id_key else "NUTS_ID"
        feat_ids = {f.get("properties", {}).get(key) for f in geojson.get("features", [])}
        unmatched = sorted(set(locations) - feat_ids)
        if unmatched:
            logger.warning("choropleth: %d location(s) have no %s feature, dropped from map: %s",
                           len(unmatched), key, unmatched)
        fig = go.Figure(go.Choropleth(geojson=geojson, featureidkey=feature_id_key, **common))
        if view:
            fig.update_geos(visible=False, bgcolor="rgba(0,0,0,0)", **view)
        else:
            fig.update_geos(fitbounds="locations", visible=False, bgcolor="rgba(0,0,0,0)")
    else:
        location_mode = opts.get("location_mode", "ISO-3166-1-alpha-2")
        fig = go.Figure(go.Choropleth(locationmode=location_mode, **common))
        fig.update_geos(
            scope=opts.get("scope", "europe"),
            showframe=False, showcoastlines=False, bgcolor="rgba(0,0,0,0)",
        )
        if show_labels:
            fig.add_trace(go.Scattergeo(
                locations=locations, locationmode=location_mode,
                text=[format_value(v, val_fmt) for v in z],
                mode="text", textfont=dict(size=9, color="white"),
                showlegend=False, hoverinfo="skip",
            ))

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        geo=dict(bgcolor="rgba(0,0,0,0)"),
        paper_bgcolor="rgba(0,0,0,0)",
    )
    # Fill the flex page cell like every other visual instead of baking a fixed
    # pixel height. A baked height taller than the cell's definite-height share
    # (rows split the viewport) overflows downward into the next row — invisible
    # on wide maps (Europe leaves vertical margin) but obvious on tall ones
    # (Poland fills the frame). chart_with_optional_table clears layout.height,
    # turns on a responsive 100%-height graph (.dbr-fill-graph for the mobile
    # pin), and renders the optional CSV download. `options.height` stays in the
    # schema for back-compat but, as with the other fill charts, the desktop
    # height now comes from the cell, not the figure.
    return chart_with_optional_table(fig, df, opts, _CARD_STYLE)
