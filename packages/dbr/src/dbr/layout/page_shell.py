"""page_shell — outer page wrapper that composes sidebar + (header + main canvas + footer).

Layout: full-viewport flex row, no page scroll.
- Sidebar: left column, fills 100vh, internal scroll if nav overflows. Its internal
  divider lines (brand borderBottom, portal-footer borderTop) sit at the SAME y as the
  right column's header borderBottom and footer borderTop — see the alignment note below.
- Right column: CSS-Grid column — header (fixed) + scrollable main + footer (fixed).

Line alignment (the contract this layout exists to honour):
  The sidebar carries NO outer border (see sidebar.py), so its first child (brand) and
  last child (portal-footer) start/end at exactly the same y as the right column's header
  and footer. With brand height == header height and sidebar-footer height == page-footer
  height, the four horizontal divider lines line up across the page gap as two continuous
  rules. Do not re-add an outer border to the sidebar without compensating both offsets.

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
    MAIN_PADDING,
    PAGE_GAP,
    PAGE_PADDING,
    ROW_GAP,
    SIZE_SECTION_HEADING,
    TEXT,
    WEIGHT_SECTION_HEADING,
)

# Outer row: sidebar + right column, fills the full viewport — no page scroll.
# `padding` insets the whole app from the viewport edge on all four sides so every
# panel floats on the page canvas with a visible margin to the browser border.
# `gap` separates the sidebar from the right column. Sidebar and right column are
# both align-stretch children, so their TOP and BOTTOM edges are identical — this
# is what lets their respective divider lines align (see module docstring).
_PAGE_OUTER_STYLE = {
    "display":    "flex",
    "height":     "100vh",
    "overflow":   "hidden",
    "padding":    PAGE_PADDING,
    "gap":        PAGE_GAP,
    "boxSizing":  "border-box",
    "background": BG_PAGE,
    "color":      TEXT,
    "fontFamily": FONT_FAMILY,
}

# Right column: header (fixed) + scrollable main + footer (fixed). Uses CSS
# Grid rather than flex-column because the "fixed-header / scroll-body /
# pinned-footer" pattern is browser-fragile under flexbox: the scroll body's
# default min-height:auto lets it grow to full content height, pushing the
# footer past this column's `overflow:hidden` clip boundary — where it is both
# invisible AND unreachable (you can't scroll to a clipped sibling). Flexbox's
# `minHeight:0` is supposed to prevent that but isn't honoured consistently
# across browsers/zoom. Grid solves it structurally: the scroll track is
# declared `minmax(0, 1fr)` (see page_shell()), which explicitly permits the
# track to shrink below its content, guaranteeing header + footer always keep
# their `auto` (content) height pinned in the viewport regardless of body length.
#
# NO row gap (gap: 0): the header sits flush on top of the scroll body and the
# footer flush beneath it, so the header's bottom border IS the line where content
# disappears as it scrolls up (and the footer's top border the line where it
# disappears scrolling down). A canvas gap here would detach the header from that
# scroll-clip line, leaving a dead band. The right column is therefore one
# contiguous panel — header | scroll | footer — mirroring the sidebar (also a single
# panel), and its borderBottom/borderTop divider lines still align with the sidebar's
# at the same y (the gap change moves no row edge; it only grows the scroll track).
_PAGE_RIGHT_STYLE = {
    "display":   "grid",
    "flex":      "1",
    "minWidth":  0,
    "minHeight": 0,
    "overflow":  "hidden",
    "gap":       "0",
    # `gridTemplateRows` is assembled per-page in page_shell() from the
    # enabled chrome (header? scroll, footer?) — the scroll row is the only
    # `minmax(0, 1fr)` track; header/footer rows are `auto`.
}

# Scrollable wrapper around the page stack — scrollspy listens on this.
# It occupies the grid's `minmax(0, 1fr)` track (a definite height), so its direct
# children can size against that viewport via `height: 100%` (see _PAGE_SECTION_STYLE).
# minHeight:0 is belt-and-braces so the element itself never imposes a min-content
# floor on that track.
#
# FIXED-PAGE model: each section is a Power BI–style fixed canvas — exactly one viewport
# tall, never more, never less. `scrollSnapType: y mandatory` snaps to exactly one page
# at a time so clicking an anchor (or scrolling) shows ONE page and never bleeds the
# next/previous into view. Because each page is exactly the viewport height (with
# `overflow: hidden`), nothing scrolls *under* the header/footer within a page, so the
# page's own MAIN_PADDING provides clean breathing space against the chrome at rest —
# no edge-fade mask needed (the old mask read as a shadow; real padding is the space).
_MAIN_SCROLL_STYLE = {
    "minHeight":        0,
    "overflowY":        "auto",
    "overflowX":        "hidden",
    "scrollBehavior":   "smooth",
    "scrollSnapType":   "y mandatory",
}

# One "page": a FIXED full-viewport canvas holding a section's heading + rows.
# `height: 100%` (not min-height) resolves against the scroll container's definite
# height, so every page is exactly one screen — `overflow: hidden` clips anything that
# would spill, guaranteeing no page overlaps its neighbour. Flex-column so the heading
# takes its natural height and the row body distributes the remaining vertical space
# across the grow rows (see page_shell()). Full width (no max-width cap): content spans
# the whole canvas, leaving only MAIN_PADDING as the inset — symmetric with the
# sidebar↔canvas gap, and the same padding becomes the space against header/footer.
_PAGE_SECTION_STYLE = {
    "height":          "100%",
    "padding":         MAIN_PADDING,
    "minWidth":        0,
    "boxSizing":       "border-box",
    "display":         "flex",
    "flexDirection":   "column",
    "overflow":        "hidden",
    "scrollSnapAlign": "start",
}

# Minimum height for a grow (chart) row. A fixed one-viewport page divides its space
# across grow rows, but a chart squeezed below this floor becomes an unreadable sliver
# (Plotly's ~88px of vertical margins eat a short plot area). So grow rows never shrink
# below this; if a page's content needs more than one viewport even at the floor, the
# page BODY scrolls internally (the page itself stays a fixed one-viewport tile that
# snaps as a unit, so neighbouring pages never bleed into view — you still only ever see
# one page's content). When content fits, grow rows stretch past the floor to fill.
_MIN_GROW_ROW_HEIGHT = "260px"

# The page body: everything below the H2 heading. Flex-column so its rows distribute the
# remaining vertical space (grow rows stretch, KPI/slicer rows keep natural height).
# minHeight:0 lets it shrink within the fixed page. `overflowY: auto` is the graceful
# fallback for over-dense pages (see _MIN_GROW_ROW_HEIGHT); overflowX hidden prevents any
# horizontal scrollbar.
_PAGE_BODY_STYLE = {
    "flex":          "1 1 0",
    "minHeight":     0,
    "display":       "flex",
    "flexDirection": "column",
    "overflowY":     "auto",
    "overflowX":     "hidden",
}

# Every heading now sits at the top of its own full-viewport page, so there is no
# inter-section gap to open — marginTop is always 0 (the page's top padding provides
# the breathing room beneath the header / above the heading).
_SECTION_HEADING_STYLE = {
    "fontSize":     SIZE_SECTION_HEADING,
    "fontWeight":   WEIGHT_SECTION_HEADING,
    "color":        TEXT,
    "marginTop":    "0",
    "marginBottom": "16px",
    "paddingBottom": "12px",
    "borderBottom": f"1px solid {BORDER}",
    "flexShrink":   0,
}

# Sub-headings and prose take their natural height and never stretch — flexShrink 0
# keeps them from being squeezed when the page's grow rows compete for vertical space.
_ROW_HEADING_STYLE = {
    "fontSize":     "16px",
    "fontWeight":   600,
    "color":        TEXT,
    "marginTop":    "16px",
    "marginBottom": "8px",
    "flexShrink":   0,
}

_ROW_PROSE_STYLE = {
    "fontSize":     "13px",
    "color":        TEXT,
    "lineHeight":   "1.5",
    "marginTop":    "0",
    "marginBottom": "12px",
    "maxWidth":     "780px",   # readable line length — narrative shouldn't span full canvas
    "flexShrink":   0,
}

# Base style for a row of visuals (a horizontal flex track). marginBottom separates
# stacked rows. A grow row additionally gets `flex: 1 1 0` + `minHeight: 0` (applied in
# page_shell) so it shares the page's remaining vertical space; a natural-height row
# (KPI cards) gets `flexShrink: 0` so it keeps its content height.
_ROW_STYLE = {
    "display":      "flex",
    "gap":          ROW_GAP,
    "marginBottom": ROW_GAP,
    "alignItems":   "stretch",
}


def _item_flex(width: str | None) -> str:
    """Resolve a flex-item's CSS ``flex`` shorthand from its YAML ``width``.

    The previous ``flex: 0 0 <width>`` overflowed the row: with percentage widths
    (e.g. four ``25%`` cards) the bases summed to 100% AND the inter-item gaps pushed
    the total past the row, so each row's right edge landed at a different x and some
    cards clipped past the canvas. Instead:
      - percentage width → a *grow ratio* with a 0 basis (``<n> 1 0``): items share the
        row width MINUS the gaps in proportion to their percentages, so every row fills
        exactly [row-left, row-right] and all rows align edge-to-edge.
      - pixel/explicit width → fixed (``0 0 <width>``): caller wants a hard size.
      - no width → ``1 1 0`` (equal share of the row).
    """
    if width is None:
        return "1 1 0"
    w = str(width).strip()
    if w.endswith("%"):
        try:
            ratio = float(w[:-1])
            return f"{ratio} 1 0"
        except ValueError:
            return "1 1 0"
    return f"0 0 {w}"


def _wrap_item(component, width: str | None) -> html.Div:
    """Wrap one visual in a flex-item div: fills its share of the row width and the
    full row height (so charts stretch to fill the page), letting inner content shrink."""
    return html.Div(
        component,
        style={
            "minWidth":      0,
            "flex":          _item_flex(width),
            "height":        "100%",
            "display":       "flex",
            "flexDirection": "column",
        },
    )


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

    # Each section is rendered as its own FIXED full-viewport "page" (Power BI–style),
    # stacked vertically inside the scroll container. The page wrapper carries
    # id ``dbr-section-<anchor>`` so the nav-click handler can snap-scroll the whole
    # page to the top; the H2 keeps id=anchor for the scrollspy active-state.
    # (Prefix is ``dbr-section-`` not ``dbr-page-`` — the latter is owned by the
    # header/footer chrome elements; keeping them distinct avoids any id collision.)
    #
    # Layout per page: the H2 heading takes its natural height; everything below it lives
    # in a flex-column "body" that consumes the rest of the page. Within the body, each
    # row is either natural-height (KPI/slicer rows: flexShrink 0) or a grow row (charts:
    # flex 1 1 0) — the grow rows split the leftover vertical space equally so the page
    # fills exactly one viewport with no overlap and no dead band.
    page_children: list = []
    for label, anchor, rows in sections:
        body_children: list = []
        for row_title, row_prose, row_items, grow in rows:
            if row_title:
                body_children.append(html.H3(row_title, style=_ROW_HEADING_STYLE))
            if row_prose:
                body_children.append(dcc.Markdown(row_prose, style=_ROW_PROSE_STYLE))
            flex_items = [_wrap_item(component, width) for component, width in row_items]
            if grow:
                row_style = {**_ROW_STYLE, "flex": "1 1 0", "minHeight": _MIN_GROW_ROW_HEIGHT}
            else:
                row_style = {**_ROW_STYLE, "flexShrink": 0}
            body_children.append(html.Div(flex_items, style=row_style))
        body = html.Div(style=_PAGE_BODY_STYLE, children=body_children)
        section_children = [html.H2(label, id=anchor, style=_SECTION_HEADING_STYLE), body]
        page_children.append(
            html.Div(id=f"dbr-section-{anchor}", style=_PAGE_SECTION_STYLE, children=section_children)
        )

    # Right column: fixed header + scrollable page stack + fixed footer.
    # Build the children and the matching grid-row tracks in lockstep so the
    # `minmax(0, 1fr)` scroll track always lines up with the scroll element and
    # header/footer keep their `auto` (content) height pinned in the viewport.
    right_children: list = []
    grid_rows: list[str] = []
    if HEADER_ENABLED:
        header_title = dashboard_title if HEADER_SHOW_TITLE else ""
        right_children.append(build_header(title=header_title, subtitle=dashboard_subtitle))
        grid_rows.append("auto")
    right_children.append(
        html.Div(id="dbr-main-scroll", style=_MAIN_SCROLL_STYLE, children=page_children)
    )
    grid_rows.append("minmax(0, 1fr)")
    if FOOTER_ENABLED:
        right_children.append(build_footer(source=footer_source, updated=footer_updated))
        grid_rows.append("auto")
    right_style = {**_PAGE_RIGHT_STYLE, "gridTemplateRows": " ".join(grid_rows)}
    right_col = html.Div(style=right_style, children=right_children)

    # Assemble outer row: sidebar (if enabled) + right column
    if not SIDEBAR_ENABLED:
        outer_children: list = [right_col]
    else:
        sidebar = build_sidebar(sections=sidebar_pairs, dashboard_title=dashboard_title)
        outer_children = [sidebar, right_col] if SIDEBAR_POSITION == "left" else [right_col, sidebar]

    return html.Div(style=_PAGE_OUTER_STYLE, children=outer_children)
