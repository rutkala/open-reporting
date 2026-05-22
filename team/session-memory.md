# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-04-16 -->

## Current Focus
Phase 1 cleanup complete. Repo unblocked. Next: finish pilot_template (Phase 2) then first domain product (Phase 3).

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
- `docs/ARCHITECTURE.md` — authoritative two-plane architecture + AI delegation contract
- `team/knowledge-base/` — 10 KB modules (all complete except public-finance domain ⏳ draft)
- `team/standards/build/` — 6 build standards (all with "Derived from" headers)
- `team/standards/evaluation/` — 12 eval standards (all wired to agents)
- `team/playbooks/` — 9 playbooks covering all sub-products

## Recently Completed (2026-04-16)
- OR-143 Phase 1 cleanup (PR #59 + #60, merged):
  - Extracted 5 chart fix files to clean branch, merged independently
  - Added AGENTS.md (universal token-efficiency rules for Claude Code + OpenCode)
  - Added docs/SITUATION.md (architectural situation + plan)
  - Added team/factory/ DAGs + workstation definitions
  - Added team/standards/build/dashboard-assembly.md
  - Added products/dashboards/pilot_template/ (P00.1–P19.1 checklists + Dash skeleton)
  - Discarded 70+ dept-task-dev/test agents, factory-execution.md, workstation-template.md
  - 23 original agents + 9 playbooks intact

## Previously Completed (2026-04-07)
- OR-138: Rename data-architect → data-engineer across all 17 references
- OR-135–141: KB modules, agents, playbooks, eval standards (all complete)

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
