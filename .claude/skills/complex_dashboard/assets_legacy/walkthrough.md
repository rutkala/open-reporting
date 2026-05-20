# Walkthrough — `example/app.py`

A working showroom dashboard — every chart family + slicer wired
through the skill's runtime helpers. The factory that builds it,
[`example/showroom.py`](example/showroom.py), is also called from
[`products/dashboards/template/app.py`](../../../../products/dashboards/template/app.py),
so the same showroom is served on both `/example/` and `/template/`.

Sibling files:
[`example/app.py`](example/app.py),
[`example/showroom.py`](example/showroom.py),
[`example/data_loaders.py`](example/data_loaders.py),
[`example/measures.py`](example/measures.py).

## Run it

```bash
PYTHONPATH=/opt/open-reporting:/opt/open-reporting/.claude/skills \
python3 .claude/skills/complex_dashboard/assets/example/app.py
```

Then open `http://localhost:8060/example/`. The healthcheck is at
`http://localhost:8060/example/health` and returns
`{"status":"ok"}`.

## Smoke-test it

The skill's smoke test verifies the app starts and serves HTTP 200:

```bash
PYTHONPATH=/opt/open-reporting:/opt/open-reporting/.claude/skills \
python3 .claude/skills/complex_dashboard/assets/example/smoke_test.py \
    .claude/skills/complex_dashboard/assets/example/app.py 8060 /example/
```

`smoke_test.py` takes an optional URL path as its third argument —
required for dashboards built on this skill, because `make_app(domain=...)`
mounts the app under `/{domain}/`, not `/`.

## Multi-page variant

The same skill helpers also ship a multi-page form (Dash Pages
framework, `use_pages=True`). Run it on a separate port to compare
side by side:

```bash
PYTHONPATH=/opt/open-reporting:/opt/open-reporting/.claude/skills \
python3 .claude/skills/complex_dashboard/assets/example/app_multipage.py
```

Then open `http://localhost:8061/example/` for the overview page or
`http://localhost:8061/example/regional` for the regional page.

## What it demonstrates

| Skill component | Where it appears |
|---|---|
| `build_showroom_app(...)` | `example/app.py` — single call returns a fully wired Dash app |
| `make_app(..., assets_folder=...)` | `example/showroom.py` — pins the SVG-icon dir at `example/assets/` so callers anywhere on disk see the same icons |
| `S` (styles dict) | `example/showroom.py` — `S["card"]`, `S["section-heading"]`, `S["group"]` |
| `build_page_layout(...)` | `example/showroom.py` — replaces ~30 lines of nested `html.Div`/`html.Main` boilerplate |
| `build_sidebar(...)` / `build_header(...)` / `build_footer(...)` | wrapped by `build_page_layout` |
| `register_toggle_callback(app)` | `example/showroom.py` — wires the sidebar collapse |
| `register_healthcheck(app)` | `example/app.py` — exposes `/example/health` |
| `Dimension` / `Measure` | `example/measures.py` — `DIMS` / `MEASURES` registries (10 measures, 7 dims) |
| `load_*(...)` interface | `example/data_loaders.py` — 20 synthetic loaders, real interface shape |
| `kpi_row` + `kpi_standard` + `kpi_compact` | `example/showroom.py` — KPI section variants |
| Every chart family | `example/showroom.py` — bar, line, area, combo, scatter, pie, treemap, funnel, waterfall, distribution, gauge, table, heatmap, map, ribbon, candlestick |
| Every slicer | `example/showroom.py` — dropdown, list, range, date, tile |
| Chart `subtitle="Źródło: …"` | per-chart source attribution rule |

## What it does *not* demonstrate

The showroom skips the things every domain dashboard adds on top:

- **Warehouse loaders** — uses synthetic `pd.DataFrame`s in
  `example/data_loaders.py` instead of DuckDB queries. See
  `scaffolds/data_loaders.py.template` for the real pattern.
- **Slicer-driven callbacks** — only the shared sidebar-collapse
  callback is registered. Slicers are rendered as static examples;
  see `specs/controls/slicers/*.md` for the filter-callback pattern.
- **Polish structural break annotations** — when the real series has
  one (e.g. GUS methodology change in 2023), add a reference line and
  caption.

## When to use it

- **Onboarding** — read this file alongside `SKILL.md` to see how the
  factored helpers actually compose. The TODO-laden
  `app.py.template` shows the *shape*; this example shows *substance*.
- **Regression check** — after any change to the skill helpers, run
  the smoke test. If the example breaks, the change is wrong.
- **Reference for new dashboards** — copy patterns from here, not from
  the deployed `template/app.py` (which is now a 5-line wrapper around
  `build_showroom_app(...)`). To start a real domain dashboard, copy
  the directory shape and replace `build_showroom_app(...)` with your
  own page assembly.
