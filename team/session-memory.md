# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-04-07 -->

## Current Focus
Full gap-closure pass complete: all 18 audit items addressed. 14 agents, 8 evaluation standards, derivation chain intact on all standards.

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
- `team/PLATFORM.md` — factory blueprint (source of truth for competency map, agent roster, quality system)
- `team/knowledge-base/` — research syntheses (was: team/analytics/)
- `team/standards/build/` — developer-facing build rules (all have "Derived from" headers)
- `team/standards/evaluation/` — agent-facing evaluation rules (8 standards)
- `team/domain-briefs/` — domain research outputs (was: docs/domain-briefs/)

## Recently Completed (2026-04-07)
- Gap-closure pass part 2 (PR #51):
  - NEW agent: brief-reviewer (plan-phase evaluator for business-analyst briefs — closes dual-control loop)
  - NEW evaluation standard: brief-review.md (KB-traced to business-analysis + analytical-methods)
  - Build-standard "Derived from" headers added to all 5 build standards (ingestion, processing, storage, visualisation, measures)
  - /plan skill: Agent A/B descriptions updated to correct file paths + KB refs
  - data-architect: DDL section expanded — PostgreSQL catalogue.* store + bus_matrix.md maintenance
  - /domain-brief skill: Step 6.5 gate added (brief-reviewer runs before presenting to PO)
  - PLATFORM.md §5.1 updated to 14 agents, §5.3 invocation map adds /domain-brief gate, §8.2 adds brief-review standard, §11.1/§11.2 updated
  - CLAUDE.md: brief-reviewer added to evaluator table + standards table; evaluation/ directory listing updated
  - standards/INDEX.md: brief-review.md row added; stale "header re-trace pending" note removed
  - Linear ideas captured: OR-135 (Content KB), OR-136 (Research Methods KB), OR-137 (Platform/Ops KB)
- PR #50 (merged): dashboard-dev, measures-reviewer, Semantic Modelling competency, 7 eval standards live
- OR-133 (PR #49): Quality system infrastructure — 4 new KB files, 10 agents, 5 evaluation standards
- Platform Blueprint Restructure (PR #48): team/PLATFORM.md, team/analytics/ → team/knowledge-base/, team/standards/ → build/ + evaluation/

## Knowledge Base Status
- Analytical methods: ✅ Complete (team/knowledge-base/analytical-methods/)
- Visualization + charts: ✅ Complete (team/knowledge-base/visualization/)
- UX/Perception: ✅ Complete (team/knowledge-base/ux-perception/perception.md)
- Data Architecture: ✅ Complete (team/knowledge-base/data-architecture/architecture.md)
- Data Engineering: ✅ Complete (team/knowledge-base/data-engineering/engineering.md)
- Business Analysis: ✅ Complete (team/knowledge-base/business-analysis/kpi-indicator-design.md)
- Public Finance domain: ⏳ Draft (team/knowledge-base/domains/public-finance.md)

## Agent Infrastructure (14 live)
- Builders: data-architect (platform/ + semantic layer), dashboard-dev (products/dashboards/ + visuals/), business-analyst (analytical briefs)
- Evaluators: architecture-critic, code-reviewer, data-engineer-reviewer, analytical-validator, brief-reviewer, visualization-reviewer, visual-screenshot-reviewer, measures-reviewer, domain-specialist, cost-estimator
- Diagnostics: debug

## Linear — Active
- OR-78 (Ghost admin), OR-85 (daily cron), OR-90 (Instagram token ~2026-05-20)
- OR-108: Mobile-optimized dashboards (Backlog)
- OR-135: Content/Editorial KB + agents (Backlog — Idea)
- OR-136: Research Methods KB + agents (Backlog — Idea)
- OR-137: Platform/Ops KB + agents (Backlog — Idea)
