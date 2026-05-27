# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-05-27 08:00 UTC -->

## Current Focus

AI Lead autonomous week underway. 4h cron cadence. Theme 3 code-complete; Theme 2 second article drafted.

- OR-56 Labour Market — **Live** ✓
- OR-52 National Accounts — **Code in git**, deploy pending VPS
- OR-55 Demographics — **Code in git**, deploy pending VPS
- OR-145 Labour Market article — **Draft committed**, publish pending VPS

## What shipped (recent commits)

| Commit | What | Linear |
|---|---|---|
| `92733d8` / `f79b904` / `ee5022b` | OR-56 Labour Market dbt mart + dashboard YAML | OR-56 |
| `fe9beac` | OR-56 complete: fix YAML parse error + seed dimension_key mismatch | OR-56 |
| `ad1e34a` | OR-52 National Accounts dashboard — 24 files | OR-52 |
| `b0598ab` | OR-55 Demographics dashboard — 27 files | OR-55 |
| `eddd1c1` | Run #12 post-mortem | — |
| TBD (run #13) | OR-145 article draft + decisions + session-memory | OR-145 |

## Live production state

- **Public finance:** `portal.open-reporting.dev/public_finance/` — Live ✓
- **Labour market:** `portal.open-reporting.dev/labour_market/` — Live ✓
- **National accounts:** `portal.open-reporting.dev/national_accounts/` — **PENDING VPS DEPLOY**
- **Demographics:** `portal.open-reporting.dev/demographics/` — **PENDING VPS DEPLOY**
- **Blog:** `www.open-reporting.dev` — Live ✓
  - Article 1 (SGP/Maastricht) — Live ✓
  - Article 2 (Labour market) — **Draft committed, PENDING VPS PUBLISH**
- **Daily ingestion:** cron `0 22 * * *` UTC

## Note: autonomous runs from cloud containers

- `dbr run`, `dbt run`, Ghost publish (JWT/crypto) NOT available from cloud
- Production health checks return 403 (nginx allowlist) — NOT a service failure
- Deploy requires VPS access (PO action or VPS-side session)
- **IMPORTANT:** Cloud containers start with local `main` pointing to stale commit.
  Always `git pull --ff-only` at start of Step 0 before any other git work.

## VPS action queue (all pending PO)

```bash
# Step 1: Pull latest
cd /opt/open-reporting && git pull --ff-only

# Step 2: Publish labour market article (OR-145)
PYTHONPATH=/opt/open-reporting python3 products/blog/publish_to_ghost.py \
    products/blog/drafts/or-145-labour.md --publish

# Step 3: Deploy OR-52 National Accounts
cd products/warehouse && dbt run --select fact_macro_overview --profiles-dir .
dbr validate products/dashboards/national_accounts
dbr run products/dashboards/national_accounts

# Step 4: Deploy OR-55 Demographics
dbt run --select fact_demo_overview --profiles-dir .
dbr validate products/dashboards/demographics
dbr run products/dashboards/demographics
```
After each dashboard deploy: verify charts render data (not just 200 OK). If "No data": check raw.eurostat_observations dimension_keys.

## Linear blocked on PO action

| Issue | What |
|---|---|
| OR-90 | Instagram token — Meta Developer portal |
| OR-79 | Ghost nav link — browser admin session |

## Architecture (current)

- Port assignments: public_finance=8057, labour_market=8058, national_accounts=8059, demographics=8060
- Next dashboard port: 8061
- All Theme 3 dashboards coded; Theme 2 has 2 articles (1 live, 1 draft)

## Key Technical Facts

- **Detached HEAD pattern:** Cloud containers start with local `main` behind origin. Fix: `git pull --ff-only` in Step 0 before other git ops.
- All 5 POP dimension_keys verified correct for OR-55 (cross-checked catalogue seed vs `_dimension_key()` sort logic).
- All 5 MAC dimension_keys verified correct for OR-52.
- OR-52 quarterly BOP series averaged to annual (AVG in fact_macro_overview).
- natural_increase_per1000 is derived in fact_demo_overview (births − deaths, can go negative).

## Deferred / Next runs

- Theme 2: Third article (topic TBD — debt service costs, or COFOG analysis)
- EU comparison for macro (needs ALL_GEOS sentinel + backfill run)
- OR-77 social automation, OR-89 weekly snapshot (Theme 4)
- OR-76 pipeline robustness, OR-86 BDL ingestion (Theme 5)
- Grey-history primitive, Wave 3 reference captures
