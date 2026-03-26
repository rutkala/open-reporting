# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-03-26 -->

## Current Focus
Explorer dashboard improved — pivot with domain/indicator filters, correct chart axes.
Next: continue explorer UX improvements, then domain dashboards (LAB, MAC, ENV first).

## Last Session Summary (2026-03-26)
Improved data explorer and laid groundwork for domain dashboard phase.

### What was built:
- **Explorer v2** (`products/dashboards/explorer/app.py`):
  - Filter panel: Domain (multi-select) → Indicator (multi-select, updates on domain change) → Period from/to
  - Pivot controls: Rows / Columns / Values / Aggregation — explicit, user-controlled
  - Smart defaults for indicator tables: rows=detail_id, columns=period, values=value, agg=SUM
  - Chart axes corrected: X=column dim values, Y=measure, series=row dim breakdown
  - Sidebar organised into sections: Data source / Filters / Pivot
  - Metadata columns (geo, obs_status, dataset_code, fetched_at, updated_at) excluded from dim options

### Pipeline (from previous session, still live):
- **NBP ingestion**: `platform/ingestion/to_raw/nbp_exchange_rates.py` — 23,976 rows
- **Eurostat ingestion**: `platform/ingestion/to_raw/eurostat_observations.py` — 71,098 rows
- **dbt curated**: 20 models — `fin_exchange_rates` + `all_indicators` + 17 domain `*_indicators`
- **Portal homepage**: two cards — Labour (/labour/) and Explorer (/explorer/)

### URL scheme (domain-based English):
- `/labour/` → Labour domain Dash dashboard (port 8050)
- `/explorer/` → Data explorer Dash app (port 8051)
- Future: `/mac/`, `/env/`, `/pub/`, etc. as new dashboards are built

### Process management (systemd):
- `or-labour.service` → port 8050 | `or-explorer.service` → port 8051
- Unit files: `infra/systemd/` (deployed to `/etc/systemd/system/`)
- Commands: `systemctl status or-explorer`, `journalctl -u or-explorer -f`

### Curated table row counts:
- fin_exchange_rates: 23,976 | all_indicators: 1,906 (unified Eurostat)
- clt: 551 | pop: 196 | trp: 174 | sci: 137 | trd: 120 | env: 122 | lab: 119
- prc: 89 | soc: 82 | mac: 80 | edu: 76 | pub: 60 | crm: 32 | agr: 26 | ene: 25 | hlt: 17
- bus: 0 (sts_inpr_a returns no PL data — needs series_id fix)

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
- Explorer UX: still needs work (user confirmed path is right, more iterations needed)
- Domain dashboards: next phase — LAB, MAC, ENV first; standard template (KPI cards, time series, cross-indicator bar)
- Fix BUS: `sts_inpr_a` series_id (try `indic_bt=PROD`)
- BDL ingestion: pending user confirmation on API key
- SDP ingestion: pending user confirmation on data format
- Install dbt-metricflow, migrate products/semantic/ → dbt metrics/
