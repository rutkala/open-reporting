# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-03-26 -->

## Current Focus
Explorer hierarchy drill + Default aggregation + NUTS2 regional data + Mobile PWA built and deployed.

## Last Session Summary (2026-03-26)
Explorer enhancements, regional geodata, and mobile PWA — all built in one session.

### What was built/changed:

**Explorer — hierarchy drill bar**
- Replaced flat Rows/Columns dropdowns with dimension hierarchy selectors (Period: Year/Quarter/Month; Domain: Group/Domain/Detail)
- Drill bar above chart: `◄ Domain Detail ►` / `◄ Year ►` buttons for Power BI-style drill-down
- `dcc.Store(id="store-drill")` with `auto_run` flag — drill buttons auto-rerun, hierarchy changes require Run button
- `_HIERARCHIES` registry: each dim has ordered levels with SQL expression + required JOIN

**Explorer — Default aggregation**
- Added `default_agg` column to `dim_domain_detail.csv` seed (AVG for rates/indices/prices, SUM for flows/counts)
- "Default (per indicator)" option in Aggregation dropdown — `_resolve_agg()` looks up `default_agg` at query time
- Mixed selections fall back to AVG

**Regional geodata (NUTS2)**
- `dim_geo.csv` expanded: PL country + 7 NUTS1 macroregions + 17 NUTS2 voivodeships (25 rows total)
- `PL_NUTS2` sentinel in `eurostat_observations.py` — fetches without geo filter, post-filters to PL* rows
- `stg_eurostat.sql` — removed `where geo = 'PL'` blocking filter so regional rows flow through
- Two domains re-configured for NUTS2: `mac.gdp_per_capita_regional`, `pop.population_regional`

**Mobile PWA (`products/mobile/`)**
- FastAPI + Jinja2 + Chart.js app at port 8052, nginx proxy at `/app/`
- Routes: home (KPI cards), domains list, domain indicators, indicator detail
- PWA: manifest.json + service worker — installs as standalone Android app via "Add to Home Screen"
- Polish content: KPI labels, domain names, navigation
- Systemd service: `or-mobile.service`
- User confirmed: "It works as normal android app"

### DuckDB schema layout (current):
- `raw` — raw ingested tables (eurostat_observations, nbp_exchange_rates)
- `curated` — 22 dbt models + 6 seeds:
  - Facts: `all_indicators`, 19 domain `*_indicators` (incl. `fin_indicators`)
  - Staging: `stg_eurostat`, `stg_nbp`
  - Dimensions: `dim_calendar`, `dim_domain_detail` (with default_agg), `dim_geo` (NUTS1+NUTS2), `dim_source`, `dim_primary_source`
- `main` — internal seeds: `eurostat_series`, `nbp_series`

### Important: DuckDB concurrency
- Only one process can hold a write lock at a time
- Stop dashboards + Harlequin before running `dbt run`: `sudo systemctl stop or-explorer or-labour`
- Dashboards connect read-only so they can coexist, but Harlequin takes an exclusive lock

### Pipeline (live):
- NBP: 23,976 rows | Eurostat: 71,098 rows + 625 GDP regional + 2,364 population regional
- dbt: 22 curated models + 6 seeds, all passing
- Dashboards: `/labour/` (port 8050), `/explorer/` (port 8051), `/app/` (port 8052) — all systemd-managed

## Key Technical Facts
- DB (analytical): DuckDB at data/warehouse.duckdb (DUCKDB_PATH env var)
- DB (operational): PostgreSQL localhost:5432 db=reporting user=reporting
- dbt: `cd platform/processing/dbt && DUCKDB_PATH=/opt/open-reporting/data/warehouse.duckdb dbt run --profiles-dir .`
- dbt seed: add `--select <seed_name>` to seed only one file; schema change requires `--full-refresh`
- Harlequin: `harlequin /opt/open-reporting/data/warehouse.duckdb` (run in tmux new-window)
- dbt schemas: `curated` (custom macro overrides default `main_curated` naming)

## Catalogue State
- `catalogue.domain_details`: 222 indicators across 18 domains
- `catalogue.domain_detail_sources`: 483 mappings — Eurostat: 73 verified (2 NUTS2); NBP FX: 4 verified
- `dim_primary_source`: 77 verified mappings — used as Explorer default
- NUTS2 domains: `mac.gdp_per_capita_regional`, `pop.population_regional`

## Open Items
- Domain dashboards: next phase — LAB, MAC, ENV first; standard template (KPI cards, time series, cross-indicator bar)
- Fix BUS: `sts_inpr_a` series_id (try `indic_bt=PROD`)
- BDL ingestion: pending user confirmation on API key
- SDP ingestion: pending user confirmation on data format
- Install dbt-metricflow, migrate products/semantic/ → dbt metrics/
- `eurostat_series` + `nbp_series` seeds still in `main` schema (internal mapping seeds — low priority to move)
- Mobile PWA: add more KPI cards, expand DOMAIN_NAMES_PL dict, add charts to indicator detail page
