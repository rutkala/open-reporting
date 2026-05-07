"""
Map chart variants.
KB reference: team/knowledge-base/visualization/charts/map.md

choropleth_map — filled countries/regions by value
bubble_map     — sized bubbles at geographic points
"""
import plotly.graph_objects as go

from complex_dashboard.assets.theme import (
    AZURE_1, TEAL_1, TEAL_PALE, BORDER, SUBTEXT, TEXT, FONT_FAMILY, SLATE_4,
)
from complex_dashboard.assets.components import PLOT_H, PLOT_H_TALL, _chart

# ── Map-specific colour constants ─────────────────────────────────────────────
_MAP_OCEAN_COLOR = "#EEF3F7"   # light blue-grey for ocean/water fill
_MAP_DIVERGING_MID = "#FFFFFF"  # white midpoint for diverging colour scale


def choropleth_map(title, locations, values, subtitle="",
                   scope="europe", location_mode="ISO-3",
                   color_scale="teal", hover_labels=None):
    """
    Choropleth (filled) map — regions coloured by value.

    Args:
        locations:     list of ISO-3 country codes (e.g. "POL", "DEU")
        values:        list of numeric values
        scope:         "europe" | "world" | "asia" | "africa" | "north america" | "south america"
        location_mode: "ISO-3" | "country names" | "USA-states"
        color_scale:   "teal" (sequential) | "diverging" (neg→white→pos)
        hover_labels:  list of label strings for hover (default: location codes)
    """
    if color_scale == "diverging":
        cscale = [[0, "#C0503A"], [0.5, _MAP_DIVERGING_MID], [1, "#4A9B6F"]]
    else:
        cscale = [[0, TEAL_PALE], [1, TEAL_1]]

    labels = hover_labels or locations

    fig = go.Figure(go.Choropleth(
        locations=locations,
        z=values,
        locationmode=location_mode,
        colorscale=cscale,
        text=labels,
        hovertemplate="<b>%{text}</b><br>Wartość: %{z}<extra></extra>",
        marker_line_color="white",
        marker_line_width=0.5,
        colorbar=dict(
            thickness=12, len=0.7,
            tickfont=dict(size=10, color=SUBTEXT),
            outlinewidth=0,
        ),
    ))

    fig.update_geos(
        scope=scope,
        showcoastlines=True, coastlinecolor=BORDER,
        showland=True, landcolor=SLATE_4,
        showocean=True, oceancolor=_MAP_OCEAN_COLOR,
        showframe=False,
        projection_type="natural earth",
    )

    h = PLOT_H_TALL
    fig.update_layout({
        "height": h,
        "margin": dict(l=0, r=0, t=4, b=0),
        "paper_bgcolor": "rgba(0,0,0,0)",
        "font": dict(family=FONT_FAMILY, color=TEXT, size=12),
        "showlegend": False,
    })

    return _chart(title=title, subtitle=subtitle, figure=fig, height=h)


def bubble_map(title, lat, lon, size, labels, subtitle="",
               scope="europe", color=None):
    """
    Bubble map — sized circles at geographic coordinates.

    Args:
        lat:    list of latitudes
        lon:    list of longitudes
        size:   list of values for bubble size (proportional to area)
        labels: list of point labels
        scope:  geographic scope
        color:  bubble colour (default AZURE_1)
    """
    import math
    max_s = max(abs(s) for s in size) if size else 0
    if max_s == 0:
        max_s = 1  # all-zero or empty — render uniform minimum bubbles
    scaled = [math.sqrt(abs(s) / max_s) * 30 + 5 for s in size]

    fig = go.Figure(go.Scattergeo(
        lat=lat,
        lon=lon,
        text=labels,
        marker=dict(
            size=scaled,
            color=color or AZURE_1,
            opacity=0.7,
            line=dict(color="white", width=0.5),
            sizemode="diameter",
        ),
        hovertemplate="<b>%{text}</b><br>Wartość: %{customdata}<extra></extra>",
        customdata=size,
    ))

    fig.update_geos(
        scope=scope,
        showcoastlines=True, coastlinecolor=BORDER,
        showland=True, landcolor=SLATE_4,
        showocean=True, oceancolor=_MAP_OCEAN_COLOR,
        showframe=False,
        projection_type="natural earth",
    )

    h = PLOT_H_TALL
    fig.update_layout({
        "height": h,
        "margin": dict(l=0, r=0, t=4, b=0),
        "paper_bgcolor": "rgba(0,0,0,0)",
        "font": dict(family=FONT_FAMILY, color=TEXT, size=12),
        "showlegend": False,
    })

    return _chart(title=title, subtitle=subtitle, figure=fig, height=h)
