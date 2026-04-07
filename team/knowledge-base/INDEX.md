# Knowledge Base — Index

Research syntheses for the Open Reporting team. Each file is source-first — no opinions, only synthesis of authoritative sources.

**Loading rule:** Read only what is relevant to the current task. Do not auto-load every session.
See `team/PLATFORM.md §7` for the full KB map and priority build order.

---

## Analytical Methods

| File | Covers | Read when |
|------|--------|-----------|
| [analytical-methods/analytical-thinking.md](analytical-methods/analytical-thinking.md) | Five analytical moves, insight hierarchy, when indicators are interesting, Polish public data context, aggregation rules | Before designing any analytical output |

---

## Visualization

| File | Covers | Read when |
|------|--------|-----------|
| [visualization/principles.md](visualization/principles.md) | IBCS SUCCESS, Gestalt, data-ink ratio, colour semantics, reference lines | Before designing any chart or dashboard |
| [visualization/ui-principles.md](visualization/ui-principles.md) | Layout, grid, dashboard types, interaction | Before designing dashboard layout |
| [visualization/charts/bar.md](visualization/charts/bar.md) | Bar and column charts | Before building any bar/column chart |
| [visualization/charts/line.md](visualization/charts/line.md) | Line charts, area charts | Before building any line or area chart |
| [visualization/charts/combo-subplots.md](visualization/charts/combo-subplots.md) | Combo charts, dual-axis, subplots | Before building any multi-measure chart |
| [visualization/charts/waterfall.md](visualization/charts/waterfall.md) | Waterfall charts — contribution, variance | Before building any waterfall |
| [visualization/charts/scatter.md](visualization/charts/scatter.md) | Scatter, bubble charts | Before building any scatter |
| [visualization/charts/map.md](visualization/charts/map.md) | Choropleth, symbol maps | Before building any map |
| [visualization/charts/table.md](visualization/charts/table.md) | Tables, heatmap tables | Before building any table |

---

## UX / Perception

| File | Covers | Status |
|------|--------|--------|
| `ux-perception/` | Visual cortex processing, pre-attentive attributes, cognitive load, eye-tracking patterns, colour perception, WCAG, Gestalt primary sources | **Planned — Priority 1** |

Sources to research: Colin Ware "Information Visualization: Perception for Design", Steven Few "Show Me the Numbers", Alberto Cairo "The Functional Art", Nielsen Norman Group eye-tracking corpus, WCAG 2.2, cognitive load theory (Sweller), pre-attentive processing literature.

---

## Data Architecture

| File | Covers | Status |
|------|--------|--------|
| `data-architecture/` | Dimensional modelling (Kimball), medallion architecture, schema design principles, layer contracts | **Planned — Priority 2** |

Sources: Kimball "The Data Warehouse Toolkit", Inmon "Building the Data Warehouse", Databricks medallion docs, dbt Labs documentation.

---

## Data Engineering

| File | Covers | Status |
|------|--------|--------|
| `data-engineering/` | ELT patterns, SQL standards, DuckDB best practices, dbt conventions, data quality patterns | **Planned — Priority 3** |

---

## Business Analysis

| File | Covers | Status |
|------|--------|--------|
| `business-analysis/` | KPI theory, indicator design, Balanced Scorecard, public sector analytics frameworks | **Planned — Priority 4** |

---

## Domains

| File | Covers | Status |
|------|--------|--------|
| [domains/public-finance.md](domains/public-finance.md) | Fiscal KPIs, SGP rules, Polish benchmarks, canonical chart patterns | Draft |
| `domains/labour-market.md` | Labour market indicators, ILO framework, Polish context | Planned |
| `domains/{18 domains}` | Per-domain KB | Not started |

Domain files are created via `/domain-brief` skill before dashboard work begins on that domain.

---

## Content / Editorial

| File | Covers | Status |
|------|--------|--------|
| `content/` | Data journalism standards, Polish editorial style, storytelling frameworks | Planned |

---

## Status Summary

| Module | Status | Issue |
|--------|--------|-------|
| Analytical methods | ✅ Complete | OR-119 |
| Visualization principles + charts | ✅ Complete | OR-118 |
| UX / Perception | 📋 Planned — Priority 1 | — |
| Data Architecture | 📋 Planned — Priority 2 | — |
| Data Engineering | 📋 Planned — Priority 3 | — |
| Business Analysis | 📋 Planned — Priority 4 | — |
| Domains — public finance | ⏳ Draft | OR-120 |
| Domains — labour market | 📋 Planned | — |
