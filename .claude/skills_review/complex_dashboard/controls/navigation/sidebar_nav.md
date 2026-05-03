# Sidebar Navigation

## When to use
Every dashboard. The collapsible sidebar provides page/section navigation and the
Open Reporting logo. It collapses to an icon strip when toggled.

## What the dashboard authors
The layout tree for the sidebar — logo, links, collapse button — lives in the
dashboard's `app.py` because the links are dashboard-specific. The collapse
callback is shared across every dashboard and lives in this skill.

## Usage in `app.py`

```python
from dashboard.controls.navigation.sidebar_nav import register_toggle_callback

# … build app and layout …

register_toggle_callback(app)   # call once, after app.layout is set
```

Prerequisite: `/opt/open-reporting/.claude/skills` on `PYTHONPATH` (see
`settings/deploy.md` and `layout/styles.md`).

## Layout template — sidebar structure in `app.py`

```python
from dash import html
from dashboard.layout.styles import S

html.Aside(id="sidebar", style=S["sidebar"], children=[

    # Logo
    html.Div(id="sidebar-logo", style=S["sidebar-logo"], children=[
        html.A(
            html.Img(id="sidebar-logo-img",
                     src="/TODO_DOMAIN/assets/images/logo.svg",
                     style=S["logo"]),
            href="/",
        ),
    ]),

    html.Hr(id="sidebar-divider", style=S["sidebar-divider"]),

    # Navigation links — one per dashboard section
    # First link uses nav-item-active; rest use nav-item
    html.Nav(id="sidebar-nav", style=S["sidebar-nav"], children=[
        html.A("TODO: Section 1", href="#TODO_SECTION_1_ID", style=S["nav-item-active"]),
        html.A("TODO: Section 2", href="#TODO_SECTION_2_ID", style=S["nav-item"]),
        html.A("TODO: Section 3", href="#TODO_SECTION_3_ID", style=S["nav-item"]),
    ]),

    # Collapse toggle button
    html.Button(id="btn-toggle", style=S["toggle-btn"], children=[
        html.Img(id="toggle-icon",
                 src="/TODO_DOMAIN/assets/images/sidebar.svg",
                 style=S["toggle-icon"]),
    ]),
])
```

## Required element IDs
The shared callback wires these IDs — they must exist in the layout exactly as named:

| ID | Element |
|---|---|
| `sidebar` | `html.Aside` — root of the sidebar |
| `sidebar-logo` | `html.Div` wrapping the logo |
| `sidebar-logo-img` | `html.Img` — the logo graphic |
| `sidebar-nav` | `html.Nav` — the links container |
| `btn-toggle` | `html.Button` — the collapse toggle |

If any ID is missing or renamed, `register_toggle_callback(app)` will raise at
dashboard startup.

## Rules
- One `html.A` per section — `href="#section-id"` must match the `id=` of the section `html.H2`
- First link always `nav-item-active`; rest `nav-item` (no JS needed — anchor scrolling)
- Never re-implement the collapse callback inline — always `register_toggle_callback(app)`
- Element IDs above are fixed — do not rename them in `app.py`
- `src` paths must use the dashboard's URL prefix: `/TODO_DOMAIN/assets/images/`
- Register the callback **after** `app.layout` is assigned, not before
