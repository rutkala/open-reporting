# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-03-26 -->

## Current Focus
Star schema + conformed fact table built. Explorer redesigned. Next: domain dashboards (LAB, MAC, ENV first).

## Last Session Summary (2026-03-26)
Full dimensional modelling refactor of the curated layer + Explorer dashboard redesign.

### What was built/changed:

**Period normalisation**
- Added `period_date DATE` to `stg_eurostat` — converts all Eurostat period formats (annual, quarterly, semi-annual, monthly) to first-day-of-period DATE
- Removed `period VARCHAR` from fact table (kept only `period_date`)

**Calendar dimension**
- `curated.dim_calendar` — monthly spine 1995–2029, columns: `date_day`, `year`, `quarter`, `month`, `year_quarter`, `year_month`

**Conformed fact table (`all_indicators`)**
- Now a true UNION ALL of all sources: Eurostat + NBP
- Schema: `source_id, domain_id, detail_id, geo, period_date, value, obs_status, fetched_at, updated_at`
- 25,882 rows: eurostat (1,906) + nbp (23,976)

**NBP integration into catalogue pattern**
- New seed: `nbp_series.csv` — maps currency_code → detail_id/domain_id
- New staging model: `curated.stg_nbp` — conformed schema, source_id='nbp'
- Deleted `fin_exchange_rates.sql` — replaced by `fin_indicators.sql` (domain model, same pattern as all others)

**Common dimension tables (all in `curated` schema)**
- `dim_domain_detail` — 222 indicators: detail_id PK, domain_id, detail_name, detail_unit, detail_frequency, domain_name, domain_group
- `dim_geo` — geographic hierarchy (PL only for now, designed for expansion)
- `dim_source` — source registry (eurostat, nbp)
- `dim_primary_source` — 77 rows: detail_id → primary_source_id (derived from catalogue.domain_detail_sources WHERE verified=TRUE)

**Explorer (`products/dashboards/explorer/app.py`) — full rewrite**
- No table picker — always queries `curated.all_indicators`
- Filter pane: Source → Domain → Domain Detail (cascading) → Geographic Unit → Period (year from/to)
- "Primary source" virtual option pre-selected by default — joins `dim_primary_source` for one clean row per indicator
- Pivot: Rows / Columns / Aggregation / Run (same as before but cleaner)
- Domain Detail dropdown shows human-readable names from `dim_domain_detail`

### DuckDB schema layout (current):
- `raw` — raw ingested tables (eurostat_observations, nbp_exchange_rates)
- `curated` — 22 dbt models + 6 seeds:
  - Facts: `all_indicators`, 19 domain `*_indicators` (incl. `fin_indicators`)
  - Staging: `stg_eurostat`, `stg_nbp`
  - Dimensions: `dim_calendar`, `dim_domain_detail`, `dim_geo`, `dim_source`, `dim_primary_source`
- `main` — internal seeds: `eurostat_series`, `nbp_series`

### dbt seed schema config (dbt_project.yml):
- `dim_domain_detail`, `dim_geo`, `dim_source`, `dim_primary_source` → `curated` schema
- `eurostat_series`, `nbp_series` → `main` (internal mapping seeds)

### Important: DuckDB concurrency
- Only one process can hold a write lock at a time
- Stop dashboards + Harlequin before running `dbt run`: `sudo systemctl stop or-explorer or-labour`
- Dashboards connect read-only so they can coexist, but Harlequin takes an exclusive lock

### Pipeline (live):
- NBP: 23,976 rows | Eurostat: 71,098 rows across 53 datasets
- dbt: 22 curated models + 6 seeds, all passing
- Dashboards: `/labour/` (port 8050), `/explorer/` (port 8051) — both systemd-managed

## Key Technical Facts
- DB (analytical): DuckDB at data/warehouse.duckdb (DUCKDB_PATH env var)
- DB (operational): PostgreSQL localhost:5432 db=reporting user=reporting
- dbt: `cd platform/processing/dbt && DUCKDB_PATH=/opt/open-reporting/data/warehouse.duckdb dbt run --profiles-dir .`
- dbt seed: add `--select <seed_name>` to seed only one file
- Harlequin: `harlequin /opt/open-reporting/data/warehouse.duckdb` (run in tmux new-window)
- dbt schemas: `curated` (custom macro overrides default `main_curated` naming)

## Catalogue State
- `catalogue.domain_details`: 222 indicators across 18 domains
- `catalogue.domain_detail_sources`: 483 mappings — Eurostat: 73 verified; NBP FX: 4 verified; 37 unverified Eurostat; rest unverified
- `dim_primary_source`: 77 verified mappings (73 eurostat + 4 nbp) — used as Explorer default

## Open Items
- Domain dashboards: next phase — LAB, MAC, ENV first; standard template (KPI cards, time series, cross-indicator bar)
- Fix BUS: `sts_inpr_a` series_id (try `indic_bt=PROD`)
- BDL ingestion: pending user confirmation on API key
- SDP ingestion: pending user confirmation on data format
- Install dbt-metricflow, migrate products/semantic/ → dbt metrics/
- `eurostat_series` + `nbp_series` seeds still in `main` schema (internal mapping seeds — low priority to move)
