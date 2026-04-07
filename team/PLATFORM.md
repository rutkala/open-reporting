# Open Reporting — Platform Blueprint

**Version:** 1.0 | **Owner:** Lead Analyst & Architect | **Updated:** 2026-04-07

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

### 1.2 Sub-products (assembled into finished products)

| Sub-product | Used in | Description |
|-------------|---------|-------------|
| **Dashboards** | Portal, Blog, Mobile | Dash interactive apps per domain |
| **Visuals / Charts** | Dashboards, Articles, Social | Reusable Plotly chart + KPI components |
| **Articles** | Blog, Social | Editorial data journalism pieces |
| **Social Cards** | Social, Blog | Visual exports for Instagram |
| **Research** | Articles, Dashboards | Quantitative analysis, econometric models |
| **Data Cards** | Social | Formatted single-stat visual exports |

### 1.3 Sub-product relationships

```
Portal
  └── Dashboards
        ├── Visuals (chart components)
        ├── Semantic Model (measures, dimensions)
        └── Curated Data Layer

Blog
  ├── Articles
  │     ├── Visuals (embedded charts)
  │     └── Research (analysis backing)
  └── Social Cards → Social Media

Mobile App
  └── Portal + Blog (PWA wrapper)

Social Media
  └── Social Cards
        └── Visuals
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
  Curated Data Layer         ←──────  team/knowledge-base/
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
| Visual component library | `products/visuals/components/` | Live |
| Semantic model | `products/semantic/` | Live (legacy, migration pending) |
| Dashboards (labour, explorer, finance) | `products/dashboards/` | Live |
| Blog (Ghost CMS) | Docker / Ghost | Live |
| Mobile PWA | `products/mobile/` | Live |
| Social publishing | `products/social/` | Live |
| Research library | `products/research/` | Partial |
| Data ingestion | `platform/ingestion/` | Live |
| dbt transforms | `platform/processing/dbt/` | Live |
| DuckDB warehouse | `data/warehouse.duckdb` | Live |
| PostgreSQL operational DB | Docker / postgres | Live |

---

## 3. Task Taxonomy

Every unit of work belongs to one of these task types. Task type determines which competencies are required and which agents are involved.

| Domain | Task types |
|--------|-----------|
| **Data** | Source research · Data ingestion · Schema design · dbt transformation · Data quality validation · Semantic modelling |
| **Analytics** | Domain research · KPI design · Indicator selection · Statistical analysis · Insight framing · Benchmark selection |
| **Development** | Dashboard development · Visual component development · Research notebook · Content tooling |
| **Content** | Article writing · Social card creation · Data storytelling · Editorial review |
| **Infrastructure** | Service configuration · Deployment · SSL / DNS · Performance |
| **Quality** | Code review · Architecture review · Visual design review · Analytical review · Domain review · Feasibility study |
| **Workflow** | Sprint planning · Issue management · Documentation · Version control · Self-improvement |

---

## 4. Competency Map

Competency = a cluster of related skills. Each competency has a builder role (does the work) and an evaluator role (reviews the output with domain-matching knowledge). This is the **dual-control principle** — no agent evaluates its own work.

### 4.1 Competencies

| # | Competency | Core skills | KB that grounds it |
|---|-----------|-------------|-------------------|
| 1 | **Data Architecture** | Dimensional modelling, data vault, schema design, layer contracts, medallion architecture | `knowledge-base/data-architecture/` |
| 2 | **Data Engineering** | ETL scripting, SQL, DuckDB, dbt, API integration, data quality | `knowledge-base/data-engineering/` |
| 3 | **UX / UI Design** | Visual perception, cognitive load, Gestalt, colour theory, eye-tracking, WCAG, dashboard layout | `knowledge-base/ux-perception/` |
| 4 | **Dashboard Development** | Plotly, Dash, Python, Nordic design system, component API, responsive layout | `knowledge-base/ux-perception/` + `standards/build/visualisation.md` |
| 5 | **Business Analysis** | KPI theory, indicator selection, aggregation methods, insight hierarchy, Polish public data context | `knowledge-base/business-analysis/` + `knowledge-base/analytical-methods/` |
| 6 | **Domain Specialist** | Domain-specific economics, policy frameworks, benchmark knowledge, Polish statistical context | `knowledge-base/domains/{domain}.md` |
| 7 | **Content / Editorial** | Data journalism, Polish language, storytelling, editorial standards, Ghost CMS | `knowledge-base/content/` |
| 8 | **Research** | Econometrics, statistical methods, academic standards, model application | `products/research/library/` |
| 9 | **Platform / Ops** | Linux, Docker, nginx, systemd, SSL, deployment, performance | — |
| 10 | **Cost Estimation** | Token usage patterns, task complexity modelling, decomposition heuristics | `team/lessons-learned.md` (historical) |
| 11 | **Diagnostics** | Tracing, root cause analysis, read-only investigation | — |

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
| `visualization-reviewer` | Dashboard Dev / UX | Evaluator (diff) | PR | ✓ Live |
| `visual-screenshot-reviewer` | UX / UI Design | Evaluator (screenshot + perception science) | PR | ✓ Live |
| `analytical-validator` | Business Analysis | Evaluator | Plan + PR | ✓ Live |
| `domain-specialist` | Domain Specialist | Evaluator | Plan + PR | ✓ Live |
| `business-analyst` | Business Analysis | Builder | Plan + Implementation | ✓ Live |
| `cost-estimator` | Cost Estimation | Evaluator | Feasibility | ✓ Live |

### 5.2 Planned agents

| Agent | Competency | Role | Phase | Priority |
|-------|-----------|------|-------|----------|
| `data-architect` | Data Architecture | Builder | Implementation | Medium |
| `data-engineer-reviewer` | Data Engineering | Evaluator (domain-matched) | PR | Medium |
| `ui-designer` | UX / UI Design | Builder | Implementation | Low |
| `content-writer` | Content / Editorial | Builder | Implementation | Low |
| `content-reviewer` | Content / Editorial | Evaluator | PR | Low |
| `researcher` | Research | Builder | Implementation | Low |
| `research-reviewer` | Research | Evaluator | PR | Low |
| `ops-engineer` | Platform / Ops | Builder | Implementation | Low |
| `ops-reviewer` | Platform / Ops | Evaluator | PR | Low |

### 5.3 Agent invocation map

```
/feasibility (pre-sprint) ← NEW: wired via /review-ideas + /sprint + /kickoff
  → architecture-critic (data feasibility)
  → analytical-validator (analytical feasibility)
  → cost-estimator (token budget)
  All parallel. FEASIBLE → issue accepted.
  PARTIAL → accept with conditions. BLOCKED → return for redesign.

/plan (before coding)
  → architecture-critic (structural soundness)
  → analytical-validator (analytical soundness)
  Both parallel. Must both APPROVE before plan shown to human.

/review (after coding)
  Part 0: parallel
    → code-reviewer
    → visualization-reviewer
    → analytical-validator
  Part 0.5: if dashboard changed
    → visual-screenshot-reviewer
  Any BLOCK → builder fixes → re-review (autonomous, no human).

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
team/knowledge-base/{competency}/     ← Research synthesis. No opinions.
      ↓
team/standards/build/{standard}.md    ← Our implementation decisions, KB-derived.
      ↓
team/standards/evaluation/{rules}.md  ← Agent evaluation checklist, traced to standard.
      ↓
.claude/agents/{evaluator}.md         ← Agent reads evaluation rules, applies to output.
```

Every evaluation standard file opens with:
```
Derived from: team/knowledge-base/{path}
Used by: .claude/agents/{agent}.md
Does NOT cover: {explicit scope boundary}
```

### 6.2 Feasibility gate

Triggered at `/review-ideas` (idea → issue conversion) and `/sprint` (backlog → Todo).

All relevant evaluators run in parallel and return: **FEASIBLE / PARTIAL / BLOCKED**.

| Evaluator | Checks |
|-----------|--------|
| `architecture-critic` | Data model compatibility, schema conflicts |
| `analytical-validator` | Analytical design validity |
| `cost-estimator` | Token budget estimate, decomposition recommendation |
| `domain-specialist` | Domain framing correctness, KPI validity |
| `data-engineer-reviewer` | Source data availability, ingestion feasibility |

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
- `team/lessons-learned.md` updated: what worked, what failed, actual token usage vs estimate
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
- Historical data from `team/lessons-learned.md` for similar task types

**Output:** estimated range + risk level + recommendation (proceed / split into sub-issues / warn about rate limit risk)

The estimate improves as `lessons-learned.md` accumulates actual token counts per task type.

---

## 7. Knowledge Base Map

Each KB entry is research-first — no opinions, only synthesis of authoritative sources. Reading list is in each KB file's header.

### 7.1 Current KB

| KB | Location | Status | Grounded in |
|----|----------|--------|-------------|
| Analytical methods | `team/knowledge-base/analytical-methods/analytical-thinking.md` | ✓ Complete | ONS, UNECE, IZA, GSS, IRE, GIJN |
| Visualization principles | `team/knowledge-base/visualization/principles.md` | ✓ Complete | Playfairdata, EU Data Viz Guide, IBCS |
| Visualization charts | `team/knowledge-base/visualization/charts/*.md` (7 files) | ✓ Complete | Same sources |
| Visualization UI | `team/knowledge-base/visualization/ui-principles.md` | ✓ Complete | Same sources |
| UX / Perception | `team/knowledge-base/ux-perception/perception.md` | ✓ Complete | Colin Ware, Treisman, Sweller, Nielsen Norman, WCAG 2.2 |
| Data Architecture | `team/knowledge-base/data-architecture/architecture.md` | ✓ Complete | Kimball, Databricks medallion, dbt Labs |
| Data Engineering | `team/knowledge-base/data-engineering/engineering.md` | ✓ Complete | DuckDB docs, dbt docs, DAMA, ANSI SQL |
| Business Analysis | `team/knowledge-base/business-analysis/kpi-indicator-design.md` | ✓ Complete | Eurostat, OECD, Kaplan & Norton, ONS, IMF, GUS |
| Domain — public finance | `team/knowledge-base/domains/public-finance.md` | Draft — needs review | Eurostat, IMF, MF Poland |
| Domain — labour market | `team/knowledge-base/domains/labour-market.md` | Planned | ILO, Eurostat, IZA |
| Economics theory | `products/research/library/` | Partial | Standard textbooks |

### 7.2 Planned KB (priority order)

| KB | Location | Priority | Sources to research |
|----|----------|----------|-------------------|
| **Content / Editorial** | `team/knowledge-base/content/` | Medium | Data journalism curricula (Columbia, CUL), Reuters Institute, GUS publication style, Polish editorial standards |
| **Research Methods** | `team/knowledge-base/research-methods/` | Medium | Econometrics textbooks, panel data methods, reproducible research standards |

### 7.3 Domain KB (per domain, on demand before dashboard work)

| Domain | KB file | Status |
|--------|---------|--------|
| Public Finance | `team/knowledge-base/domains/public-finance.md` | Draft |
| Labour Market | `team/knowledge-base/domains/labour-market.md` | Planned |
| Demographics | `team/knowledge-base/domains/demographics.md` | Not started |
| (remaining 15 domains) | `team/knowledge-base/domains/{domain}.md` | Not started |

Domain KB files are created via `/domain-brief` skill before any dashboard work begins on that domain.

---

## 8. Standards Map

### 8.1 Build standards (how we build)

Developer-facing. Derived from KB. Tells practitioners what to do.

| Standard | File | Derived from KB | Status |
|----------|------|----------------|--------|
| Data ingestion | `team/standards/build/ingestion.md` | `knowledge-base/data-engineering/` | Live — not yet KB-traced |
| Data processing | `team/standards/build/processing.md` | `knowledge-base/data-engineering/` | Live — not yet KB-traced |
| Data storage | `team/standards/build/storage.md` | `knowledge-base/data-architecture/` | Live — not yet KB-traced |
| Visualisation design | `team/standards/build/visualisation.md` | `knowledge-base/visualization/` + `ux-perception/` | Live — not yet KB-traced |
| Measures | `team/standards/build/measures.md` | `knowledge-base/business-analysis/` | Live — not yet KB-traced |
| Linear requirements | `team/standards/build/requirements.md` | — (workflow, not KB-derived) | Live |

### 8.2 Evaluation standards (how we review)

Agent-facing. Derived from KB via build standard. Tells evaluator agents what to check.

| Standard | File | Derived from | Agent that uses it | Status |
|----------|------|-------------|-------------------|--------|
| Code review | `team/standards/evaluation/code-review.md` | `knowledge-base/data-engineering/` | `code-reviewer` | Live — not KB-traced |
| Architecture review | `team/standards/evaluation/architecture-review.md` | `knowledge-base/data-architecture/` | `architecture-critic` | Implicit in agent — needs extraction |
| Visualization diff | `team/standards/evaluation/visualization-diff.md` | `knowledge-base/visualization/` + `ux-perception/` | `visualization-reviewer` | Live — not KB-traced |
| Visualization image | `team/standards/evaluation/visualization-image.md` | `knowledge-base/ux-perception/` | `visual-screenshot-reviewer` | Live — not KB-traced |
| Analytical review | `team/standards/evaluation/analytical-review.md` | `knowledge-base/analytical-methods/` | `analytical-validator` | Implicit in agent — needs extraction |
| Feasibility criteria | `team/standards/evaluation/feasibility.md` | All KB | `feasibility-panel` (planned) | Not built |
| Cost estimation rules | `team/standards/evaluation/cost-estimation.md` | `team/lessons-learned.md` | `cost-estimator` (planned) | Not built |
| Domain review | `team/standards/evaluation/domain-review.md` | `knowledge-base/domains/{domain}/` | `domain-specialist` (planned) | Not built |

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
└── team/                        ← TEAM OPERATING SYSTEM
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
    ├── domain-briefs/           ← Research outputs (what was found → feeds KB)
    │   └── public-finance.md    ← Links to: knowledge-base/domains/public-finance.md
    │
    └── playbooks/               ← Step-by-step process guides
        ├── dashboard.md
        └── social.md
```

### 9.3 Workflow documents (not duplicated)

| Topic | Authoritative source | Other references |
|-------|---------------------|-----------------|
| Three-stage workflow | `CLAUDE.md` | `docs/CONTRIBUTING.md` (human-readable summary, links to CLAUDE.md) |
| Sprint process | `.claude/skills/sprint/SKILL.md` | `docs/ROADMAP.md` (links to Linear) |
| Issue templates | `team/standards/build/requirements.md` | Referenced from CLAUDE.md |
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
- 9 agents live (debug, architecture-critic, code-reviewer, visualization-reviewer, visual-screenshot-reviewer, analytical-validator, domain-specialist, business-analyst, cost-estimator)
- 13 skills live (including /feasibility + /standards-review)
- KB: analytical-methods ✓, visualization ✓, ux-perception ✓, data-architecture ✓, data-engineering ✓, business-analysis ✓; public-finance domain draft
- Standards: 6 build standards live (KB-traceable), 5 evaluation standards live (full traceability — all KBs now complete)

### 11.2 What is next (priority order)

| # | Item | Type | Status | Blocks |
|---|------|------|--------|--------|
| 1 | KB-to-standards trace audit | Standards update | 🔜 Next | Re-trace build standards against new KBs; update rules where gaps found |
| 2 | Content / Editorial KB | Knowledge base | 📋 Planned | Blog editorial standards, data journalism quality |
| 3 | Research Methods KB | Knowledge base | 📋 Planned | Econometrics, reproducible research standards |
| 6 | `/feasibility` skill + agents | Skill + agents | ✅ Done | Pre-sprint quality gate |
| 7 | `cost-estimator` agent | Agent | ✅ Done | Token budget awareness |
| 8 | Autonomous loop updates | Skill updates | ✅ Done | Reduced human involvement |
| 9 | `visual-screenshot-reviewer` merged with `visual-design-reviewer` | Agent | ✅ Done | Consolidated into one agent backed by ux-perception KB |
| 10 | `domain-specialist` agent | Agent | ✅ Done | Domain review quality |
| 11 | `business-analyst` agent | Agent | ✅ Done | Analytical build quality |
| 12 | `/standards-review` skill | Skill | ✅ Done | Self-improvement loop |
| 13 | Extracted evaluation standards | Standards | ✅ Done | Traceability (analytical-review.md, architecture-review.md) |
