"""Page footer — full-width bar pinned below the sidebar + main canvas.

Shows data source attribution and the OR brand. Optional last-updated
indicator sourced from ``dashboard.yml``. All visual tokens come from
``dbr.theme``; behaviour flags come from ``dbr.layout.loader``.
"""
from dash import html

from dbr.layout.loader import FOOTER_SHOW_SOURCE, FOOTER_SHOW_UPDATED
from dbr.theme import (
    BG_SURFACE,
    BORDER,
    FONT_FAMILY,
    SUBTEXT,
    TEAL_PRIMARY,
)

_FOOTER_STYLE = {
    "display":     "flex",
    "alignItems":  "center",
    "padding":     "10px 24px",
    "background":  BG_SURFACE,
    "borderTop":   f"1px solid {BORDER}",
    "fontFamily":  FONT_FAMILY,
    "flexShrink":  0,
    "boxSizing":   "border-box",
    "gap":         "12px",
}

_SOURCE_STYLE = {
    "fontSize": "12px",
    "color":    SUBTEXT,
    "flex":     1,
}

_OR_STYLE = {
    "fontSize":   "12px",
    "color":      SUBTEXT,
    "display":    "flex",
    "alignItems": "center",
    "gap":        "6px",
    "whiteSpace": "nowrap",
}

_OR_BADGE_STYLE = {
    "width":          "18px",
    "height":         "18px",
    "borderRadius":   "4px",
    "background":     TEAL_PRIMARY,
    "display":        "flex",
    "alignItems":     "center",
    "justifyContent": "center",
    "color":          "#FFFFFF",
    "fontSize":       "8px",
    "fontWeight":     700,
    "flexShrink":     0,
}

_SEPARATOR_STYLE = {
    "color":   SUBTEXT,
    "opacity": "0.4",
}


def build_footer(source: str = "", updated: str = "") -> html.Footer:
    """Return the full-width page footer bar.

    ``source`` is the data attribution string (e.g. "Źródło: Eurostat").
    ``updated`` is a last-updated indicator (e.g. "Dane: 2024").
    Both are sourced from ``dashboard.yml``.
    """
    left_parts = []
    if FOOTER_SHOW_SOURCE and source:
        left_parts.append(source)
    if FOOTER_SHOW_UPDATED and updated:
        if left_parts:
            left_parts.append(" · ")
        left_parts.append(updated)

    left = html.Div(
        "".join(left_parts),
        style=_SOURCE_STYLE,
    )

    right = html.Div(
        style=_OR_STYLE,
        children=[
            html.Div("OR", style=_OR_BADGE_STYLE),
            html.Span("Open Reporting"),
        ],
    )

    return html.Footer(
        id="dbr-page-footer",
        style=_FOOTER_STYLE,
        children=[left, right],
    )
