# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-03-26 -->

## Current Focus
Full ELT pipeline live for FIN (NBP) + all Eurostat domains. Data explorer live at /explorer/.
Next: BDL/SDP ingestion (needs API key confirm), fix BUS sts_inpr_a series_id.

## Last Session Summary (2026-03-26)
Built full pipeline from catalogue → raw → curated, and a data explorer dashboard.

### What was built:
- **NBP ingestion**: `platform/ingestion/to_raw/nbp_exchange_rates.py` — 23,976 rows (USD/EUR/CHF/GBP from 2002)
- **Eurostat ingestion**: `platform/ingestion/to_raw/eurostat_observations.py` — 71,098 rows across 53 datasets
- **Raw tables**: `raw.nbp_exchange_rates`, `raw.eurostat_observations` (DDL in `platform/warehouse/raw/`)
- **dbt seed**: `platform/processing/dbt/seeds/eurostat_series.csv` — 73-row mapping (detail_id → dataset_code + dimension_key)
- **dbt staging**: `platform/processing/dbt/models/eurostat/stg_eurostat.sql`
- **dbt curated**: 20 models — `fin_exchange_rates` + `all_indicators` (unified) + 17 domain `*_indicators` tables
- **Data explorer**: `products/dashboards/explorer/app.py` — pivot-style UI at portal.open-reporting.dev/explorer/
  - Auto-discovers all curated tables; stg_eurostat hidden; friendly display names; all_indicators first
- **Nginx**: proxy for /explorer/ in `infra/nginx/conf.d/portal.conf`
- **loader.py bug fix**: was silently dropping series_id + verified columns on INSERT (now fixed)

### Curated table row counts:
- fin_exchange_rates: 23,976 | all_indicators: 1,906 (unified Eurostat)
- pop: 196 | trp: 174 | sci: 137 | clt: 551 | env: 122 | lab: 119 | trd: 120
- prc: 89 | soc: 82 | mac: 80 | edu: 76 | pub: 60 | crm: 32 | agr: 26 | ene: 25 | hlt: 17
- bus: 0 (sts_inpr_a returns no PL data — needs series_id fix with indic_bt dimension)

### Known issues / TODO:
- BUS `sts_inpr_a`: needs `indic_bt=PROD` in series_id; currently 0 rows
- AGR `ef_m_farmleg`: no TOTAL key in raw; agricultural_area_used / crop_area_arable not loading
- CLT `overnight_stays_domestic`: no R_DOM data for Poland in tour_occ_nim
- 37 unverified Eurostat series remaining (tran_sf_roadse 404, lfsa_urgaed dim issue, etc.)

## Key Technical Facts
- DB (analytical): DuckDB at data/warehouse.duckdb (DUCKDB_PATH env var)
- DB (operational): PostgreSQL localhost:5432 db=reporting user=reporting
- Catalogue loader: `PYTHONPATH=/opt/open-reporting python3 platform/database/loader.py`
- dbt: `cd platform/processing/dbt && DUCKDB_PATH=/opt/open-reporting/data/warehouse.duckdb dbt run --profiles-dir .`
- Eurostat ingestion: `PYTHONPATH=/opt/open-reporting python3 platform/ingestion/to_raw/eurostat_observations.py [--dataset X] [--backfill]`
- Data explorer: `PYTHONPATH=/opt/open-reporting python3 products/dashboards/explorer/app.py` (port 8051)
- PYTHONPATH=/opt/open-reporting required for all python3 commands
- dbt schemas in DuckDB: `main_curated` (dbt prepends `main_` to schema names)

## Catalogue State
- `catalogue.sources`: 87 sources
- `catalogue.domain_details`: 222 indicators
- `catalogue.domain_detail_sources`: 483 mappings — Eurostat: 73 verified, 37 unverified; NBP FX: 4 verified

## Open Items
- Fix BUS: `sts_inpr_a` series_id needs `indic_bt=PROD` (or find correct indicator for industrial output PL)
- BDL ingestion: pending user confirmation on API key / registration
- SDP ingestion: pending user confirmation on data format
- Install dbt-metricflow, migrate products/semantic/ → dbt metrics/
- Fix infra: gitignore certs, fix certbot volume paths in docker-compose
