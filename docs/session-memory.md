# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-05-30 21:30 UTC -->

## Current Focus

**15 domain dashboards live + 17 article drafts in Ghost.**
Interactive session (goal-mode): roadmap defined + Phase 2 delivery — 3 new dashboards (Health, Energy, Tourism), 3 new articles, 16 seed dimension_key bugs fixed, science dashboard enriched. All committed and pushed to main.

## Live production state

- **Public finance:** `/public_finance/` — Live ✓
- **Labour market:** `/labour_market/` — Live ✓
- **National accounts:** `/national_accounts/` — Live ✓ (current account now flowing — was broken)
- **Demographics:** `/demographics/` — Live ✓ (life expectancy now showing — was null before fix)
- **Environment:** `/environment/` — Live ✓
- **Income & Living Conditions:** `/living_conditions/` — Live ✓ (port 8062)
- **Prices & Inflation:** `/prices/` — Live ✓ (port 8063)
- **Education:** `/education/` — Live ✓ (port 8064)
- **Transport:** `/transport/` — Live ✓ (port 8065)
- **Science & R&D:** `/science/` — Live ✓ (port 8066) — NEW: Cyfryzacja page added
- **Trade:** `/trade/` — Live ✓ (port 8067)
- **Production:** `/production/` — Live ✓ (port 8068)
- **Health:** `/health/` — Live ✓ (port 8069) — NEW 2026-05-30
- **Energy:** `/energy/` — Live ✓ (port 8070) — NEW 2026-05-30
- **Tourism:** `/tourism/` — Live ✓ (port 8071) — NEW 2026-05-30
- **Portal homepage:** `/` — Live ✓ all 15 dashboards linked
- **Blog:** `www.open-reporting.dev` — Live ✓; **17 articles in Ghost as DRAFTS**, awaiting PO preview
- **Daily ingestion:** 22:00 UTC cron; exit=0 on 2026-05-29.
- **Autonomous-lead cron:** `0 2,7,12,17 * * *` UTC.

## Ghost draft inventory (17 articles, all awaiting PO review)

| Slug | Domain | OR |
|---|---|---|
| bezrobocie-polska-2024-historyczny-rekord | Labour | OR-145 |
| koszty-obslugi-dlugu-polska-2024 | Public Finance | OR-146 |
| cofog-wydatki-polska-2023-gdzie-trafi-kazda-zlotowka | Public Finance | OR-147 |
| polska-na-tle-ue-deficyt-dlug-2024 | Public Finance | OR-148 |
| wzrost-plac-polska-2024 | Labour | OR-149 |
| polska-demografia-przyrost-naturalny-2024 | Demographics | OR-150 |
| polska-produkcja-przemyslowa-2024 | Production | OR-151 |
| polska-srodowiskowo-1990-2024 | Environment | OR-154 |
| polska-inflacja-2022-2025 | Prices | OR-156 |
| handel-zagraniczny-polski-2002-2025 | Trade | OR-157 |
| polska-edukacja-wyzsza-1997-2025 | Education | OR-158 |
| polska-warunki-zycia-nierownosci-2005-2025 | Living Conditions | OR-159 |
| polska-kolej-covid-rekord-pasazerow-2025 | Transport | OR-160 |
| polska-nauka-rd-wydatki-2003-2024 | Science & R&D | OR-161 |
| polska-dlugosc-zycia-covid-rekord-2024 | Health | — |
| turystyka-polska-rekord-noclegow-2025 | Tourism | — |
| polska-transformacja-energetyczna-oze-2004-2024 | Energy | — |

## Discord bot fleet (live)

8 bots, `infra/discord-bot/bot.py`, tokens in `.env` as `DISCORD_BOT_<NAME>_TOKEN`.
project-lead (opus), scrum-master (haiku), dashboard-dev/data-engineer/content-writer/researcher/code-reviewer (sonnet), debug (haiku).
Service files: `or-discord-<name>-bot.service`. Agent prompts: `.claude/agents/<name>.md`. Channels: `#general`, `#daily-standup`, `#dashboard-dev`, `#blockers`, `#linear-feed`.
Untracked `infra/systemd/or-*-bot.service` + modified `infra/discord-bot/bot.py` are PO WIP — leave untouched, never commit.

## Recent commits

| Commit | What |
|---|---|
| `a507288b` | feat(science+content): Cyfryzacja page + 3 new articles (health, energy, tourism) |
| `34113664` | feat(tourism): Tourism dashboard — port 8071 |
| `ea7e5233` | feat(energy): Energy dashboard — port 8070 |
| `86af7fff` | feat(portal): Health added to homepage (13th) |
| `befd544d` | feat(health): Health dashboard + 16 dimension_key seed fixes |
| `61d32fd9` | docs: ROADMAP.md rewrite — grounded in May 2026 state |

## Open / blocked work

| # | Linear | What | Status |
|---|---|---|---|
| 1 | OR-153 | Telegram inbound (systemd `${}` non-expansion) | Blocked — PO; outbox works |
| 2 | OR-86 | BDL (GUS) ingestion | Backlog — needs `BDL_API_KEY` from PO |
| 3 | OR-90 | Instagram token (Meta portal) — blocks OR-89 publish | Blocked — PO action |
| 4 | OR-79 | Ghost nav "Portal" link — browser admin | Blocked — PO action |
| 5 | 17 drafts | Ghost preview + publish decisions | Awaiting PO (bottleneck) |
| 6 | OR-89 | Weekly snapshot — code ready, publish blocked on OR-90 | Buildable remainder: cron entry |
| 7 | Phase 2 remaining | BUS (1 indicator), FIN (0 indicators) — need ingestion | Needs new Eurostat datasets or BDL key |

## Key technical facts (current)

- **15 Eurostat domain dashboards deployed.** Next free port: 8072.
- **Seed dimension_key audit:** 16 mismatches fixed in `products/warehouse/seeds/eurostat_series.csv`. Run `dbt seed --select eurostat_series` after any seed change, then `dbt run --select stg_eurostat+`.
- **dbt write-lock dance:** stop live dashboard services (kill all `dbr serve` PIDs) → dbt run → restart with `dbr run`. Boot ~20s → brief 502.
- **Weekly snapshot card:** `products/social/weekly_snapshot.py --dry-run` works. Publish needs `INSTAGRAM_ACCESS_TOKEN` (OR-90).
- **New-domain dashboard recipe:** verify seed `dimension_key` == raw → mart → semantic → dashboard YAML → `dbr validate` → `dbr run` → verify.
- **Portal homepage** is static `infra/nginx/html/index.html`. Deploy: `docker compose up -d --force-recreate nginx`.
- **KPI cards resolve latest *non-null* value** (run #24 fix in `packages/dbr/.../semantic.py`).
- dbr `bar` = horizontal (metric x, dim y); `column` = vertical bars.
- `dbr` editable-installed; source edits live on service restart.
- Dashboard service + nginx route files ARE git-tracked.
- CLAUDE.md's `from dbr.semantic import query` is stale — use `semantic_query` / `_run_latest_query`.
- **Auto mode enabled** in `~/.claude/settings.json` (defaultMode: auto) + environment/allow rules for this VPS.
- Monthly tourism data (CLT): sum 12 months to annual via SUM in mart. Incomplete year (current year) included but undercounts — KPI shows last complete year.

## Stale feature branches

`feat/OR-95-dbw-hvd-explorer`, `feat/OR-template-clustered-stacked`, `feat/or-114-sustainability-tab-enhancements`, `feat/or-118-analytics-competence-structure`, `feat/or-121-measure-reference-system`, `feat/or-122-chart-visual-config`, `feat/template-one-per-family`, `feat/telegram-claude-bridge` (PR #62).
