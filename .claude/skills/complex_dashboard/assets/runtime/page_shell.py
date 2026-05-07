"""Page-shell builder.

`build_page_layout(...)` assembles the canonical sidebar + header +
scrollable content + footer skeleton so a dashboard's ``app.layout =
...`` reduces to a single call instead of 30 lines of nested
``html.Div`` / ``html.Main`` boilerplate.

Use it when a dashboard's layout is "standard shape, varying content"
(the common case). When you need a non-standard outer frame (e.g. a
full-bleed splash page), inline the ``html.Div(style=S["body"], ...)``
yourself and call the individual builders directly.
"""
from dash import html

from complex_dashboard.assets.runtime.footer import build_footer
from complex_dashboard.assets.runtime.header import build_header
from complex_dashboard.assets.runtime.sidebar_nav import build_sidebar
from complex_dashboard.assets.runtime.styles import S


def build_page_layout(
    *,
    domain: str,
    title: str,
    subtitle: str,
    sections: list[tuple[str, str]],
    content: list,
    footer_name: str,
    footer_source: str,
    footer_updated: str,
    sidebar_active_index: int = 0,
    header_kwargs: dict | None = None,
    footer_kwargs: dict | None = None,
) -> html.Div:
    """Return the full ``app.layout`` ``html.Div`` tree.

    Parameters
    ----------
    domain
        URL prefix segment, e.g. ``"labour"``. Passed to ``build_sidebar``
        and ``build_header`` so asset paths resolve correctly.
    title
        Header H1 text (Polish).
    subtitle
        Header subtitle (Polish).
    sections
        Ordered ``(label, anchor_id)`` pairs for the sidebar nav. Each
        ``anchor_id`` must match the ``html.H2(id=...)`` of the
        corresponding section in ``content``.
    content
        Children of the scrollable ``main-content-area`` ``html.Div``.
        This is the section blocks: ``html.H2``, ``html.P``, ``kpi_row``,
        chart cards, etc.
    footer_name
        Dashboard name in Polish (footer left slot, before attribution).
    footer_source
        Source attribution (Polish), e.g. ``"GUS BDL"``.
    footer_updated
        Coverage window or refresh date (Polish), e.g. ``"luty 2026"``.
    sidebar_active_index
        Which sidebar link gets ``nav-item-active`` styling. Default 0.
    header_kwargs
        Extra kwargs forwarded to ``build_header`` (e.g. logo overrides).
    footer_kwargs
        Extra kwargs forwarded to ``build_footer`` (e.g. ``link_label``).
    """
    header_kwargs = header_kwargs or {}
    footer_kwargs = footer_kwargs or {}
    return html.Div(style=S["body"], children=[
        build_sidebar(
            domain=domain,
            sections=sections,
            active_index=sidebar_active_index,
        ),
        html.Main(style=S["main"], children=[
            *build_header(
                title=title,
                subtitle=subtitle,
                domain=domain,
                **header_kwargs,
            ),
            html.Div(style=S["main-content-area"], children=content),
            *build_footer(
                name=footer_name,
                source=footer_source,
                updated=footer_updated,
                **footer_kwargs,
            ),
        ]),
    ])
