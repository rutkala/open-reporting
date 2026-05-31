"""Page header — fixed bar at the top of the right column (dashboard canvas).

Shows only the dashboard title and optional subtitle. The OR logo and
"Open Reporting" wordmark live exclusively in the sidebar. All visual
tokens come from ``dbr.theme``; behaviour flags from ``dbr.layout.loader``.
"""
from dash import html

from dbr.theme import (
    BG_SURFACE,
    BORDER,
    CARD_SHADOW,
    FONT_FAMILY,
    SUBTEXT,
    TEXT,
)

_HEADER_STYLE = {
    "display":      "flex",
    "alignItems":   "center",
    "padding":      "0 24px",
    "background":   BG_SURFACE,
    "borderBottom": f"1px solid {BORDER}",
    "boxShadow":    CARD_SHADOW,
    "fontFamily":   FONT_FAMILY,
    "flexShrink":   0,
    "minHeight":    "56px",
    "boxSizing":    "border-box",
}

_TITLE_STYLE = {
    "fontSize":   "18px",
    "fontWeight": 700,
    "color":      TEXT,
    "lineHeight": "1.2",
}

_SUBTITLE_STYLE = {
    "fontSize":  "13px",
    "color":     SUBTEXT,
    "lineHeight": "1.3",
    "marginTop": "2px",
}


def build_header(title: str = "", subtitle: str = "") -> html.Header:
    """Return the fixed page header bar showing only the dashboard title."""
    children = []
    if title:
        children.append(html.Div(title, style=_TITLE_STYLE))
    if subtitle:
        children.append(html.Div(subtitle, style=_SUBTITLE_STYLE))

    title_block = html.Div(
        children,
        style={"display": "flex", "flexDirection": "column"},
    )

    return html.Header(
        id="dbr-page-header",
        style=_HEADER_STYLE,
        children=[title_block],
    )
