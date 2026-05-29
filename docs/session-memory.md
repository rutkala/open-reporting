# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-05-29 09:50 UTC -->

## Current Focus

**The AI scrum team is now live on Discord.** Eight bots running on this VPS as `claude -p` subprocesses, each acting as a named team member in the `Open Reporting` Discord server. PO (Radek) talks to them by `@`-mention or DM. The Project Lead (`@OR Project Lead`, opus) is the show-runner and is meant to seamlessly continue the work from the Claude Code interactive session that built the fleet.

Autonomous-lead cron still runs 02/07/12/17 UTC — but the **chat office is Discord now**, not Telegram.

## Discord bot fleet (live)

| Bot | Model | Service file | Agent file |
|---|---|---|---|
| `@OR Project Lead` | opus | `or-discord-project-lead-bot.service` | `.claude/agents/project-lead.md` |
| `@OR Scrum Master` | haiku | `or-discord-scrum-master-bot.service` | `.claude/agents/scrum-master.md` |
| `@OR Dashboard Dev` | sonnet | `or-discord-dashboard-dev-bot.service` | `.claude/agents/dashboard-dev.md` |
| `@OR Data Engineer` | sonnet | `or-discord-data-engineer-bot.service` | `.claude/agents/data-engineer.md` |
| `@OR Content Writer` | sonnet | `or-discord-content-writer-bot.service` | `.claude/agents/content-writer.md` |
| `@OR Researcher` | sonnet | `or-discord-researcher-bot.service` | `.claude/agents/researcher.md` |
| `@OR Code Reviewer` | sonnet | `or-discord-code-reviewer-bot.service` | `.claude/agents/code-reviewer.md` |
| `@OR Debug` | haiku | `or-discord-debug-bot.service` | `.claude/agents/debug.md` |

Source: `infra/discord-bot/bot.py`. Tokens in `.env` as `DISCORD_BOT_<NAME>_TOKEN`. Full team roster + interaction rules also in `CLAUDE.md` (auto-loaded by every bot subprocess).

Discord channels: `#general`, `#daily-standup`, `#dashboard-dev`, `#blockers`, `#linear-feed` (Linear app not wired yet).

## Collaboration model (current)

PO does **feedback + direction only**. Claude (in any of: this interactive session, the autonomous-lead cron, or any of the 8 Discord bots) owns all VPS development, deploy, and infra. Bypass-permissions is on for radek. See `~/.claude/projects/-opt-open-reporting/memory/feedback_autonomous_ops_on_vps.md` and `feedback_agent_bot_model_tiering.md`.

## What just happened (handoff context for Project Lead)

This session's work (2026-05-29 07–10 UTC, in interactive Claude Code chat with PO):

1. **Telegram comms (OR-153)** — root cause diagnosed: systemd `Environment=FOO=${BAR}` doesn't shell-expand from `EnvironmentFile`. Refactored `infra/telegram-bot/bot.py` to derive `TELEGRAM_BOT_TOKEN` from `BOT_NAME` (clean `BOT_NAME` / `OTHER_BOT_NAMES` pattern). Three Telegram bots restored: `@open_reporting_claude_bot` (opus), `@open_reporting_gemini_bot`, `@open_reporting_opencode_bot`. **Telegram outbox poller is alive again** — autonomous-cron run reports can deliver.
2. **PO pivoted comms to Discord.** Rationale: Telegram's single-stream group can't support a real scrum team — needed channels, threads, native bot-to-bot. Discord chosen.
3. **Discord 8-bot fleet built**: framework (`infra/discord-bot/bot.py`), 8 service files, `.claude/agents/project-lead.md` created from charter, tokens registered by PO, all 8 services Active. PO created the server + 4 working channels.
4. **Model tiering** corrected (saved to memory): opus = project-lead only; sonnet for builders/reviewers; haiku for scrum-master/debug.
5. **Next agreed steps** (not yet implemented):
   - Goal-file pattern: `data/agent-goals/<name>.md` per bot, loaded into system prompt at invocation time. PO sets via DM command or direct file edit.
   - Independent-work cron: each bot wakes periodically (e.g. every 6h) to make progress on its goal and post to its channel.
   - Cross-bot `@`-mention with depth cap (currently other-bot messages dropped).

## Live production state

- **Public finance:** `portal.open-reporting.dev/public_finance/` — Live ✓
- **Labour market:** `portal.open-reporting.dev/labour_market/` — Live ✓
- **National accounts:** `portal.open-reporting.dev/national_accounts/` — Live ✓
- **Demographics:** `portal.open-reporting.dev/demographics/` — Live ✓
- **Environment:** `portal.open-reporting.dev/environment/` — Live ✓
- **Blog:** `www.open-reporting.dev` — Live ✓; Articles OR-145..OR-151 in Ghost as **DRAFTS**, awaiting PO preview
- **Daily ingestion:** 22:00 UTC cron; OR-76 outbox alert on failure (Telegram path is the alert channel).
- **Autonomous-lead cron:** `0 2,7,12,17 * * *` UTC.

## Recent commits

| Commit | What |
|---|---|
| `e89360d2` | fix(public_finance): OR-152 P2/P3 — Wydatki 2024 re-anchor + trend legend overlap |
| `8bdb235a` | docs: run #22 post-mortem + OR-152 P1 |
| `ca5ece47` | feat(content): OR-151 industrial output article (8th Theme 2) |
| `1fd7b9dc` | feat(ingestion): OR-76 — alert PO via Telegram outbox on daily-ingest failure |

Uncommitted in working tree (this session's work): `infra/discord-bot/bot.py`, `infra/telegram-bot/bot.py` (refactor), 9 new `infra/systemd/or-*-bot.service` files, `.claude/agents/project-lead.md`, `.claude/agents/scrum-master.md`, `CLAUDE.md` + `docs/session-memory.md` updates.

## Open work

| # | Linear | What | Status |
|---|---|---|---|
| 1 | — | Goal-file pattern + independent-work cron + cross-bot @ (next planned step) | Open |
| 2 | — | Commit + push this session's work (Discord scaffold + Telegram fix) | Open |
| 3 | OR-86 | BDL (GUS) ingestion first run | Blocked — needs `BDL_API_KEY` from PO |
| 4 | OR-90 | Instagram token (Meta portal) — blocks Theme 4 publishing | Blocked — PO action |
| 5 | OR-79 | Ghost nav link — browser admin | Blocked — PO action |
| 6 | 7 drafts | Ghost preview + publish decisions | Awaiting PO via Discord |
| 7 | OR-89 | Weekly snapshot (social) | Buildable; publish blocked on OR-90 |

## Key technical facts (current)

- COFOG 2024 in `curated.fact_finance_cofog` (PL: social 18,3 / economic 6,1 / health 6,1 / education 5,6 / gen-services 5,2 / defence 2,9; total 49,3% GDP).
- DuckDB write-locked while any `dbr serve` runs. Mart builds stop dashboards first (`run_daily.sh` pattern).
- dbr `bar` is **horizontal** (metric x, dim y); `column` for vertical bars.
- dbr line charts: `label_endpoints: true` has no collision avoidance; for converging series use legend.
- systemd `Environment=FOO=${BAR}` does NOT expand from `EnvironmentFile`. The Discord bots avoid this by deriving tokens from `BOT_NAME` in `bot.py`.
- Each Discord bot subprocess auto-loads `CLAUDE.md` + persistent memory + this `session-memory.md` — that's how fresh subprocesses stay context-aware. There is NO in-chat memory across messages by default (would need channel-history fetch enhancement).

## Stale feature branches

`feat/OR-95-dbw-hvd-explorer`, `feat/OR-template-clustered-stacked`, `feat/or-114-sustainability-tab-enhancements`, `feat/or-118-analytics-competence-structure`, `feat/or-121-measure-reference-system`, `feat/or-122-chart-visual-config`, `feat/template-one-per-family`, `feat/telegram-claude-bridge` (PR #62 — may be obsolete now that bot.py is refactored).
