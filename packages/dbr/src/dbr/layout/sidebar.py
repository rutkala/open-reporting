"""Sidebar — vertical nav strip, full-height left column.

Design:
  - Full-height: fills the outer 100vh flex row — always visible, no external scroll.
  - Brand header: OR logo mark + "Open Reporting" wordmark. Dashboard title lives
    in the page header (right column), not here.
  - Nav links: className="dbr-nav-link" + data-anchor attribute so the scrollspy
    script can highlight the active section.
  - Toggle button: collapses sidebar to 52px icon strip; state persisted in
    localStorage under key ``dbr-sidebar-collapsed``.
  - Portal back-link at the bottom.

All visual tokens (colours, fonts, widths, paddings) come from
``dbr.theme`` (sourced from ``theme.yaml``).
"""
from dash import html

from dbr.layout.loader import SIDEBAR_SHOW_TOGGLE
from dbr.theme import (
    BG_SURFACE,
    BORDER,
    FONT_FAMILY,
    SIDEBAR_WIDTH,
    SIZE_BODY,
    SUBTEXT,
    TEXT,
    TEAL_PRIMARY,
)

# No outer border/radius: the sidebar is a flat white surface distinguished from the
# page canvas by its BG_SURFACE fill + the PAGE_GAP of canvas around it. Carrying no
# border is deliberate — it keeps the sidebar's internal divider lines (brand
# borderBottom, portal-footer borderTop) at exactly the same y as the right column's
# header/footer divider lines, so all four read as two continuous rules across the page
# gap. Re-adding a border would offset those internal lines by 1px (top + bottom) and
# break the alignment contract documented in page_shell.py.
_SIDEBAR_STYLE = {
    "width":         SIDEBAR_WIDTH,
    "flexShrink":    0,
    "background":    BG_SURFACE,
    "boxSizing":     "border-box",
    "fontFamily":    FONT_FAMILY,
    "color":         TEXT,
    "display":       "flex",
    "flexDirection": "column",
    # Full-height: outer container is height:100vh so sidebar fills it.
    "height":        "100%",
    "overflowY":     "auto",
    "overflowX":     "hidden",
    "transition":    "width 0.2s ease",
}

_BRAND_STYLE = {
    "padding":      "14px 20px 14px 20px",
    "borderBottom": f"1px solid {BORDER}",
    "flexShrink":   0,
    "minHeight":    "56px",   # match page header height for visual alignment
    "boxSizing":    "border-box",
    "display":      "flex",
    "alignItems":   "center",
}

# Logo row: badge + wordmark on left, toggle button pushed to the right.
_LOGO_ROW_STYLE = {
    "display":    "flex",
    "alignItems": "center",
    "gap":        "8px",
    "width":      "100%",
}

_LOGO_BADGE_STYLE = {
    "width":          "28px",
    "height":         "28px",
    "borderRadius":   "6px",
    "background":     TEAL_PRIMARY,
    "display":        "flex",
    "alignItems":     "center",
    "justifyContent": "center",
    "color":          "#FFFFFF",
    "fontSize":       "10px",
    "fontWeight":     700,
    "letterSpacing":  "0.5px",
    "flexShrink":     0,
}

_LOGO_NAME_STYLE = {
    "fontSize":   "11px",
    "fontWeight": 600,
    "color":      SUBTEXT,
    "lineHeight": "1.2",
    "whiteSpace": "nowrap",
    "overflow":   "hidden",
}

_TOGGLE_BTN_STYLE = {
    "marginLeft":     "auto",
    "width":          "26px",
    "height":         "26px",
    "borderRadius":   "5px",
    "border":         f"1px solid {BORDER}",
    "background":     BG_SURFACE,
    "cursor":         "pointer",
    "fontSize":       "13px",
    "color":          SUBTEXT,
    "padding":        "0",
    "lineHeight":     "1",
    "display":        "flex",
    "alignItems":     "center",
    "justifyContent": "center",
    "flexShrink":     0,
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
    "padding":    "0 20px",
    "borderTop":  f"1px solid {BORDER}",
    "flexShrink": 0,
    "minHeight":  "48px",     # == page footer height so the two top lines align
    "boxSizing":  "border-box",
    "display":    "flex",
    "alignItems": "center",
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
    """Return the full-height left sidebar.

    ``sections`` is a list of ``(label, anchor_id)`` pairs — one nav link
    per entry. ``dashboard_title`` is unused; the title is shown in the
    page header only.
    """
    logo_row_children: list = [
        html.Div("OR", id="dbr-logo-badge", style=_LOGO_BADGE_STYLE),
        html.Div(
            "Open Reporting",
            id="dbr-logo-name",
            style=_LOGO_NAME_STYLE,
        ),
    ]
    if SIDEBAR_SHOW_TOGGLE:
        logo_row_children.append(
            html.Button(
                "‹",
                id="dbr-sidebar-toggle",
                title="Zwiń / rozwiń panel",
                style=_TOGGLE_BTN_STYLE,
            )
        )

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
        id="dbr-sidebar",
        style=_SIDEBAR_STYLE,
        children=[
            html.Div(
                id="dbr-sidebar-brand",
                style=_BRAND_STYLE,
                children=[html.Div(id="dbr-logo-row", style=_LOGO_ROW_STYLE, children=logo_row_children)],
            ),
            html.Div(id="dbr-sidebar-nav", style=_NAV_SECTION_STYLE, children=[
                html.Div("Nawigacja", className="dbr-nav-label", style=_NAV_LABEL_STYLE),
                html.Nav(children=links, style=_NAV_STYLE),
            ]),
            html.Div(id="dbr-sidebar-footer", style=_FOOTER_STYLE, children=[
                html.A("← Portal", href="/", style=_PORTAL_LINK_STYLE),
            ]),
        ],
    )
