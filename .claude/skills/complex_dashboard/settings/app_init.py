"""Shared Dash app factory for Open Reporting dashboards.

Every dashboard calls `make_app(domain=..., title=...)` to construct the Dash
instance with the canonical URL prefix, theme registration, and `index_string`.
"""
from dash import Dash

import products.visuals.lib.theme as _theme  # noqa: F401 — registers 'teal' Plotly template


INDEX_TEMPLATE = """<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            html, body { margin: 0; padding: 0; height: 100vh; }
            #react-entry-point { height: 100%; }
            .js-plotly-plot .plotly { width: 100% !important; }
            .js-plotly-plot .plotly .main-svg { width: 100% !important; }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>"""


def make_app(*, domain: str, title: str, module_name: str = __name__) -> Dash:
    """Build a Dash app with the standard URL prefix, title, and CSS shell.

    Parameters
    ----------
    domain : str
        URL prefix segment — must match the nginx `location` block and systemd
        unit name. Example: ``"labour"`` produces ``/labour/`` routing.
    title : str
        Browser tab title (Polish). The suffix ``— Open Reporting`` is appended.
    module_name : str, optional
        Dash `__name__` argument. Pass `__name__` from the calling `app.py`.
    """
    prefix = f"/{domain}/"
    return Dash(
        module_name,
        title=f"{title} — Open Reporting",
        suppress_callback_exceptions=True,
        requests_pathname_prefix=prefix,
        routes_pathname_prefix=prefix,
        index_string=INDEX_TEMPLATE,
    )
