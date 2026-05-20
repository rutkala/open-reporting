"""Sidebar — vertical nav strip on the left edge.

Single-page mode: pass ``sections=[(label, anchor_id), ...]`` and each
link scrolls to the matching ``<H2 id="anchor_id">`` on the same page.

All visual tokens (colours, fonts, widths, paddings) come from
``dbr.theme`` (sourced from ``theme.yaml``).
"""
from dash import html

from dbr.theme import (
    BG_SURFACE,
    CARD_RADIUS,
    CARD_SHADOW,
    FONT_FAMILY,
    NAV_LINK_PADDING,
    SIDEBAR_PADDING,
    SIDEBAR_WIDTH,
    SIZE_BODY,
    SUBTEXT,
    TEXT,
)

_SIDEBAR_STYLE = {
    "width":        SIDEBAR_WIDTH,
    "flexShrink":   0,
    "background":   BG_SURFACE,
    "borderRadius": CARD_RADIUS,
    "boxShadow":    CARD_SHADOW,
    "padding":      SIDEBAR_PADDING,
    "boxSizing":    "border-box",
    "fontFamily":   FONT_FAMILY,
    "color":        TEXT,
    "display":      "flex",
    "flexDirection": "column",
}

_NAV_STYLE = {
    "display":       "flex",
    "flexDirection": "column",
}

_LINK_STYLE = {
    "display":        "block",
    "padding":        NAV_LINK_PADDING,
    "color":          SUBTEXT,
    "fontSize":       SIZE_BODY,
    "textDecoration": "none",
}


def build_sidebar(sections: list[tuple[str, str]]) -> html.Aside:
    """Return the standard left-edge sidebar.

    ``sections`` is a list of ``(label, anchor_id)`` pairs — one nav
    link per pair. Each link points to ``#anchor_id`` on the same page.
    """
    links = [
        html.A(label, href=f"#{anchor}", style=_LINK_STYLE)
        for label, anchor in sections
    ]
    return html.Aside(
        style=_SIDEBAR_STYLE,
        children=html.Nav(children=links, style=_NAV_STYLE),
    )
