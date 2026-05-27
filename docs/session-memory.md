# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-05-27 02:10 UTC -->

## Current Focus

AI Lead autonomous week underway. 4h cron cadence. Theme 3 complete in code:
- OR-56 Labour Market — **Live** ✓
- OR-52 National Accounts — **Code in git**, deploy pending VPS
- OR-55 Demographics — **Code in git**, deploy pending VPS (this run)

Next: Theme 2 article (second blog post) or Theme 4/5 depending on what Linear shows.

## What shipped (recent commits)

| Commit | What | Linear |
|---|---|---|
| `92733d8` / `f79b904` / `ee5022b` | OR-56 Labour Market dbt mart + dashboard YAML | OR-56 |
| `fe9beac` | OR-56 complete: fix YAML parse error + seed dimension_key mismatch | OR-56 |
| `ad1e34a` | OR-52 National Accounts dashboard — 24 files | OR-52 |
| `1585b74` | Delete STATUS.md | — |
| `b0598ab` | **OR-55 Demographics dashboard** — 27 files (dbt mart, semantic, YAML, infra) | OR-55 |

## Live production state

- **Public finance:** `portal.open-reporting.dev/public_finance/` — Live ✓
- **Labour market:** `portal.open-reporting.dev/labour_market/` — Live ✓
- **National accounts:** `portal.open-reporting.dev/national_accounts/` — **PENDING VPS DEPLOY**
- **Demographics:** `portal.open-reporting.dev/demographics/` — **PENDING VPS DEPLOY**
- **Blog:** `www.open-reporting.dev` — Live ✓
- **Daily ingestion:** cron `0 22 * * *` UTC

## Note: autonomous runs from cloud containers

- `dbr run`, `dbt run`, `docker compose` NOT available from cloud
- Production health checks return 403 (nginx allowlist) — NOT a service failure
- Deploy requires VPS access (PO action or VPS-side session)

## VPS Deploy queue (both pending)

```bash
# OR-52 National Accounts
cd products/warehouse && dbt run --select fact_macro_overview --profiles-dir .
dbr validate products/dashboards/national_accounts && dbr run products/dashboards/national_accounts

# OR-55 Demographics
dbt run --select fact_demo_overview --profiles-dir .
dbr validate products/dashboards/demographics && dbr run products/dashboards/demographics
```
After each: verify charts render data (not just 200 OK). If "No data": check raw.eurostat_observations dimension_keys.

## Linear blocked on PO action

| Issue | What |
|---|---|
| OR-90 | Instagram token — Meta Developer portal |
| OR-79 | Ghost nav link — browser admin session |

## Architecture (current)

- Port assignments: public_finance=8057, labour_market=8058, national_accounts=8059, demographics=8060
- Next dashboard port: 8061
- All Theme 3 dashboards now coded; Theme 4/5 next

## Key Technical Facts

- Demographics seed dimension_keys inferred from ingestion code (canonical sorted format, excludes geo/freq/time). Verified for POP series: `indic_de=GBIRTHRT`, `indic_de=GDEATHRT`, `indic_de=JAN`, `age=Y_LT1&sex=F`, `age=Y_LT1&sex=M`. Cannot confirm without DB query.
- natural_increase_per1000 is a derived column in fact_demo_overview (births − deaths, can go negative).
- OR-52 quarterly BOP series averaged to annual (AVG in fact_macro_overview).

## Deferred

- EU comparison for macro (needs ALL_GEOS sentinel + backfill run)
- OR-77 social automation, OR-89 weekly snapshot (Theme 4)
- OR-76 pipeline robustness, OR-86 BDL ingestion (Theme 5)
- Theme 2 second article (next blog post after OR-80)
- Grey-history primitive, Wave 3 reference captures
