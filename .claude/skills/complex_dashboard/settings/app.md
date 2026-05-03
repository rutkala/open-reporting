# App Settings

## What it is
The Dash application init — URL prefix, browser tab title, HTML shell, and the
`teal` Plotly template registration. **Source of truth:**
`dashboard.settings.app_init` — a real Python module inside this skill.
Dashboards import `make_app` and never redefine the Dash init inline.

## Usage in `app.py`

```python
from dashboard.settings.app_init import make_app

app = make_app(domain="TODO_DOMAIN", title="TODO: Dashboard title (Polish)",
               module_name=__name__)
```

Prerequisite: `/opt/open-reporting/.claude/skills` on `PYTHONPATH` — set in the
systemd unit (see `deploy.md`) and in local dev before launching `app.py`.

## What `make_app` does

| Responsibility | Behaviour |
|---|---|
| Import `products.visuals.lib.theme` | Registers the `teal` Plotly template globally — do this once per process |
| Set `requests_pathname_prefix` | `/TODO_DOMAIN/` — matches the nginx `location` block |
| Set `routes_pathname_prefix` | Same prefix — the two must match |
| Set `suppress_callback_exceptions=True` | Required when callbacks reference components in other sections |
| Set browser tab title | `"TODO Title — Open Reporting"` — the suffix is appended automatically |
| Set `index_string` | Canonical HTML shell with the four Plotly-sizing CSS rules |

## Full `app.py` skeleton

```python
#!/usr/bin/env python3
"""
TODO_DOMAIN dashboard — Open Reporting

Run:
    PYTHONPATH=/opt/open-reporting:/opt/open-reporting/.claude/skills \
    DUCKDB_PATH=/opt/open-reporting/data/warehouse.duckdb \
    python3 products/dashboards/TODO_DOMAIN/app.py
"""
import logging

from dash import html

from dashboard.layout.styles import S, SIDEBAR_W, SIDEBAR_COLLAPSED
from dashboard.controls.navigation.sidebar_nav import register_toggle_callback
from dashboard.settings.app_init import make_app

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

PORT = TODO_PORT   # unique per dashboard — check existing ports before assigning

app = make_app(domain="TODO_DOMAIN",
               title="TODO: Dashboard title (Polish)",
               module_name=__name__)

# app.layout = html.Div(style=S["body"], children=[ ... ])   # see SKILL.md for skeleton

register_toggle_callback(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=False)
```

## Rules
- Never call `Dash(...)` directly in a dashboard `app.py` — always `make_app(...)`
- `domain` argument must match the nginx `location` block **and** the systemd unit name
- `title` is Polish; do not append `— Open Reporting` yourself — `make_app` does it
- `PORT` is unique per dashboard — check existing ports before assigning (8050, 8051, 8052, 8053 taken)
- Pass `module_name=__name__` so Dash resolves the assets folder relative to the dashboard, not the skill
- Assets directory is auto-served by Dash from `products/dashboards/TODO_DOMAIN/assets/`
- Call `register_toggle_callback(app)` after `app.layout` is assigned
- To change the HTML shell or the `teal` template registration, edit `settings/app_init.py` here — never override in a dashboard
