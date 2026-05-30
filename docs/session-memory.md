# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-05-30 07:15 UTC -->

## Current Focus

**Six domain dashboards live + correct; AI scrum team live on Discord.** The autonomous-lead cron (02/07/12/17 UTC) keeps shipping product work; the chat office is Discord (8 `claude -p` bot subprocesses). Telegram **outbox poller still works** for delivering autonomous-run reports to PO.

Run #27 (this run): **Shipped OR-59 — 6th live domain dashboard**, `portal.open-reporting.dev/living_conditions/` (Income & Living Conditions). End-to-end: fixed two broken `eurostat_series` seed keys (silent zero-row trap) + added income indicator → built `fact_soc_overview` mart + `soc_overview` semantic model → 2-page dbr dashboard → deployed + verified (200, Dash app, screenshot shows real data) → analytical-validator (Opus) PASS. Breaks a 3-run maintenance/draft streak. Data already ingested (Eurostat ILC), no PO credential needed. Filed OR-155 (portal homepage links stale). 1 subagent spawn, 2 code commits.

## Live production state

- **Public finance:** `/public_finance/` — Live ✓
- **Labour market:** `/labour_market/` — Live ✓
- **National accounts:** `/national_accounts/` — Live ✓
- **Demographics:** `/demographics/` — Live ✓
- **Environment:** `/environment/` — Live ✓
- **Income & Living Conditions:** `/living_conditions/` — Live ✓ NEW (OR-59, run #27; port 8062, service or-living_conditions)
- **Blog:** `www.open-reporting.dev` — Live ✓; Articles OR-145..151 + OR-154 (8 total) in Ghost as **DRAFTS**, awaiting PO preview
- **Daily ingestion:** 22:00 UTC cron; exit=0 on 2026-05-29. OR-76 outbox alert on failure.
- **Autonomous-lead cron:** `0 2,7,12,17 * * *` UTC.

## Big unused asset discovered (run #27)

`raw.eurostat_observations` already holds ingested datasets for MANY domains beyond the 6 live (health hlth_*, education edat_*/educ_*, trade ext_lt_intratrd/bop_*, transport rail_*/road_*, digital isoc_*/rd_*, crime crim_*, tourism tour_*, prices prc_hicp_aind). Intermediate `*_indicators.sql` models exist for all 18 domains; only 6 have marts+semantic+dashboards. **Next domain dashboards are buildable end-to-end without PO credentials** — same pattern as OR-59. WARNING: several existing seed rows have dimension_keys that DON'T match raw (silent zero rows) — always verify against raw first.

## Discord bot fleet (live)

8 bots, `infra/discord-bot/bot.py`, tokens in `.env` as `DISCORD_BOT_<NAME>_TOKEN`.
project-lead (opus), scrum-master (haiku), dashboard-dev/data-engineer/content-writer/researcher/code-reviewer (sonnet), debug (haiku).
Service files: `or-discord-<name>-bot.service`. Agent prompts: `.claude/agents/<name>.md`. Channels: `#general`, `#daily-standup`, `#dashboard-dev`, `#blockers`, `#linear-feed`.
Untracked `infra/systemd/or-*-bot.service` + modified `infra/discord-bot/bot.py` are PO WIP — leave untouched, never commit.

## Recent commits

| Commit | What |
|---|---|
| `4a2c2e94` | feat(dashboards): OR-59 Income & Living Conditions dashboard (6th domain) |
| `408175e8` | feat(warehouse): OR-59 SOC data layer — fix 2 broken seed keys + mart + semantic |
| `970ce6ef` | docs: run #26 [QUIET RUN] — data-quality pass + Linear grooming |
| `bb736432` | feat(content): OR-154 environment article draft |
| `74190707` | docs: run #24 post-mortem — OR-83 + global dbr KPI latest-non-null fix |

## Open / blocked work

| # | Linear | What | Status |
|---|---|---|---|
| 1 | OR-155 | Portal homepage links stale (only /labour//explorer/, neither live) | Backlog (filed run #27) — buildable, infra/PR |
| 2 | OR-153 | Telegram inbound (systemd `${}` non-expansion) | Blocked — PO; outbox works |
| 3 | OR-86 | BDL (GUS) ingestion | Backlog — needs `BDL_API_KEY` from PO |
| 4 | OR-90 | Instagram token (Meta portal) — blocks Theme 4 | Blocked — PO action |
| 5 | OR-79 | Ghost nav "Portal" link — browser admin | Blocked — PO action |
| 6 | 8 drafts | OR-145..151 + OR-154 Ghost preview + publish | Awaiting PO (bottleneck) |
| 7 | OR-89 | Weekly snapshot (social) | Buildable; publish blocked on OR-90 |

## Key technical facts (current)

- **New-domain dashboard recipe (proven OR-59):** verify seed `dimension_key` == raw (`raw.eurostat_observations`, cols dataset_code/geo/period/dimension_key/value) → `marts/<x>/fact_<x>_overview.sql` (MAX-pivot, annual, group by geo+year) → `semantic/<x>_overview.yml` (agg: average collapses to identity for single-value cells; set ascending_is_good per metric) → `products/dashboards/<route>/` (dashboard.yml + app.py + pages/) → `dbr validate` → `dbr run` → curl 200 + `<title>Dash</title>` + `screenshot <route> --output /tmp/x.png`. Next free port after 8062.
- **dbt write-lock dance:** stop the live dashboard services (`sudo -n /usr/bin/systemctl stop or-<name>.service`), run `dbt seed`/`dbt run` (`cd products/warehouse && DUCKDB_PATH=/opt/open-reporting/data/warehouse.duckdb dbt ... --profiles-dir .`), then start them again. Env service boot ~20s → brief 502 right after restart (wait ~25s before re-curl).
- **KPI cards resolve latest *non-null* value** (run #24 fix in `packages/dbr/.../semantic.py`). Handles wide-fact end-year gaps (e.g. SOC material_deprivation ends 2020 while others reach 2024/25).
- dbr `bar` is **horizontal** (metric x, dim y); `column` for vertical bars. (OR-59 used only line/card.)
- `dbr` editable-installed; source edits go live on service restart.
- Dashboard service + nginx route files ARE git-tracked (`infra/systemd/or-<route>.service`, `infra/nginx/conf.d/dbr-routes/<route>.conf`) — commit them with the dashboard.
- CLAUDE.md's `from dbr.semantic import query` helper is stale — module exports `semantic_query`/`semantic_query_history`/`_run_latest_query`. Use direct read-only duckdb for QA.

## Stale feature branches

`feat/OR-95-dbw-hvd-explorer`, `feat/OR-template-clustered-stacked`, `feat/or-114-sustainability-tab-enhancements`, `feat/or-118-analytics-competence-structure`, `feat/or-121-measure-reference-system`, `feat/or-122-chart-visual-config`, `feat/template-one-per-family`, `feat/telegram-claude-bridge` (PR #62). `fix/or-83-kpi-latest-nonnull` merged → deletable.
