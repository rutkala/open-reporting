# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-05-27 08:15 UTC -->

## Current Focus

AI Lead autonomous week underway. 4h cron cadence. Theme 3 fully live. Theme 2 has 3 articles live.

All VPS items from queue executed by PO on 2026-05-27.

## Live production state

- **Public finance:** `portal.open-reporting.dev/public_finance/` — Live ✓
- **Labour market:** `portal.open-reporting.dev/labour_market/` — Live ✓
- **National accounts:** `portal.open-reporting.dev/national_accounts/` — **Live ✓** (deployed by PO)
- **Demographics:** `portal.open-reporting.dev/demographics/` — **Live ✓** (deployed by PO)
- **Blog:** `www.open-reporting.dev` — Live ✓
  - Article 1 (SGP/Maastricht) — Live ✓
  - Article 2 (Labour market) — **Live ✓** (published by PO)
  - Article 3 (Debt service costs) — **Live ✓** (published by PO)
- **Daily ingestion:** cron `0 22 * * *` UTC

## What shipped (recent commits)

| Commit | What | Linear |
|---|---|---|
| `fe9beac` | OR-56 Labour Market — fix YAML + seed | OR-56 Done |
| `ad1e34a` | OR-52 National Accounts dashboard | OR-52 Done |
| `b0598ab` | OR-55 Demographics dashboard | OR-55 Done |
| `e65e48f` | OR-145 Labour market article draft | OR-145 Done |
| `42d7f43b` | OR-146 Debt service article draft | OR-146 Done |

## What's next (no VPS queue pending)

All Theme 1 + Theme 2 (3 articles) + Theme 3 (3 dashboards) now complete.

**Next priorities:**
1. **Theme 2 — 4th article:** COFOG "where does money go?" paired with wydatki page, OR EU fiscal comparison article, OR labour market depth (regional, wages breakdown)
2. **Theme 4 — Social automation:** OR-77/OR-89 — still blocked on OR-90 (Instagram token, Meta portal PO action)
3. **Theme 5 — Pipeline depth:** OR-86 BDL ingestion, OR-87 BUS domain fix (needs VPS DuckDB query to diagnose), OR-88 NUTS2 expansion
4. **New domain dashboards:** ENV (OR-83) — emissions/energy; LAB richer (OR-82) — regional wages; possible 4th Eurostat domain

## Linear blocked on PO action

| Issue | What |
|---|---|
| OR-90 | Instagram token — Meta Developer portal (blocks all of Theme 4) |
| OR-79 | Ghost nav link — browser admin session |

## Architecture (current)

- Port assignments: public_finance=8057, labour_market=8058, national_accounts=8059, demographics=8060
- Next dashboard port: 8061
- All Theme 3 dashboards live on portal
- Theme 2: 3 articles published on blog

## Note: autonomous runs from cloud containers

- `dbr run`, `dbt run`, Ghost publish (JWT/crypto) NOT available from cloud
- Production health checks return 403 (nginx allowlist) — NOT a service failure
- **CRITICAL on startup:** `git pull --ff-only` before any git ops

## Stale feature branches on origin (pre-autonomous phase — do not merge/delete without PO)

- `feat/OR-95-dbw-hvd-explorer`, `feat/OR-template-clustered-stacked`
- `feat/or-114-sustainability-tab-enhancements`, `feat/or-118-analytics-competence-structure`
- `feat/or-121-measure-reference-system`, `feat/or-122-chart-visual-config`, `feat/template-one-per-family`

## Key Technical Facts

- Demographics seed dimension_keys verified correct (pop.births, pop.deaths, pop.population_total, pop.life_expectancy_f, pop.life_expectancy_m)
- OR-52 quarterly BOP series averaged to annual (AVG in fact_macro_overview)
- natural_increase_per1000 derived in fact_demo_overview (births − deaths, can go negative)
- OR-87 BUS domain fix: needs DuckDB query to verify actual dimension_key in raw.eurostat_observations — VPS-side diagnosis required
