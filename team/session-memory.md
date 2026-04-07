# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-04-07 -->

## Current Focus
Infrastructure build-out complete. All KB + agent pairs done. Backlog now shifts to product work.

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
- `team/knowledge-base/` — 10 KB modules (all complete except public-finance domain ⏳ draft)
- `team/standards/build/` — 6 build standards (all with "Derived from" headers)
- `team/standards/evaluation/` — 12 eval standards (all wired to agents)
- `team/playbooks/` — 9 playbooks covering all sub-products

## Recently Completed (2026-04-07)
- OR-138 (PR #53, merged by Claude): Rename data-architect → data-engineer across all 17 references
- OR-135–137, 139–141 (merged by opencode):
  - Content/Editorial KB + content-writer + content-reviewer + content-review.md
  - Research Methods KB + researcher + research-reviewer + research-review.md
  - Platform/Ops KB + ops-engineer + ops-reviewer + ops-review.md
  - Data Research KB + data-researcher + data-research-reviewer + data-research-review.md
  - data-architect builder agent (Design-phase, Data Architecture competency)
  - article.md + research.md playbooks (sub-products #17, #18)
- Index gap fix (direct commit): data-research KB and eval standard added to INDEX files

## Knowledge Base Status (10 modules)
- Analytical methods: ✅ Complete
- Visualization + charts: ✅ Complete
- UX/Perception: ✅ Complete
- Data Architecture: ✅ Complete
- Data Engineering: ✅ Complete
- Business Analysis: ✅ Complete
- Data Research: ✅ Complete (OR-139)
- Content/Editorial: ✅ Complete (OR-135)
- Research Methods: ✅ Complete (OR-136)
- Platform/Ops: ✅ Complete (OR-137)
- Public Finance domain: ⏳ Draft (OR-120)

## Agent Infrastructure (23 live)
Builders: data-engineer, data-architect, data-researcher, dashboard-dev, business-analyst, content-writer, researcher, ops-engineer
Evaluators: architecture-critic, code-reviewer, data-engineer-reviewer, data-research-reviewer, analytical-validator, brief-reviewer, visualization-reviewer, visual-screenshot-reviewer, measures-reviewer, domain-specialist, cost-estimator, content-reviewer, research-reviewer, ops-reviewer
Diagnostics: debug

## Linear — Active
- OR-78 (Ghost admin), OR-85 (daily cron), OR-90 (Instagram token ~2026-05-20)
- OR-108: Mobile-optimized dashboards (Backlog)
- OR-120: Public Finance domain KB — review & promote (Backlog)
- OR-129: Domain Specialist agents one-per-domain (Backlog — Infra)
- Product backlog: OR-74 to OR-113 (dashboards, data pipeline, content, social)
