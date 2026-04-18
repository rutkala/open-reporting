---
name: dashboard
description: >
  Dashboard artifact skill. Describes what a dashboard is as an analytical product and
  provides the complete component library for building one in Dash/Python. Covers all
  chart types, slicers, layout, data connection, settings, and theme. Load this skill
  when any work targets a dashboard product — designing, building, reviewing, or evaluating.
  Triggers when: "build the dashboard", "design the dashboard", "implement the [domain]
  dashboard", "review the dashboard", or when /develop reaches a dashboard product.
user-invocable: true
---

# Dashboard

A Dash (Python) single-page application that assembles chart components, KPI cards,
slicers, and navigation into a scrollable analytical report. It consumes data from a
MetricFlow semantic model via pre-aggregated DataFrames — it contains no business logic,
no SQL aggregation, and no measure definitions.

Mental model: **Power BI report layer only.** The semantic model is a separate product.

---

## Folder structure

```
.claude/skills/dashboard/
├── SKILL.md                          ← this file — product context + component index
├── chart-types.md                    ← when-to-use decision guide (read before picking any chart)
│
├── visuals/                          ← chart and KPI components (Visualizations pane)
│   ├── cards/kpi_card.md             ← kpi_standard, kpi_compact, kpi_row
│   ├── bar/                          ← clustered_column, stacked_column, pct_stacked_column,
│   │                                    clustered_bar, stacked_bar, pct_stacked_bar,
│   │                                    clustered_stacked_column, clustered_stacked_bar
│   ├── line/                         ← line, area, stacked_area, pct_stacked_area
│   ├── combo/                        ← line_clustered_column, line_stacked_column, line_pct_stacked_column
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
│   └── navigation/sidebar_nav.md     ← collapsible sidebar with collapse callback
│
├── layout/                           ← structural scaffolding
│   ├── page.md                       ← section block (H2 + desc + KPI row + chart grid)
│   ├── header.md                     ← dashboard header (title, subtitle, action buttons)
│   ├── footer.md                     ← source attribution footer (mandatory)
│   ├── styles.md                     ← complete S dict + layout constants (copy verbatim)
│   └── grid.md                       ← card + grid patterns (grid-2, grid-3, grid-4)
│
├── data/connection.md                ← measures.py + semantic_service.py patterns
│
├── settings/
│   ├── app.md                        ← Dash app init (port, URL prefix, title, index_string)
│   └── deploy.md                     ← systemd service, nginx route, portal registration
│
└── theme/
    ├── colours.md                    ← colour tokens and palette
    ├── typography.md                 ← font family, sizes, weights
    └── icons.md                      ← SVG asset paths and setup
```

---

## Load map — what to read when

| Task | Files to read |
|------|--------------|
| Starting a new dashboard | `settings/app.md`, `layout/styles.md`, `layout/page.md`, `layout/header.md`, `layout/footer.md`, `controls/navigation/sidebar_nav.md`, `data/connection.md` |
| Picking chart types | `chart-types.md` first, then the relevant `visuals/` file |
| Building KPI section | `visuals/cards/kpi_card.md`, `layout/page.md` |
| Adding a slicer + callback | The matching `controls/slicers/*.md` |
| Deploying | `settings/deploy.md` |
| Colours or fonts | `theme/colours.md`, `theme/typography.md` |
| Icon paths | `theme/icons.md` |

---

## Component imports (standard header for every app.py)

```python
from products.visuals.components.kpi_card import kpi_row, kpi_standard, kpi_compact
from products.visuals.components.bar_chart import (
    clustered_column, stacked_column, pct_stacked_column,
    clustered_bar, stacked_bar, pct_stacked_bar,
    clustered_stacked_column, clustered_stacked_bar,
)
from products.visuals.components.line_chart import line, area, stacked_area, pct_stacked_area
from products.visuals.components.combo_chart import (
    line_clustered_column, line_stacked_column, line_pct_stacked_column,
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

---

## app.py file structure (top to bottom)

```
1. imports (Dash, callbacks, theme, components, measures, semantic_service)
2. PORT constant
3. app = Dash(...)               — see settings/app.md
4. data loaders                  — call semantic_service functions, store in module-level _df_* vars
5. dimension value shortcuts     — _TODO_values = m.DIMS["key"].values(_df_*)
6. S = {...}                     — inline style dictionary (see layout/grid.md + sidebar_nav.md)
7. app.layout                    — sidebar + main (header + content area + footer)
8. callbacks                     — one @callback per interactive chart; sidebar toggle from sidebar_nav.md
9. if __name__ == "__main__": app.run(...)
```

---

## Types

| Type | Primary question | Update frequency | Audience |
|------|-----------------|-----------------|---------|
| **Operational** | What is happening right now? | Real-time or near-real-time | Operations, on-call |
| **Analytical** | Why is this happening? What are the trends? | Daily / weekly / quarterly | Analysts, domain experts |
| **Strategic** | Are we on track toward goals? | Monthly / quarterly | Leadership, stakeholders |

Most Open Reporting dashboards are **analytical** — they support exploration and insight,
not real-time monitoring.

---

## Design principles

**Audience first** — every design decision follows from who will use the dashboard and what question they need answered.

**One question per section** — each section answers one analytical question. Never mix unrelated topics.

**KPIs before charts** — KPI cards establish the overall picture. Charts below explain it.

**Titles state conclusions** — "Zatrudnienie spada od 2023 r." not "Wykres liniowy zatrudnienia".

**Filters are navigation** — include only filters the audience will actually use.

**Source attribution is mandatory** — every dashboard must include data source and date range.

---

## Quality criteria

Before any dashboard is released:
- [ ] Each section answers exactly one analytical question
- [ ] Every chart has a title that states the analytical conclusion in Polish
- [ ] KPIs are present and include a comparison value (target, prior period, or benchmark)
- [ ] All filters are necessary — no filter included that the audience will not use
- [ ] Footer with source attribution is present
- [ ] Every chart wrapped in `S["card"]`; every section H2 id matches sidebar nav href

---

## Core rules
- Dashboard = report layer only — no SQL, no aggregation, no business logic in app.py
- All data comes from `semantic_service.py` loaders, loaded once at startup
- All styles go in the `S` dict — no inline hex values, no hardcoded pixel values outside S
- Chart titles state the analytical conclusion in Polish — never the chart type
- Footer is mandatory on every dashboard
- Copy sidebar collapse callback verbatim from `controls/navigation/sidebar_nav.md`
