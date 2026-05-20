"""Shared sidebar layout + collapse callback.

Two helpers:

- ``build_sidebar(domain, sections=None, *, from_page_registry=False, active_index=0)``
  returns the full ``html.Aside(...)`` tree. Single-page apps pass
  ``sections=[(label, anchor_id), ...]`` and the nav renders anchor
  links. Multi-page apps pass ``from_page_registry=True`` and the nav
  is generated from ``dash.page_registry`` (sorted by the ``order``
  kwarg given to ``dash.register_page``).
- ``register_toggle_callback(app)`` registers the collapse callback
  that swaps the sidebar between ``SIDEBAR_W`` and ``SIDEBAR_COLLAPSED``
  when the toggle button is clicked. Call once after ``app.layout`` is
  assigned.
"""
from __future__ import annotations

import dash
from dash import Input, Output, State, html

from complex_dashboard.assets.runtime.styles import S, SIDEBAR_COLLAPSED, SIDEBAR_W


def build_sidebar(
    domain: str,
    sections: list[tuple[str, str | None]] | None = None,
    *,
    from_page_registry: bool = False,
    active_index: int = 0,
):
    """Return the standard sidebar ``html.Aside(...)`` tree.

    Parameters
    ----------
    domain
        URL prefix segment, e.g. ``"labour"``. Used to build asset
        ``src`` paths — must match ``make_app(domain=...)``.
    sections
        Ordered ``(label, anchor_id)`` pairs. ``anchor_id`` must match
        the ``id=`` of the corresponding section ``html.H2``. Pass
        ``anchor_id=None`` to render a non-clickable section separator
        (uses the ``nav-item-section-label`` style — small, muted,
        ``pointer-events: none``). Required unless
        ``from_page_registry=True``.
    from_page_registry
        Render the nav from ``dash.page_registry`` instead of from
        ``sections``. Use for ``make_app(..., use_pages=True)`` apps.
        Page entries are sorted by the ``order`` kwarg and link to
        ``page["relative_path"]`` so the URL prefix is preserved.
    active_index
        Which link gets ``nav-item-active`` styling. Defaults to 0
        (first link). Separator entries are skipped when matching this
        index. For ``from_page_registry=True`` apps this is only the
        initial styling — Dash's Pages framework handles active-link
        state at runtime via the URL.

    The element IDs (``sidebar``, ``sidebar-logo``, ``sidebar-logo-img``,
    ``sidebar-nav``, ``btn-toggle``) are fixed because the toggle
    callback wires them by name.
    """
    if from_page_registry:
        nav_links = _nav_from_page_registry(active_index)
    else:
        if sections is None:
            raise ValueError(
                "build_sidebar requires either sections=[...] or "
                "from_page_registry=True"
            )
        nav_links = []
        link_index = 0
        for label, anchor in sections:
            if anchor is None:
                nav_links.append(
                    html.A(label, style=S["nav-item-section-label"])
                )
                continue
            nav_links.append(
                html.A(
                    label,
                    href=f"#{anchor}",
                    style=S["nav-item-active"] if link_index == active_index else S["nav-item"],
                )
            )
            link_index += 1

    return html.Aside(id="sidebar", style=S["sidebar"], children=[
        html.Div(id="sidebar-logo", style=S["sidebar-logo"], children=[
            html.A(
                html.Img(
                    id="sidebar-logo-img",
                    src=f"/{domain}/assets/images/logo.svg",
                    style=S["logo"],
                ),
                href="/",
            ),
        ]),
        html.Hr(id="sidebar-divider", style=S["sidebar-divider"]),
        html.Nav(id="sidebar-nav", style=S["sidebar-nav"], children=nav_links),
        html.Button(id="btn-toggle", style=S["toggle-btn"], children=[
            html.Img(
                id="toggle-icon",
                src=f"/{domain}/assets/images/sidebar.svg",
                style=S["toggle-icon"],
            ),
        ]),
    ])


def _nav_from_page_registry(active_index: int) -> list:
    pages = sorted(
        dash.page_registry.values(),
        key=lambda p: (p.get("order", 1_000), p["name"]),
    )
    return [
        html.A(
            page["name"],
            href=page["relative_path"],
            style=S["nav-item-active"] if i == active_index else S["nav-item"],
        )
        for i, page in enumerate(pages)
    ]


def register_toggle_callback(app):
    """Register the sidebar-collapse callback on the given Dash app."""

    @app.callback(
        Output("sidebar", "style"),
        Output("btn-toggle", "style"),
        Output("sidebar-logo", "style"),
        Output("sidebar-nav", "style"),
        Output("sidebar-logo-img", "style"),
        Input("btn-toggle", "n_clicks"),
        State("sidebar", "style"),
        prevent_initial_call=True,
    )
    def _toggle_sidebar(_n_clicks, sidebar_style):
        is_expanded = sidebar_style.get("width", SIDEBAR_W) == SIDEBAR_W
        btn_open = {**S["toggle-btn"], "right": "10px", "transform": "none"}
        btn_closed = {**S["toggle-btn"], "right": "50%", "transform": "translateX(50%)"}
        if is_expanded:
            return (
                {**sidebar_style, "width": SIDEBAR_COLLAPSED},
                btn_closed,
                {"display": "none"},
                {"display": "none"},
                {"display": "none"},
            )
        return (S["sidebar"], btn_open, S["sidebar-logo"], S["sidebar-nav"], S["logo"])

    return _toggle_sidebar
