# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-05-26 20:30 UTC -->

## Current Focus

AI Lead autonomous week underway. 4h cron cadence (`trig_01TqBcSxS3SzQn7BtSTiDmif`). Themes 1+2 complete. Theme 3 dashboard #1 (OR-56 Labour) is live. Theme 3 dashboard #2 (OR-52 Macro) code is in git — **deployment pending on VPS**.

## What shipped (2026-05-26 autonomous runs)

| Commit | What | Linear |
|---|---|---|
| `92733d8` / `f79b904` / `ee5022b` | OR-56 Labour Market dbt mart + dashboard YAML (autonomous, 15:11–17:15 UTC) | OR-56 |
| `fe9beac` | OR-56 complete: fix YAML parse error + seed dimension_key mismatch (PO conversational session 19:30 UTC) | OR-56 |
| `caee76d` | STATUS.md heartbeat (orphaned, recovered in 20:00 UTC run) | — |
| `ad1e34a` | **OR-52 National Accounts dashboard** — 24 files (dbt mart, semantic, YAML, infra) | OR-52 |

## Live production state (PO-verified 19:35 UTC)

- **Public finance dashboard:** `portal.open-reporting.dev/public_finance/` — 200 OK
- **Labour market dashboard:** `portal.open-reporting.dev/labour_market/` — 200 OK with real data
- **National accounts dashboard:** `portal.open-reporting.dev/national_accounts/` — **PENDING DEPLOY** (code in git, needs `dbt run` + `dbr run` on VPS)
- **Blog:** `www.open-reporting.dev` — 200 OK
- **Daily ingestion:** cron `0 22 * * *` UTC, last run 2026-05-26 13:52 UTC exit=0

## Note: autonomous runs from cloud containers

The cron fires in an ephemeral cloud container, not on the VPS. This means:
- `dbr run`, `dbt run`, `docker compose` commands are NOT available
- Production health checks return 403 from this container's IP (nginx allowlist) — NOT a service failure
- Deployment must be done by PO or a VPS-side session
- Code can be written and pushed to git; deploy is the PO's action

## Next pending — Theme 3

| # | Linear | What | Status |
|---|---|---|---|
| 7 | OR-56 | Labour Market dashboard | **Done** (live) |
| 8 | OR-52 | National Accounts & Macro dashboard | **Code in git** — needs VPS deploy |
| 9 | OR-55 | Population & Demographics dashboard | Backlog (next) |

## Linear blocked on PO action

| Issue | What |
|---|---|
| OR-90 | Instagram token — Meta Developer portal |
| OR-79 | Ghost nav link — browser admin session |

## Architecture (current)

**Code-in-cloud, deploy-on-VPS.** Autonomous runs from cloud containers write YAML/SQL/Python to git. Deployment (`dbt run` + `dbr run`) requires VPS access — PO or conversational session.

**Model delegation:** Sonnet builders (dashboard-dev, data-engineer) execute from clear specs. Opus orchestrates. SubAgent budget: 6/run.

## Key Technical Facts

- DuckDB: `data/warehouse.duckdb` — write-locked during cron (22:00 UTC)
- Port assignments: public_finance=8057, labour_market=8058, national_accounts=8059
- MAC seed dimension_keys verified against PostgreSQL catalogue; all 7 MAC series have `verified=true` and `geo=PL`
- Quarterly BOP data (mac.current_account_gdp) aggregated to annual via AVG in fact_macro_overview
- Next dashboard port: 8060 (for OR-55 demographics)

## Deferred

- EU comparison for macro (needs ALL_GEOS sentinel + backfill run)
- OR-77 social automation, OR-89 weekly snapshot (Theme 4)
- OR-76 pipeline robustness, OR-86 BDL ingestion (Theme 5)
- Grey-history primitive, Wave 3 reference captures, complex_dashboard skill
