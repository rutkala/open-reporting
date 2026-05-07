"""Shared sidebar layout + collapse callback.

Two helpers:

- `build_sidebar(domain, sections, active_index=0)` — returns the
  full `html.Aside(...)` tree. Section list is the only dashboard-
  specific input; everything else is identical across dashboards.
- `register_toggle_callback(app)` — registers the collapse callback
  that swaps the sidebar between `SIDEBAR_W` and `SIDEBAR_COLLAPSED`
  when the toggle button is clicked. Call once after `app.layout`
  is assigned.
"""
from dash import Input, Output, State, html

from complex_dashboard.assets.pages.layout.styles import S, SIDEBAR_COLLAPSED, SIDEBAR_W


def build_sidebar(domain: str, sections: list[tuple[str, str]], *, active_index: int = 0):
    """Return the standard sidebar `html.Aside(...)` tree.

    Parameters
    ----------
    domain
        URL prefix segment, e.g. ``"labour"``. Used to build asset
        ``src`` paths — must match ``make_app(domain=...)``.
    sections
        Ordered list of ``(label, anchor_id)`` pairs. ``anchor_id``
        must match the ``id=`` of the corresponding section ``html.H2``.
    active_index
        Which link gets ``nav-item-active`` styling. Defaults to 0
        (first section). Anchor scrolling does the rest — no JS.

    The element IDs (``sidebar``, ``sidebar-logo``, ``sidebar-logo-img``,
    ``sidebar-nav``, ``btn-toggle``) are fixed because the toggle
    callback wires them by name.
    """
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
        html.Nav(id="sidebar-nav", style=S["sidebar-nav"], children=[
            html.A(
                label,
                href=f"#{anchor}",
                style=S["nav-item-active"] if i == active_index else S["nav-item"],
            )
            for i, (label, anchor) in enumerate(sections)
        ]),
        html.Button(id="btn-toggle", style=S["toggle-btn"], children=[
            html.Img(
                id="toggle-icon",
                src=f"/{domain}/assets/images/sidebar.svg",
                style=S["toggle-icon"],
            ),
        ]),
    ])


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
