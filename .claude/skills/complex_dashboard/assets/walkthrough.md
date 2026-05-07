# Walkthrough — `example/app.py`

A working mini-dashboard that proves the `complex_dashboard` skill
helpers compose into a runnable Dash app. Sibling files:
[`example/app.py`](example/app.py),
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

The same example also ships in multi-page form (Dash Pages framework,
`use_pages=True`). Run it on a separate port to compare side by side:

```bash
PYTHONPATH=/opt/open-reporting:/opt/open-reporting/.claude/skills \
python3 .claude/skills/complex_dashboard/assets/example/app_multipage.py
```

Then open `http://localhost:8061/example/` for the overview page or
`http://localhost:8061/example/regional` for the regional page.

## What it demonstrates

| Skill component | Where it appears |
|---|---|
| `make_app(...)` | `example/app.py` — app init |
| `S` (styles dict) | `example/app.py` — `S["card"]`, `S["section-heading"]`, … |
| `build_page_layout(...)` | `example/app.py` — replaces ~30 lines of nested `html.Div`/`html.Main` boilerplate |
| `build_sidebar(...)` / `build_header(...)` / `build_footer(...)` | wrapped by `build_page_layout` |
| `register_toggle_callback(app)` | `example/app.py` — wires the sidebar collapse |
| `register_healthcheck(app)` | `example/app.py` — exposes `/example/health` |
| `Dimension` / `Measure` | `example/measures.py` — `DIMS` / `MEASURES` registries |
| `load_*(...)` interface | `example/data_loaders.py` — `load_by_year`, `load_by_region`, `load_scalars` |
| `kpi_row` + `kpi_standard` | `example/app.py` — KPI section above each chart |
| `line(...)`, `clustered_column(...)` | `example/app.py` — chart components from `products/visuals/components/` |
| Chart `subtitle="Źródło: …"` | per-chart source attribution rule |

## What it does *not* demonstrate

The example skips the things every domain dashboard adds on top:

- **Warehouse loaders** — uses synthetic `pd.DataFrame`s in
  `example/data_loaders.py` instead of DuckDB queries. See
  `scaffolds/data_loaders.py.template` for the real pattern.
- **Multiple measures with comparisons** — single-card KPI rows; real
  dashboards use 3–5 cards with `reference_value` + `reference_label`.
- **Slicers and filtering callbacks** — only the shared
  sidebar-collapse callback is registered. See
  `specs/controls/slicers/*.md` for the slicer + filter pattern.
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
  `template/app.py` (which predates the skill).
