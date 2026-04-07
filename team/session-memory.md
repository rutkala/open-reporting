# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-04-07 -->

## Current Focus
Sub-product recipe system complete: 18 sub-products across 6 groups, each with formal task→skill→competency→agent→standard recipe tables. PLATFORM.md is now the routing index for all ORs.

## MVP Status: COMPLETE (v0.1.0 — 2026-03-28)

## Products Live
- `portal.open-reporting.dev` — Labour (8050) + Explorer (8051) + Mobile (8052) + Finance (8053)
- Instagram: @otwarteraporty (token expires ~2026-05-20 — OR-90)

## Key Technical Facts
- DuckDB: data/warehouse.duckdb
- PostgreSQL: localhost:5432 db=reporting
- sudo NOPASSWD: systemctl or-* + cp infra/systemd/*.service
- .claude/ writes: auto-approved via approve-claude-dir.js hook

## Directory Structure (current)
- `team/PLATFORM.md` — factory blueprint (source of truth: sub-product recipes, competency map, agent roster, quality system)
- `team/knowledge-base/` — research syntheses
- `team/standards/build/` — developer-facing build rules (all have "Derived from" headers)
- `team/standards/evaluation/` — agent-facing evaluation rules (8 standards)
- `team/playbooks/` — step-by-step process guides with recipe tables at top

## Recently Completed (2026-04-07)
- Sub-product recipe system (PR #52):
  - PLATFORM.md §1.2 expanded to 18 sub-products across 6 groups (Data Platform, Portal, Blog, Mobile, Social Media, Infra, Content)
  - PLATFORM.md §3 rewritten: Task Taxonomy → Sub-product Recipes (18 recipe tables: task→skill→competency→builder→evaluator→standards)
  - PLATFORM.md §4.1 Competency Map updated: 14 competencies with builder+evaluator columns and sub-products served
  - PLATFORM.md §5.1 corrected: data-architect footnoted as misnamed (should be data-engineer); OR-138 created
  - PLATFORM.md §5.2 updated: 3 new gaps flagged (data-researcher, data-research-reviewer, data-architect builder)
  - PLATFORM.md §5.3 invocation map: recipe-based routing documented
  - PLATFORM.md §11 updated to reflect current state
  - Recipe tables added to dashboard.md and social.md playbooks
  - NEW playbooks: data-ingestion.md, data-mart.md, portal.md, blog.md, infra.md
  - Linear issues: OR-138 (rename data-architect→data-engineer), OR-139 (data-researcher agents), OR-140 (data-architect builder agent)
- PR #51 (merged): brief-reviewer agent, build-standard headers, doc wiring (14 agents, 8 eval standards)
- PR #50 (merged): dashboard-dev, measures-reviewer, Semantic Modelling competency

## Knowledge Base Status
- Analytical methods: ✅ Complete
- Visualization + charts: ✅ Complete
- UX/Perception: ✅ Complete
- Data Architecture: ✅ Complete
- Data Engineering: ✅ Complete
- Business Analysis: ✅ Complete
- Public Finance domain: ⏳ Draft

## Agent Infrastructure (14 live)
- Builders: data-architect¹ (platform/ + semantic layer), dashboard-dev (products/dashboards/ + visuals/), business-analyst (analytical briefs)
- Evaluators: architecture-critic, code-reviewer, data-engineer-reviewer, analytical-validator, brief-reviewer, visualization-reviewer, visual-screenshot-reviewer, measures-reviewer, domain-specialist, cost-estimator
- Diagnostics: debug

¹ Correctly named `data-engineer` per recipe system — rename pending OR-138.

## Linear — Active
- OR-78 (Ghost admin), OR-85 (daily cron), OR-90 (Instagram token ~2026-05-20)
- OR-108: Mobile-optimized dashboards (Backlog)
- OR-138: Rename data-architect → data-engineer (Backlog)
- OR-139: data-researcher + data-research-reviewer agents (Backlog — Idea)
- OR-140: data-architect builder agent (Backlog — Idea)
- OR-135/136/137: Content/Research/Ops KBs + agents (Backlog — Ideas)
