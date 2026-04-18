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

from dash import Dash, html, callback, Input, Output, State

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
    requests_pathname_prefix="/TODO_DOMAIN/",
    title="TODO: Dashboard title (Polish) — Open Reporting",
    index_string="""
<!DOCTYPE html>
<html lang="pl">
<head>
    {%metas%}
    <title>{%title%}</title>
    {%favicon%}
    {%css%}
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>*, *::before, *::after { box-sizing: border-box; }</style>
</head>
<body>
    {%app_entry%}
    <footer>
        {%config%}
        {%scripts%}
        {%renderer%}
    </footer>
</body>
</html>
""",
)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=False)
```

## Rules
- `requests_pathname_prefix` must match the nginx route: `/TODO_DOMAIN/`
- `PORT` is unique per dashboard — check existing ports before assigning
- `title` in Polish; the suffix `— Open Reporting` is mandatory
- `lang="pl"` on `<html>` — all content is Polish
- Import `_theme` before any chart component — it registers the `teal` Plotly template globally
- Assets directory is auto-served by Dash from `products/dashboards/TODO_DOMAIN/assets/`
