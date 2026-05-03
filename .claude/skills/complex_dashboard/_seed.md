# Seed input for `complex_dashboard`

> Read by `/composite_knowledge complex_dashboard/knowledge/`. Knowledge bucket
> was populated in a prior run (see `knowledge/raw/` and `knowledge/summary.md`);
> this seed is preserved for re-runs and as a record of the original framing.

## What this skill should do

Define the **report layer** of a Power BI-style data product: visuals,
controls, layout, theme, and the binding to a semantic model. The skill
covers what a dashboard is made of, when each chart type is appropriate,
how the canvas is laid out, and how the report consumes (does not
define) measures and dimensions. The output it produces is a Dash
single-page application that assembles components from the skill's
`assets/` and reads data through a narrow semantic-model interface.

The skill is consumed by the `dashboard-dev` builder agent and by
`/composite_kickoff` runs that target a dashboard product.

## Out of scope

- **Semantic model definitions** — DAX/measure logic, aggregation rules,
  dimension definitions. These belong in the `semantic-model` skill.
- **ETL / data engineering** — ingestion, dbt models, schema design.
  These belong to `data-engineer` and the platform skills.
- **Domain-specific KPI choice** — what to put on the labour-market or
  public-finance dashboard. That is a `business-analyst` concern; this
  skill describes *how to render* the chosen KPIs, not *which KPIs*.
- **Editorial copy** — the analytical narrative, headline phrasing in
  Polish. Belongs to `content-writer`.

## Pre-existing experience

- Power BI mental model is the right framing: Visualizations / Slicers /
  Canvas / Theme / Fields / Properties map cleanly onto the skill folder
  shape (`visuals/`, `controls/`, `layout/`, `theme/`, `model/`, `settings/`).
- Chart titles must state the analytical conclusion in Polish — never
  the chart type. "Zatrudnienie spada od 2023 r." not "Wykres liniowy".
- Subtitle is the audit trail: every chart must carry
  `subtitle="Źródło: <agency> — dane za <period>"`.
- The S dict (style tokens) and the sidebar callback are imported, never
  redefined inline.
- Cowan 4±1 — series count caps at 5 distinct lines/bars; beyond that,
  switch chart type or split.

## Seed sources

- *(primary)* https://ibcs.com/standards/ — IBCS SUCCESS standards
- *(primary)* https://www.yellowfinbi.com/blog/dashboard-design-principles
- *(primary)* https://www.datacamp.com/tutorial/dashboard-design
- *(primary)* https://learn.microsoft.com/power-bi/create-reports/desktop-report-design-tips
- *(secondary)* https://dash.plotly.com/ — Dash framework reference
- *(local)* file:///opt/open-reporting/team/knowledge-base/visualization/principles.md
- *(local)* file:///opt/open-reporting/team/knowledge-base/ux-perception/perception.md
