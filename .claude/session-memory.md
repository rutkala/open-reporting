# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-03-29 -->

## Current Focus
OR-96 epic complete. Next: pick from Urgent backlog (OR-78, OR-85, OR-90) or new ideas.

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
- bypassPermissions: set via `permissions.defaultMode` in settings.json

## DW Architecture (OR-97 + OR-100 Done)
- `curated.all_indicators`: 33-column Kimball wide fact table — 5 core, 24 named semantic dims, 4 metadata
- Named dims: dim_sex, dim_age_group, dim_nace_sector, dim_employment_status, dim_education_level, etc. (24 total)
- Three sources: eurostat (~2,506 rows), nbp (~23,976), dbw (568,133)
- stg_dbw.sql uses dim_id CASE routing — dim_sex is always dim_sex regardless of source slot
- Layer contract: raw → stg_{source}.sql (dbt) → curated.all_indicators → dashboards
- Rule: dashboards query curated.* ONLY — never raw.*
- Decision record: docs/DATA_MODEL.md | Standard: standards/storage.md

## OR-99 — Next
Unify Explorer dashboard on curated layer (blockers OR-97/OR-98 both Done)
- Remove the separate DBW HVD tab (queries raw directly)
- Replace with unified Explorer querying curated.all_indicators
- Filter/split by dim1–dim4 columns for dimension-aware charting
- Source is an attribute (filter), not a tab

## DBW HVD Data
- Landing: `data/landing/dbw_hvd/` (426 files)
- Raw: `raw.dbw_observations` (756,626 rows), `raw.dbw_positions` (14,390), `raw.dbw_variables` (85)
- Curated: 568,133 annual rows via stg_dbw (period_id=282 only — mixed periods excluded)
- Known issue: some variables mix annual/quarterly/index (GDP section 16) — period_id filter handles this

## Catalogue State
- `catalogue.domain_details`: 222 indicators (PostgreSQL — Explorer pivot tab)
- `curated.dim_domain_detail`: 305 rows (DuckDB — unified fact table)
- `curated.all_indicators`: ~594k rows total (eurostat + nbp + dbw)

## Linear — Active Issues
- OR-96 (epic): Done — full DW architecture complete
- OR-97: Done (PR #25), OR-98: Done (subsumed), OR-99: Done (PR #27), OR-100: Done (PR #26)
- OR-91: Deferred (ENG/PL i18n — Phase 2)
- Urgent backlog: OR-78 (Ghost admin), OR-85 (daily cron), OR-90 (Instagram token 2026-05-20)
