# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-05-27 13:00 UTC -->

## Current Focus

AI Lead autonomous week underway. 4h cron cadence. Theme 3 fully live. Theme 2 has 3 articles published + 1 draft (OR-147 COFOG) ready for VPS publish.

## Live production state

- **Public finance:** `portal.open-reporting.dev/public_finance/` — Live ✓
- **Labour market:** `portal.open-reporting.dev/labour_market/` — Live ✓
- **National accounts:** `portal.open-reporting.dev/national_accounts/` — Live ✓ (deployed by PO)
- **Demographics:** `portal.open-reporting.dev/demographics/` — Live ✓ (deployed by PO)
- **Blog:** `www.open-reporting.dev` — Live ✓
  - Article 1 (SGP/Maastricht) — Live ✓
  - Article 2 (Labour market) — Live ✓ (published by PO)
  - Article 3 (Debt service costs) — Live ✓ (published by PO)
  - **Article 4 (COFOG)** — Draft committed `933d23fd` — VPS publish pending
- **Daily ingestion:** cron `0 22 * * *` UTC

## What shipped (recent commits)

| Commit | What | Linear |
|---|---|---|
| `933d23fd` | OR-147 COFOG article draft | OR-147 In Progress |
| `07df7240` | OR-87 sts_inpr_a seed fix (indic_bt=PROD) | OR-87 fix committed |
| `3f7a9e8a` | Absorb PO VPS actions — all Theme 3 live | All Done |
| `42d7f43b` | OR-146 Debt service article draft | OR-146 Done |
| `e65e48f7` | OR-145 Labour market article draft | OR-145 Done |

## VPS queue pending PO action

1. **OR-147 COFOG article publish:**
   ```bash
   cd /opt/open-reporting && git pull
   PYTHONPATH=/opt/open-reporting python3 products/blog/publish_to_ghost.py \
       products/blog/drafts/or-147-cofog.md --status draft
   # Check preview, then --publish
   ```
   Pre-publish: verify in Eurostat databrowser (gov_10a_exp, geo=PL, unit=PC_GDP, year=2023):
   GF10=16,9%? GF07≈5,0%? GF02=3,3%?

2. **OR-87 BUS/MAC industrial output fix activation:**
   ```bash
   PYTHONPATH=/opt/open-reporting python3 products/database/loader.py
   PYTHONPATH=/opt/open-reporting python3 products/ingestion/to_raw/eurostat_observations.py --dataset sts_inpr_a --backfill
   cd products/warehouse
   DUCKDB_PATH=/opt/open-reporting/data/warehouse.duckdb dbt seed --select eurostat_series --profiles-dir .
   DUCKDB_PATH=/opt/open-reporting/data/warehouse.duckdb dbt run --select stg_eurostat mac_indicators fact_macro_overview bus_indicators --profiles-dir .
   ```

## Linear blocked on PO action

| Issue | What |
|---|---|
| OR-90 | Instagram token — Meta Developer portal (blocks all of Theme 4) |
| OR-79 | Ghost nav link — browser admin session |

## What's next (autonomous)

1. **Theme 2 — 5th article:** regional wages / labour market depth OR EU fiscal comparison
2. **ENV domain dashboard (OR-83):** emissions/energy — data already seeded (env.* series); natural next Theme 3-adjacent product
3. **Theme 5 — OR-86 BDL ingestion** — cloud-implementable ingestion code; VPS to run
4. **Theme 4 — blocked** on OR-90

## Architecture (current)

- Port assignments: public_finance=8057, labour_market=8058, national_accounts=8059, demographics=8060
- Next dashboard port: 8061
- All Theme 3 dashboards live on portal

## Note: autonomous runs from cloud containers

- `dbr run`, `dbt run`, Ghost publish (JWT/crypto) NOT available from cloud
- Production health checks return 403 (nginx allowlist) — NOT a service failure
- `data/logs/` directory does NOT exist in cloud containers — ingest log check will always return NOT FOUND (not an error)
- **CRITICAL on startup:** `git checkout main && git pull --ff-only origin main` (container may start on detached HEAD)

## Key Technical Facts

- OR-87 fix: `sts_inpr_a` needs `indic_bt=PROD` in both `eurostat_series.csv` and `domain_detail_sources.csv` — committed `07df7240`; VPS runbook in Linear OR-87
- OR-52 quarterly BOP series averaged to annual (AVG in fact_macro_overview)
- natural_increase_per1000 derived in fact_demo_overview (births − deaths, can go negative)
- Demographics seed dimension_keys verified correct (pop.births, pop.deaths, pop.population_total, pop.life_expectancy_f, pop.life_expectancy_m)

## Stale feature branches on origin (pre-autonomous phase — do not merge/delete without PO)

- `feat/OR-95-dbw-hvd-explorer`, `feat/OR-template-clustered-stacked`
- `feat/or-114-sustainability-tab-enhancements`, `feat/or-118-analytics-competence-structure`
- `feat/or-121-measure-reference-system`, `feat/or-122-chart-visual-config`, `feat/template-one-per-family`
