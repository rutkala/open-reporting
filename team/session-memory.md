# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-04-07 -->

## Current Focus
Evaluation framework complete. 5 review agents live + screenshot reviewer. Analytics KB foundation in place.

## MVP Status: COMPLETE (v0.1.0 — 2026-03-28)

## Products Live
- `portal.open-reporting.dev` — Labour (8050) + Explorer (8051) + Mobile (8052) + Finance (8053)
- Instagram: @otwarteraporty (token expires ~2026-05-20 — OR-90)

## Key Technical Facts
- DuckDB: data/warehouse.duckdb
- PostgreSQL: localhost:5432 db=reporting
- sudo NOPASSWD: systemctl or-* + cp infra/systemd/*.service
- .claude/ writes: auto-approved via approve-claude-dir.js hook

## Recently Completed (2026-04-06/07)
- OR-124: Measure-driven value formatting across all chart components (format_type, scale, decimals, kpi_value, y_measure)
- OR-125: kpi_row() flex container for multi-card KPI rows
- OR-126: Template dashboard — y_measure and measure.to_series() wired to all chart calls; Polish palette labels fixed
- OR-127: Code Reviewer agent (team/standards/code-review.md + .claude/agents/code-reviewer.md + /review Part 0)
- OR-128: Visualization Reviewer agent (team/standards/visualization-review.md + .claude/agents/visualization-reviewer.md + /review Part 0 parallel)
- OR-130: Architecture Critic agent (.claude/agents/architecture-critic.md + /plan Step 3.5)
- OR-119: Analytical Thinking Framework (team/analytics/analytical-thinking.md)
- OR-131: Analytical Validator agent ✓ DONE (.claude/agents/analytical-validator.md + /plan Step 3.5 parallel + /review Part 0 three agents)
- OR-132: Screenshot visual reviewer ✓ DONE (tools/screenshot.py + Playwright + .claude/agents/visual-screenshot-reviewer.md + /review Part 0.5)

## Evaluation Framework — Backlog
- OR-127: Code Reviewer ✓ DONE
- OR-128: Visualization Reviewer ✓ DONE
- OR-129: Domain Specialist agents (one per domain) — SKIPPED for now
- OR-130: Architecture Critic agent ✓ DONE
- OR-131: Analytical Validator agent ✓ DONE

## Linear — Active
- OR-78 (Ghost admin), OR-85 (daily cron), OR-90 (Instagram token ~2026-05-20)
- OR-108: Mobile-optimized dashboards (Backlog)
