# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-03-31 — hook test 2 -->

## Current Focus
Finance dashboard complete. Sudo NOPASSWD configured. approve-claude-dir.js hook enables silent writes to .claude/. Ready for next epic.

## MVP Status: COMPLETE (v0.1.0 — 2026-03-28)

## Products Live
- `portal.open-reporting.dev` — Labour (8050) + Explorer (8051) + Mobile (8052) + Finance (8053)
- Instagram: @otwarteraporty (token expires ~2026-05-20 — OR-90)

## Key Technical Facts
- DuckDB: data/warehouse.duckdb
- PostgreSQL: localhost:5432 db=reporting
- sudo NOPASSWD: systemctl or-* + cp infra/systemd/*.service
- .claude/ writes: auto-approved via approve-claude-dir.js hook

## OR-102 Done (2026-03-31)
- curated.mart_finance: 29,914 rows, 50 indicators, 34 geos
- Dashboard: 7 tabs at /finance/

## Linear — Active
- OR-78 (Ghost admin), OR-85 (daily cron), OR-90 (Instagram token ~2026-05-20)
- OR-108: Mobile-optimized dashboards (Backlog)
