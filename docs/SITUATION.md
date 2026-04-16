# Open Reporting — Situation, Architecture & Plan

*Last updated: 2026-04-16*

---

## Who You Are

Economist and analyst, 10 years experience, 7 in Power BI and BI. Strong business instincts, analytical thinking, experience across the full project lifecycle. Not a technical engineer — no background in data engineering, infrastructure, or AI tooling.

You have ideas, domain instinct, and analytical experience. What you lack is the technical execution capacity and the time to do it all manually.

---

## What You Want to Build

**Open Reporting** — a platform that collects Polish public data and turns it into products:
- Analytical dashboards (one per statistical domain)
- Articles and blog content
- Academic research
- Social media content

There are ~18 public data domains (labour market, public finance, macroeconomics, health, education, etc.). Each domain can eventually have its own set of products.

**The Jarvis model:** You provide ideas, direction, and domain instinct. The AI handles all technical execution autonomously. You shouldn't need to understand how something is built — only whether the output is right.

---

## The Core Problem You Were Trying to Solve

You noticed the AI was working without enough guidance — producing output that didn't match your analytical standards. You tried to solve this by building detailed workflow infrastructure: agents, workstations, DAGs, standards, documentation.

This instinct was correct. But you were building the factory before building the first product. You were generalizing before having a concrete example to generalize from.

The result: the repo became a mix of two incomplete systems, neither working.

---

## Key Insight: How Domain Knowledge Actually Works

You don't have pre-built domain knowledge to give the AI. You'd need to research each domain yourself before designing a dashboard for it — what questions to ask, what data exists, what good analysis looks like.

This is not a weakness. It's the correct way to work. The AI researches the domain first (this is what `/domain-brief` does), builds a brief, and that brief becomes the domain knowledge that drives everything downstream.

You don't teach the AI your expertise upfront. You build expertise together, domain by domain, as you go.

---

## The AI Operating Principle (Most Important)

The AI should never be stuck and never transfer uncertainty to you. If it doesn't know something:
1. It researches it (web search, authoritative sources, codebase)
2. It forms a view based on research
3. It presents the decision and reasoning — not the open question

You should never be asked "what should I do?" You should only be asked "does this direction make sense?"

---

## The Architecture Vision

### Three Layers

```
LAYER 1 — KNOWLEDGE          LAYER 2 — BUILD              LAYER 3 — PRODUCTS
─────────────────────        ────────────────────         ──────────────────────
What to build & why          How to build it              What gets published

Domain Brief                 Data Pipeline                Dashboard
Requirements Doc             Dashboard Build              Article
                             Code Review                  Social content
```

### Products and Components

Everything is either a **Product** or a **Component**. Each has its own DAG.

**Products** — standalone publishable outputs:
- Dashboard
- Article / Blog post
- Social media content
- Academic research

Products are independent. An article about the labour market and a labour market dashboard are two separate products. They may share components (same domain brief, same data), but they have separate processes, separate issues in Linear, separate DAGs.

### What gets its own Linear issue

Not everything needs a Linear issue — only things that deserve dedicated attention and resources because getting them wrong has consequences downstream.

**Gets its own issue:**
- Domain Brief — research-heavy, wrong brief = wrong everything built on top
- Requirements Document — defines scope, wrong here = wasted build
- Architecture Design — structural decisions are hard to undo
- Semantic Model — measure definitions affect all downstream analysis

**Does not need its own issue:**
- QA checklist, deployment script, chart component — mechanical outputs of the parent task, tracked in the DAG not in Linear

**Components** — reusable building blocks consumed by products:
- Domain Brief
- Requirements Document
- Architecture Design
- UX/UI Design
- Visual component (chart, KPI card)
- Semantic Model
- QA Report

A component can be shared across products. The domain brief for labour market feeds both the dashboard AND the article. But the component is produced once and reused — not rebuilt for each product.

### The Flow (generic — applies to any product)

```
You drop an idea (any product type)
      ↓
Linear issue created (OR-xxx)
      ↓
/kickoff OR-xxx
      ↓
[AI] Identify which components are needed for this product
      ↓
[AI] Check which components already exist (reuse if available)
      ↓
[AI] Build missing components (each follows its own DAG)
      ↓  ← YOU REVIEW key components: requirements, domain brief
[AI] Assemble product from components
      ↓
[AI] Quality review
      ↓
Published
```

### Example: Labour Market Dashboard

```
Dashboard (product DAG)
  ├── Domain Brief (component) ← produced once, reused by article too
  ├── Requirements Doc (component)
  ├── Architecture Design (component)
  ├── Semantic Model (component)
  ├── Visual Components (component) ← charts, KPI cards
  └── QA Report (component)
```

### Example: Labour Market Article

```
Article (product DAG)
  ├── Domain Brief (component) ← REUSED from dashboard if exists
  ├── Research findings (component)
  ├── Charts/visuals (component) ← REUSED from dashboard if exists
  └── Editorial review (component)
```

### Workstations / Agents

Your instinct to define workstations was correct. Each workstation = an agent with a specialized role.

| Workstation | Agent | What it does |
|------------|-------|-------------|
| Business Domain | `business-analyst` | Research domain, define KPIs, write brief |
| Architecture | `data-engineer` (architect mode) | Design data model, layer contracts |
| Data Engineering | `data-engineer` | Build ingestion, dbt models |
| UX/UI + Dashboard | `dashboard-dev` | Build visual product using template |
| Quality Assurance | evaluator agents | Review output at each stage |
| Content Creation | `content-writer` | Write articles from briefs |
| Research | `researcher` | Academic analysis |

You don't need one agent per domain. One `business-analyst` + a domain brief = domain specialisation. The brief IS the domain knowledge.

### Component DAGs

A dashboard is assembled from components. Each component has its own production process:

| Component | Who builds it | Output |
|-----------|--------------|--------|
| Domain Brief (P09) | business-analyst | `team/domain-briefs/{domain}.md` |
| Requirements (P14) | business-analyst | Requirements doc |
| Architecture (P00) | data-engineer | Schema design |
| Semantic Model (P07) | data-engineer | dbt MetricFlow measures |
| Visual Design (P12) | dashboard-dev | Layout + chart specs |
| Dashboard Code (P15/P16) | dashboard-dev | Working Dash app |
| QA Report (P19) | evaluators | Review findings |

The pilot_template checklists you started (P00.1, P07.1, P12.1, P14.1, P15.1, P16.x, P19.1) are exactly this — each P-number is a component, each checklist is its production process. **This was the right idea.**

### The Template's Role

The dashboard template is the reusable mould. Every domain dashboard follows the same structure — different content, same pattern. Once the template is right:
- Layout is solved
- Chart types are established
- Data connection pattern is defined
- The template defines what inputs the data pipeline must produce

**The template comes first. Then domain work.**

---

## Current Repo Situation

### Branch: `feat/OR-143-chart-fixes`

Three things are mixed together on this branch:

| What | Status |
|------|--------|
| OR-143 chart fixes (5 files) | Done, needs PR — stuck |
| Agent restructuring (23 deleted, 70+ new) | Incomplete, skills broken |
| Factory/DAG system | Created, not wired |

### What's broken right now
- Skills (`/review`, `/plan`, `/feasibility`) call agents by old names that no longer exist on disk
- Playbooks deleted — no process documentation accessible
- OR-143 legitimate work can't be merged

### What's good
- `team/factory/` DAG system — well structured, useful
- `biz-specialists/` domain agents — good idea, keep
- `team/knowledge-base/` — complete (10 modules)
- `team/standards/` — complete
- `products/dashboards/pilot_template/` — good foundation

---

## The Plan

### Phase 1 — Cleanup (do now)

**Step 1: Rescue OR-143**
Extract the 5 chart fix files to a clean branch, open PR, merge.

**Step 2: Restore working system**
Restore from git history: 23 original agents + 9 playbooks.
Skills will work again.

**Step 3: Keep the best of opencode work**
- Keep: `team/factory/` DAGs, `biz-specialists/` agents, `dashboard-assembly.md` standard, `pilot_template/`
- Discard: `factory-execution.md`, `workstation-template.md`, the 70+ generic dept-task agents

**Step 4: Update AGENTS.md**
Add the core AI operating principle prominently.

### Phase 2 — Finish the Template (next sprint)

Complete OR-143 template work. The template needs to be the validated, production-ready mould before domain work starts.

Validate the component DAG approach against the template build — observe what steps were actually needed, then formalize.

### Phase 3 — First Domain (after template)

Pick one domain (Labour Market is natural — data already in warehouse, dashboard exists).
Run the full pipeline: domain brief → requirements → data → dashboard → article → social.

This validates the Jarvis model end-to-end and produces the first reusable domain brief as a template for all future domains.

### Phase 4 — Remaining Domains

Each domain follows the same pattern. The factory is now real — built from observed patterns, not assumptions.

---

## Token Efficiency Rules (for reference)

Already encoded in `AGENTS.md`. Summary:
- One session per task
- Read only what's needed
- Prefer grep/glob over full file reads
- Use OpenCode + Gemini Flash for exploration, Claude for precision work
- `/clear` after heavy tool use mid-session
