# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-03-24 -->

## Current Focus
Platform infrastructure complete. Next: first ingestion pipeline or MetricFlow setup.

## Last Session Summary (2026-03-24)
Full platform/ architecture designed and built. Analytical stack installed and configured.

### Platform structure finalised:
```
platform/
├── sources/              → YAML source catalogue
├── ingestion/
│   ├── to_landing/       → plain Python fetch scripts (no tooling)
│   └── to_raw/           → dlt pipelines → DuckDB raw schema
│       ├── .dlt/config.toml
│       ├── pipelines/
│       └── schemas/
├── warehouse/            → schema definitions
│   ├── raw/              → DDL for raw tables
│   ├── curated/          → DDL for curated tables
│   └── deploy/           → SQL scripts applied to warehouse
└── processing/
    └── dbt/              → dbt project (open_reporting) + MetricFlow semantic layer
```

### Analytical stack installed:
- DuckDB 1.5.1 — analytical warehouse at data/warehouse.duckdb (git-ignored)
- dbt-core 1.11.7 + dbt-duckdb 1.10.1 — transformations + MetricFlow semantic layer
- dlt 1.24.0 — ingestion pipelines into DuckDB raw schema
- requirements.txt created at repo root

### Key architectural decisions:
- PostgreSQL retained for Ghost CMS only — no analytical use
- DuckDB is the analytical warehouse (raw + curated schemas via dbt)
- MetricFlow (dbt semantic layer) replaces hand-rolled products/semantic/ — migration pending
- products/semantic/ is DEPRECATED — will be deleted once MetricFlow is in place
- products/visuals/lib/db.py — DuckDB direct queries (filters, lookups)
- products/visuals/lib/metrics.py — MetricFlow queries (KPIs, charts) — TO BE CREATED
- Dash remains the dashboard framework
- Visuals are pure rendering components (take DataFrames, don't query)
- Dashboards call db.py or metrics.py depending on need

### Dashboard data flow:
```
Dash callback → db.py (filters/lookups) → DuckDB direct
             → metrics.py (KPIs/charts) → MetricFlow → DuckDB
             → visual component (render only)
```

## Previous Session Summary (2026-03-24)
Full repo reorganisation + semantic layer + labour dashboard built.
- products/semantic/ — YAML domain models + Python engine (ibis + pandas)
- products/visuals/lib/ — db.py, theme.py
- products/dashboards/rynek_pracy/ — Dash app + static generator

## Key Technical Facts
- DB (analytical): DuckDB at data/warehouse.duckdb (DUCKDB_PATH env var)
- DB (operational): PostgreSQL localhost:5432 — Ghost CMS only
- dbt: cd platform/processing/dbt && dbt run --profiles-dir .
- Dash: portal.open-reporting.dev/dash/ via nginx reverse proxy
- Static HTML: infra/nginx/html/ (nginx root /usr/share/nginx/charts)
- PYTHONPATH=/opt/open-reporting required for all python3 commands

## Open Items
- Install dbt-metricflow, migrate products/semantic/ → dbt metrics/
- Create products/visuals/lib/metrics.py (MetricFlow query wrapper)
- Write first dlt ingestion pipeline (platform/ingestion/to_raw/pipelines/)
- Write first dbt model (platform/processing/dbt/models/)
- Write first warehouse deploy script (platform/warehouse/deploy/)
- Populate products/visuals/labour/ with reusable chart components
- Review and update docs/ folder (ARCHITECTURE.md refs are stale)
