# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-03-25 -->

## Current Focus
Catalogue fully populated. Next: verify series_ids source by source, then write first ingestion pipeline.

## Last Session Summary (2026-03-25)
Catalogue data layer completed: domain_details, bus matrix, domain_detail_sources, ingestion standard updated.

### domain_details populated:
- 222 indicators across all 18 domains (FIN/PUB/MAC/PRC/LAB/BUS/TRD/AGR/TRP/ENE/POP/HLT/EDU/SOC/CRM/CLT/ENV/SCI)
- Fields: detail_id, domain_id, name, unit, frequency, detail_type, entity_level, description, notes
- `platform/database/data/domain_details.csv`

### Bus matrix fully populated:
- All 18 domain sections filled with dimension mappings (D1–D7)
- `platform/warehouse/bus_matrix.md`

### domain_detail_sources populated:
- 483 source mappings (avg ~2-3 sources per indicator)
- Top sources: eurostat (110), bdl (59), sdp (45), nbp (19), are (12)
- All rows: `verified=false`, `series_id=null` — none confirmed against live sources yet
- `platform/database/data/domain_detail_sources.csv`

### Schema: domain_detail_sources extended:
- Added `series_id VARCHAR(300)` — exact locator within source system (endpoint, dataset code, variable ID)
- Added `verified BOOLEAN DEFAULT FALSE` — ingestion pipelines must only trust verified=true rows
- Idempotent ALTER TABLE migrations in `platform/database/catalogue/04_domain_detail_sources.sql`
- series_id format convention: REST = `endpoint?param=val`, SDMX = `dataset?filter`, BDL = `variables/{id}`, XLSX = `file::sheet::column`

### Ingestion standard updated:
- Phase 0 added: catalogue verification gate (REQUIRED before any ingestion code)
- series_id format table per source type (REST, SDMX/Eurostat, BDL, XLSX, HTML)
- Script docstring template now includes Catalogue block (detail_id / source_id / series_id)
- Phase 6 validation: catalogue check as first item
- Architecture diagram: catalogue as entry point, output corrected to `curated.*`
- `.claude/standards/ingestion.md`

## Key Technical Facts
- DB (analytical): DuckDB at data/warehouse.duckdb (DUCKDB_PATH env var) — currently empty
- DB (operational): PostgreSQL localhost:5432 db=reporting user=reporting
- Catalogue loader: `PYTHONPATH=/opt/open-reporting python3 platform/database/loader.py`
- dbt: `cd platform/processing/dbt && dbt run --profiles-dir .`
- PYTHONPATH=/opt/open-reporting required for all python3 commands

## Catalogue State
- `catalogue.sources`: 87 sources (34 tier-1 / 46 tier-2 / 7 tier-3)
- `catalogue.domains`: 18 domains across Economy / Society / Environment groups
- `catalogue.domain_details`: 222 indicators
- `catalogue.domain_detail_sources`: 483 mappings — all unverified (series_id=null, verified=false)

## Verification Work Remaining
Before any ingestion pipeline can be written, series_ids must be confirmed per source.
Natural order: tier-1 API sources first (nbp, eurostat/sdmx, bdl, sdp, pse, gios, gaz_system).
Each verification: open source docs → find exact series → test → set series_id + verified=true in CSV → reload catalogue.

## Open Items
- Verify series_ids: start with nbp (exchange rates, reference rate) — well-documented REST API
- Verify series_ids: eurostat SDMX — dataset codes for MAC/LAB/PRC indicators
- Verify series_ids: bdl API — variable IDs for regional indicators
- Write first ingestion pipeline (candidate: fin.exchange_rate_* via NBP — simplest tier-1 REST API)
- Install dbt-metricflow, migrate products/semantic/ → dbt metrics/
- Create products/visuals/lib/metrics.py (MetricFlow query wrapper)
- Write first dbt model
- Fix infra: gitignore certs, fix certbot volume paths in docker-compose
