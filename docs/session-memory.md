# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-05-29 12:15 UTC -->

## Current Focus

**Five domain dashboards live + correct; AI scrum team live on Discord.** The autonomous-lead cron (02/07/12/17 UTC) keeps shipping product work; the chat office is Discord (8 `claude -p` bot subprocesses). The Telegram **outbox poller still works** for delivering autonomous-run reports to PO.

Run #24 (this run): closed OR-83 (ENV dashboard) and fixed a global KPI-card engine bug.

## Live production state

- **Public finance:** `portal.open-reporting.dev/public_finance/` — Live ✓
- **Labour market:** `portal.open-reporting.dev/labour_market/` — Live ✓
- **National accounts:** `portal.open-reporting.dev/national_accounts/` — Live ✓
- **Demographics:** `portal.open-reporting.dev/demographics/` — Live ✓
- **Environment:** `portal.open-reporting.dev/environment/` — Live ✓ (OR-83 Done; KPI cards fixed run #24)
- **Blog:** `www.open-reporting.dev` — Live ✓; Articles OR-145..OR-151 in Ghost as **DRAFTS**, awaiting PO preview
- **Daily ingestion:** 22:00 UTC cron; exit=0 on 2026-05-28. OR-76 outbox alert on failure.
- **Autonomous-lead cron:** `0 2,7,12,17 * * *` UTC.

## Discord bot fleet (live)

8 bots, `infra/discord-bot/bot.py`, tokens in `.env` as `DISCORD_BOT_<NAME>_TOKEN`.
project-lead (opus), scrum-master (haiku), dashboard-dev/data-engineer/content-writer/researcher/code-reviewer (sonnet), debug (haiku).
Service files: `or-discord-<name>-bot.service`. Agent prompts: `.claude/agents/<name>.md`.
Channels: `#general`, `#daily-standup`, `#dashboard-dev`, `#blockers`, `#linear-feed`.
Each `@`-mention/DM spawns a fresh subprocess — no in-chat memory; relies on CLAUDE.md + persistent memory + this file.

## Recent commits

| Commit | What |
|---|---|
| `fca7b818` | fix(dbr): KPI card resolves latest non-null value, not latest spine year (run #24) |
| `c4b33f4b` | feat(infra): Discord 8-bot scrum team — framework, services, agent files |
| `e89360d2` | fix(public_finance): OR-152 P2/P3 — Wydatki 2024 re-anchor + trend legend |
| `8bdb235a` | docs: run #22 post-mortem + OR-152 P1 |
| `ca5ece47` | feat(content): OR-151 industrial output article (8th Theme 2) |

## Open / blocked work

| # | Linear | What | Status |
|---|---|---|---|
| 1 | OR-153 | Telegram comms inbound (systemd `${}` non-expansion) | Blocked — PO action; outbox delivery works |
| 2 | OR-86 | BDL (GUS) ingestion first run | Blocked — needs `BDL_API_KEY` from PO |
| 3 | OR-90 | Instagram token (Meta portal) — blocks Theme 4 publishing | Blocked — PO action |
| 4 | OR-79 | Ghost nav "Portal" link — browser admin | Blocked — PO action |
| 5 | 7 drafts | OR-145..151 Ghost preview + publish decisions | Awaiting PO |
| 6 | OR-89 | Weekly snapshot (social) | Buildable; publish blocked on OR-90 |
| 7 | — | Discord goal-file pattern + independent-work cron + cross-bot @ | Open (PO WIP, infra in flux) |

## Key technical facts (current)

- **KPI cards resolve latest *non-null* value** (run #24 fix). `_run_latest_query` in `packages/dbr/src/dbr/semantic/semantic.py` now fetches the full annual series, drops NULL-metric rows, then takes latest N. Fixes wide-fact end-year mismatches (e.g. `fact_env_overview`: GHG/water end 2023, renewable/waste reach 2024). Global across all dashboards.
- `dbr` is **editable-installed** (`~/.local/lib/.../site-packages` → `packages/dbr/src/dbr`). Source edits go live on `systemctl restart or-<name>.service`. Env service boot takes ~20s (MetricFlow engine + dbt project load) — expect a brief 502 right after restart.
- dbr `bar` is **horizontal** (metric x, dim y); `column` for vertical bars.
- DuckDB write-locked while any `dbr serve` runs; dashboards use read-only `dashboard` profile target. Mart builds stop dashboards first (`run_daily.sh` pattern).
- COFOG 2024 in `curated.fact_finance_cofog` (PL: social 18,3 / economic 6,1 / health 6,1 / education 5,6 / gen-services 5,2 / defence 2,9; total 49,3% GDP).
- systemd `Environment=FOO=${BAR}` does NOT shell-expand from `EnvironmentFile` (root cause of OR-153 Telegram inbound).
- Untracked `infra/systemd/or-*-bot.service` (Telegram-era + test) are PO WIP — leave untouched.
- Screenshot CLI: `screenshot <dashboard> --output <path>` (`packages/screenshot`).

## Stale feature branches

`feat/OR-95-dbw-hvd-explorer`, `feat/OR-template-clustered-stacked`, `feat/or-114-sustainability-tab-enhancements`, `feat/or-118-analytics-competence-structure`, `feat/or-121-measure-reference-system`, `feat/or-122-chart-visual-config`, `feat/template-one-per-family`, `feat/telegram-claude-bridge` (PR #62). `fix/or-83-kpi-latest-nonnull` merged → deletable.
