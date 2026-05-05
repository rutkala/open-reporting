# Sidebar Navigation

## When to use
Every dashboard. The collapsible sidebar provides page/section navigation and the
Open Reporting logo. It collapses to an icon strip when toggled.

## What the dashboard authors
The dashboard supplies the section list — everything else (tree, IDs,
toggle behaviour) is identical across dashboards and ships from this skill.

## Usage in `app.py`

```python
from complex_dashboard.assets.controls.navigation.sidebar_nav import (
    build_sidebar, register_toggle_callback,
)

_SECTIONS = [
    ("Sekcja 1", "section-1"),
    ("Sekcja 2", "section-2"),
]

app.layout = html.Div(style=S["body"], children=[
    build_sidebar(domain="TODO_DOMAIN", sections=_SECTIONS),
    html.Main(style=S["main"], children=[ ... ]),
])

register_toggle_callback(app)   # call once, after app.layout is set
```

Prerequisite: `/opt/open-reporting/.claude/skills` on `PYTHONPATH` (see
`settings/deploy.md` and `layout/styles.md`).

## What `build_sidebar` does

| Argument | Type | Purpose |
|---|---|---|
| `domain` | `str` | URL prefix, e.g. `"labour"` — must match `make_app(domain=...)` |
| `sections` | `list[tuple[str, str]]` | `(label, anchor_id)` pairs — `anchor_id` matches each section's `html.H2(id=...)` |
| `active_index` | `int` | Which link gets `nav-item-active` styling. Default `0`. |

Returns the full `html.Aside(...)` tree with the five wired IDs:
`sidebar`, `sidebar-logo`, `sidebar-logo-img`, `sidebar-nav`, `btn-toggle`.

## When to drop the helper

Only if the dashboard genuinely needs a non-standard sidebar — e.g. an
extra slicer pinned above the nav. In that case, hand-write the tree
following the structure documented below; keep the five IDs.

## Layout structure (for reference / hand-written sidebars)

```python
from dash import html
from complex_dashboard.assets.layout.styles import S

html.Aside(id="sidebar", style=S["sidebar"], children=[
    html.Div(id="sidebar-logo", style=S["sidebar-logo"], children=[ ... ]),
    html.Hr(id="sidebar-divider", style=S["sidebar-divider"]),
    html.Nav(id="sidebar-nav", style=S["sidebar-nav"], children=[ ... ]),
    html.Button(id="btn-toggle", style=S["toggle-btn"], children=[ ... ]),
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
