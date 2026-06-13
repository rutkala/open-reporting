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

1. **Master schedule view** — extend `ingestion-plan.html` to list all 44 sources: category, mode, cadence, status, last/next run. Delivers milestone 4's "see when each runs."
2. **International bulk loaders (category d, 11 sources)** — mostly easy: Eurostat-style bulk (World Bank ZIP, IMF WEO files, UN WPP) and SDMX APIs (OECD, ECB, IMF IFS, ILOSTAT). Biggest coverage gain.
3. **Replace the 3 mock extractors** with real dane.gov.pl loaders (data already in `*_bulk/` landing).
4. **Incremental modes** for bulk-only Polish sources that update (dane.gov.pl resource diffing).
5. **Unblock the 5 GUS SPA systems** (STRATEG, SMUP, BDM, BDP, TranStat) via browser network capture.
6. **Category-c approval** — confirm Stooq/GPW with PO or drop (policy requires explicit approval).

## Cron (live)
- `03:30` BDL · `04:00 + 16:00` DBW · `22:00` nightly incremental + dbt + catalog refresh · `:15` hourly catalog refresh.
