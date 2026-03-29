# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-03-29 -->

## Current Focus
OR-95 PR open (rutkala/open-reporting#24) — DBW HVD explorer tab. Awaiting merge.

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
- bypassPermissions: set via `permissions.defaultMode` (not `defaultPermissionMode`) in settings.json — no CLI flag needed, works as root

## DBW HVD Data (OR-93 Done, OR-95 PR #24 open)
- Source: dbw.stat.gov.pl/pl/katalog/bulk — 213 CSV ZIPs, 18 HVD categories (EU regulation 2023/138)
- Ingestion: `platform/ingestion/to_landing/dbw_hvd.py` → `platform/ingestion/to_raw/dbw_observations.py`
- Landing zone: `data/landing/dbw_hvd/` (426 files — *_data.csv + *_dict.csv per dataset)
- Raw tables: `raw.dbw_observations` (756,626 rows), `raw.dbw_positions` (14,390 labels), `raw.dbw_variables` (85 rows)
- Coverage: 85 variables, 82 sections, years 1995–2026
- Reload: stop dashboards → run to_raw script → restart dashboards (~11s DuckDB bulk load)
- Known issue: some variables (e.g. GDP section 16) mix annual + quarterly + index values — KPIs may be misleading without period_id filter

## Catalogue State
- `catalogue.domain_details`: 222 indicators across 18 domains
- `catalogue.domain_detail_sources`: 483 mappings — Eurostat: 73 verified (2 NUTS2); NBP FX: 4 verified
- NUTS2 domains: `mac.gdp_per_capita_regional`, `pop.population_regional`

## Linear — Phase 1 Backlog
Epics: OR-74 (Blog), OR-75 (Dashboards), OR-76 (Data), OR-77 (Social)
Sub-issues: OR-78 to OR-93 — OR-93 Done; OR-78 to OR-92 in Backlog
Urgent: OR-78 (Ghost admin), OR-85 (daily cron), OR-90 (Instagram token due 2026-05-20)
