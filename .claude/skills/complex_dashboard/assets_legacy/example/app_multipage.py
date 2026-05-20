#!/usr/bin/env python3
"""Multi-page example — proves use_pages=True wiring works.

Two URLs:

- ``/example/`` — overview, time-series chart
- ``/example/regional`` — clustered-column chart of regional values

Run:
    PYTHONPATH=/opt/open-reporting:/opt/open-reporting/.claude/skills \\
    python3 .claude/skills/complex_dashboard/assets/example/app_multipage.py

Then open http://localhost:8061/example/
"""
from pathlib import Path

from dash import html, page_container

from complex_dashboard.assets.runtime import (
    S,
    build_footer, build_header,
    build_sidebar, register_toggle_callback,
    register_healthcheck,
    make_app,
)


PORT = 8061
_PAGES_DIR = str(Path(__file__).parent / "pages")


app = make_app(
    domain="example",
    title="Przykład wielostronicowy — complex_dashboard",
    module_name=__name__,
    use_pages=True,
    pages_folder=_PAGES_DIR,
)
register_healthcheck(app)


app.layout = html.Div(style=S["body"], children=[
    build_sidebar(domain="example", from_page_registry=True),

    html.Main(style=S["main"], children=[
        *build_header(
            title="Przykład wielostronicowy",
            subtitle="Dane syntetyczne — dwie strony",
            domain="example",
        ),
        html.Div(style=S["main-content-area"], children=[page_container]),
        *build_footer(
            name="Przykład wielostronicowy — complex_dashboard",
            source="dane syntetyczne",
            updated="2018–2024",
        ),
    ]),
])


register_toggle_callback(app)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=False)
