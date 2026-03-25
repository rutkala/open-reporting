# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-03-25 -->

## Current Focus
Ready to populate domain_details.csv + bus_matrix.md domain by domain.
Schema, dimensions, and bus matrix blueprint all in place.

## Last Session Summary (2026-03-25)
Three areas covered: source catalogue, research product, warehouse architecture.

### Warehouse architecture built (`e8ed1bd6`):
- `catalogue.domain_details` extended: +`detail_type` (indicator/micro_indicator/sentiment/reference) +`entity_level` (national/regional/local/sectoral/company/individual)
- `platform/warehouse/bus_matrix.md` — Kimball bus matrix blueprint (7 conformed dimensions)
- `platform/warehouse/dimensions/` — DDL stubs for all 7 conformed dimensions:
  - dim_date, dim_geography (TERYT hierarchy), dim_sector (NACE/PKD)
  - dim_company (KRS/GPW/SCD2), dim_demographic, dim_commodity, dim_institution

### Data model design decisions:
- domain_details has 4 types: indicator (aggregate TS) | micro_indicator (entity-level) | sentiment (text-derived) | reference (doc pointer only)
- Text data (articles, laws, rulings) → never stored as full text; store derived scores/counts or reference links only
- Bus matrix maps facts to 7 dimensions: Date, Geography, Sector, Company, Demographic, Commodity, Institution
- domain_details + bus_matrix populated in parallel domain by domain

### Research product created (`595b2cce`):
- `products/research/` — academic research workspace
- Library seeded with 7 entries: Solow, IS-LM, Phillips Curve, Taylor Rule, Consumer Theory, Production Theory, Market Equilibrium
- Next library additions: AS-AD, Okun's Law, Mundell-Fleming, then econometrics (OLS, time series)

### Source catalogue finalised (`caaed777`):
- 87 sources, 18 domains, 34 tier-1 APIs / 46 tier-2 files / 7 tier-3 reports

## Key Technical Facts
- DB (analytical): DuckDB at data/warehouse.duckdb (DUCKDB_PATH env var)
- DB (operational): PostgreSQL localhost:5432 db=reporting user=reporting
- Catalogue loader: `PYTHONPATH=/opt/open-reporting python3 platform/database/loader.py`
- dbt: `cd platform/processing/dbt && dbt run --profiles-dir .`
- PYTHONPATH=/opt/open-reporting required for all python3 commands

## Domain → Primary Vertical Sources
- FIN: nbp, gpw, knf, ecb, bis, tge, gpw_benchmark, mf_dlug
- PUB: mf, mf_dlug, kas, bgk | MAC: nbp, bdm, ec_bcs, ameco
- PRC: nbp, ure, tge, uokik | LAB: mrpips, zus, cbop, pracuj_pl
- BUS: regon, gunb, pmi_pl | TRD: un_comtrade, puesc, wto
- AGR: kowr, arimir, mrirw, lasy_panstwowe, iung | TRP: utk, gddkia, ulc, pkp_plk
- ENE: pse, ure, are, tge, entso_e, iea, gaz_system | POP: demografia, un_wpp
- HLT: nfz, gis, nizp_pzh, who, ecdc, csioz | EDU: sio, polon
- SOC: zus, mrpips, pfron | CRM: policja, ms_stat, sw, prokuratura
- CLT: pot, mkidn, msit, bn | ENV: gios, kobize, imgw, eea, copernicus
- SCI: uke, opi_pib, ncn, nask

## Open Items
- Populate domain_details.csv + bus_matrix.md domain by domain (next)
- Populate domain_detail_sources.csv mapping indicators to sources
- Install dbt-metricflow, migrate products/semantic/ → dbt metrics/
- Create products/visuals/lib/metrics.py (MetricFlow query wrapper)
- Write first dlt ingestion pipeline
- Write first dbt model
- Fix infra: gitignore certs, fix certbot volume paths in docker-compose
