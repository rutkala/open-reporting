# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-03-28 -->

## Current Focus
Post-MVP setup complete. Process, skills, and Linear backlog all in place. Ready for first sprint.

## MVP Status: COMPLETE (v0.1.0 — 2026-03-28)
See `docs/MVP.md` and `docs/RELEASE_NOTES.md`.

## Workflow — 4 stages
1. `/capture-idea` — idea from chat → Backlog (Idea label)
2. `/review-ideas` — convert ideas to proper issues → Backlog
3. `/sprint` — pick issues from Backlog → Todo
4. `/kickoff` — plan → implement → PR → Done

See `CLAUDE.md` for full process, labels, and chat contract.

## Products Live
- `open-reporting.dev` — Ghost blog "Otwarte Raporty"
- `portal.open-reporting.dev` — Labour dashboard (port 8050) + Explorer (port 8051)
- `portal.open-reporting.dev/app/` — Mobile PWA (port 8052)
- Instagram: @otwarteraporty (token expires ~2026-05-20 — OR-90)

## Key Technical Facts
- DB (analytical): DuckDB at data/warehouse.duckdb (DUCKDB_PATH env var)
- DB (operational): PostgreSQL localhost:5432 db=reporting user=reporting
- dbt: `cd platform/processing/dbt && DUCKDB_PATH=/opt/open-reporting/data/warehouse.duckdb dbt run --profiles-dir .`
- dbt seed schema change: requires `--full-refresh`
- DuckDB concurrency: stop dashboards before dbt run — `sudo systemctl stop or-explorer or-labour`
- Instagram API: two-step publish (create container → wait 10s → publish); unique filename per post
- kaleido installed for Plotly PNG export

## Catalogue State
- `catalogue.domain_details`: 222 indicators across 18 domains
- `catalogue.domain_detail_sources`: 483 mappings — Eurostat: 73 verified (2 NUTS2); NBP FX: 4 verified
- NUTS2 domains: `mac.gdp_per_capita_regional`, `pop.population_regional`

## Linear — Phase 1 Backlog
Epics: OR-74 (Blog), OR-75 (Dashboards), OR-76 (Data), OR-77 (Social)
Sub-issues: OR-78 to OR-90 — all in Backlog, awaiting first `/sprint`
Urgent: OR-78 (Ghost admin), OR-85 (daily cron), OR-90 (Instagram token due 2026-05-20)
