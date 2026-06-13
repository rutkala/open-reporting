# Ingestion Pipeline — Goal & Roadmap

**Goal (PO, 2026-06-13):** a data-ingestion pipeline for *all possible public data sources*
across all categories. Every source should be ingested, tracked, and either running
concurrently or on a visible limit-aware schedule, with live status (files, categories, quotas).

## The four milestones

### 1. Research the source universe — **DONE**
Complete list of public sources, grouped into four provider types:
- **a — Polish government, combined** → GUS family (BDL, DBW, biuletyn, TERYT, SDG, BDM, BDP, STRATEG, SMUP, TranStat, REGON, SDP)
- **b — Polish government, institutional** → NBP, MF, NFZ, ZUS, MEN, KNF, GDDKiA, URE, GIOŚ, MRiRW, SAOS, KRS, OPI RAD-on
- **c — Polish private** → Stooq, GPW Benchmark *(require PO approval per policy)*
- **d — International, combined** → Eurostat, OECD, World Bank, IMF (WEO+IFS), ECB, ILOSTAT, UN WPP, FAOSTAT, WTO, UNdata

44 sources in `products/ingestion/registry/source_registry.yaml`, mirrored to the admin portal.

> **Progress 2026-06-13:** International extractor built (World Bank, IMF WEO, ECB live —
> category-d coverage 1→4 of 11). The 3 mock extractors (MF/NFZ/ZUS) removed and their fake
> tables dropped. Master tracker (all 44 sources) live on the ingestion-plan page.

### 2. Bulk + incremental per source — **PARTIAL (model done, build mostly open)**
Each source declares an `ingestion_mode`:
- `bulk` — full historical load (raw file download)
- `incremental` — ongoing updates via API
- `bulk+incremental` — both wired
- `api_full` — API serves both (no separate bulk file source)
- `none` — nothing yet

Current: only **NBP** and **Eurostat** have both. 14 bulk-only, 2 api_full, 1 incremental-only, **25 with no mode**.
Target: every viable source has a bulk mode (full history) and, where the source updates, an incremental mode.

### 3. Develop the ingestion product — **PARTIAL**
- **Solid:** `bdl_extractor.py`, `dbw_extractor.py` (rate-limited, resumable, scheduled via `run_gus_bulk.sh`).
- **Bulk downloaders:** `bulk/run_bulk.py` + `universal_bulk_downloader.py` cover most dane.gov.pl + GUS bulk sources.
- **⚠ Mocks (data-integrity risk):** `mf_extractor.py`, `nfz_extractor.py`, `zus_extractor.py` write **fake hardcoded rows** into `raw_mf_budget` / `raw_nfz_health` / `raw_zus_benefits` every night. Must be replaced with real loaders or removed from `run_daily.sh`.
- **Unbuilt:** all 11 international sources; 5 blocked GUS systems (need browser network-inspector to capture real API paths — same method that unblocked DBW).

### 4. One master plan + tracker — **PARTIAL**
- `source-registry.html` — the catalogue (category, mode, endpoints, scope, verification). **Done.**
- `ingestion-plan.html` — capacity + quotas for BDL/DBW, full schedule table. Deep-dives the two big APIs; needs to surface **all 44** as one limit-aware timeline with per-source status (files, last run, next run).
- Landing + DuckDB catalogs — **done.**

## Sequenced backlog (highest value first)

1. ~~**Master schedule view**~~ — **DONE.** `ingestion-plan.html` lists all 44 sources grouped a/b/c/d.
2. **International loaders (category d)** — **4 of 11 DONE** (Eurostat, World Bank, IMF WEO, ECB via `intl_extractor.py`). Remaining 7, with the discovered next-step for each:
   - **OECD** — new SDMX at `sdmx.oecd.org/public/rest/data/{agency},{dataflow},{version}/{key}`; needs the exact dataflow IDs (browse the OECD Data Explorer "developer API" panel per dataset). Header `Accept: application/vnd.sdmx.data+csv`.
   - **ILOSTAT** — bulk via `rplumber.ilo.org/data/indicator/?id={CODE}&ref_area=POL&format=.csv`; the test returned 200/0-bytes → needs a valid indicator id (list at `rplumber.ilo.org/metadata/indicator/`).
   - **UN WPP** — `population.un.org/dataportalapi/api/v1/` works (indicators list 200); data endpoint `/data/indicators/{id}/locations/{loc}/start/{y}/end/{y}` returned empty → confirm Poland loc code + indicator id from `/locations/` and `/indicators/`.
   - **IMF IFS** — SDMX JSON at `dataservices.imf.org/REST/SDMX_JSON.svc/CompactData/IFS/{key}`; same DataMapper pattern may also cover key series.
   - **FAOSTAT** — bulk CSV ZIP per domain at `fenixservices.fao.org/faostat/api/v1/en/data/{domain}?area=173` (Poland=173). Lower priority.
   - **WTO** — needs a free API key (register at api.wto.org) → **PO action**.
   - **UNdata** — deprioritised; prefer agency-specific sources above.
3. ~~**Replace the 3 mock extractors**~~ — **DONE.** Removed from nightly run, fake tables dropped, files `.mock-disabled`. Real incremental loaders for MF/NFZ/ZUS still to build (data is in the `*_bulk/` mirrors).
4. **Incremental modes** for bulk-only Polish sources that update (dane.gov.pl resource diffing).
5. **Unblock the 5 GUS SPA systems** (STRATEG, SMUP, BDM, BDP, TranStat) — fetch the Swagger/OpenAPI JSON the way DBW was unblocked (the apidocs page references a spec JSON; capture it via browser network panel, then the real `/api/...` paths follow).
6. **Category-c approval** — confirm Stooq/GPW with PO or drop (policy requires explicit approval).
7. **Real MF/NFZ/ZUS loaders** — model the heterogeneous dane.gov.pl files in `*_bulk/` into typed raw tables.

## Cron (live)
- `03:30` BDL · `04:00 + 16:00` DBW · `22:00` nightly incremental + dbt + catalog refresh · `:15` hourly catalog refresh.
