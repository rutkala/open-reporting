# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-04-07 -->

## Current Focus
Post-audit gap-closure pass: added Semantic Modelling competency, dashboard-dev + measures-reviewer agents, expanded data-architect to cover semantic layer, fixed all stale doc references and ghost agent rows. 13 agents, 7 evaluation standards live. Full derivation chain intact.

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
- `team/standards/build/` — developer-facing build rules
- `team/standards/evaluation/` — agent-facing evaluation rules
- `team/domain-briefs/` — domain research outputs (was: docs/domain-briefs/)

## Recently Completed (2026-04-07)
- Post-audit gap-closure pass:
  - NEW agent: dashboard-dev (builder for products/dashboards/ + products/visuals/, reads ux-perception + visualization KBs)
  - NEW agent: measures-reviewer (PR-phase semantic-layer reviewer)
  - NEW evaluation standard: measures-review.md (KB-traced to business-analysis + analytical-methods)
  - data-architect scope expanded to include semantic layer (MetricFlow, measures, dimensions, metrics)
  - PLATFORM.md §4.1 added Semantic Modelling competency (12 competencies total)
  - PLATFORM.md §5.1/§5.2/§5.3/§6.2/§8.2/§11.1 reconciled with disk reality (13 agents, 7 evaluation standards)
  - CLAUDE.md ghost agents removed (dashboard-dev/data-engineer no-longer-stale), all KBs and standards listed correctly
  - Four stale "KB not yet built" headers fixed in evaluation standards
  - /kickoff step renumbering fixed
  - /review skill wired with measures-reviewer (Agent F)
- OR-133 (PR #49): Quality system infrastructure — 4 new KB files, 10 agents, 5 evaluation standards extracted
- Platform Blueprint Restructure (PR #48): team/PLATFORM.md, team/analytics/ → team/knowledge-base/, team/standards/ → build/ + evaluation/ subdirs

## Knowledge Base Status
- Analytical methods: ✅ Complete (team/knowledge-base/analytical-methods/)
- Visualization + charts: ✅ Complete (team/knowledge-base/visualization/)
- UX/Perception: ✅ Complete (team/knowledge-base/ux-perception/perception.md)
- Data Architecture: ✅ Complete (team/knowledge-base/data-architecture/architecture.md)
- Data Engineering: ✅ Complete (team/knowledge-base/data-engineering/engineering.md)
- Business Analysis: ✅ Complete (team/knowledge-base/business-analysis/kpi-indicator-design.md)
- Public Finance domain: ⏳ Draft (team/knowledge-base/domains/public-finance.md)

## Agent Infrastructure (13 live)
- Builders: data-architect (platform/ + semantic layer), dashboard-dev (products/dashboards/ + visuals/), business-analyst (analytical briefs)
- Evaluators: architecture-critic, code-reviewer, data-engineer-reviewer, analytical-validator, visualization-reviewer, visual-screenshot-reviewer, measures-reviewer, domain-specialist, cost-estimator
- Diagnostics: debug

## Linear — Active
- OR-78 (Ghost admin), OR-85 (daily cron), OR-90 (Instagram token ~2026-05-20)
- OR-108: Mobile-optimized dashboards (Backlog)
