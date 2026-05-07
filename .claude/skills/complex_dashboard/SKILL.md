---
name: complex_dashboard
description: >
  Dashboard report artifact skill. Describes a dashboard as a Power BI-style
  **report layer** — visuals, controls, layout, theme, and model binding.
  It does not contain semantic model definitions, DAX/measure logic, or ETL.
  Load this skill when any work targets the visual side of a dashboard —
  designing, building, reviewing, or evaluating the report. For measures and
  aggregation rules, load the `semantic-model` skill instead.
  Triggers when: "build the dashboard", "design the dashboard", "implement the
  [domain] dashboard", "review the dashboard", or when /composite_develop reaches a
  dashboard product.
user-invocable: true
---

# Dashboard (Report Layer)

A Dash (Python) application — single-page or multi-page — that
assembles chart components, KPI cards, slicers, and navigation into a
scrollable analytical report. It consumes a semantic model through a
narrow interface (see `assets/specs/data/data_loaders.md`) — the
report contains **no** SQL, aggregation, measure definitions, or
business logic.

## Power BI mental model

Power BI Desktop combines four concerns; after publishing they
separate into two artifacts:

| Power BI concern | Handled by | Open Reporting skill |
|---|---|---|
| Visualization pane (visuals, slicers, canvas) | Report | **`complex_dashboard` (this skill)** |
| Analysis Services Tabular + DAX | Semantic model | `semantic-model` skill |
| Power Query (ETL) | Data source | `data-engineer` / platform skills |

This skill owns only the **report** half. One semantic model can feed
many reports; one report binds to exactly one model via the interface
documented in `assets/specs/data/data_loaders.md`.

---

## Folder structure

```
.claude/skills/complex_dashboard/
├── SKILL.md                 ← this file — report context + load map
├── _seed.md                 ← purpose / scope / seed sources for /composite_knowledge
│
├── knowledge/               ← upstream content learned from external sources
├── experience/              ← framed lessons from real use (filled by /composite_experience)
│
└── assets/                  ← practitioner's opinionated starter kit, lifecycle-grouped
    │                          (runtime/ = imported, scaffolds/ = copied, specs/ = read)
    │
    ├── README.md            ← tri-modal map + quickstart (start here when bootstrapping)
    ├── walkthrough.md       ← narrated tour of example/
    │
    ├── app.py.template, app_multipage.py.template
    ├── requirements.txt.template, requirements-dev.txt.template
    ├── pyproject.toml.template, start.sh.template, .env.example
    │
    ├── runtime/             ← imported helpers (the only Python that runs at startup)
    │   ├── __init__.py      ← re-exports the public surface
    │   ├── app_init.py      ← make_app(domain, title, *, use_pages=False, pages_folder=None)
    │   ├── styles.py        ← S, SIDEBAR_W, SIDEBAR_COLLAPSED, GAP, RADIUS
    │   ├── header.py        ← build_header(...)
    │   ├── footer.py        ← build_footer(name, *, source, updated)  ← required kwargs
    │   ├── sidebar_nav.py   ← build_sidebar(...) + register_toggle_callback(app)
    │   ├── page_shell.py    ← build_page_layout(...)
    │   ├── healthcheck.py   ← register_healthcheck(app)
    │   └── log.py           ← configure_logging() + get_logger() + require_env()
    │
    ├── scaffolds/           ← copied per dashboard, never imported
    │   ├── data_loaders.py.template, measures.py.template
    │   ├── pages/{_README, overview, _section}.py.template
    │   └── tests/{conftest, test_smoke, test_data_contract, test_page_overview}.py.template
    │
    ├── specs/               ← read-only authoring docs (markdown only)
    │   ├── _index.md, load_map.md
    │   ├── page_layout.md, chart_types.md, testing.md, config.md
    │   ├── visuals/{cards, bar, line, combo, waterfall, scatter, distribution, maps, tables, other}/
    │   ├── controls/{slicers, navigation}/
    │   ├── layout/{header, footer, styles}.md
    │   ├── data/data_loaders.md
    │   ├── theme/{colours, typography, icons}.md
    │   └── deploy/{app_init, deploy, observability}.md
    │
    ├── example/             ← runnable demo
    │   ├── app.py           ← single-page (port 8060)
    │   ├── app_multipage.py ← multi-page (port 8061)
    │   ├── pages/{overview, regional}.py
    │   ├── data_loaders.py, measures.py
    │   └── smoke_test.py
    │
    └── static/              ← canonical SVG icons (logo, sidebar, settings, user)
```

The skill's three buckets follow the `_template/` contract:
`knowledge/` carries upstream content learned from articles and
research; `experience/` accumulates framed lessons from real
projects; `assets/` is the practitioner's opinionated starter kit —
grouped by **file lifecycle** so "do I import this, copy this, or
read this?" is answered by the folder name. The Power BI analogy is
preserved as documentation in `assets/README.md`, not as folder
names.

---

## Load map — what to read when

All paths below are under `assets/` unless noted otherwise. The
canonical, per-task version lives at
[`assets/specs/load_map.md`](assets/specs/load_map.md) — read that
when starting work; what follows is the high-level pointer.

| Task | Files to read |
|------|--------------|
| Seeing the helpers compose end-to-end | `walkthrough.md`, then run `example/app.py` (port 8060) and `example/app_multipage.py` (port 8061) |
| Bootstrapping a new dashboard | `README.md` quickstart, then `app.py.template` (single-page) or `app_multipage.py.template` (multi-page) |
| Picking the spec set for the task | `specs/load_map.md` |
| Understanding the data binding | `specs/data/data_loaders.md` (then jump to the `semantic-model` skill if you need to add measures) |
| Picking chart types | `specs/chart_types.md` first, then the relevant `specs/visuals/<family>/` |
| Building KPI section | `specs/visuals/cards/kpi_card.md`, `specs/page_layout.md` |
| Adding a slicer + callback | The matching `specs/controls/slicers/*.md` |
| Configuring multi-page | `specs/controls/navigation/sidebar_nav.md`, `specs/deploy/app_init.md`, `scaffolds/pages/_README.md` |
| Writing tests | `specs/testing.md`, then copy `scaffolds/tests/` |
| Deploying | `specs/deploy/deploy.md`, `specs/deploy/observability.md` |
| Env vars and config | `specs/config.md`, `.env.example` |
| Colours, fonts, icons | `specs/theme/colours.md`, `specs/theme/typography.md`, `specs/theme/icons.md` |
| Background, patterns, gaps | `knowledge/summary.md` |

---

## Component imports (standard header for every app.py)

The skill's runtime helpers are re-exported from a single module so
the import header stays short:

```python
# Shared report infrastructure — from the skill itself
from complex_dashboard.assets.runtime import (
    S, SIDEBAR_W, SIDEBAR_COLLAPSED,
    build_header, build_footer,
    build_sidebar, register_toggle_callback,
    build_page_layout,
    configure_logging, get_logger, require_env,
    register_healthcheck,
    make_app,
)

# Visual components — pick only the ones the dashboard actually uses
from complex_dashboard.assets.components.kpi_card import kpi_row, kpi_standard, kpi_compact
from complex_dashboard.assets.components.bar_chart import (
    clustered_column, stacked_column, pct_stacked_column,
    clustered_bar, stacked_bar, pct_stacked_bar,
    clustered_stacked_column, clustered_stacked_bar,
)
from complex_dashboard.assets.components.line_chart import line, area, stacked_area, pct_stacked_area
from complex_dashboard.assets.components.combo_chart import (
    line_clustered_column, line_stacked_column, line_pct_stacked_column, combo_subplots,
)
from complex_dashboard.assets.components.waterfall_chart import waterfall_contribution, waterfall_variance
from complex_dashboard.assets.components.scatter_chart import scatter_bubble
from complex_dashboard.assets.components.distribution_chart import histogram, box_plot
from complex_dashboard.assets.components.special_chart import funnel, treemap, gauge, bullet, ribbon, heatmap_matrix
from complex_dashboard.assets.components.map_chart import choropleth_map, bubble_map
from complex_dashboard.assets.components.financial_chart import candlestick
from complex_dashboard.assets.components.table_chart import table_basic, table_matrix, data_list
from complex_dashboard.assets.components.pie_chart import pie_chart
from complex_dashboard.assets.components.slicer import (
    dropdown_slicer, list_slicer, range_slicer, date_range_slicer, tile_slicer,
)
```

The `complex_dashboard.assets.runtime` import requires
`/opt/open-reporting/.claude/skills` on `PYTHONPATH`. The systemd
unit in `assets/specs/deploy/deploy.md` sets this; for local runs,
use `assets/start.sh.template` (which exports both `PYTHONPATH` and
`DUCKDB_PATH`).

---

## app.py file structure (top to bottom)

```
1. imports                     — Dash, runtime helpers, visual components, measures, data_loaders
2. PORT constant
3. configure_logging() + log = get_logger(__name__)
4. app = make_app(...)         — see specs/deploy/app_init.md (use_pages=True for multi-page)
   register_healthcheck(app)
5. data loaders                — call data_loaders functions, store in module-level _df_* vars
6. dimension value shortcuts   — _years = m.DIMS["year"].values(_df_*)
7. app.layout                  — sidebar + main (header + content area + footer)
                                 multi-page apps put dash.page_container in the content area
8. callbacks                   — one @callback per interactive chart
                                 call register_toggle_callback(app) for the sidebar collapse
9. if __name__ == "__main__": app.run(...)
```

### `app.layout` skeleton

The layout is a two-column flex — the sidebar on the left, the
scrollable main column on the right. Each named block is documented
in its own spec file under `specs/`.

```python
app.layout = html.Div(style=S["body"], children=[

    # ── Sidebar — see specs/controls/navigation/sidebar_nav.md ───────────────
    build_sidebar(domain="<domain>", sections=_SECTIONS),
    # multi-page variant: build_sidebar(domain=..., from_page_registry=True)

    # ── Main column — header + scrollable content + footer ───────────────────
    html.Main(style=S["main"], children=[

        # Header — see specs/layout/header.md
        *build_header(title=..., subtitle=..., domain="<domain>"),

        # Scrollable content area — one block per section (see specs/page_layout.md)
        html.Div(style=S["main-content-area"], children=[
            # Section 1: H2 + description + KPI row + chart grid
            # Section 2: ...
            # multi-page: dash.page_container goes here instead
        ]),

        # Footer — see specs/layout/footer.md (mandatory; source/updated REQUIRED)
        *build_footer(name="<name>", source="<source>", updated="<period>"),
    ]),
])
```

For the standard case, `build_page_layout(...)` from
`runtime/page_shell.py` returns the entire tree above in one call —
use it unless the dashboard needs a non-standard outer frame.

---

## Dashboard types

| Type | Primary question | Update frequency | Audience |
|------|-----------------|-----------------|---------|
| **Operational** | What is happening right now? | Real-time or near-real-time | Operations, on-call |
| **Analytical** | Why is this happening? What are the trends? | Daily / weekly / quarterly | Analysts, domain experts |
| **Strategic** | Are we on track toward goals? | Monthly / quarterly | Leadership, stakeholders |

Most Open Reporting dashboards are **analytical**. Tactical and
explanatory variants exist in the literature (see
`knowledge/summary.md` §3) but we do not currently build them.

---

## Design principles

**Audience first** — every design decision follows from who will use
the dashboard and what question they need answered.

**One question per section** — each section answers one analytical
question. Never mix unrelated topics.

**KPIs before charts** — KPI cards establish the overall picture.
Charts below explain it.

**Titles state conclusions** — "Zatrudnienie spada od 2023 r." not
"Wykres liniowy zatrudnienia".

**Subtitles attribute sources** — every chart `subtitle` is
`"Źródło: <agency> — dane za <period>"`. This is the report's audit
trail; no chart ships without it.

**Filters are navigation** — include only filters the audience will
actually use.

**Source attribution is mandatory** — every dashboard must include
data source and date range in the footer, in addition to per-chart
subtitles. `build_footer(...)` enforces this with required `source`
and `updated` kwargs.

---

## Quality criteria

Before any dashboard is released:
- [ ] Each section answers exactly one analytical question
- [ ] Every chart has a title that states the analytical conclusion in Polish
- [ ] Every chart has a `subtitle="Źródło: …"` attributing the source and period
- [ ] KPIs are present and include a comparison value (target, prior period, or benchmark)
- [ ] All filters are necessary — no filter included that the audience will not use
- [ ] Footer present with real `source` / `updated` (not TODO placeholders)
- [ ] Every chart wrapped in `S["card"]`; every section H2 `id` matches sidebar nav `href` (single-page) or `register_page(name=...)` (multi-page)
- [ ] No SQL, aggregation, or `groupby` in `app.py` — all data comes from `data_loaders.py` loaders
- [ ] No `Measure` or `Dimension` instantiation in the report — only consumption
- [ ] `register_healthcheck(app)` registered; smoke test from `scaffolds/tests/test_smoke.py.template` passes

---

## Core rules

- Report = visual layer only — no SQL, no aggregation, no business
  logic, no measure definitions in `app.py`
- All data comes from `data_loaders.py` loaders, loaded once at
  startup — never inside callbacks
- The report consumes `MEASURES` / `DIMS` through the interface in
  `assets/specs/data/data_loaders.md` — it never defines them
- All styles come from
  `complex_dashboard.assets.runtime.S` — no inline hex values,
  no hardcoded pixel values outside `S`
- Chart titles state the analytical conclusion in Polish — never the
  chart type
- Every chart subtitle attributes the source —
  `"Źródło: <agency> — dane za <period>"`
- Footer is mandatory; `build_footer` requires `source` and `updated`
  kwargs — calling without them raises `TypeError` at app import
- Sidebar collapse callback comes from
  `complex_dashboard.assets.runtime.register_toggle_callback(app)` —
  never redefined inline
- Required env vars (e.g. `DUCKDB_PATH`) read with
  `require_env(name)` so misconfiguration fails at app import
