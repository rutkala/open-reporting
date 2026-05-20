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
from dash import html

from dbr.layout.loader import SIDEBAR_ENABLED, SIDEBAR_POSITION
from dbr.layout.sidebar import build_sidebar
from dbr.theme import (
    BG_PAGE,
    FONT_FAMILY,
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
    "flex":    1,
    "padding": MAIN_PADDING,
}

_SECTION_HEADING_STYLE = {
    "fontSize":     SIZE_SECTION_HEADING,
    "fontWeight":   WEIGHT_SECTION_HEADING,
    "color":        TEXT,
    "marginTop":    SECTION_TOP_GAP,
    "marginBottom": SECTION_BOTTOM_GAP,
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


def page_shell(sections: list[tuple[str, str, list[list[tuple[object, str | None]]]]]) -> html.Div:
    """Return the full page tree (sidebar + main canvas) for ``app.layout``.

    ``sections`` is a list of ``(title, anchor_id, rows)`` where each
    row is a list of ``(component, width-or-None)`` tuples.

    Chrome behaviour (sidebar on/off, sidebar position) comes from
    ``layout.yaml``.
    """
    sidebar_pairs = [(label, anchor) for label, anchor, _ in sections]

    main_children: list = []
    for label, anchor, rows in sections:
        main_children.append(html.H2(label, id=anchor, style=_SECTION_HEADING_STYLE))
        for row in rows:
            flex_items = [_wrap_item(component, width) for component, width in row]
            main_children.append(html.Div(flex_items, style=_ROW_STYLE))

    main = html.Main(style=_MAIN_STYLE, children=main_children)

    if not SIDEBAR_ENABLED:
        return html.Div(style=_PAGE_STYLE, children=[main])

    sidebar = build_sidebar(sections=sidebar_pairs)
    children = [sidebar, main] if SIDEBAR_POSITION == "left" else [main, sidebar]
    return html.Div(style=_PAGE_STYLE, children=children)
