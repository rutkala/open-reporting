"""page_shell — outer page wrapper that composes header + (sidebar + main canvas) + footer.

Layout: full-viewport flex column, no page scroll.
- Header: full-width top bar — spans sidebar + content column so its borderBottom forms
  one continuous horizontal rule across the entire page.
- Middle row: flex row — sidebar (left) + scrollable main canvas (right, flex:1).
- Footer: full-width bottom bar — same full-width treatment as header.

Visual tokens (colours, fonts, paddings, heading sizes, row gap) come
from ``dbr.theme`` (sourced from ``theme.yaml``).
Chrome behaviour flags (sidebar enabled, sidebar position, header/footer
enabled) come from ``dbr.layout.loader`` (sourced from ``layout.yaml``).
"""
from dash import dcc, html

from dbr.layout.footer import build_footer
from dbr.layout.header import build_header
from dbr.layout.loader import (
    FOOTER_ENABLED,
    HEADER_ENABLED,
    HEADER_SHOW_TITLE,
    SIDEBAR_ENABLED,
    SIDEBAR_POSITION,
)
from dbr.layout.sidebar import build_sidebar
from dbr.theme import (
    BG_PAGE,
    BORDER,
    FONT_FAMILY,
    MAIN_MAX_WIDTH,
    MAIN_PADDING,
    PAGE_GAP,
    PAGE_PADDING,
    ROW_GAP,
    SECTION_TOP_GAP,
    SIZE_SECTION_HEADING,
    TEXT,
    WEIGHT_SECTION_HEADING,
)

# Outer column: header (auto) → middle row (flex:1) → footer (auto).
# Fills the full viewport; `padding` insets everything from the browser edge.
# No gap between rows — header/footer separator lines directly abut the middle row.
_PAGE_OUTER_STYLE = {
    "display":       "flex",
    "flexDirection": "column",
    "height":        "100vh",
    "overflow":      "hidden",
    "padding":       PAGE_PADDING,
    "boxSizing":     "border-box",
    "background":    BG_PAGE,
    "color":         TEXT,
    "fontFamily":    FONT_FAMILY,
}

# Middle row: sidebar (fixed width) + scrollable main canvas (flex:1).
# `gap` provides visual separation between sidebar and content column.
_PAGE_MIDDLE_STYLE = {
    "display":   "flex",
    "flex":      "1",
    "minHeight": 0,
    "overflow":  "hidden",
    "gap":       PAGE_GAP,
}

# Scrollable wrapper around the main canvas — scrollspy listens on this.
# flex:1 + minWidth/Height:0 lets it fill the remaining space in the middle row.
_MAIN_SCROLL_STYLE = {
    "flex":           "1",
    "minWidth":       0,
    "minHeight":      0,
    "overflowY":      "auto",
    "overflowX":      "hidden",
    "scrollBehavior": "smooth",
}

_MAIN_STYLE = {
    "padding":   MAIN_PADDING,
    "maxWidth":  MAIN_MAX_WIDTH,
    "minWidth":  0,
    "boxSizing": "border-box",
}

_SECTION_HEADING_STYLE = {
    "fontSize":     SIZE_SECTION_HEADING,
    "fontWeight":   WEIGHT_SECTION_HEADING,
    "color":        TEXT,
    "marginTop":    SECTION_TOP_GAP,
    "marginBottom": "16px",
    "paddingBottom": "12px",
    "borderBottom": f"1px solid {BORDER}",
}

_ROW_HEADING_STYLE = {
    "fontSize":     "16px",
    "fontWeight":   600,
    "color":        TEXT,
    "marginTop":    "16px",
    "marginBottom": "8px",
}

_ROW_PROSE_STYLE = {
    "fontSize":     "13px",
    "color":        TEXT,
    "lineHeight":   "1.5",
    "marginTop":    "0",
    "marginBottom": "12px",
    "maxWidth":     "780px",   # readable line length — narrative shouldn't span full canvas
}

_ROW_STYLE = {
    "display":      "flex",
    "gap":          ROW_GAP,
    "marginBottom": ROW_GAP,
    "alignItems":   "stretch",
}


def _wrap_item(component, width: str | None) -> html.Div:
    """Wrap one visual in a flex-item div with the requested width."""
    style: dict = {"minWidth": 0}                       # let inner content shrink
    style["flex"] = f"0 0 {width}" if width else "1"
    return html.Div(component, style=style)


def page_shell(
    sections: list[tuple[str, str, list[tuple[str | None, str | None, list[tuple[object, str | None]]]]]],
    dashboard_title: str = "",
    dashboard_subtitle: str = "",
    footer_source: str = "",
    footer_updated: str = "",
) -> html.Div:
    """Return the full page tree (header + sidebar + main canvas + footer) for ``app.layout``.

    ``sections`` is a list of ``(title, anchor_id, rows)`` where each
    row is a 3-tuple of ``(row_title_or_None, row_prose_or_None,
    [(component, width-or-None), ...])``. When ``row_title`` is set an
    H3 sub-heading renders above the row; when ``row_prose`` is set a
    Markdown paragraph renders below the title and above the items
    (narrative bridge between charts per rubric dim 17).

    ``dashboard_title`` is the human-readable title (sourced from
    ``dashboard.yml``). Shown in the sidebar brand area and, when
    ``header.enabled`` is true, in the full-width page header.

    ``dashboard_subtitle`` is an optional one-liner shown beneath the
    title in the page header only.

    ``footer_source`` and ``footer_updated`` populate the footer bar
    when ``footer.enabled`` is true.

    Chrome behaviour (header/sidebar/footer on/off, positions) comes
    from ``layout.yaml``.
    """
    sidebar_pairs = [(label, anchor) for label, anchor, _ in sections]

    main_children: list = []
    for label, anchor, rows in sections:
        main_children.append(html.H2(label, id=anchor, style=_SECTION_HEADING_STYLE))
        for row_title, row_prose, row_items in rows:
            if row_title:
                main_children.append(html.H3(row_title, style=_ROW_HEADING_STYLE))
            if row_prose:
                main_children.append(dcc.Markdown(row_prose, style=_ROW_PROSE_STYLE))
            flex_items = [_wrap_item(component, width) for component, width in row_items]
            main_children.append(html.Div(flex_items, style=_ROW_STYLE))

    main = html.Main(style=_MAIN_STYLE, children=main_children)

    scroll_body = html.Div(id="dbr-main-scroll", style=_MAIN_SCROLL_STYLE, children=[main])

    # Middle row: sidebar (if enabled) + scrollable main area.
    if SIDEBAR_ENABLED:
        sidebar = build_sidebar(sections=sidebar_pairs, dashboard_title=dashboard_title)
        middle_children = [sidebar, scroll_body] if SIDEBAR_POSITION == "left" else [scroll_body, sidebar]
    else:
        middle_children = [scroll_body]
    middle_row = html.Div(style=_PAGE_MIDDLE_STYLE, children=middle_children)

    # Outer column: full-width header → middle row → full-width footer.
    # Header and footer span across both the sidebar and the content column so
    # their separator lines form one continuous horizontal rule — no horizontal
    # gap between sidebar and content breaks the alignment.
    outer_children: list = []
    if HEADER_ENABLED:
        header_title = dashboard_title if HEADER_SHOW_TITLE else ""
        outer_children.append(build_header(title=header_title, subtitle=dashboard_subtitle))
    outer_children.append(middle_row)
    if FOOTER_ENABLED:
        outer_children.append(build_footer(source=footer_source, updated=footer_updated))

    return html.Div(style=_PAGE_OUTER_STYLE, children=outer_children)
