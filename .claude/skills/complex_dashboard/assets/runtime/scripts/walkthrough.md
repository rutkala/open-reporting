# Walkthrough — `example_app.py`

A working mini-dashboard that proves the `complex_dashboard` skill
helpers compose into a runnable Dash app. Sibling file:
[`example_app.py`](example_app.py).

## Run it

```bash
PYTHONPATH=/opt/open-reporting:/opt/open-reporting/.claude/skills \
python3 .claude/skills/complex_dashboard/assets/runtime/scripts/example_app.py
```

Then open `http://localhost:8060/example/`.

## Smoke-test it

The skill's smoke test verifies the app starts and serves HTTP 200:

```bash
PYTHONPATH=/opt/open-reporting:/opt/open-reporting/.claude/skills \
python3 .claude/skills/complex_dashboard/assets/runtime/scripts/smoke_test.py \
    .claude/skills/complex_dashboard/assets/runtime/scripts/example_app.py 8060 /example/
```

`smoke_test.py` takes an optional URL path as its third argument —
required for dashboards built on this skill, because `make_app(domain=...)`
mounts the app under `/{domain}/`, not `/`.

## What it demonstrates

| Skill component | Where it appears in `example_app.py` |
|---|---|
| `make_app(...)` | App init — line ~57 |
| `S` (styles dict) | Layout — `S["body"]`, `S["main"]`, `S["card"]`, `S["section-heading"]`, … |
| `build_sidebar(...)` | Layout — replaces ~30 lines of `html.Aside` boilerplate |
| `build_header(...)` | Layout — replaces ~25 lines of header markup |
| `build_footer(...)` | Layout — replaces ~9 lines of footer markup |
| `register_toggle_callback(app)` | Callbacks — wires the sidebar collapse |
| `Dimension` / `Measure` | `DIMS` and `MEASURES` registries |
| `kpi_row` + `kpi_standard` | KPI section above each chart |
| `line(...)`, `clustered_column(...)` | Chart components from `products/visuals/components/` |
| Chart `subtitle="Źródło: …"` | Per-chart source attribution rule |

## What it does *not* demonstrate

The example skips the things every domain dashboard adds on top:

- **Warehouse loaders** — uses an inline synthetic `pd.DataFrame`
  instead of `semantic_service.py` calling DuckDB. See
  `assets/semantic_model/definition/data_sources/semantic_service_template.py` for the real pattern.
- **Multiple measures with comparisons** — single-card KPI rows; real
  dashboards use 3–5 cards with `reference_value` + `reference_label`.
- **Slicers and filtering callbacks** — the example only registers
  the shared sidebar-collapse callback. See
  `assets/report/controls/slicers/*.md` for the slicer + filter pattern.
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
