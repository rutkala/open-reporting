"""Shared sidebar collapse callback.

Every dashboard registers the same toggle callback. Call
`register_toggle_callback(app)` once during app setup — after the layout has
been defined — and the sidebar will collapse between `SIDEBAR_W` and
`SIDEBAR_COLLAPSED` when the toggle button is clicked.
"""
from dash import Input, Output, State

from dashboard.layout.styles import S, SIDEBAR_COLLAPSED, SIDEBAR_W


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
