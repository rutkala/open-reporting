# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-03-25 -->

## Current Focus
Source catalogue complete (87 sources, all 18 domains). Next: populate domain_details.csv with atomic indicators per domain, then domain_detail_sources.csv mappings.

## Last Session Summary (2026-03-25)
Built out the full data source catalogue in PostgreSQL, domain by domain.

### What was done:
- Researched and added 65 new sources to `platform/database/data/sources.csv`
- Ran `platform/database/loader.py` after each batch — 87 sources upserted cleanly
- Reviewed all 18 domains for coverage gaps, filled them systematically
- Committed and pushed to main (commit `caaed777`)

### Final catalogue state:
- **87 sources** total: 34 tier-1 (API), 46 tier-2 (files), 7 tier-3 (reports)
- All 18 domains covered with both vertical (domain-specific) and horizontal (cross-domain) sources

### Domain → primary vertical sources:
- FIN: nbp, gpw, knf, ecb, bis, tge, gpw_benchmark, mf_dlug
- PUB: mf, mf_dlug, kas, bgk
- MAC: nbp, bdm, ec_bcs, ameco
- PRC: nbp, ure, tge, uokik
- LAB: mrpips, zus, cbop, pracuj_pl, linkedin_eg
- BUS: regon, gunb, pmi_pl, ec_bcs
- TRD: un_comtrade, puesc, wto
- AGR: kowr, arimir, mrirw, lasy_panstwowe, iung, faostat
- TRP: utk, gddkia, ulc, pkp_plk, transtat
- ENE: pse, ure, are, tge, entso_e, iea, kobize, gaz_system
- POP: demografia, un_wpp
- HLT: nfz, gis, nizp_pzh, who, ecdc, csioz
- EDU: sio, polon
- SOC: zus, mrpips, pfron
- CRM: policja, ms_stat, sw, prokuratura
- CLT: pot, mkidn, msit, bn
- ENV: gios, kobize, imgw, eea, copernicus, wody_polskie
- SCI: uke, opi_pib, ncn, nask

### Horizontal sources (cover many domains):
- GUS: bdl, dbw, sdp, smup, strateg, sdg, regon, teryt, transtat, bdm, demografia, bdp, dekompozycje
- International: eurostat, oecd, worldbank, ilostat, imf, faostat, wto, un_wpp, ecb, bis

## Previous Session Summary (2026-03-24)
Full platform/ architecture designed and built. Analytical stack installed and configured.

### Platform structure finalised:
```
platform/
├── ingestion/
│   ├── to_landing/     → plain Python fetch scripts
│   └── to_raw/         → dlt pipelines → DuckDB raw schema
├── warehouse/          → DuckDB schema definitions (raw/, curated/, deploy/)
├── database/           → PostgreSQL operational schema
│   ├── catalogue/      → DDL files (01-04)
│   ├── data/           → CSV source-of-truth files
│   └── deploy/
└── processing/
    └── dbt/            → dbt project (open_reporting)
```

### Analytical stack installed:
- DuckDB 1.5.1 — analytical warehouse at data/warehouse.duckdb (git-ignored)
- dbt-core 1.11.7 + dbt-duckdb 1.10.1 — transformations + MetricFlow semantic layer
- dlt 1.24.0 — ingestion pipelines into DuckDB raw schema

### Key architectural decisions:
- PostgreSQL retained for Ghost CMS + operational catalogue — no analytical use
- DuckDB is the analytical warehouse (raw + curated schemas via dbt)
- MetricFlow (dbt semantic layer) replaces hand-rolled products/semantic/ — migration pending
- products/semantic/ is DEPRECATED — will be deleted once MetricFlow is in place

## Key Technical Facts
- DB (analytical): DuckDB at data/warehouse.duckdb (DUCKDB_PATH env var)
- DB (operational): PostgreSQL localhost:5432 db=reporting user=reporting
- Catalogue loader: `PYTHONPATH=/opt/open-reporting python3 platform/database/loader.py`
- dbt: `cd platform/processing/dbt && dbt run --profiles-dir .`
- Dash: portal.open-reporting.dev/dash/ via nginx reverse proxy
- PYTHONPATH=/opt/open-reporting required for all python3 commands

## Open Items
- Populate `domain_details.csv` with atomic indicators per domain
- Populate `domain_detail_sources.csv` mapping indicators to sources
- Install dbt-metricflow, migrate products/semantic/ → dbt metrics/
- Create products/visuals/lib/metrics.py (MetricFlow query wrapper)
- Write first dlt ingestion pipeline (platform/ingestion/to_raw/pipelines/)
- Write first dbt model (platform/processing/dbt/models/)
