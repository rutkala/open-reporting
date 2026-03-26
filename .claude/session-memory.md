# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-03-26 -->

## Current Focus
Full ELT pipeline live for FIN (NBP) + all Eurostat domains. Portal cleaned up with correct URLs.
Next: BDL/SDP ingestion (needs API key confirm), fix BUS sts_inpr_a series_id.

## Last Session Summary (2026-03-26)
Built full pipeline from catalogue → raw → curated, data explorer, and cleaned up portal.

### What was built:
- **NBP ingestion**: `platform/ingestion/to_raw/nbp_exchange_rates.py` — 23,976 rows (USD/EUR/CHF/GBP from 2002)
- **Eurostat ingestion**: `platform/ingestion/to_raw/eurostat_observations.py` — 71,098 rows across 53 datasets
- **Raw tables**: `raw.nbp_exchange_rates`, `raw.eurostat_observations` (DDL in `platform/warehouse/raw/`)
- **dbt seed**: `platform/processing/dbt/seeds/eurostat_series.csv` — 73-row mapping (detail_id → dataset_code + dimension_key)
- **dbt curated**: 20 models — `fin_exchange_rates` + `all_indicators` (unified) + 17 domain `*_indicators` tables
- **Data explorer**: `products/dashboards/explorer/app.py` — pivot UI at /explorer/
- **Portal homepage**: two cards — Labour (/labour/) and Explorer (/explorer/)

### URL scheme (domain-based English):
- `/labour/` → Labour domain Dash dashboard (port 8050)
- `/explorer/` → Data explorer Dash app (port 8051)
- Future: `/mac/`, `/env/`, `/pub/`, etc. as new dashboards are built

### Running processes (must be started manually after reboot):
- `PYTHONPATH=/opt/open-reporting python3 products/dashboards/rynek_pracy/app.py` → port 8050
- `PYTHONPATH=/opt/open-reporting DUCKDB_PATH=/opt/open-reporting/data/warehouse.duckdb python3 products/dashboards/explorer/app.py` → port 8051

### Curated table row counts:
- fin_exchange_rates: 23,976 | all_indicators: 1,906 (unified Eurostat)
- clt: 551 | pop: 196 | trp: 174 | sci: 137 | trd: 120 | env: 122 | lab: 119
- prc: 89 | soc: 82 | mac: 80 | edu: 76 | pub: 60 | crm: 32 | agr: 26 | ene: 25 | hlt: 17
- bus: 0 (sts_inpr_a returns no PL data — needs series_id fix)

### Known issues / TODO:
- BUS `sts_inpr_a`: needs `indic_bt` dimension in series_id; currently 0 rows
- AGR `ef_m_farmleg`: no clean TOTAL key; agricultural_area_used / crop_area_arable not loading
- CLT `overnight_stays_domestic`: no R_DOM data for Poland in tour_occ_nim
- 37 unverified Eurostat series remaining
- Processes not managed by a supervisor — die on reboot; consider systemd units or docker

## Key Technical Facts
- DB (analytical): DuckDB at data/warehouse.duckdb (DUCKDB_PATH env var)
- DB (operational): PostgreSQL localhost:5432 db=reporting user=reporting
- Catalogue loader: `PYTHONPATH=/opt/open-reporting python3 platform/database/loader.py`
- dbt: `cd platform/processing/dbt && DUCKDB_PATH=/opt/open-reporting/data/warehouse.duckdb dbt run --profiles-dir .`
- Eurostat ingestion: `PYTHONPATH=/opt/open-reporting python3 platform/ingestion/to_raw/eurostat_observations.py [--dataset X] [--backfill]`
- dbt schemas in DuckDB: `main_curated` (dbt prepends `main_` to schema names)

## Catalogue State
- `catalogue.domain_details`: 222 indicators across 18 domains
- `catalogue.domain_detail_sources`: 483 mappings — Eurostat: 73 verified, 37 unverified; NBP FX: 4 verified

## Open Items
- Fix BUS: `sts_inpr_a` series_id (try `indic_bt=PROD`)
- BDL ingestion: pending user confirmation on API key
- SDP ingestion: pending user confirmation on data format
- Process supervision: systemd units or docker so dashboards survive reboot
- Install dbt-metricflow, migrate products/semantic/ → dbt metrics/
