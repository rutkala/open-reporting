"""Page header — full-width bar pinned above the sidebar + main canvas.

Contains the OR brand mark, dashboard title, and optional subtitle.
All visual tokens come from ``dbr.theme``; behaviour flags come from
``dbr.layout.loader``.
"""
from dash import html

from dbr.theme import (
    BG_SURFACE,
    BORDER,
    CARD_SHADOW,
    FONT_FAMILY,
    SUBTEXT,
    TEXT,
    TEAL_PRIMARY,
)

_HEADER_STYLE = {
    "display":      "flex",
    "alignItems":   "center",
    "padding":      "12px 24px",
    "background":   BG_SURFACE,
    "borderBottom": f"1px solid {BORDER}",
    "boxShadow":    CARD_SHADOW,
    "fontFamily":   FONT_FAMILY,
    "flexShrink":   0,
    "gap":          "16px",
    "boxSizing":    "border-box",
}

_LOGO_BADGE_STYLE = {
    "width":          "32px",
    "height":         "32px",
    "borderRadius":   "7px",
    "background":     TEAL_PRIMARY,
    "display":        "flex",
    "alignItems":     "center",
    "justifyContent": "center",
    "color":          "#FFFFFF",
    "fontSize":       "11px",
    "fontWeight":     700,
    "letterSpacing":  "0.5px",
    "flexShrink":     0,
}

_WORDMARK_STYLE = {
    "fontSize":   "13px",
    "fontWeight": 600,
    "color":      SUBTEXT,
    "whiteSpace": "nowrap",
}

_DIVIDER_STYLE = {
    "width":      "1px",
    "height":     "28px",
    "background": BORDER,
    "flexShrink": 0,
}

_TITLE_STYLE = {
    "fontSize":   "18px",
    "fontWeight": 700,
    "color":      TEXT,
    "lineHeight": "1.2",
}

_SUBTITLE_STYLE = {
    "fontSize":   "13px",
    "color":      SUBTEXT,
    "lineHeight": "1.3",
    "marginTop":  "2px",
}


def build_header(title: str = "", subtitle: str = "") -> html.Header:
    """Return the full-width page header bar.

    ``title`` is the dashboard title; ``subtitle`` is an optional one-liner
    description sourced from ``dashboard.yml``.
    """
    title_block_children = []
    if title:
        title_block_children.append(html.Div(title, style=_TITLE_STYLE))
    if subtitle:
        title_block_children.append(html.Div(subtitle, style=_SUBTITLE_STYLE))

    brand_children: list = [
        html.Div("OR", style=_LOGO_BADGE_STYLE),
        html.Div("Open Reporting", style=_WORDMARK_STYLE),
    ]
    if title_block_children:
        brand_children.append(html.Div(style=_DIVIDER_STYLE))
        brand_children.append(html.Div(title_block_children, style={"display": "flex", "flexDirection": "column"}))

    return html.Header(
        id="dbr-page-header",
        style=_HEADER_STYLE,
        children=brand_children,
    )
