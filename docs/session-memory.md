# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-05-28 02:30 UTC -->

## Current Focus

AI Lead autonomous week underway. 4h cron cadence. Theme 3 fully live (5 dashboards including ENV code committed). Theme 2: 5 article drafts committed (OR-147 COFOG, OR-148 EU fiscal, OR-149 wages), all pending VPS publish. Large VPS action queue for PO.

## Live production state

- **Public finance:** `portal.open-reporting.dev/public_finance/` — Live ✓
- **Labour market:** `portal.open-reporting.dev/labour_market/` — Live ✓
- **National accounts:** `portal.open-reporting.dev/national_accounts/` — Live ✓
- **Demographics:** `portal.open-reporting.dev/demographics/` — Live ✓
- **Blog:** `www.open-reporting.dev` — Live ✓
  - Article 1 (SGP/Maastricht) — Live ✓
  - Article 2 (Labour market / unemployment) — Live ✓
  - Article 3 (Debt service costs) — Live ✓
  - Article 4 (COFOG) — Draft `933d23f` — VPS publish pending
  - Article 5 (EU fiscal/EDP) — Draft `6fda803` — VPS publish pending
  - **Article 6 (Wages/real wage growth)** — Draft `c4d210e` — VPS publish pending
- **Daily ingestion:** cron `0 22 * * *` UTC

## What shipped (recent commits)

| Commit | What | Linear |
|---|---|---|
| `c4d210e` | OR-149 wages article draft — real wage growth Poland 2024 | OR-149 In Progress |
| `b60b697` | deploy-all.sh one-command VPS runbook | chore |
| `988bc9c` | run #17 post-mortem | docs |
| `796e0eb` | OR-83 ENV dashboard YAML + infra — port 8061 | OR-83 In Progress |
| `8f4328d` | OR-83 ENV mart + semantic layer | OR-83 In Progress |
| `6fda803` | OR-148 EU fiscal article draft | OR-148 In Progress |
| `dcacc49` | run #16 post-mortem | docs |
| `933d23f` | OR-147 COFOG article draft | OR-147 In Progress |
| `07df724` | OR-87 sts_inpr_a seed fix (indic_bt=PROD) | OR-87 fix |
| `3f7a9e8` | Absorb PO VPS actions — all Theme 3 live | All Done |

## VPS queue pending PO action

1. **OR-147 COFOG article publish:**
   ```bash
   cd /opt/open-reporting && git pull
   PYTHONPATH=/opt/open-reporting python3 products/blog/publish_to_ghost.py \
       products/blog/drafts/or-147-cofog.md --status draft
   # Check preview, then --publish
   ```

2. **OR-148 EU fiscal article publish:**
   ```bash
   PYTHONPATH=/opt/open-reporting python3 products/blog/publish_to_ghost.py \
       products/blog/drafts/or-148-eu-fiscal-comparison.md --publish
   ```

3. **OR-149 wages article publish:**
   ```bash
   PYTHONPATH=/opt/open-reporting python3 products/blog/publish_to_ghost.py \
       products/blog/drafts/or-149-wages.md --status draft
   # Verify: (a) nominal wage growth "ponad 11%" vs 13.7% in OR-145; (b) EUR min wage ~960 EUR. Then --publish
   ```

4. **OR-83 ENV dashboard deploy (port 8061):**
   ```bash
   cd products/warehouse
   DUCKDB_PATH=/opt/open-reporting/data/warehouse.duckdb dbt seed --select eurostat_series --profiles-dir .
   DUCKDB_PATH=/opt/open-reporting/data/warehouse.duckdb dbt run --select env_indicators fact_env_overview --profiles-dir .
   dbr validate products/dashboards/environment
   dbr run products/dashboards/environment
   sudo cp infra/systemd/or-environment.service /etc/systemd/system/
   sudo systemctl daemon-reload && sudo systemctl enable or-environment && sudo systemctl start or-environment
   sudo cp infra/nginx/conf.d/dbr-routes/environment.conf /etc/nginx/conf.d/dbr-routes/
   sudo nginx -t && sudo nginx -s reload
   ```

5. **OR-87 BUS/MAC industrial output fix activation:**
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

1. **OR-86 BDL ingestion** — cloud-implementable ingestion code (Theme 5)
2. **Theme 2 — 7th article:** Regional wages / NUTS2 depth OR public finance topic
3. **OR-76 Data pipeline Phase 1** — robustness, retries, alerting
4. **Theme 4 — blocked** on OR-90

## Article series status (Theme 2)

| # | Issue | Topic | Status |
|---|---|---|---|
| 1 | OR-80 | SGP/Maastricht | Live ✓ |
| 2 | OR-145 | Unemployment (3.1% record) | Live ✓ |
| 3 | OR-146 | Debt service costs | Live ✓ |
| 4 | OR-147 | COFOG spending breakdown | Draft — VPS pending |
| 5 | OR-148 | EU fiscal comparison (EDP) | Draft — VPS pending |
| 6 | OR-149 | Real wage growth 2024 | Draft — VPS pending |

## Architecture (current)

- Port assignments: public_finance=8057, labour_market=8058, national_accounts=8059, demographics=8060, environment=8061
- Next dashboard port: 8062
- All Theme 3 dashboards live on portal; OR-83 ENV code committed, deploy pending

## Note: autonomous runs from cloud containers

- `dbr run`, `dbt run`, Ghost publish (JWT/crypto) NOT available from cloud
- Production health checks return 403 (nginx allowlist) — NOT a service failure
- `data/logs/` directory does NOT exist in cloud containers — ingest log check will always return NOT FOUND (not an error)
- **CRITICAL on startup:** `git checkout main && git pull --ff-only origin main` (container may start on detached HEAD)

## Key Technical Facts

- OR-83: `env_indicators` intermediate model pre-existed; 4 series in eurostat_series.csv; fact_env_overview pivots 4 metrics; port 8061
- OR-87 fix: `sts_inpr_a` needs `indic_bt=PROD` — committed `07df724`; VPS runbook in Linear OR-87
- OR-148 article: Poland 2024 deficit = **6.5% GDP** (Eurostat April 2026 EDP notification)
- OR-149 article: Nominal wage growth 2024 uses "ponad 11%" (conservative; verify 13.7% vs GUS annual communiqué); EUR min wage ~960 EUR midpoint
- OR-52 quarterly BOP series averaged to annual (AVG in fact_macro_overview)
- natural_increase_per1000 derived in fact_demo_overview (births − deaths, can go negative)

## Stale feature branches on origin (pre-autonomous phase — do not merge/delete without PO)

- `feat/OR-95-dbw-hvd-explorer`, `feat/OR-template-clustered-stacked`
- `feat/or-114-sustainability-tab-enhancements`, `feat/or-118-analytics-competence-structure`
- `feat/or-121-measure-reference-system`, `feat/or-122-chart-visual-config`, `feat/template-one-per-family`
