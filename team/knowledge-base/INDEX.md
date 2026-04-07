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

| File | Covers | Read when |
|------|--------|-----------|
| [ux-perception/perception.md](ux-perception/perception.md) | Pre-attentive attributes (Treisman), Gestalt laws, cognitive load (Sweller), eye-tracking patterns, colour perception + blindness, WCAG 2.2, working memory (Cowan 4±1) | Before designing any dashboard layout, colour scheme, or visual hierarchy |

---

## Data Architecture

| File | Covers | Read when |
|------|--------|-----------|
| [data-architecture/architecture.md](data-architecture/architecture.md) | Medallion layer contracts, dimensional modelling (Kimball), dbt patterns (staging, mart, ref/source), schema naming, SCD types, DuckDB implications | Before any schema design, new data source, or mart design |

---

## Data Engineering

| File | Covers | Read when |
|------|--------|-----------|
| [data-engineering/engineering.md](data-engineering/engineering.md) | ELT principle, DuckDB patterns (upsert, TRY_CAST, fetched_at), dbt conventions (staging, incremental, tests), Python ETL standards, DAMA quality dimensions, security | Before writing any ingestion script or dbt model |

---

## Data Research

| File | Covers | Read when |
|------|--------|-----------|
| [data-research/research.md](data-research/research.md) | Source discovery methodology, DAMA quality dimensions, source authority hierarchy (L1–L3), licence assessment, indicator prioritisation, structural break documentation | Before any data source research or ingestion planning |

---

## Business Analysis

| File | Covers | Read when |
|------|--------|-----------|
| [business-analysis/kpi-indicator-design.md](business-analysis/kpi-indicator-design.md) | SMART+FABRIC indicator tests, output/outcome/impact levels, leading/lagging/stock/flow types, KPI design patterns, aggregation correctness, Polish structural breaks, EU benchmarking, BSC, insight framing | Before designing KPIs for any dashboard or analytical product |

---

## Domains

| File | Covers | Status |
|------|--------|--------|
| [domains/public-finance.md](domains/public-finance.md) | Fiscal KPIs, SGP rules, Polish benchmarks, canonical chart patterns | Draft |
| `domains/labour-market.md` | Labour market indicators, ILO framework, Polish context | Planned |
| `domains/{18 domains}` | Per-domain KB | Not started |

Domain files are created via `/domain-brief` skill before dashboard work begins on that domain.

---

## Research Methods

| File | Covers | Read when |
|------|--------|-----------|
| [research-methods/methods.md](research-methods/methods.md) | Reproducible research, OLS/IV/DiD/synthetic control assumptions, robustness checks, standard errors, Polish data quirks, coefficient interpretation | Before building any econometric model, Jupyter notebook, or quantitative analysis |

---

## Platform / Ops

| File | Covers | Read when |
|------|--------|-----------|
| [platform-ops/ops.md](platform-ops/ops.md) | Docker Compose production, nginx security, systemd hygiene, TLS lifecycle, security posture, observability, backup & recovery | Before making any infrastructure change — nginx config, Docker Compose, systemd units, certs |

---

## Content / Editorial

| File | Covers | Read when |
|------|--------|-----------|
| [content/editorial.md](content/editorial.md) | Inverted pyramid, fact-checking, source attribution, Polish press law, writing structure, social media card standards, blog article templates | Before writing any blog article, social card, or editorial content |

---

## Status Summary

| Module | Status | Issue |
|--------|--------|-------|
| Analytical methods | ✅ Complete | OR-119 |
| Visualization principles + charts | ✅ Complete | OR-118 |
| UX / Perception | ✅ Complete | OR-133 |
| Data Architecture | ✅ Complete | OR-133 |
| Data Engineering | ✅ Complete | OR-133 |
| Business Analysis | ✅ Complete | OR-133 |
| Data Research | ✅ Complete | OR-139 |
| Content / Editorial | ✅ Complete | OR-135 |
| Research Methods | ✅ Complete | OR-136 |
| Platform / Ops | ✅ Complete | OR-137 |
| Domains — public finance | ⏳ Draft | OR-120 |
| Domains — labour market | 📋 Planned | — |
