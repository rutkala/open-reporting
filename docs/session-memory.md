# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-05-31 02:00 UTC -->

## Current Focus

**16 domain dashboards live. All 18 blog articles PUBLISHED to Ghost (2026-05-31).**
Interactive session (2026-05-31): Built autonomous release pipeline + pushed all 18 draft articles live. Review applied inline (content/analytical/domain criteria). 9 PASS, 9 CONDITIONAL (P2 only — published per gate logic), 0 BLOCK. OR-145 fixed (added GUS Prognoza source for working-age projection) before publishing. Blog is now fully live at www.open-reporting.dev.

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
- **Health:** `/health/` — Live ✓ (port 8069)
- **Energy:** `/energy/` — Live ✓ (port 8070)
- **Tourism:** `/tourism/` — Live ✓ (port 8071)
- **Financial Markets:** `/financial_markets/` — Live ✓ (port 8072) — NEW 2026-05-30
- **Portal homepage:** `/` — Live ✓ all 16 dashboards linked
- **Blog:** `www.open-reporting.dev` — Live ✓; **18 articles PUBLISHED** (2026-05-31) — pipeline review complete
- **Daily ingestion:** 22:00 UTC cron; exit=0 on 2026-05-29.
- **Autonomous-lead cron:** `0 2,7,12,17 * * *` UTC.

## Ghost draft inventory (18 articles, all awaiting PO review)

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
| kursy-walutowe-pln-historia-2002-2026 | Financial Markets | — |

## Discord bot fleet (live)

8 bots, `infra/discord-bot/bot.py`, tokens in `.env` as `DISCORD_BOT_<NAME>_TOKEN`.
project-lead (opus), scrum-master (haiku), dashboard-dev/data-engineer/content-writer/researcher/code-reviewer (sonnet), debug (haiku).
Service files: `or-discord-<name>-bot.service`. Agent prompts: `.claude/agents/<name>.md`. Channels: `#general`, `#daily-standup`, `#dashboard-dev`, `#blockers`, `#linear-feed`.
Untracked `infra/systemd/or-*-bot.service` + modified `infra/discord-bot/bot.py` are PO WIP — leave untouched, never commit.

## Recent commits

| Commit | What |
|---|---|
| `b3e50ad5` | feat(content): financial markets article — exchange rate history PLN 2002-2026 |
| `d52369a1` | feat(financial-markets): Financial Markets dashboard — port 8072, Phase 2 complete |
| `2cfb6cde` | docs: session memory update — 15 dashboards live |
| `HEAD` | feat(content): all 18 articles published — pipeline review complete 2026-05-31 |
| `cd106eb4` | feat(content): autonomous article release pipeline — 3-reviewer gate, auto-publish |
| `b3e50ad5` | feat(content): financial markets article — exchange rate history PLN 2002-2026 |
| `d52369a1` | feat(financial-markets): Financial Markets dashboard — port 8072, Phase 2 complete |
| `a507288b` | feat(science+content): Cyfryzacja page + 3 new articles (health, energy, tourism) |

## Open / blocked work

| # | Linear | What | Status |
|---|---|---|---|
| 1 | OR-153 | Telegram inbound (systemd `${}` non-expansion) | Blocked — PO; outbox works |
| 2 | OR-86 | BDL (GUS) ingestion | Backlog — needs `BDL_API_KEY` from PO |
| 3 | OR-90 | Instagram token (Meta portal) — blocks OR-89 publish | Blocked — PO action |
| 4 | OR-79 | Ghost nav "Portal" link — browser admin | Blocked — PO action |
| 5 | 18 articles | All PUBLISHED 2026-05-31 via inline review pipeline | Done ✓ |
| 6 | OR-89 | Weekly snapshot — code ready, publish blocked on OR-90 | Buildable remainder: cron entry |
| 7 | Phase 3 | Data depth: BDL, Finance v2, dbt tests, freshness indicators | Next focus |

## Key technical facts (current)

- **Article release pipeline:** `python3 products/blog/release_pipeline.py` — reviews 18 drafts via content+analytical+domain reviewers, publishes passing ones. Must run STANDALONE (not nested in active Claude Code session — hits Max rate limits). Standalone run works fine; integrated into Step 2b of autonomous lead protocol.
- **16 Eurostat domain dashboards deployed.** Next free port: 8073.
- **Phase 2 complete:** Health (8069), Energy (8070), Tourism (8071), Financial Markets (8072).
- **Financial Markets:** fact_fin_overview mart = annual avg exchange rates from fin_indicators (NBP). Semantic: fin_overview.yml.
- **Seed dimension_key audit:** 16 mismatches fixed in `products/warehouse/seeds/eurostat_series.csv`. Run `dbt seed --select eurostat_series` after any seed change, then `dbt run --select stg_eurostat+`.
- **dbt write-lock dance:** kill all `dbr serve` PIDs → dbt run → restart with `dbr run`. Boot ~20s → brief 502.
- **Weekly snapshot card:** `products/social/weekly_snapshot.py --dry-run` works. Publish needs `INSTAGRAM_ACCESS_TOKEN` (OR-90).
- **Portal homepage** is static `infra/nginx/html/index.html`. Deploy: `docker compose up -d --force-recreate nginx`.
- **KPI cards resolve latest *non-null* value** (run #24 fix in `packages/dbr/.../semantic.py`).
- dbr `bar` = horizontal (metric x, dim y); `column` = vertical bars.
- `dbr` editable-installed; source edits live on service restart.
- Dashboard service + nginx route files ARE git-tracked.
- CLAUDE.md's `from dbr.semantic import query` is stale — use `semantic_query` / `_run_latest_query`.
- **Auto mode enabled** in `~/.claude/settings.json` (defaultMode: auto) + environment/allow rules for this VPS.
- Monthly tourism data (CLT): sum 12 months to annual via SUM in mart. Incomplete year (current year) included but undercounts — KPI shows last complete year.
- Line chart supports multi-metric y: `y: { metric: [metric1, metric2] }` — one trace per metric.

## Stale feature branches

`feat/OR-95-dbw-hvd-explorer`, `feat/OR-template-clustered-stacked`, `feat/or-114-sustainability-tab-enhancements`, `feat/or-118-analytics-competence-structure`, `feat/or-121-measure-reference-system`, `feat/or-122-chart-visual-config`, `feat/template-one-per-family`, `feat/telegram-claude-bridge` (PR #62).
