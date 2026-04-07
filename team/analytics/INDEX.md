# Analytics Competence — Index

Agent reference library. Load on demand at the start of `/domain-brief` and `/plan` phases.
**Do not auto-load every session** — read only the file relevant to the current task.

---

## Visualization competence

| File | Covers | Read when |
|------|--------|-----------|
| [visualization/principles.md](visualization/principles.md) | IBCS SUCCESS, Gestalt, data-ink ratio, colour semantics, reference lines | Before designing any chart or dashboard |
| [visualization/ui-principles.md](visualization/ui-principles.md) | Layout, grid, dashboard types (executive / operational / analytical), interaction | Before designing dashboard layout or page structure |
| [visualization/charts/bar.md](visualization/charts/bar.md) | Bar and column charts — grouped, stacked, horizontal, diverging | Before building any bar/column chart |
| [visualization/charts/line.md](visualization/charts/line.md) | Line charts — single series, multi-series, area | Before building any line or area chart |
| [visualization/charts/combo-subplots.md](visualization/charts/combo-subplots.md) | Combo charts, stacked subplots, dual-axis — when each is correct; fiscal rev/exp/balance pattern | Before building any multi-measure chart |
| [visualization/charts/waterfall.md](visualization/charts/waterfall.md) | Waterfall charts — composition, contribution, variance | Before building any waterfall or bridge chart |
| [visualization/charts/scatter.md](visualization/charts/scatter.md) | Scatter plots, bubble charts — correlation, distribution | Before building any scatter or bubble chart |
| [visualization/charts/map.md](visualization/charts/map.md) | Choropleth, symbol maps — geographic data | Before building any map |
| [visualization/charts/table.md](visualization/charts/table.md) | Tables, heatmap tables, sparkline tables | Before building any table or grid |

**Source materials:** Full extracted resources in `visualization/docs/viz-kb-full/` (618 files from playfairdata.com, EU Data Viz Guide, Google Material Design, Urban Institute styleguide). Source summaries in `sources/SUMMARY.md`.

---

## Domain competence

| File | Covers | Read when |
|------|--------|-----------|
| [domains/public-finance.md](domains/public-finance.md) | Fiscal KPIs, SGP rules, canonical chart patterns, Polish benchmarks | Before any public finance dashboard or chart work |
| `domains/labour-market.md` | _(planned)_ | Before any labour market dashboard work |

---

## Analytical thinking

| File | Covers | Read when |
|------|--------|-----------|
| [analytical-thinking.md](analytical-thinking.md) | Five analytical moves, insight hierarchy, when indicators are interesting, Polish public data context, aggregation rules | Before designing any analytical output (dashboard, article, social card) |

---

## How to add a new domain module

1. Create `team/analytics/domains/{domain-slug}.md`
2. Add a row to the table above
3. Create a sub-issue under OR-116

Domain modules are added on a rolling basis — one per domain, before that domain's dashboard work starts.

---

## Source Materials

Extracted and cached resources for visualization knowledge base:

| Source | Files | Content Type | Location |
|--------|-------|--------------|----------|
| playfairdata.com | 618 | Tableau tutorials, viz guides, 4 PDFs | `visualization/docs/viz-kb-full/https:/playfairdata.com/` |
| data.europa.eu | 20 | EU Data Visualisation Guide | `visualization/docs/viz-kb-full/https:/data.europa.eu/apps/data-visualisation-guide/` |
| hype4.academy | 2 | Learning platform (courses) | `visualization/docs/viz-kb-full/https:/hype4.academy/` |
| UrbanInstitute/graphics-styleguide | 470+ | Full git clone: CSS, PDFs, chart guides | `visualization/docs/viz-kb-full/graphics-styleguide/` |
| m2.material.io | 9 | Google Material Design | `visualization/docs/viz-kb-full/https:/m2.material.io/` |
| ibcs.com | 1 | IBCS standards overview | `visualization/docs/viz-kb-full/https:/ibcs.com/` |

---

## Status

| Module | Status | Issue |
|--------|--------|-------|
| Structure & delivery | ✅ Done | OR-117 |
| visualization/ principles.md | ✅ Complete | OR-118 |
| visualization/ chart files | ✅ Complete | OR-118 |
| sources/SUMMARY.md | ✅ Complete | OR-118 |
| domains/public-finance.md | ⏳ Draft (opencode) — needs review | OR-120 |
| Analytical thinking framework | ✅ Complete | OR-119 |
