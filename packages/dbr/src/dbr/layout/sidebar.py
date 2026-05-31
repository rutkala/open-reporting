"""Sidebar — vertical nav strip, sticky-positioned on the left edge.

Design:
  - Sticky: stays visible while main content scrolls (position: sticky).
  - Brand header: OR logo mark + "Open Reporting" wordmark + dashboard title.
  - Nav links: className="dbr-nav-link" + data-anchor attribute so the
    scrollspy script injected by make_app can highlight the active section.
  - Portal back-link at the bottom.

All visual tokens (colours, fonts, widths, paddings) come from
``dbr.theme`` (sourced from ``theme.yaml``).
"""
from dash import html

from dbr.theme import (
    BG_SURFACE,
    BORDER,
    CARD_RADIUS,
    CARD_SHADOW,
    FONT_FAMILY,
    SIDEBAR_WIDTH,
    SIZE_BODY,
    SUBTEXT,
    TEXT,
    TEAL_PRIMARY,
)

_SIDEBAR_STYLE = {
    "width":         SIDEBAR_WIDTH,
    "flexShrink":    0,
    "background":    BG_SURFACE,
    "borderRadius":  CARD_RADIUS,
    "boxShadow":     CARD_SHADOW,
    "boxSizing":     "border-box",
    "fontFamily":    FONT_FAMILY,
    "color":         TEXT,
    "display":       "flex",
    "flexDirection": "column",
    # Sticky: the sidebar stays in the viewport while the main area scrolls.
    "position":      "sticky",
    "top":           "8px",
    "height":        "calc(100vh - 16px)",
    "overflowY":     "auto",
    "overflowX":     "hidden",
}

_BRAND_STYLE = {
    "padding":      "20px 20px 16px 20px",
    "borderBottom": f"1px solid {BORDER}",
    "flexShrink":   0,
}

_LOGO_ROW_STYLE = {
    "display":        "flex",
    "alignItems":     "center",
    "gap":            "8px",
    "marginBottom":   "10px",
}

_LOGO_BADGE_STYLE = {
    "width":           "28px",
    "height":          "28px",
    "borderRadius":    "6px",
    "background":      TEAL_PRIMARY,
    "display":         "flex",
    "alignItems":      "center",
    "justifyContent":  "center",
    "color":           "#FFFFFF",
    "fontSize":        "10px",
    "fontWeight":      700,
    "letterSpacing":   "0.5px",
    "flexShrink":      0,
}

_LOGO_NAME_STYLE = {
    "fontSize":   "11px",
    "fontWeight": 600,
    "color":      SUBTEXT,
    "lineHeight": "1.2",
}

_DASH_TITLE_STYLE = {
    "fontSize":   "14px",
    "fontWeight": 700,
    "color":      TEXT,
    "lineHeight": "1.3",
}

_NAV_SECTION_STYLE = {
    "padding": "14px 0 8px 0",
    "flex":    1,
    "display": "flex",
    "flexDirection": "column",
}

_NAV_LABEL_STYLE = {
    "fontSize":      "10px",
    "fontWeight":    600,
    "color":         SUBTEXT,
    "letterSpacing": "0.08em",
    "textTransform": "uppercase",
    "padding":       "0 20px 6px 20px",
}

_NAV_STYLE = {
    "display":       "flex",
    "flexDirection": "column",
}

_LINK_STYLE = {
    "display":        "block",
    "padding":        "8px 20px 8px 20px",
    "color":          SUBTEXT,
    "fontSize":       SIZE_BODY,
    "textDecoration": "none",
    "borderLeft":     "3px solid transparent",
    "lineHeight":     "1.4",
}

_FOOTER_STYLE = {
    "padding":    "12px 20px",
    "borderTop":  f"1px solid {BORDER}",
    "flexShrink": 0,
}

_PORTAL_LINK_STYLE = {
    "fontSize":       "12px",
    "color":          SUBTEXT,
    "textDecoration": "none",
    "display":        "flex",
    "alignItems":     "center",
    "gap":            "4px",
}


def build_sidebar(
    sections: list[tuple[str, str]],
    dashboard_title: str = "",
) -> html.Aside:
    """Return the standard left-edge sticky sidebar.

    ``sections`` is a list of ``(label, anchor_id)`` pairs — one nav link
    per entry. ``dashboard_title`` is shown under the OR brand mark.
    """
    brand_children: list = [
        html.Div(style=_LOGO_ROW_STYLE, children=[
            html.Div("OR", style=_LOGO_BADGE_STYLE),
            html.Div("Open Reporting", style=_LOGO_NAME_STYLE),
        ]),
    ]
    if dashboard_title:
        brand_children.append(html.Div(dashboard_title, style=_DASH_TITLE_STYLE))

    links = [
        html.A(
            label,
            href=f"#{anchor}",
            className="dbr-nav-link",
            style=_LINK_STYLE,
            **{"data-anchor": anchor},
        )
        for label, anchor in sections
    ]

    return html.Aside(
        style=_SIDEBAR_STYLE,
        children=[
            html.Div(style=_BRAND_STYLE, children=brand_children),
            html.Div(style=_NAV_SECTION_STYLE, children=[
                html.Div("Nawigacja", style=_NAV_LABEL_STYLE),
                html.Nav(children=links, style=_NAV_STYLE),
            ]),
            html.Div(style=_FOOTER_STYLE, children=[
                html.A("← Portal", href="/", style=_PORTAL_LINK_STYLE),
            ]),
        ],
    )
