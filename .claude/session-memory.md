# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-03-26 -->

## Current Focus
Schema cleanup done, tooling settled. Next: domain dashboards (LAB, MAC, ENV first).

## Last Session Summary (2026-03-26)
Explorer improvements, schema rename, VS Code SQLTools troubleshooting, Harlequin setup.

### What was built/changed:
- **dbt schema rename**: `main_curated` → `curated` via `generate_schema_name` macro
  (`platform/processing/dbt/macros/generate_schema_name.sql`)
- **Explorer updated**: `CURATED_SCHEMA = "curated"` in `products/dashboards/explorer/app.py`
- **Old schema dropped**: `main_curated` removed from warehouse.duckdb
- **`.gitignore` updated**: added `/node_modules/`, `/package.json`, `/package-lock.json`
- **VS Code SQLTools**: installed `evidence.sqltools-duckdb-driver`, removed `randomfractalsinc.duckdb-sql-tools`
  — both fail due to DuckDB version mismatch (extensions bundle 0.x, warehouse is 1.5.1)
- **Harlequin**: installed, used as primary SQL client (run in separate tmux window)
  — shortcut to run query: `F5`; quit: `Ctrl+Q`
- **duckdb-async**: installed at `/root/.local/share/vscode-sqltools/` (not used, SQLTools DuckDB broken)

### DuckDB schema layout (final):
- `raw` — raw ingested tables (eurostat_observations, nbp_exchange_rates)
- `curated` — 20 dbt models (all_indicators, fin_exchange_rates, 17 domain *_indicators, eurostat_series seed in `main`)
- `main` — DuckDB default schema; contains `eurostat_series` seed (dbt seeds ignore custom schema macro)

### Important: DuckDB concurrency
- Only one process can hold a write lock at a time
- Stop dashboards + Harlequin before running `dbt run`: `sudo systemctl stop or-explorer or-labour`
- Dashboards connect read-only so they can coexist, but Harlequin takes an exclusive lock

### Pipeline (live):
- NBP: 23,976 rows | Eurostat: 71,098 rows across 53 datasets
- dbt: 20 curated models, all passing
- Dashboards: `/labour/` (port 8050), `/explorer/` (port 8051) — both systemd-managed

### Curated table row counts:
- fin_exchange_rates: 23,976 | all_indicators: 1,906
- clt: 551 | pop: 196 | trp: 174 | sci: 137 | trd: 120 | env: 122 | lab: 119
- prc: 89 | soc: 82 | mac: 80 | edu: 76 | pub: 60 | crm: 32 | agr: 26 | ene: 25 | hlt: 17
- bus: 0 (needs series_id fix)

## Key Technical Facts
- DB (analytical): DuckDB at data/warehouse.duckdb (DUCKDB_PATH env var)
- DB (operational): PostgreSQL localhost:5432 db=reporting user=reporting
- dbt: `cd platform/processing/dbt && DUCKDB_PATH=/opt/open-reporting/data/warehouse.duckdb dbt run --profiles-dir .`
- Harlequin: `harlequin /opt/open-reporting/data/warehouse.duckdb` (run in tmux new-window)
- dbt schemas: `curated` (custom macro overrides default `main_curated` naming)

## Catalogue State
- `catalogue.domain_details`: 222 indicators across 18 domains
- `catalogue.domain_detail_sources`: 483 mappings — Eurostat: 73 verified, 37 unverified; NBP FX: 4 verified

## Open Items
- Domain dashboards: next phase — LAB, MAC, ENV first; standard template (KPI cards, time series, cross-indicator bar)
- Move `eurostat_series` seed to `curated` schema (minor — seeds ignore `generate_schema_name` macro)
- Fix BUS: `sts_inpr_a` series_id (try `indic_bt=PROD`)
- BDL ingestion: pending user confirmation on API key
- SDP ingestion: pending user confirmation on data format
- Install dbt-metricflow, migrate products/semantic/ → dbt metrics/
