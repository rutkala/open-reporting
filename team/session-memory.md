# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-04-07 -->

## Current Focus
Quality system infrastructure complete. All 6 core KBs built. Full derivation chain: sources → KB → standards → agents.

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
- OR-133 (PR #49): Quality system infrastructure
  - 4 new KB files: ux-perception/perception.md, data-architecture/architecture.md, data-engineering/engineering.md, business-analysis/kpi-indicator-design.md
  - 10 agents live: debug, architecture-critic, code-reviewer, visualization-reviewer, visual-screenshot-reviewer, visual-design-reviewer, analytical-validator, domain-specialist, business-analyst, cost-estimator
  - 13 skills live (including /feasibility + /standards-review)
  - 5 evaluation standards extracted to standalone files with full KB traceability
  - /review autonomous loop: auto-commit/push/PR when all agents PASS
  - /feasibility skill wired into /review-ideas, /sprint, /kickoff
- Platform Blueprint Restructure (PR #48): team/PLATFORM.md, team/analytics/ → team/knowledge-base/, team/standards/ → build/ + evaluation/ subdirs

## Knowledge Base Status
- Analytical methods: ✅ Complete (team/knowledge-base/analytical-methods/)
- Visualization + charts: ✅ Complete (team/knowledge-base/visualization/)
- UX/Perception: ✅ Complete (team/knowledge-base/ux-perception/perception.md)
- Data Architecture: ✅ Complete (team/knowledge-base/data-architecture/architecture.md)
- Data Engineering: ✅ Complete (team/knowledge-base/data-engineering/engineering.md)
- Business Analysis: ✅ Complete (team/knowledge-base/business-analysis/kpi-indicator-design.md)
- Public Finance domain: ⏳ Draft (team/knowledge-base/domains/public-finance.md)

## Agent Infrastructure (live)
- debug, architecture-critic, code-reviewer, visualization-reviewer, visual-screenshot-reviewer
- visual-design-reviewer, analytical-validator, domain-specialist, business-analyst, cost-estimator

## Linear — Active
- OR-78 (Ghost admin), OR-85 (daily cron), OR-90 (Instagram token ~2026-05-20)
- OR-108: Mobile-optimized dashboards (Backlog)
