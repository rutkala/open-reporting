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

A Dash (Python) single-page application that assembles chart components, KPI cards, slicers, and navigation into a scrollable analytical report. It consumes a semantic model through a narrow interface (see `model/model.md`) — the report contains **no** SQL, aggregation, measure definitions, or business logic.

## Power BI mental model

Power BI Desktop combines four concerns; after publishing, they separate into two artifacts:

| Power BI concern | Handled by | Open Reporting skill |
|---|---|---|
| Visualization pane (visuals, slicers, canvas) | Report | **`dashboard` (this skill)** |
| Analysis Services Tabular + DAX | Semantic model | `semantic-model` skill |
| Power Query (ETL) | Data source | `data-engineer` / platform skills |

This skill owns only the **report** half. One semantic model can feed many reports; one report binds to exactly one model via the interface documented in `model/model.md`.

---

## Folder structure

```
.claude/skills/complex_dashboard/
├── SKILL.md                          ← this file — report context + component index
├── chart-types.md                    ← when-to-use decision guide (read before picking any chart)
│
├── visuals/                          ← chart and KPI components (Visualizations pane)
│   ├── cards/kpi_card.md             ← kpi_standard, kpi_compact, kpi_row
│   ├── bar/                          ← clustered_column, stacked_column, pct_stacked_column,
│   │                                    clustered_bar, stacked_bar, pct_stacked_bar,
│   │                                    clustered_stacked_column, clustered_stacked_bar
│   ├── line/                         ← line, area, stacked_area, pct_stacked_area
│   ├── combo/                        ← line_clustered_column, line_stacked_column,
│   │                                    line_pct_stacked_column, combo_subplots
│   ├── waterfall/                    ← waterfall_contribution, waterfall_variance
│   ├── scatter/scatter_bubble.md
│   ├── distribution/                 ← histogram, box_plot
│   ├── maps/                         ← choropleth_map, bubble_map
│   ├── tables/                       ← table_basic, table_matrix, data_list
│   └── other/                        ← funnel, treemap, gauge, bullet, ribbon, heatmap_matrix,
│                                        candlestick, pie_chart
│
├── controls/                         ← interactive elements
│   ├── slicers/                      ← dropdown_slicer, list_slicer, range_slicer,
│   │                                    date_range_slicer, tile_slicer
│   └── navigation/                   ← sidebar_nav.md + sidebar_nav.py (verbatim callback)
│
├── layout/                           ← structural scaffolding (the report canvas)
│   ├── page.md                       ← section block (H2 + desc + KPI row + chart grid + grid)
│   ├── header.md                     ← dashboard header (title, subtitle, action buttons)
│   ├── footer.md                     ← source attribution footer (mandatory)
│   └── styles.md + styles.py         ← S dict + layout constants (imported, not copy-pasted)
│
├── model/                            ← semantic model binding (the Fields pane equivalent)
│   └── model.md                      ← interface the report expects the model to expose
│
├── settings/
│   ├── app.md + app_init.py          ← Dash app init (port, URL prefix, title, index_string)
│   └── deploy.md                     ← systemd service, nginx route, portal registration
│
└── theme/
    ├── colours.md                    ← colour tokens and palette
    ├── typography.md                 ← font family, sizes, weights
    └── icons.md                      ← SVG asset paths and setup
```

The top-level tree mirrors Power BI's conceptual panes: `visuals/` (Visualizations), `controls/` (Slicers + navigation), `layout/` (Canvas), `theme/` (Report theme), `model/` (Fields / Model view), `settings/` (Report properties + Publish).

---

## Load map — what to read when

| Task | Files to read |
|------|--------------|
| Starting a new dashboard | `settings/app.md`, `layout/styles.md`, `layout/page.md`, `layout/header.md`, `layout/footer.md`, `controls/navigation/sidebar_nav.md`, `model/model.md` |
| Understanding the semantic model binding | `model/model.md` (then jump to the `semantic-model` skill if you need to add measures) |
| Picking chart types | `chart-types.md` first, then the relevant `visuals/` file |
| Building KPI section | `visuals/cards/kpi_card.md`, `layout/page.md` |
| Adding a slicer + callback | The matching `controls/slicers/*.md` |
| Deploying | `settings/deploy.md` |
| Colours or fonts | `theme/colours.md`, `theme/typography.md` |
| Icon paths | `theme/icons.md` |

---

## Component imports (standard header for every app.py)

```python
# Shared report infrastructure — from the skill itself
from dashboard.layout.styles import S, SIDEBAR_W, SIDEBAR_COLLAPSED
from dashboard.controls.navigation.sidebar_nav import register_toggle_callback
from dashboard.settings.app_init import make_app

# Visual components — from products/visuals/components
from products.visuals.components.kpi_card import kpi_row, kpi_standard, kpi_compact
from products.visuals.components.bar_chart import (
    clustered_column, stacked_column, pct_stacked_column,
    clustered_bar, stacked_bar, pct_stacked_bar,
    clustered_stacked_column, clustered_stacked_bar,
)
from products.visuals.components.line_chart import line, area, stacked_area, pct_stacked_area
from products.visuals.components.combo_chart import (
    line_clustered_column, line_stacked_column, line_pct_stacked_column, combo_subplots,
)
from products.visuals.components.waterfall_chart import waterfall_contribution, waterfall_variance
from products.visuals.components.scatter_chart import scatter_bubble
from products.visuals.components.distribution_chart import histogram, box_plot
from products.visuals.components.special_chart import funnel, treemap, gauge, bullet, ribbon, heatmap_matrix
from products.visuals.components.map_chart import choropleth_map, bubble_map
from products.visuals.components.financial_chart import candlestick
from products.visuals.components.table_chart import table_basic, table_matrix, data_list
from products.visuals.components.pie_chart import pie_chart
from products.visuals.components.slicer import (
    dropdown_slicer, list_slicer, range_slicer, date_range_slicer, tile_slicer,
)
```

The `dashboard.*` imports require `/opt/open-reporting/.claude/skills` on `PYTHONPATH`. The systemd unit in `settings/deploy.md` sets this; for local runs, export it before launching `app.py`.

---

## app.py file structure (top to bottom)

```
1. imports                     — Dash, skill modules, components, measures, semantic_service
2. PORT constant
3. app = make_app(...)         — see settings/app.md
4. data loaders                — call semantic_service functions, store in module-level _df_* vars
5. dimension value shortcuts   — _TODO_values = m.DIMS["key"].values(_df_*)
6. app.layout                  — sidebar + main (header + content area + footer)
7. callbacks                   — one @callback per interactive chart
                                 call register_toggle_callback(app) for the sidebar collapse
8. if __name__ == "__main__": app.run(...)
```

### `app.layout` skeleton

The layout is a two-column flex — the sidebar on the left, the scrollable main column on the right. Each named block is documented in its own file.

```python
app.layout = html.Div(style=S["body"], children=[

    # ── Sidebar — see controls/navigation/sidebar_nav.md ──────────────────────
    html.Aside(id="sidebar", style=S["sidebar"], children=[ ... ]),

    # ── Main column — header + scrollable content + footer ────────────────────
    html.Main(style=S["main"], children=[

        # Header — see layout/header.md
        html.Div(id="main-header", style=S["main-header"], children=[ ... ]),
        html.Hr(style=S["main-divider"]),

        # Scrollable content area — one block per section (see layout/page.md)
        html.Div(style=S["main-content-area"], children=[
            # Section 1: H2 + description + KPI row + chart grid
            # Section 2: H2 + description + KPI row + chart grid
            # ...
        ]),

        # Footer — see layout/footer.md (mandatory)
        html.Hr(style=S["footer-divider"]),
        html.Footer(style=S["main-footer"], children=[ ... ]),
    ]),
])
```

---

## Dashboard types

| Type | Primary question | Update frequency | Audience |
|------|-----------------|-----------------|---------|
| **Operational** | What is happening right now? | Real-time or near-real-time | Operations, on-call |
| **Analytical** | Why is this happening? What are the trends? | Daily / weekly / quarterly | Analysts, domain experts |
| **Strategic** | Are we on track toward goals? | Monthly / quarterly | Leadership, stakeholders |

Most Open Reporting dashboards are **analytical**. Tactical and explanatory variants exist in the literature (see `knowledge-base/summary.md` §3) but we do not currently build them.

---

## Design principles

**Audience first** — every design decision follows from who will use the dashboard and what question they need answered.

**One question per section** — each section answers one analytical question. Never mix unrelated topics.

**KPIs before charts** — KPI cards establish the overall picture. Charts below explain it.

**Titles state conclusions** — "Zatrudnienie spada od 2023 r." not "Wykres liniowy zatrudnienia".

**Subtitles attribute sources** — every chart `subtitle` is `"Źródło: <agency> — dane za <period>"`. This is the report's audit trail; no chart ships without it.

**Filters are navigation** — include only filters the audience will actually use.

**Source attribution is mandatory** — every dashboard must include data source and date range in the footer, in addition to per-chart subtitles.

---

## Quality criteria

Before any dashboard is released:
- [ ] Each section answers exactly one analytical question
- [ ] Every chart has a title that states the analytical conclusion in Polish
- [ ] Every chart has a `subtitle="Źródło: …"` attributing the source and period
- [ ] KPIs are present and include a comparison value (target, prior period, or benchmark)
- [ ] All filters are necessary — no filter included that the audience will not use
- [ ] Footer with source attribution is present
- [ ] Every chart wrapped in `S["card"]`; every section H2 `id` matches sidebar nav `href`
- [ ] No SQL, aggregation, or `groupby` in `app.py` — all data comes from `semantic_service.py` loaders
- [ ] No `Measure` or `Dimension` instantiation in the report — only consumption

---

## Core rules
- Report = visual layer only — no SQL, no aggregation, no business logic, no measure definitions in `app.py`
- All data comes from `semantic_service.py` loaders, loaded once at startup
- The report consumes `MEASURES` / `DIMS` through the interface in `model/model.md` — it never defines them
- All styles come from `dashboard.layout.styles.S` — no inline hex values, no hardcoded pixel values outside `S`
- Chart titles state the analytical conclusion in Polish — never the chart type
- Every chart subtitle attributes the source — `"Źródło: <agency> — dane za <period>"`
- Footer is mandatory on every dashboard
- Sidebar collapse callback comes from `dashboard.controls.navigation.sidebar_nav.register_toggle_callback(app)` — never redefined inline
