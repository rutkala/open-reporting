"""page_shell — outer page wrapper that composes sidebar + main canvas.

A dashboard passes a list of sections — each section is
``(title, anchor_id, rows)`` where rows is a list of rows, and each row
is a list of ``(component, width-or-None)`` tuples. Sections render as
H2 headings with anchor ids; rows render as flex containers so items
sit side by side.

Visual tokens (colours, fonts, paddings, heading sizes, row gap) come
from ``dbr.theme`` (sourced from ``theme.yaml``).
Chrome behaviour flags (sidebar enabled, sidebar position) come from
``dbr.layout.loader`` (sourced from ``layout.yaml``).
"""
from dash import dcc, html

from dbr.layout.loader import SIDEBAR_ENABLED, SIDEBAR_POSITION
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
    SECTION_BOTTOM_GAP,
    SECTION_TOP_GAP,
    SIZE_SECTION_HEADING,
    TEXT,
    WEIGHT_SECTION_HEADING,
)

_PAGE_STYLE = {
    "display":    "flex",
    "gap":        PAGE_GAP,
    "padding":    PAGE_PADDING,
    "minHeight":  "100vh",
    "background": BG_PAGE,
    "color":      TEXT,
    "fontFamily": FONT_FAMILY,
    "boxSizing":  "border-box",
}

_MAIN_STYLE = {
    "flex":      1,
    "padding":   MAIN_PADDING,
    "maxWidth":  MAIN_MAX_WIDTH,    # cap on wide monitors so charts don't stretch infinitely
    "minWidth":  0,                  # let inner content shrink instead of overflowing
    "boxSizing": "border-box",       # padding counts inside maxWidth
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
) -> html.Div:
    """Return the full page tree (sidebar + main canvas) for ``app.layout``.

    ``sections`` is a list of ``(title, anchor_id, rows)`` where each
    row is a 3-tuple of ``(row_title_or_None, row_prose_or_None,
    [(component, width-or-None), ...])``. When ``row_title`` is set an
    H3 sub-heading renders above the row; when ``row_prose`` is set a
    Markdown paragraph renders below the title and above the items
    (narrative bridge between charts per rubric dim 17).

    ``dashboard_title`` is the human-readable title shown in the sidebar
    brand area (sourced from ``dashboard.yml``).

    Chrome behaviour (sidebar on/off, sidebar position) comes from
    ``layout.yaml``.
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

    if not SIDEBAR_ENABLED:
        return html.Div(style=_PAGE_STYLE, children=[main])

    sidebar = build_sidebar(sections=sidebar_pairs, dashboard_title=dashboard_title)
    children = [sidebar, main] if SIDEBAR_POSITION == "left" else [main, sidebar]
    return html.Div(style=_PAGE_STYLE, children=children)
