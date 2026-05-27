# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-05-27 08:10 UTC -->

## Current Focus

AI Lead autonomous week underway. 4h cron cadence. Theme 3 code-complete; Theme 2 content pipeline building.

- OR-56 Labour Market — **Live** ✓
- OR-52 National Accounts — **Code in git**, deploy pending VPS
- OR-55 Demographics — **Code in git**, deploy pending VPS
- OR-145 Labour Market article — **Draft committed**, publish pending VPS
- OR-146 Debt service costs article — **Draft committed**, publish pending VPS

## What shipped (recent commits)

| Commit | What | Linear |
|---|---|---|
| `fe9beac` | OR-56 complete: fix YAML parse error + seed dimension_key mismatch | OR-56 |
| `ad1e34a` | OR-52 National Accounts dashboard — 24 files | OR-52 |
| `b0598ab` | OR-55 Demographics dashboard — 27 files | OR-55 |
| `e65e48f` | OR-145 Labour Market article draft | OR-145 |
| TBD (#14) | OR-146 Debt service costs article draft + decisions | OR-146 |

## Live production state

- **Public finance:** `portal.open-reporting.dev/public_finance/` — Live ✓
- **Labour market:** `portal.open-reporting.dev/labour_market/` — Live ✓
- **National accounts:** `portal.open-reporting.dev/national_accounts/` — **PENDING VPS DEPLOY**
- **Demographics:** `portal.open-reporting.dev/demographics/` — **PENDING VPS DEPLOY**
- **Blog:** `www.open-reporting.dev` — Live ✓
  - Article 1 (SGP/Maastricht) — Live ✓
  - Article 2 (Labour market) — **Draft committed, PENDING VPS PUBLISH**
  - Article 3 (Debt service costs) — **Draft committed, PENDING VPS PUBLISH**

## Note: autonomous runs from cloud containers

- `dbr run`, `dbt run`, Ghost publish (JWT/crypto) NOT available from cloud
- Production health checks return 403 (nginx allowlist) — NOT a service failure
- **CRITICAL on startup:** `git pull --ff-only` before any git ops (cloud containers start with stale local main)

## VPS action queue (all pending PO)

```bash
# 1. Pull latest
cd /opt/open-reporting && git pull --ff-only

# 2. Publish Article 2 (OR-145 — Labour market)
PYTHONPATH=/opt/open-reporting python3 products/blog/publish_to_ghost.py \
    products/blog/drafts/or-145-labour.md --publish

# 3. Publish Article 3 (OR-146 — Debt service costs)
# First: confirm 2019 D41PAY value in Eurostat databrowser (gov_10a_main, na_item=D41PAY, S13, PC_GDP, geo=PL)
PYTHONPATH=/opt/open-reporting python3 products/blog/publish_to_ghost.py \
    products/blog/drafts/or-146-debt-service.md --publish

# 4. Deploy OR-52 National Accounts
cd products/warehouse && dbt run --select fact_macro_overview --profiles-dir .
dbr validate products/dashboards/national_accounts
dbr run products/dashboards/national_accounts

# 5. Deploy OR-55 Demographics
dbt run --select fact_demo_overview --profiles-dir .
dbr validate products/dashboards/demographics
dbr run products/dashboards/demographics
```
After each dashboard: verify charts render data (not just 200 OK).

## Linear blocked on PO action

| Issue | What |
|---|---|
| OR-90 | Instagram token — Meta Developer portal |
| OR-79 | Ghost nav link — browser admin session |

## Architecture (current)

- Port assignments: public_finance=8057, labour_market=8058, national_accounts=8059, demographics=8060
- Next dashboard port: 8061
- Theme 3: all 3 dashboards coded
- Theme 2: 3 articles (1 live, 2 drafts committed)

## Stale feature branches on origin (pre-autonomous phase — do not merge/delete without PO)

- `feat/OR-95-dbw-hvd-explorer`
- `feat/OR-template-clustered-stacked`
- `feat/or-114-sustainability-tab-enhancements`
- `feat/or-118-analytics-competence-structure`
- `feat/or-121-measure-reference-system`
- `feat/or-122-chart-visual-config`
- `feat/template-one-per-family`

## Deferred / Next runs

- Theme 2: Fourth article (COFOG "where does money go?" pairs with wydatki page, or EU comparison article)
- EU comparison for macro (needs ALL_GEOS sentinel + backfill run)
- OR-77 social automation (blocked on OR-90 Instagram token)
- OR-76 pipeline robustness, OR-86 BDL ingestion (Theme 5)
- OR-87 BUS domain fix (needs DuckDB query to diagnose, VPS-side)
- Grey-history primitive, Wave 3 reference captures
