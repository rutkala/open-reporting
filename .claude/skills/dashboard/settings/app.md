# App Settings

## What it is
The Dash application init block that configures the app's port, URL prefix, browser tab
title, and HTML shell. Copy verbatim and replace the three `TODO_DOMAIN` tokens.

## Template
```python
#!/usr/bin/env python3
"""
TODO_DOMAIN dashboard — Open Reporting

Run:
    PYTHONPATH=/opt/open-reporting \
    DUCKDB_PATH=/opt/open-reporting/data/warehouse.duckdb \
    python3 products/dashboards/TODO_DOMAIN/app.py
"""
import logging

from dash import Dash, Input, Output, State, callback, html

import products.visuals.lib.theme as _theme  # noqa: F401 — registers 'teal' Plotly template
from products.visuals.lib.theme import (
    BG_PAGE, BG_SURFACE, BORDER,
    COLORWAY, GRID, MUTED, NEGATIVE, POSITIVE,
    SUBTEXT, TEXT, WARNING, ZERO_LINE,
    FONT_FAMILY,
    TEAL_1, TEAL_2, TEAL_3, TEAL_4, TEAL_PALE,
    AZURE_1, AZURE_2, AZURE_3, AZURE_4, AZURE_PALE,
    SLATE_1, SLATE_2, SLATE_3, SLATE_4,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

PORT = TODO_PORT  # e.g. 8050 — each dashboard gets a unique port

app = Dash(
    __name__,
    title="TODO: Dashboard title (Polish) — Open Reporting",
    suppress_callback_exceptions=True,
    requests_pathname_prefix="/TODO_DOMAIN/",
    routes_pathname_prefix="/TODO_DOMAIN/",
    index_string="""<!DOCTYPE html>
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
</html>""",
)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=False)
```

## Rules
- Both `requests_pathname_prefix` and `routes_pathname_prefix` must be set to `/TODO_DOMAIN/` — they must match each other and the nginx `location` block
- `suppress_callback_exceptions=True` — required when callbacks reference components defined dynamically or in other sections
- `PORT` is unique per dashboard — check existing ports before assigning (template uses 8055)
- `title` in Polish; the suffix `— Open Reporting` is mandatory
- Import `_theme` before any chart component — it registers the `teal` Plotly template globally
- Assets directory is auto-served by Dash from `products/dashboards/TODO_DOMAIN/assets/`
- The four CSS rules in `index_string` are required for correct Plotly sizing — do not remove them
