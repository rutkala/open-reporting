"""Shared Dash app factory for Open Reporting dashboards.

Every dashboard calls `make_app(domain=..., title=...)` to construct
the Dash instance with the canonical URL prefix, theme registration,
and ``index_string``.

Multi-page apps pass ``use_pages=True`` and additionally point Dash
at the ``pages/`` directory of the calling dashboard via
``pages_folder``.
"""
from pathlib import Path

from dash import Dash

import complex_dashboard.assets.theme as _theme  # noqa: F401 — registers 'teal' Plotly template


def _index_template(domain: str | None = None) -> str:
    """Render the HTML shell.

    For multi-page apps we embed ``<base href="/{domain}/">`` so the
    relative URLs Dash's Pages framework writes (``href="overview"``,
    ``href="regional"``) resolve under the dashboard's URL prefix
    instead of the document root.
    """
    base_tag = f'<base href="/{domain}/">' if domain else ""
    return """<!DOCTYPE html>
<html>
    <head>
        """ + base_tag + """
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


# Backwards-compatible alias for callers that imported the old name.
INDEX_TEMPLATE = _index_template()


def make_app(
    *,
    domain: str,
    title: str,
    module_name: str = __name__,
    use_pages: bool = False,
    pages_folder: str | None = None,
) -> Dash:
    """Build a Dash app with the standard URL prefix, title, and CSS shell.

    Parameters
    ----------
    domain
        URL prefix segment — must match the nginx ``location`` block and
        systemd unit name. ``"labour"`` produces ``/labour/`` routing.
    title
        Browser tab title (Polish). ``" — Open Reporting"`` is appended.
    module_name
        Dash ``name`` argument. Pass ``__name__`` from the calling ``app.py``.
    use_pages
        When ``True``, switches the app into multi-page mode: Dash auto-
        discovers modules under ``pages_folder`` (default
        ``<calling-app dir>/pages``) that call ``dash.register_page(...)``.
        The HTML shell also picks up a ``<base>`` tag so relative
        page-registry URLs resolve under ``/{domain}/``.
    pages_folder
        Override the auto-discovery directory. Absolute path or path
        relative to the dashboard's ``app.py``. Only meaningful with
        ``use_pages=True``.
    """
    prefix = f"/{domain}/"
    kwargs: dict = dict(
        title=f"{title} — Open Reporting",
        suppress_callback_exceptions=True,
        requests_pathname_prefix=prefix,
        routes_pathname_prefix=prefix,
        index_string=_index_template(domain if use_pages else None),
    )
    if use_pages:
        kwargs["use_pages"] = True
        if pages_folder:
            kwargs["pages_folder"] = pages_folder
    return Dash(module_name, **kwargs)
