> **ARCHIVED 2026-05-22** — this 864-line factory blueprint described an earlier 'factory / DAG / workstation' model that was abandoned in favour of the declarative-YAML approach now described in [`../ARCHITECTURE.md`](../ARCHITECTURE.md). Specific sections (product portfolio, competency map, quality system) are largely superseded by [ARCHITECTURE.md](../ARCHITECTURE.md), the [CLAUDE.md subagent table](../../CLAUDE.md#custom-subagents), [docs/README.md](../../docs/README.md), and [docs/README.md](../../docs/README.md). Kept for history.

# Open Reporting — Platform Blueprint

**Version:** 1.0 | **Owner:** Lead Analyst & Architect | **Updated:** 2026-04-07

> **For repo layout, folder ownership, and AI delegation rules:** see [`../docs/ARCHITECTURE.md`](../docs/ARCHITECTURE.md) — the authoritative two-plane architecture document. This file (`PLATFORM.md`) describes the broader factory: product portfolio, agent roster, quality system, and workflow processes.

This document is the factory blueprint for Open Reporting. It defines what is produced, how it is produced, who produces it, and how quality is ensured. All other team documents are children of this one — they provide depth on specific areas this document maps.

**Portability:** This framework is designed to be reusable. A new project forks this document, replaces the product portfolio and domain KB, and inherits the quality infrastructure, agent pairs, workflow, and standards derivation chain intact.

---

## Table of Contents

1. [Product Portfolio](#1-product-portfolio)
2. [Platform: Dependency Graph](#2-platform-dependency-graph)
3. [Task Taxonomy](#3-task-taxonomy)
4. [Competency Map](#4-competency-map)
5. [Agent Roster](#5-agent-roster)
6. [Quality System](#6-quality-system)
7. [Knowledge Base Map](#7-knowledge-base-map)
8. [Standards Map](#8-standards-map)
9. [Document Architecture](#9-document-architecture)
10. [Workflow Processes](#10-workflow-processes)
11. [Current State](#11-current-state)

---

## 1. Product Portfolio

### 1.1 Finished Products (delivered to end users)

| Product | URL | Description |
|---------|-----|-------------|
| **Portal** | `portal.open-reporting.dev` | Analytical dashboards web application |
| **Blog** | `open-reporting.dev` | Data journalism content site |
| **Mobile App** | `portal.open-reporting.dev/app/` | PWA — Portal + Blog on mobile |
| **Social Media** | `@otwarteraporty` | Instagram data cards |

### 1.2 Sub-products

Each sub-product has a formal recipe in §3 — a routing table that maps it to tasks, competencies, agents, and standards.

**Data platform**

| # | Sub-product | What it produces | Linear label |
|---|-------------|-----------------|-------------|
| 1 | **Data ingested** | Raw tables + ingestion scripts (`raw.*`) | Data |
| 2 | **Data curated — silver** | dbt staging models → `curated.all_indicators` | Data |
| 3 | **Data mart — gold** | Domain star schema (`curated.mart_*`) | Data |
| 4 | **Semantic layer** | MetricFlow measures, dimensions, metrics | Data |

**Portal**

| # | Sub-product | What it produces | Linear label |
|---|-------------|-----------------|-------------|
| 5 | **Portal frontend** | Navigation, layout, dashboard assembly, PWA shell | Feature |
| 6 | **Portal backend** | Data query layer, DuckDB connection, caching, routing | Feature |

**Blog**

| # | Sub-product | What it produces | Linear label |
|---|-------------|-----------------|-------------|
| 7 | **Blog frontend** | Ghost theme, article templates, chart embeds | Feature |
| 8 | **Blog backend** | Ghost CMS config, content API, database | Infra |

**Mobile**

| # | Sub-product | What it produces | Linear label |
|---|-------------|-----------------|-------------|
| 9 | **Mobile frontend** | Responsive/PWA adaptation, mobile-first layout | Feature |
| 10 | **Mobile backend** | Shared with portal backend | Feature |

**Social media**

| # | Sub-product | What it produces | Linear label |
|---|-------------|-----------------|-------------|
| 11 | **Social platform setup** | API integration, token lifecycle, automation, scheduling | Infra |
| 12 | **Social card** | Individual Instagram visual export (content unit) | Content |
| 13 | **Data card** | Single-stat visual export | Content |

**Infrastructure**

| # | Sub-product | What it produces | Linear label |
|---|-------------|-----------------|-------------|
| 14 | **Platform infra** | VPS, Docker Compose, nginx, TLS/certs, DNS, systemd, backups, monitoring | Infra |

**Content / analytical units**

| # | Sub-product | What it produces | Linear label |
|---|-------------|-----------------|-------------|
| 15 | **Dashboard** | Domain-scoped interactive data app | Feature |
| 16 | **Visual component** | Reusable Plotly chart / KPI card | Feature |
| 17 | **Article** | Editorial data journalism piece | Content |
| 18 | **Research** | Econometric model / reproducible notebook | Feature |

### 1.3 Sub-product relationships

```
Portal
  ├── Portal frontend (#5)
  │     ├── Dashboard (#15) ─── Visual component (#16)
  │     └── Portal backend (#6) ── Data mart (#3) ── Data curated (#2) ── Data ingested (#1)
  └── Mobile frontend (#9) ── Portal frontend (#5) + Portal backend (#6)

Blog
  ├── Blog frontend (#7)
  │     ├── Article (#17) ── [Research (#18)] ── Visual component (#16)
  │     └── Blog backend (#8)
  └── Social card (#12) ── Visual component (#16) + Data mart (#3)

Social Media
  ├── Social platform setup (#11)
  ├── Social card (#12)
  └── Data card (#13)

All products
  └── Platform infra (#14)
        └── Semantic layer (#4) ── Data mart (#3)
```

---

## 2. Platform: Dependency Graph

What must exist to produce each sub-product. Read bottom-up — each layer depends on those below it.

```
FINISHED PRODUCTS
  Portal / Blog / Mobile / Social
        │
SUB-PRODUCTS
  Dashboards ─────────────── Articles ──── Research
        │                        │              │
  Visuals + Components       Writing       Analysis
        │                    CMS (Ghost)   Notebooks
  Semantic Model                                │
        │                              ─────────────────────
  Curated Data Layer         ←──────  docs/
        │                             (economics, domains)
  Raw Data Layer + dbt
        │
  Data Ingestion (to_landing + to_raw)
        │
  Data Sources (Eurostat, GUS, NBP, IMF)
        │
INFRASTRUCTURE
  DuckDB (warehouse) + PostgreSQL (operational)
  Docker Compose (nginx, postgres, ghost)
  Systemd services (labour, explorer, finance, mobile)
  Hetzner VPS + SSL/TLS
```

### 2.1 Component inventory

| Component | Location | Status |
|-----------|----------|--------|
| Domain briefs | `products/domain-briefs/` | 1 draft (public-finance) |
| Visual component library | `packages/dbr/src/dbr/visuals/` | Live |
| Dashboards (labour, explorer, finance) | `products/dashboards/` | Live |
| Blog (Ghost CMS) | Docker / Ghost | Live |
| Social publishing | `products/social/` | Live |
| Research library | `products/research/` | Partial |
| Data ingestion | `products/ingestion/` | Live |
| dbt transforms | `products/warehouse/` | Live |
| DuckDB warehouse | `data/warehouse.duckdb` | Live |
| PostgreSQL operational DB | Docker / postgres | Live |

---

## 3. Sub-product Recipes

Each sub-product has a recipe — a routing table that maps it to tasks, the skills those tasks require, the competency that owns them, the builder and evaluator agents, and the standards that apply. When a new OR is tagged to a sub-product, its recipe tells you everything.

**Recipe format:**

| Task | Skills | Competency | Builder | Evaluator | Build standard | Eval standard |
|------|--------|-----------|---------|-----------|---------------|---------------|

Agents marked *(gap)* are not yet live — the recipe defines the target state. Gaps are tracked in §5.2 and §11.2.

---

### 3.1 Data Platform

#### Sub-product 1 — Data ingested into environment

*Playbook:* `docs/playbooks/data-ingestion.md` | *Depends on:* —

| Task | Skills | Competency | Builder | Evaluator | Build standard | Eval standard |
|------|--------|-----------|---------|-----------|---------------|---------------|
| Research | Source discovery, API/file analysis, indicator selection, data quality, licence | Data Research | `data-researcher` *(gap)* | `data-research-reviewer` *(gap)* | — | — |
| Design | Schema design, ELT architecture, DuckDB patterns, upsert strategy | Data Architecture | `data-architect` *(gap — main Claude)* | `architecture-critic` | storage.md, ingestion.md | architecture-review.md |
| Build | Python scripting, DuckDB SQL, upsert, fetched_at, dbt sources.yml, tests | Data Engineering | `data-engineer` | `data-engineer-reviewer` | ingestion.md | data-engineering-review.md |

#### Sub-product 2 — Data curated (silver)

*Playbook:* `docs/playbooks/data-ingestion.md` (Phase 3) | *Depends on:* #1

| Task | Skills | Competency | Builder | Evaluator | Build standard | Eval standard |
|------|--------|-----------|---------|-----------|---------------|---------------|
| Design | dbt staging model structure, conformed dimensions, grain declaration | Data Architecture | `data-architect` *(gap)* | `architecture-critic` | storage.md, processing.md | architecture-review.md |
| Build | dbt SQL, staging pattern, sources.yml, schema.yml tests, all_indicators union | Data Engineering | `data-engineer` | `data-engineer-reviewer` | processing.md | data-engineering-review.md |

#### Sub-product 3 — Data mart (gold)

*Playbook:* `docs/playbooks/data-mart.md` | *Depends on:* #2

| Task | Skills | Competency | Builder | Evaluator | Build standard | Eval standard |
|------|--------|-----------|---------|-----------|---------------|---------------|
| Design | Kimball star schema, fact/dimension design, derived metrics, bus matrix | Data Architecture | `data-architect` *(gap)* | `architecture-critic` | storage.md, processing.md | architecture-review.md |
| Build | dbt mart SQL, incremental models, bus_matrix.md update | Data Engineering | `data-engineer` | `data-engineer-reviewer` | processing.md | data-engineering-review.md |

#### Sub-product 4 — Semantic layer

*Playbook:* `docs/playbooks/data-mart.md` (Phase 2) | *Depends on:* #3

| Task | Skills | Competency | Builder | Evaluator | Build standard | Eval standard |
|------|--------|-----------|---------|-----------|---------------|---------------|
| Domain brief | Indicator selection, aggregation rules, SMART+FABRIC, stock/flow | Business Analysis | `business-analyst` | `brief-reviewer` | — | brief-review.md |
| Design | MetricFlow measure/dimension/metric structure, entity model | Data Architecture + Semantic Modelling | `data-architect` *(gap)* | `architecture-critic` | measures.md | architecture-review.md |
| Build | MetricFlow YAML, agg declarations, format_type, scale, Polish labels | Semantic Modelling | `data-engineer` | `measures-reviewer` | measures.md | measures-review.md |

---

### 3.2 Portal

#### Sub-product 5 — Portal frontend

*Playbook:* `docs/playbooks/portal.md` | *Depends on:* #15, #16

| Task | Skills | Competency | Builder | Evaluator | Build standard | Eval standard |
|------|--------|-----------|---------|-----------|---------------|---------------|
| Design | Information architecture, navigation, layout system, accessibility | UX / UI Design | `dashboard-dev` | `visual-screenshot-reviewer` | visualisation.md | visualization-image.md |
| Build | Dash routing, page composition, PWA shell, responsive layout | Dashboard Development | `dashboard-dev` | `visual-screenshot-reviewer` | visualisation.md | visualization-diff.md |

#### Sub-product 6 — Portal backend

*Playbook:* `docs/playbooks/portal.md` | *Depends on:* #3

| Task | Skills | Competency | Builder | Evaluator | Build standard | Eval standard |
|------|--------|-----------|---------|-----------|---------------|---------------|
| Design | Query layer architecture, data access patterns, connection management | Data Architecture | `data-architect` *(gap)* | `architecture-critic` | storage.md | architecture-review.md |
| Build | Python/DuckDB queries, lib/db.py patterns, filter logic | Data Engineering | `data-engineer` | `data-engineer-reviewer` | storage.md | data-engineering-review.md |

---

### 3.3 Blog

#### Sub-product 7 — Blog frontend

*Playbook:* `docs/playbooks/blog.md` | *Depends on:* #17, #16

| Task | Skills | Competency | Builder | Evaluator | Build standard | Eval standard |
|------|--------|-----------|---------|-----------|---------------|---------------|
| Design | Ghost theme structure, article layout, typography, chart embeds | UX / UI Design | `dashboard-dev` *(partial)* | `visual-screenshot-reviewer` | visualisation.md | visualization-image.md |
| Build | Ghost Handlebars templating, CSS, chart embed integration | *(gap — Ghost-specific, no dedicated agent)* | *(gap)* | *(gap)* | — | — |

#### Sub-product 8 — Blog backend

*Playbook:* `docs/playbooks/blog.md` | *Depends on:* —

| Task | Skills | Competency | Builder | Evaluator | Build standard | Eval standard |
|------|--------|-----------|---------|-----------|---------------|---------------|
| Configure | Ghost CMS config, content API, webhooks, member settings | Platform / Ops | `ops-engineer` *(planned)* | `ops-reviewer` *(planned)* | — | ops-review.md *(planned)* |
| Operate | Docker lifecycle, database backup, token refresh, upgrades | Platform / Ops | `ops-engineer` *(planned)* | `ops-reviewer` *(planned)* | — | ops-review.md *(planned)* |

---

### 3.4 Mobile

#### Sub-product 9 — Mobile frontend

*Playbook:* `docs/playbooks/portal.md` (mobile-first variant) | *Depends on:* #5

| Task | Skills | Competency | Builder | Evaluator | Build standard | Eval standard |
|------|--------|-----------|---------|-----------|---------------|---------------|
| Design | Mobile-first layout, touch targets, PWA manifest, offline strategy | UX / UI Design | `dashboard-dev` | `visual-screenshot-reviewer` | visualisation.md | visualization-image.md |
| Build | Responsive CSS, PWA manifest, service worker, mobile viewport | Dashboard Development | `dashboard-dev` | `visual-screenshot-reviewer` | visualisation.md | visualization-diff.md |

#### Sub-product 10 — Mobile backend

*Same recipe as Portal backend (#6). Shared stack — see portal.md playbook.*

---

### 3.5 Social Media

#### Sub-product 11 — Social platform setup

*Playbook:* `docs/playbooks/social.md` (platform section) | *Depends on:* —

| Task | Skills | Competency | Builder | Evaluator | Build standard | Eval standard |
|------|--------|-----------|---------|-----------|---------------|---------------|
| Design | API integration architecture, token lifecycle, automation, scheduling | Platform / Ops | `ops-engineer` *(planned)* | `ops-reviewer` *(planned)* | — | ops-review.md *(planned)* |
| Build | Meta API integration, token management scripts, cron scheduling | Platform / Ops | `ops-engineer` *(planned)* | `ops-reviewer` *(planned)* | — | ops-review.md *(planned)* |

#### Sub-product 12 — Social card

*Playbook:* `docs/playbooks/social.md` | *Depends on:* #16, #3

| Task | Skills | Competency | Builder | Evaluator | Build standard | Eval standard |
|------|--------|-----------|---------|-----------|---------------|---------------|
| Domain brief | Metric selection, framing, context, Polish convention | Business Analysis | `business-analyst` | `brief-reviewer` | — | brief-review.md |
| Design | 1080×1080 layout, KPI card design, visual hierarchy, colour semantics | UX / UI Design | `dashboard-dev` | `visual-screenshot-reviewer` | visualisation.md, measures.md | visualization-image.md |
| Build | Plotly figure generation, PNG export | Dashboard Development | `dashboard-dev` | `visual-screenshot-reviewer` | visualisation.md | visualization-diff.md |
| Write caption | Polish language, factual precision, hashtag conventions | Content / Editorial | `content-writer` *(planned)* | `content-reviewer` *(planned)* | — | content-review.md *(planned)* |

#### Sub-product 13 — Data card

*Playbook:* `docs/playbooks/social.md` (data card section) | *Depends on:* #16, #3

| Task | Skills | Competency | Builder | Evaluator | Build standard | Eval standard |
|------|--------|-----------|---------|-----------|---------------|---------------|
| Design | Single-stat layout, number formatting, unit display | UX / UI Design | `dashboard-dev` | `visual-screenshot-reviewer` | measures.md, visualisation.md | visualization-image.md |
| Build | Plotly figure, PNG export | Dashboard Development | `dashboard-dev` | `visual-screenshot-reviewer` | visualisation.md | visualization-diff.md |

---

### 3.6 Infrastructure

#### Sub-product 14 — Platform infra

*Playbook:* `docs/playbooks/infra.md` | *Depends on:* —

| Task | Skills | Competency | Builder | Evaluator | Build standard | Eval standard |
|------|--------|-----------|---------|-----------|---------------|---------------|
| Design | Service topology, security posture, network design, backup strategy | Platform / Ops | `ops-engineer` *(planned)* | `ops-reviewer` *(planned)* | — | ops-review.md *(planned)* |
| Build | Docker Compose, nginx config, systemd units, TLS certs, DNS, monitoring | Platform / Ops | `ops-engineer` *(planned)* | `ops-reviewer` *(planned)* | — | ops-review.md *(planned)* |

---

### 3.7 Content and Analytical Units

#### Sub-product 15 — Dashboard

*Playbook:* `docs/playbooks/dashboard.md` | *Depends on:* #3, #16; may trigger #1–#4

| Task | Skills | Competency | Builder | Evaluator | Build standard | Eval standard |
|------|--------|-----------|---------|-----------|---------------|---------------|
| Domain brief | KPI selection, analytical angles, benchmarks, aggregation rules | Business Analysis | `business-analyst` | `brief-reviewer` | — | brief-review.md |
| Domain review | Domain KPI correctness, framing, Polish structural breaks | Domain Specialist | — *(evaluator only)* | `domain-specialist` | — | — |
| Design | Dashboard layout, tab structure, filter design, UX flow | UX / UI Design + Dashboard Development | `dashboard-dev` | `visual-screenshot-reviewer` | visualisation.md | visualization-image.md |
| Build | Dash app, chart components, KPI cards, gold mart queries | Dashboard Development | `dashboard-dev` | `visual-screenshot-reviewer` | visualisation.md | visualization-diff.md |
| Analytical review | Aggregation correctness, causal claims, chart labelling | Analytical Methods | — *(evaluator only)* | `analytical-validator` | — | analytical-review.md |

#### Sub-product 16 — Visual component

*Playbook:* inline in `docs/playbooks/dashboard.md` | *Depends on:* —

| Task | Skills | Competency | Builder | Evaluator | Build standard | Eval standard |
|------|--------|-----------|---------|-----------|---------------|---------------|
| Design | Component API, chart type selection, theme compliance, accessibility | UX / UI Design | `dashboard-dev` | `visual-screenshot-reviewer` | visualisation.md | visualization-image.md |
| Build | Plotly chart function, KPI card function, theme import | Dashboard Development | `dashboard-dev` | `visual-screenshot-reviewer` | visualisation.md | visualization-diff.md |

#### Sub-product 17 — Article

*Playbook:* `docs/playbooks/article.md` | *Depends on:* #3 (optional), #18 (optional)

| Task | Skills | Competency | Builder | Evaluator | Build standard | Eval standard |
|------|--------|-----------|---------|-----------|---------------|---------------|
| Domain brief | Analytical framing, indicator selection, story angle | Business Analysis | `business-analyst` | `brief-reviewer` | — | brief-review.md |
| Write | Data journalism, Polish language, factual precision, editorial standards | Content / Editorial | `content-writer` *(planned)* | `content-reviewer` *(planned)* | — | content-review.md *(planned)* |
| Visual embed | Chart selection, integration into article template | Dashboard Development | `dashboard-dev` | `visual-screenshot-reviewer` | visualisation.md | visualization-diff.md |

#### Sub-product 18 — Research

*Playbook:* `docs/playbooks/research.md` | *Depends on:* #3

| Task | Skills | Competency | Builder | Evaluator | Build standard | Eval standard |
|------|--------|-----------|---------|-----------|---------------|---------------|
| Research question | Hypothesis design, methodology selection, data feasibility | Business Analysis | `business-analyst` | `brief-reviewer` | — | brief-review.md |
| Model | Econometrics, statistical analysis, reproducible research, robustness checks | Research | `researcher` *(planned)* | `research-reviewer` *(planned)* | — | research-review.md *(planned)* |
| Analytical review | Model assumptions, aggregation, causal claims, interpretation | Analytical Methods | — *(evaluator only)* | `analytical-validator` | — | analytical-review.md |

---

## 4. Competency Map

Competency = a cluster of related skills. Each competency has a builder role (does the work) and an evaluator role (reviews the output with domain-matching knowledge). This is the **dual-control principle** — no agent evaluates its own work.

### 4.1 Competencies

**Note on Data Research:** Data Research is a required competency (see sub-product recipes §3.1) with no live agents yet — `data-researcher` (builder) and `data-research-reviewer` (evaluator) are gaps tracked in §5.2.

**Note on Data Architecture builder:** The Design task in data sub-products requires a `data-architect` builder agent. This is currently done by main Claude via `/plan`. A dedicated agent is a gap tracked in §5.2.

| # | Competency | Core skills | Builder agent | Evaluator agent | Sub-products served |
|---|-----------|-------------|--------------|-----------------|---------------------|
| 0 | **Data Research** | Source discovery, API/file analysis, indicator selection, data quality, licence assessment | `data-researcher` *(gap)* | `data-research-reviewer` *(gap)* | #1 |
| 1 | **Data Architecture** | Dimensional modelling, data vault, schema design, layer contracts, medallion architecture | `data-architect` *(gap — main Claude)* | `architecture-critic` | #1–#6 (Design tasks) |
| 2 | **Data Engineering** | ETL scripting, SQL, DuckDB, dbt, API integration, data quality | `data-engineer` | `data-engineer-reviewer` | #1–#4, #6 (Build tasks) |
| 3 | **Semantic Modelling** | MetricFlow measures/metrics/dimensions, aggregation correctness, format_type, unit/scale, Polish labelling | `data-engineer` | `measures-reviewer` | #4 |
| 4 | **UX / UI Design** | Visual perception, cognitive load, Gestalt, colour theory, eye-tracking, WCAG, dashboard layout | `dashboard-dev` | `visual-screenshot-reviewer` | #5, #7, #9, #12, #13, #15, #16 (Design tasks) |
| 5 | **Dashboard Development** | Plotly, Dash, Python, Nordic design system, component API, responsive layout | `dashboard-dev` | `visual-screenshot-reviewer` | #5, #9, #12, #13, #15, #16, #17 (Build tasks) |
| 6 | **Business Analysis** | KPI theory, indicator selection, aggregation methods, insight hierarchy, Polish public data context | `business-analyst` | `brief-reviewer` | #4, #12, #15, #17, #18 (Domain brief tasks) |
| 7 | **Domain Specialist** | Domain-specific economics, policy frameworks, benchmark knowledge, Polish statistical context | — *(evaluator only)* | `domain-specialist` | #15 (Domain review tasks) |
| 8 | **Analytical Methods** | Statistical correctness, aggregation in queries, causal language, chart labelling | — *(evaluator only)* | `analytical-validator` | #15, #18 (Analytical review tasks) |
| 9 | **Content / Editorial** | Data journalism, Polish language, storytelling, editorial standards, Ghost CMS | `content-writer` | `content-reviewer` | #12, #17 |
| 10 | **Research** | Econometrics, statistical methods, academic standards, model application | `researcher` | `research-reviewer` | #18 |
| 11 | **Platform / Ops** | Linux, Docker, nginx, systemd, SSL, deployment, performance | `ops-engineer` | `ops-reviewer` | #8, #11, #14 |
| 12 | **Cost Estimation** | Token usage patterns, task complexity modelling, decomposition heuristics | — | `cost-estimator` | All (feasibility gate) |
| 13 | **Diagnostics** | Tracing, root cause analysis, read-only investigation | — | `debug` | All (ad-hoc) |

### 4.2 Builder / Evaluator principle

For every atomic task:
- A **builder** agent does the work
- An **evaluator** agent with matching or higher competency reviews the output independently
- The evaluator does not see the builder's reasoning — only the output
- If the evaluator finds issues: the builder fixes, the evaluator re-reviews (autonomous loop)
- Only genuine deadlocks (N retries, still blocked) surface to the human

Human touch-points are strategic only:
- **Plan direction** — human sees a brief summary, can redirect; otherwise auto-proceeds
- **PR merge** — human authorises deployment to production
- **Deadlock** — human resolves when agents cannot converge

---

## 5. Agent Roster

### 5.1 Current agents

| Agent | Competency | Role | Phase | Status |
|-------|-----------|------|-------|--------|
| `debug` | Diagnostics | Evaluator | Ad-hoc | ✓ Live |
| `architecture-critic` | Data Architecture | Evaluator | Plan | ✓ Live |
| `code-reviewer` | Data Engineering | Evaluator | PR | ✓ Live |
| `data-engineer-reviewer` | Data Engineering | Evaluator (platform/ only) | PR | ✓ Live |
| `visual-screenshot-reviewer` | Dashboard Dev / UX | Evaluator (diff) | PR | ✓ Live |
| `visual-screenshot-reviewer` | UX / UI Design | Evaluator (screenshot + perception science) | PR | ✓ Live |
| `analytical-validator` | Analytical Methods | Evaluator | Plan + PR | ✓ Live |
| `brief-reviewer` | Business Analysis | Evaluator (brief only) | Plan | ✓ Live |
| `domain-specialist` | Domain Specialist | Evaluator | Plan + PR | ✓ Live |
| `measures-reviewer` | Semantic Modelling | Evaluator (semantic layer only) | PR | ✓ Live |
| `data-engineer` ¹ | Data Engineering + Semantic Modelling | Builder | Implementation | ✓ Live |
| `dashboard-dev` | UX / UI Design + Dashboard Development | Builder | Implementation | ✓ Live |
| `business-analyst` | Business Analysis | Builder | Plan + Implementation | ✓ Live |
| `content-writer` | Content / Editorial | Builder | Implementation | ✓ Live |
| `content-reviewer` | Content / Editorial | Evaluator (content only) | Pre-publication | ✓ Live |
| `researcher` | Research | Builder | Implementation | ✓ Live |
| `research-reviewer` | Research | Evaluator (research only) | Pre-publication | ✓ Live |
| `ops-engineer` | Platform / Ops | Builder | Implementation | ✓ Live |
| `ops-reviewer` | Platform / Ops | Evaluator (infra only) | Pre-deployment | ✓ Live |
| `cost-estimator` | Cost Estimation | Evaluator | Feasibility | ✓ Live |

¹ Previously named `data-architect` — renamed to `data-engineer` (OR-138). Covers Data Engineering Build tasks and Semantic Modelling Build tasks. Does **not** cover Data Architecture Design tasks (those are a gap — see §5.2).

### 5.2 Planned agents and gaps

| Agent | Competency | Role | Phase | Track |
|-------|-----------|------|-------|-------|
| `data-architect` | Data Architecture | Builder (Design task) | Plan | **Gap** — currently main Claude via `/plan` |
| `data-researcher` | Data Research | Builder | Research | **Gap** — no dedicated agent |
| `data-research-reviewer` | Data Research | Evaluator | Research | **Gap** — no evaluator for research output |
| `content-writer` | Content / Editorial | Builder | Implementation | ✓ Live (OR-135) |
| `content-reviewer` | Content / Editorial | Evaluator | PR | ✓ Live (OR-135) |
| `researcher` | Research | Builder | Implementation | ✓ Live (OR-136) |
| `research-reviewer` | Research | Evaluator | PR | ✓ Live (OR-136) |
| `ops-engineer` | Platform / Ops | Builder | Implementation | ✓ Live (OR-137) |
| `ops-reviewer` | Platform / Ops | Evaluator | Pre-deployment | ✓ Live (OR-137) |

### 5.3 Agent invocation map

Agent selection is driven by the sub-product recipe (§3): the recipe for the sub-product being worked on determines which agents run at which phase.

```
/feasibility (pre-sprint) — triggered by /review-ideas, /sprint, /kickoff
  → architecture-critic (data model compatibility, layer feasibility)
  → analytical-validator (analytical design validity)
  → cost-estimator (token budget, scope estimate)
  All parallel. FEASIBLE → proceed. PARTIAL → note conditions. BLOCKED → return for redesign.

/domain-brief (when business-analyst produces a brief — sub-products #4, #12, #15, #17, #18)
  → brief-reviewer (SMART+FABRIC, aggregation rules, benchmarks, Polish structural breaks)
  BLOCK → business-analyst revises → re-review. CONDITIONAL → noted in plan Risks.

/plan (before coding)
  → architecture-critic (structural soundness, layer contracts)
  → analytical-validator (analytical soundness — if analytical design involved)
  → domain-specialist (domain KPI correctness — if domain-specific)
  Parallel. All must APPROVE before plan shown to human.

/review (after coding)
  Part 0: always
    → code-reviewer
  Part 0.1: if diff touches platform/ (sub-products #1–#4, #6)
    → data-engineer-reviewer
  Part 0.2: if diff touches dashboards or visuals (sub-products #5, #9, #12–#16)
    → visualization-reviewer
    → analytical-validator
  Part 0.3: if diff touches semantic layer (sub-product #4)
    → measures-reviewer
  Part 0.4: if diff touches a domain dashboard (sub-product #15)
    → domain-specialist
  Part 0.5: if any dashboard/visual changed
    → visual-screenshot-reviewer (screenshot gate)
  Any BLOCK → builder fixes → re-review (autonomous loop, no human).

/self-improve (after every issue, automatic)
  → Update lessons-learned.md
  → Update token usage history
  → Flag recurring patterns for standards review
```

---

## 6. Quality System

### 6.1 The derivation chain

Quality is only defensible when rules are traceable to research. The chain is:

```
PRIMARY SOURCES (academic papers, standards bodies, authoritative publications)
      ↓
docs/{competency}/     ← Research synthesis. No opinions.
      ↓
docs/{standard}.md    ← Our implementation decisions, KB-derived.
      ↓
docs/{rules}.md  ← Agent evaluation checklist, traced to standard.
      ↓
.claude/agents/{evaluator}.md         ← Agent reads evaluation rules, applies to output.
```

Every evaluation standard file opens with:
```
Derived from: docs/{path}
Used by: .claude/agents/{agent}.md
Does NOT cover: {explicit scope boundary}
```

### 6.2 Feasibility gate

Triggered at `/review-ideas` (idea → issue conversion), `/sprint` (backlog → Todo), and `/kickoff` (before implementation).

Three evaluators run in parallel and return: **FEASIBLE / PARTIAL / BLOCKED**.

| Evaluator | Checks |
|-----------|--------|
| `architecture-critic` | Data model compatibility, schema conflicts, layer-contract feasibility |
| `analytical-validator` | Analytical design validity, aggregation soundness, misleading framing risks |
| `cost-estimator` | Token budget estimate, scope complexity, decomposition recommendation |

Note: `domain-specialist`, `data-engineer-reviewer`, and `measures-reviewer` are PR-phase reviewers and are not part of the feasibility gate. Their feedback happens later in the pipeline, at `/plan` (domain) and `/review` (diff-scoped reviewers).

**Decision rule:**
- All FEASIBLE → issue accepted, moves to Backlog
- Any PARTIAL → issue accepted with noted conditions
- Any BLOCKED → issue returned for redesign; specific blocker documented on the Linear issue

### 6.3 Autonomous review loop

The builder/evaluator cycle runs without human involvement:

```
Builder produces output
    ↓
Evaluator reviews
    ↓
PASS → proceed to next step
CONDITIONAL → builder addresses, evaluator re-reviews (max 2 iterations)
BLOCK → builder fixes, evaluator re-reviews (max 3 iterations)
    ↓ (if still blocked after max iterations)
Escalate to human with: what was tried, what is still blocking, options
```

Human is never involved in iteration — only in resolution of genuine deadlocks.

### 6.4 Self-improvement loop

**After every issue (automatic — part of `/document` skill):**
- `docs/lessons-learned.md` updated: what worked, what failed, actual token usage vs estimate
- Recurring failure patterns flagged: if the same type of finding appears 3+ times in lessons-learned, a standards update is proposed

**After every 10 issues (scheduled):**
- `/standards-review` skill (planned): reads lessons-learned, identifies patterns, proposes updates to evaluation standards
- No human involvement unless a structural change is recommended

**Monthly KB-to-standards drift check (planned):**
- Agent reads each KB file and its corresponding evaluation standard
- Flags contradictions or staleness (standard not updated after KB revision)

### 6.5 Cost estimation

The `cost-estimator` agent provides a token budget forecast before any task starts. It is not a precise calculator — it is a risk flag.

**Estimation model:**

| Task type | Typical range | Risk level |
|-----------|-------------|-----------|
| Config / docs only | 10–30k tokens | Low |
| Single-file feature, no agents | 20–50k tokens | Low |
| Multi-file feature, 3 parallel agents | 80–200k tokens | Medium |
| Feature with web research | 150–400k tokens | High |
| Full domain dashboard (research + build + review) | 400k–1M+ | Very High |

**Inputs to the estimate:**
- Issue type and description complexity
- Number of files likely involved (estimated from scope)
- Number of agent invocations required
- Whether web search / external sources are needed
- Historical data from `docs/lessons-learned.md` for similar task types

**Output:** estimated range + risk level + recommendation (proceed / split into sub-issues / warn about rate limit risk)

The estimate improves as `lessons-learned.md` accumulates actual token counts per task type.

---

## 7. Knowledge Base Map

Each KB entry is research-first — no opinions, only synthesis of authoritative sources. Reading list is in each KB file's header.

### 7.1 Current KB

| KB | Location | Status | Grounded in |
|----|----------|--------|-------------|
| Analytical methods | `docs/analytical-methods/principles.md` | ✓ Complete | ONS, UNECE, IZA, GSS, IRE, GIJN |
| Visualization principles | `docs/visualization/principles.md` | ✓ Complete | Playfairdata, EU Data Viz Guide, IBCS |
| Visualization charts | `docs/visualization/charts/*.md` (7 files) | ✓ Complete | Same sources |
| Visualization UI | `docs/visualization/ui-principles.md` | ✓ Complete | Same sources |
| UX / Perception | `docs/ux-perception/principles.md` | ✓ Complete | Colin Ware, Treisman, Sweller, Nielsen Norman, WCAG 2.2 |
| Data Architecture | `docs/data-architecture/principles.md` | ✓ Complete | Kimball, Databricks medallion, dbt Labs |
| Data Engineering | `docs/data-engineering/principles.md` | ✓ Complete | DuckDB docs, dbt docs, DAMA, ANSI SQL |
| Business Analysis | `docs/business-analysis/principles.md` | ✓ Complete | Eurostat, OECD, Kaplan & Norton, ONS, IMF, GUS |
| Domain — public finance | `docs/public-finance/principles.md` | Draft — needs review | Eurostat, IMF, MF Poland |
| Domain — labour market | `docs/labour-market.md` | Planned | ILO, Eurostat, IZA |
| Economics theory | `products/research/library/` | Partial | Standard textbooks |

### 7.2 Planned KB (priority order)

| KB | Location | Priority | Sources to research |
|----|----------|----------|-------------------|
| **Content / Editorial** | `docs/content/` | Medium | Data journalism curricula (Columbia, CUL), Reuters Institute, GUS publication style, Polish editorial standards |
| **Research Methods** | `docs/research-methods/` | Medium | Econometrics textbooks, panel data methods, reproducible research standards |

### 7.3 Domain KB (per domain, on demand before dashboard work)

| Domain | KB file | Status |
|--------|---------|--------|
| Public Finance | `docs/public-finance/principles.md` | Draft |
| Labour Market | `docs/labour-market.md` | Planned |
| Demographics | `docs/demographics.md` | Not started |
| (remaining 15 domains) | `docs/{domain}.md` | Not started |

Domain KB files are created via `/domain-brief` skill before any dashboard work begins on that domain.

---

## 8. Standards Map

### 8.1 Build standards (how we build)

Developer-facing. Derived from KB. Tells practitioners what to do.

| Standard | File | Derived from KB | Status |
|----------|------|----------------|--------|
| Data ingestion | `docs/data-engineering/ingestion.md` | `knowledge-base/data-engineering/` ✓ | ✓ Live |
| Data processing | `docs/data-engineering/processing.md` | `knowledge-base/data-engineering/` ✓ | ✓ Live |
| Data storage | `docs/data-engineering/storage.md` | `knowledge-base/data-architecture/` ✓ | ✓ Live |
| Visualisation design | `docs/visualization/building.md` | `knowledge-base/visualization/` ✓ + `ux-perception/` ✓ | ✓ Live |
| Measures | `docs/data-engineering/measures.md` | `knowledge-base/business-analysis/` ✓ | ✓ Live |
| Linear requirements | `docs/process/requirements.md` | — (workflow, not KB-derived) | ✓ Live |

### 8.2 Evaluation standards (how we review)

Agent-facing. Derived from KB via build standard. Tells evaluator agents what to check.

| Standard | File | Derived from | Agent that uses it | Status |
|----------|------|-------------|-------------------|--------|
| Code review | `docs/process/code-review.md` | `knowledge-base/data-engineering/` ✓ | `code-reviewer` | ✓ Live |
| Architecture review | `docs/data-architecture/reviewing.md` | `knowledge-base/data-architecture/` ✓ | `architecture-critic` | ✓ Live |
| Analytical review | `docs/analytical-methods/reviewing.md` | `knowledge-base/analytical-methods/` ✓ | `analytical-validator` | ✓ Live |
| Data engineering review | `docs/data-engineering/reviewing.md` | `knowledge-base/data-engineering/` ✓ + `data-architecture/` ✓ | `data-engineer-reviewer` | ✓ Live |
| Visualization diff | `docs/visualization/reviewing.md` | `knowledge-base/visualization/` ✓ + `ux-perception/` ✓ | `visual-screenshot-reviewer` | ✓ Live |
| Visualization image | `docs/visualization/reviewing.md` | `knowledge-base/ux-perception/` ✓ | `visual-screenshot-reviewer` | ✓ Live |
| Measures review | `docs/data-engineering/measures-review.md` | `knowledge-base/business-analysis/` ✓ + `analytical-methods/` ✓ + `build/measures.md` | `measures-reviewer` | ✓ Live |
| Brief review | `docs/business-analysis/reviewing.md` | `knowledge-base/business-analysis/` ✓ + `analytical-methods/` ✓ | `brief-reviewer` | ✓ Live |
| Cost estimation rules | *(heuristics inline in agent)* | `docs/lessons-learned.md` | `cost-estimator` | ✓ Live (no standalone file) |
| Domain review | *(heuristics inline in agent)* | `knowledge-base/domains/{domain}/` | `domain-specialist` | ✓ Live (no standalone file) |

---

## 9. Document Architecture

### 9.1 Principle: one purpose per directory, one source per topic

Every document declares:
- **Purpose** — what it is
- **Audience** — who reads it
- **Derived from** — what feeds it (upstream)
- **Used by** — what reads it (downstream)
- **Does NOT cover** — explicit boundary

### 9.2 Directory map

```
/opt/open-reporting/
│
├── README.md                    ← Project intro + MASTER DOC INDEX
│                                  Entry point to all documentation
│
├── CLAUDE.md                    ← AI orchestrator config. References this file
│                                  for team design. Not a workflow doc.
│
├── docs/                        ← Project documentation (what was built, decisions)
│   ├── PROJECT.md               ← Vision, mission, what we make
│   ├── ARCHITECTURE.md          ← Technical infrastructure (VPS, Docker, nginx)
│   ├── DATA_MODEL.md            ← Warehouse design decisions
│   ├── DATA_SOURCES.md          ← Source policy
│   ├── DOMAINS.md               ← 18-domain taxonomy
│   ├── CONTRIBUTING.md          ← Git/PR process for contributors
│   ├── RELEASE_NOTES.md         ← Changelog
│   ├── ROADMAP.md               ← Direction
│   └── MVP.md                   ← MVP summary
│
├── platform/                    ← Data platform code + inline docs
│   ├── ingestion/               ← ETL scripts
│   ├── processing/dbt/          ← dbt models
│   └── warehouse/
│       └── bus_matrix.md        ← Kimball bus matrix (data artefact, stays here)
│
├── products/                    ← Product code
│   ├── domain-briefs/           ← Domain research outputs — shared components (one per domain)
│   ├── dashboards/              ← Dash apps
│   ├── visuals/                 ← Reusable components
│   ├── research/                ← Research product
│   │   ├── CLAUDE.md            ← Research sub-agent (extends root CLAUDE.md)
│   │   └── library/             ← Economic theory reference (research product KB)
│   ├── portal/
│   ├── blog/
│   ├── mobile/
│   └── social/
│
├── tools/                       ← Utility scripts (screenshot.py etc.)
│
├── infra/                       ← Infrastructure configuration
│
└── docs/                        ← TEAM OPERATING SYSTEM
    │
    ├── PLATFORM.md              ← THIS FILE. The factory blueprint.
    │
    ├── session-memory.md        ← AI working memory (current session state)
    ├── lessons-learned.md       ← Continuous improvement log + token history
    │
    ├── knowledge-base/          ← Research syntheses. Source-first, no opinions.
    │   ├── INDEX.md             ← What exists, what is planned, loading guide
    │   ├── analytical-methods/  ← Statistical thinking, aggregation, insight framing
    │   ├── visualization/       ← Chart theory, perception principles, UI
    │   ├── ux-perception/       ← Neuroscience, eye-tracking, cognitive load (PRIORITY)
    │   ├── data-architecture/   ← Kimball, medallion, modelling theory
    │   ├── data-engineering/    ← ETL, SQL, dbt standards
    │   ├── business-analysis/   ← KPI theory, indicator frameworks
    │   ├── domains/             ← Per-domain distilled KB
    │   └── content/             ← Data journalism, Polish writing, storytelling
    │
    ├── standards/
    │   ├── INDEX.md             ← Which standard covers what + KB derivation links
    │   ├── build/               ← How we build (developer-facing)
    │   │   ├── ingestion.md
    │   │   ├── processing.md
    │   │   ├── storage.md
    │   │   ├── visualisation.md
    │   │   ├── measures.md
    │   │   └── requirements.md
    │   └── evaluation/          ← How we review (agent-facing)
    │       ├── code-review.md
    │       ├── visualization-diff.md
    │       ├── visualization-image.md
    │       └── analytical-review.md
    │
    └── playbooks/               ← Step-by-step process guides
        ├── dashboard.md
        └── social.md
```

### 9.3 Workflow documents (not duplicated)

| Topic | Authoritative source | Other references |
|-------|---------------------|-----------------|
| Three-stage workflow | `CLAUDE.md` | `docs/CONTRIBUTING.md` (human-readable summary, links to CLAUDE.md) |
| Sprint process | `.claude/skills_review/composite_sprint/SKILL.md` (under review) | `docs/ROADMAP.md` (links to Linear) |
| Issue templates | `docs/process/requirements.md` | Referenced from CLAUDE.md |
| Git conventions | `CLAUDE.md` | `docs/CONTRIBUTING.md` |

---

## 10. Workflow Processes

### 10.1 Skill map

| Skill | Stage | Invokes agents | Human gate |
|-------|-------|---------------|-----------|
| `/capture-idea` | 1 — Collect | None | Brief confirm |
| `/review-ideas` | 2 — Convert | `feasibility-panel` (planned) | Accept/reject |
| `/sprint` | 2 — Prioritise | `cost-estimator` (planned) | Priority approval |
| `/kickoff OR-XXX` | 3 — Implement | Drives full pipeline | Plan skim + merge |
| `/domain-brief` | 3 — Research | Domain researcher | None |
| `/research` | 3 — Research | None (orchestrator does it) | None |
| `/plan` | 3 — Design | `architecture-critic` + `analytical-validator` | Direction skim |
| `/review` | 3 — QA | All evaluators (parallel) | None (auto if PASS) |
| `/commit` | 3 — Deliver | None | None |
| `/document` | 3 — Document | Self-improvement updater | None |

### 10.2 Autonomous loop design

The orchestrator (Lead Analyst & Architect) drives the loop. Human involvement is minimised:

```
kickoff
  ├─ domain-brief (if new domain) ────────────── no human
  ├─ research ──────────────────────────────────── no human
  ├─ plan
  │    ├─ architecture-critic ─── fix if BLOCK ── no human
  │    ├─ analytical-validator ── fix if BLOCK ── no human
  │    └─ present to human ────────────────────── HUMAN SKIMS (30-60s)
  │         └─ proceed on no objection
  ├─ implement ────────────────────────────────── no human
  ├─ review
  │    ├─ all evaluators parallel ── fix if BLOCK ── no human (loop)
  │    ├─ screenshot reviewer ─────── fix if BLOCK ── no human (loop)
  │    └─ if all PASS: auto-commit ────────────── no human
  ├─ open PR ──────────────────────────────────── no human
  ├─ merge ────────────────────────────────────── HUMAN APPROVES
  ├─ document + lessons-learned ───────────────── no human
  └─ close issue ──────────────────────────────── no human
```

---

## 11. Current State

### 11.1 What is live

**Products:** Portal (labour, explorer, finance dashboards) + Blog + Mobile + Instagram

**Platform:** DuckDB warehouse (222 indicators, 18 domains) + 3-source ingestion (Eurostat, NBP, GUS DBW) + dbt (22 curated models) + Kimball dimensional model

**Team infrastructure:**
- 14 agents live (debug, architecture-critic, code-reviewer, data-engineer-reviewer, visualization-reviewer, visual-screenshot-reviewer, analytical-validator, brief-reviewer, domain-specialist, measures-reviewer, data-engineer, dashboard-dev, business-analyst, cost-estimator)
- 18 sub-products defined with formal recipes (§3) across 6 groups
- 14 skills live (including /feasibility + /standards-review)
- KB: analytical-methods ✓, visualization ✓, ux-perception ✓, data-architecture ✓, data-engineering ✓, business-analysis ✓; public-finance domain draft
- Standards: 6 build standards ✓, 8 evaluation standards ✓

### 11.2 What is next (priority order)

| # | Item | Type | Status | Blocks |
|---|------|------|--------|--------|
| 1–6, 11 | Agent + standard gap closure (previous pass) | Agents + standards | ✅ Done | See git log |
| 12 | Sub-product recipe system | PLATFORM.md restructure | ✅ Done | Recipe-based routing for all ORs |
| 13 | Rename `data-architect` → `data-engineer` | Agent + references | ✅ Done (OR-138) | Naming matches recipe system |
| 14 | `data-researcher` + `data-research-reviewer` agents + standards | Agents + standards | 🔜 Next | Closes Data Research competency gap |
| 15 | `data-architect` as dedicated Design-phase builder | Agent | 🔜 Next | Closes Data Architecture builder gap |
| 7 | Content / Editorial KB + content-writer/reviewer agents | Knowledge base + agents | 📋 Planned (OR-135) | Blog editorial standards, data journalism quality |
| 8 | Research Methods KB + researcher/research-reviewer agents | Knowledge base + agents | 📋 Planned (OR-136) | Econometrics, reproducible research standards |
| 9 | Platform / Ops KB + ops-engineer/ops-reviewer agents | Knowledge base + agents | 📋 Planned (OR-137) | Infra change review quality |
| 10 | Public-finance domain KB | KB — draft promotion | 🔜 Next | Move from Draft to Complete |
| 16 | Article playbook | Playbook | 🔜 Next | Sub-product #17 has no playbook |
| 17 | Research playbook | Playbook | 🔜 Next | Sub-product #18 has no playbook |
