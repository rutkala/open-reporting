# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-05-30 14:10 UTC -->

## Current Focus

**12 domain dashboards live + 14 article drafts in Ghost — 12/12 dashboard-article pairing complete.**
Interactive session (goal-mode): OR-159/160/161 articles written via parallel content-writer agents + OR-89 weekly snapshot script built. 1 commit, pushed to main.

## Live production state

- **Public finance:** `/public_finance/` — Live ✓
- **Labour market:** `/labour_market/` — Live ✓
- **National accounts:** `/national_accounts/` — Live ✓
- **Demographics:** `/demographics/` — Live ✓
- **Environment:** `/environment/` — Live ✓
- **Income & Living Conditions:** `/living_conditions/` — Live ✓ (port 8062)
- **Prices & Inflation:** `/prices/` — Live ✓ (port 8063)
- **Education:** `/education/` — Live ✓ (port 8064)
- **Transport:** `/transport/` — Live ✓ (port 8065)
- **Science & R&D:** `/science/` — Live ✓ (port 8066)
- **Trade:** `/trade/` — Live ✓ (port 8067)
- **Production:** `/production/` — Live ✓ (port 8068)
- **Portal homepage:** `/` — Live ✓ all 12 dashboards linked (PR #63 merged 2026-05-30)
- **Blog:** `www.open-reporting.dev` — Live ✓; **14 articles in Ghost as DRAFTS**, awaiting PO preview
- **Daily ingestion:** 22:00 UTC cron; exit=0 on 2026-05-29.
- **Autonomous-lead cron:** `0 2,7,12,17 * * *` UTC.

## Ghost draft inventory (14 articles, all awaiting PO review)

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

## Discord bot fleet (live)

8 bots, `infra/discord-bot/bot.py`, tokens in `.env` as `DISCORD_BOT_<NAME>_TOKEN`.
project-lead (opus), scrum-master (haiku), dashboard-dev/data-engineer/content-writer/researcher/code-reviewer (sonnet), debug (haiku).
Service files: `or-discord-<name>-bot.service`. Agent prompts: `.claude/agents/<name>.md`. Channels: `#general`, `#daily-standup`, `#dashboard-dev`, `#blockers`, `#linear-feed`.
Untracked `infra/systemd/or-*-bot.service` + modified `infra/discord-bot/bot.py` are PO WIP — leave untouched, never commit.

## Recent commits

| Commit | What |
|---|---|
| `6d577935` | feat(content): OR-159/160/161 — living conditions, transport, science articles |
| `980e1cb4` | feat(content): OR-156/157/158 — three new article drafts (prices, trade, education) |
| `403d95fb` | feat(dashboards): production & agriculture dashboard (12th domain) |
| `6a7ebf2b` | feat(dashboards): trade dashboard (11th domain) |
| `5455cd63` | feat(dashboards): science & R&D dashboard (10th domain) |
| PR #63 | fix(portal): OR-155 homepage links — merged 2026-05-30 |

## Open / blocked work

| # | Linear | What | Status |
|---|---|---|---|
| 1 | OR-153 | Telegram inbound (systemd `${}` non-expansion) | Blocked — PO; outbox works |
| 2 | OR-86 | BDL (GUS) ingestion | Backlog — needs `BDL_API_KEY` from PO |
| 3 | OR-90 | Instagram token (Meta portal) — blocks OR-89 publish | Blocked — PO action |
| 4 | OR-79 | Ghost nav "Portal" link — browser admin | Blocked — PO action |
| 5 | 14 drafts | Ghost preview + publish decisions | Awaiting PO (bottleneck) |
| 6 | OR-89 | Weekly snapshot — code ready, publish blocked on OR-90 | Buildable remainder: cron entry |

## Key technical facts (current)

- **All 12 Eurostat domain dashboards deployed.** Next data expansion requires new ingestion (BDL key OR-86, or new Eurostat datasets via daily cron). Next free port after 8068.
- **Weekly snapshot card:** `products/social/weekly_snapshot.py --dry-run` works. Generates 1080×1080 Nordic card. Publish needs `INSTAGRAM_ACCESS_TOKEN` (OR-90).
- **New-domain dashboard recipe (proven OR-59):** verify seed `dimension_key` == raw → mart → semantic → dashboard YAML → `dbr validate` → `dbr run` → verify.
- **Portal homepage** is static `infra/nginx/html/index.html`. Deploy: `docker compose up -d --force-recreate nginx`.
- **dbt write-lock dance:** stop live dashboard services → dbt run → restart. Boot ~20s → brief 502.
- **KPI cards resolve latest *non-null* value** (run #24 fix in `packages/dbr/.../semantic.py`).
- dbr `bar` = horizontal (metric x, dim y); `column` = vertical bars.
- `dbr` editable-installed; source edits live on service restart.
- Dashboard service + nginx route files ARE git-tracked.
- CLAUDE.md's `from dbr.semantic import query` is stale — use `semantic_query` / `_run_latest_query`.
- **Auto mode enabled** in `~/.claude/settings.json` (defaultMode: auto) + environment/allow rules for this VPS.

## Stale feature branches

`feat/OR-95-dbw-hvd-explorer`, `feat/OR-template-clustered-stacked`, `feat/or-114-sustainability-tab-enhancements`, `feat/or-118-analytics-competence-structure`, `feat/or-121-measure-reference-system`, `feat/or-122-chart-visual-config`, `feat/template-one-per-family`, `feat/telegram-claude-bridge` (PR #62).
