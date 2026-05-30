# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-05-30 12:00 UTC -->

## Current Focus

**Six domain dashboards live + correct + now discoverable from the portal homepage.** The autonomous-lead cron (02/07/12/17 UTC) keeps shipping product work; the chat office is Discord (8 `claude -p` bot subprocesses). Telegram **outbox poller still works** for delivering autonomous-run reports to PO.

Run #28 (this run): **Shipped OR-155** — fixed the portal landing page (`portal.open-reporting.dev/`), which advertised two dead routes (`/labour/`, `/explorer/`) and surfaced none of the 6 live dashboards. Rewrote the card grid to one card per live domain (titles from each `dashboard.yml`), PR #63 squash-merged, nginx force-recreate deploy, curl-verified 6 live hrefs + dead cards gone. 0 subagent spawns, 1 commit. Picked because it was the only actionable production-correctness item — broken discoverability undermined every shipped product.

## Live production state

- **Public finance:** `/public_finance/` — Live ✓
- **Labour market:** `/labour_market/` — Live ✓
- **National accounts:** `/national_accounts/` — Live ✓
- **Demographics:** `/demographics/` — Live ✓
- **Environment:** `/environment/` — Live ✓
- **Income & Living Conditions:** `/living_conditions/` — Live ✓ (OR-59, port 8062, service or-living_conditions)
- **Portal homepage:** `/` — Live ✓ now links all 6 (OR-155, run #28)
- **Blog:** `www.open-reporting.dev` — Live ✓; Articles OR-145..151 + OR-154 (8 total) in Ghost as **DRAFTS**, awaiting PO preview
- **Daily ingestion:** 22:00 UTC cron; exit=0 on 2026-05-29. OR-76 outbox alert on failure.
- **Autonomous-lead cron:** `0 2,7,12,17 * * *` UTC.

## Big unused asset (still available — next product work)

`raw.eurostat_observations` already holds ingested datasets for MANY domains beyond the 6 live (health hlth_*, education edat_*/educ_*, trade ext_lt_intratrd/bop_*, transport rail_*/road_*, digital isoc_*/rd_*, crime crim_*, tourism tour_*, prices prc_hicp_aind). Intermediate `*_indicators.sql` models exist for all 18 domains; only 6 have marts+semantic+dashboards. **Next domain dashboards are buildable end-to-end without PO credentials** — proven recipe (OR-59). WARNING: several seed rows have dimension_keys that DON'T match raw (silent zero rows) — always verify against raw first.

## Discord bot fleet (live)

8 bots, `infra/discord-bot/bot.py`, tokens in `.env` as `DISCORD_BOT_<NAME>_TOKEN`.
project-lead (opus), scrum-master (haiku), dashboard-dev/data-engineer/content-writer/researcher/code-reviewer (sonnet), debug (haiku).
Service files: `or-discord-<name>-bot.service`. Agent prompts: `.claude/agents/<name>.md`. Channels: `#general`, `#daily-standup`, `#dashboard-dev`, `#blockers`, `#linear-feed`.
Untracked `infra/systemd/or-*-bot.service` + modified `infra/discord-bot/bot.py` are PO WIP — leave untouched, never commit.

## Recent commits

| Commit | What |
|---|---|
| PR #63 | fix(portal): OR-155 homepage links to the 6 live dashboards |
| `4a2c2e94` | feat(dashboards): OR-59 Income & Living Conditions dashboard (6th domain) |
| `408175e8` | feat(warehouse): OR-59 SOC data layer — fix 2 broken seed keys + mart + semantic |
| `970ce6ef` | docs: run #26 [QUIET RUN] — data-quality pass + Linear grooming |
| `bb736432` | feat(content): OR-154 environment article draft |

## Open / blocked work

| # | Linear | What | Status |
|---|---|---|---|
| 1 | OR-153 | Telegram inbound (systemd `${}` non-expansion) | Blocked — PO; outbox works |
| 2 | OR-86 | BDL (GUS) ingestion | Backlog — needs `BDL_API_KEY` from PO |
| 3 | OR-90 | Instagram token (Meta portal) — blocks Theme 4 | Blocked — PO action |
| 4 | OR-79 | Ghost nav "Portal" link — browser admin | Blocked — PO action |
| 5 | 8 drafts | OR-145..151 + OR-154 Ghost preview + publish | Awaiting PO (bottleneck) |
| 6 | OR-89 | Weekly snapshot (social) | Buildable; publish blocked on OR-90 |
| 7 | — | 7th domain dashboard (health/education/trade/...) | Buildable end-to-end, OR-59 recipe |

## Key technical facts (current)

- **New-domain dashboard recipe (proven OR-59):** verify seed `dimension_key` == raw (`raw.eurostat_observations`, cols dataset_code/geo/period/dimension_key/value) → `marts/<x>/fact_<x>_overview.sql` (MAX-pivot, annual, group by geo+year) → `semantic/<x>_overview.yml` → `products/dashboards/<route>/` → `dbr validate` → `dbr run` → curl 200 + `<title>Dash</title>` + `screenshot`. Next free port after 8062.
- **Portal homepage** is static `infra/nginx/html/index.html`, hand-authored card grid, served by nginx (no build step). Deploy: `docker compose up -d --force-recreate nginx`. Add a card per new dashboard. If route count grows past ~10, consider generating the grid in the deploy path (noted in #28, not yet an issue).
- **dbt write-lock dance:** stop live dashboard services, run `dbt seed`/`dbt run` (`cd products/warehouse && DUCKDB_PATH=/opt/open-reporting/data/warehouse.duckdb dbt ... --profiles-dir .`), restart. Boot ~20s → brief 502; wait ~25s before re-curl.
- **KPI cards resolve latest *non-null* value** (run #24 fix in `packages/dbr/.../semantic.py`).
- dbr `bar` is **horizontal** (metric x, dim y); `column` for vertical bars.
- `dbr` editable-installed; source edits go live on service restart.
- Dashboard service + nginx route files ARE git-tracked (`infra/systemd/or-<route>.service`, `infra/nginx/conf.d/dbr-routes/<route>.conf`).
- CLAUDE.md's `from dbr.semantic import query` helper is stale — module exports `semantic_query`/`semantic_query_history`/`_run_latest_query`.

## Stale feature branches

`feat/OR-95-dbw-hvd-explorer`, `feat/OR-template-clustered-stacked`, `feat/or-114-sustainability-tab-enhancements`, `feat/or-118-analytics-competence-structure`, `feat/or-121-measure-reference-system`, `feat/or-122-chart-visual-config`, `feat/template-one-per-family`, `feat/telegram-claude-bridge` (PR #62).
