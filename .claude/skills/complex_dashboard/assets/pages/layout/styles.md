# Styles (S dict)

## What it is
The shared layout style dictionary and sidebar constants for every dashboard.
**Source of truth:** `complex_dashboard.assets.pages.layout.styles` — a real Python module inside
this skill. `app.py` imports `S`, `SIDEBAR_W`, and `SIDEBAR_COLLAPSED` directly;
none of these are redefined inline in a dashboard.

## Usage in `app.py`

```python
from complex_dashboard.assets.pages.layout.styles import S, SIDEBAR_W, SIDEBAR_COLLAPSED
```

Prerequisite: `/opt/open-reporting/.claude/skills` must be on `PYTHONPATH`.
Set in `deploy/deploy.md` systemd unit; for local runs, `export PYTHONPATH=...`
before launching `app.py`.

## What the module exposes

| Name | Kind | Use |
|---|---|---|
| `S` | dict | Every layout style keyed by block name (`body`, `sidebar`, `main`, `card`, `grid-2`, …) |
| `SIDEBAR_W` | str (`"240px"`) | Expanded sidebar width |
| `SIDEBAR_COLLAPSED` | str (`"44px"`) | Collapsed sidebar width |
| `GAP`, `RADIUS` | str | Page edge gap + sidebar border radius |

All colour tokens (`BG_PAGE`, `BG_SURFACE`, `BORDER`, `TEXT`, `SUBTEXT`, `FONT_FAMILY`)
are imported by the module from `products.visuals.lib.theme`. The dashboard does
not re-import them for styling purposes (theme tokens are still needed for chart
components and inline text styles — see `theme/colours.md`).

## Key catalogue

| Section of `S` | Keys |
|---|---|
| Page shell | `body`, `main` |
| Sidebar | `sidebar`, `sidebar-logo`, `sidebar-divider`, `sidebar-nav`, `logo`, `nav-item`, `nav-item-active`, `toggle-btn`, `toggle-icon` |
| Header | `main-header`, `header-actions`, `header-btn`, `header-icon`, `main-divider` |
| Footer | `footer-divider`, `main-footer`, `footer-text` |
| Content area | `main-content-area` |
| Section typography | `section-heading`, `section-desc` |
| Content groups | `group`, `group-title` |
| Grid layouts | `grid-2`, `grid-3`, `grid-4`, `grid-auto` |
| Card container | `card` |

## Grid & card usage

Every chart lives inside `S["card"]`. Cards are arranged in a grid container or
placed full-width without a grid wrapper.

| Key | Columns | Gap | Use for |
|-----|---------|-----|---------|
| `grid-2` | 2 equal | 20px | Standard side-by-side charts |
| `grid-3` | 3 equal | 20px | Narrow charts or KPI tiles |
| `grid-4` | 4 equal | 16px | KPI tiles only |
| `grid-auto` | auto-fit ≥180px | 16px | Responsive KPI strips |

### Template — two charts side by side
```python
html.Div(style=S["grid-2"], children=[
    html.Div(style=S["card"], children=[ ... ]),
    html.Div(style=S["card"], children=[ ... ]),
]),
```

### Template — full-width chart
```python
html.Div(style=S["card"], children=[ ... ]),
```

### Template — four KPI-sized tiles
```python
html.Div(style=S["grid-4"], children=[
    html.Div(style=S["card"], children=[ ... ]),
    html.Div(style=S["card"], children=[ ... ]),
    html.Div(style=S["card"], children=[ ... ]),
    html.Div(style=S["card"], children=[ ... ]),
]),
```

## Rules
- Never redefine `S` or the sidebar constants in a dashboard `app.py` — always import
- To add a new style key, edit `styles.py` (sibling); the change propagates to every dashboard on next restart
- Do not add inline style dicts to layout components — add a key to `S` and reference by name
- `group` and `group-title` are for optional named sub-sections within a section — use only when needed
- Every chart must be wrapped in `S["card"]` — never render a chart directly into a grid cell
- Max 2 charts per row (`grid-2`); `grid-3` / `grid-4` are for KPI tiles or narrow bar charts only
- Full-width charts use a single `html.Div(style=S["card"], ...)` — no grid wrapper
- `minWidth: 0` on `card` prevents grid blowout from wide chart content
- KPI rows use the `kpi_row()` component — not the grid system
