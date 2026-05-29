# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-05-29 02:10 UTC -->

## Current Focus

**Autonomous-lead schedule runs ON the VPS** via radek's crontab at 02/07/12/17 UTC. Each run reads state from disk + Linear + Telegram inbox/outbox; ships work end-to-end (code + deploy + verify); writes a post-mortem; posts a Telegram report.

Run #22 (02:00 UTC, 2026-05-29): **[P0 found] Telegram bots crash-looping** — stopped to silence churn, did NOT touch PO's WIP. Shipped OR-152 P1 (stale dług narrative on public_finance) + branch cleanup. Tonight's 22:00 ingest passed silently (OR-76 alert path correctly didn't fire on success).

## Collaboration model (current)

PO does **feedback + new-idea direction only**. Claude owns all VPS development, deploy, infra. Bypass-permissions is on for radek. See `~/.claude/projects/-opt-open-reporting/memory/feedback_autonomous_ops_on_vps.md`.

## Live production state

- **Public finance:** `portal.open-reporting.dev/public_finance/` — Live ✓ (dług narrative refreshed run #22)
- **Labour market:** `portal.open-reporting.dev/labour_market/` — Live ✓
- **National accounts:** `portal.open-reporting.dev/national_accounts/` — Live ✓
- **Demographics:** `portal.open-reporting.dev/demographics/` — Live ✓
- **Environment:** `portal.open-reporting.dev/environment/` — Live ✓
- **Blog:** `www.open-reporting.dev` — Live ✓
  - Articles 2–8 (OR-145..OR-151) — **In Ghost as DRAFTS**, awaiting PO preview
- **Daily ingestion:** 2026-05-28 22:00 ingest succeeded (exit=0) — `cfab32ab` + `1fd7b9dc` passed first live test. Alert path correctly silent on success.
- **Autonomous-lead cron:** `0 2,7,12,17 * * *` UTC.
- **Telegram bots:** **DOWN** — `or-claude-bot`, `or-gemini-bot`, `or-opencode-bot` all crash-loop on `KeyError: TELEGRAM_BOT_TOKEN`. Stopped run #22. systemd `Environment=` doesn't shell-expand `${VAR}` — that's the bug in new unit files. Source-tree files (bot.py + 7 `or-*-bot.service`) remain uncommitted — PO's WIP, do not touch.

## Recent commits

| Commit | What |
|---|---|
| `ca5ece47` | feat(content): OR-151 industrial output article (8th Theme 2) — PL +0.5%/+2.5% vs DE -4.6% divergence story |
| `1fd7b9dc` | feat(ingestion): OR-76 — alert PO via Telegram outbox on daily-ingest failure |
| `efd256f0` | docs: run #20 post-mortem |
| `c160a6ab` | fix(macro): OR-87 sts_inpr_a Eurostat codes corrected |
| `cfab32ab` | fix(ingestion): stop all or-* dashboards before daily ingestion |

## Open PRs

- **#62 (draft) `feat/telegram-claude-bridge`** — single-bot Claude-responder rewrite. ALSO blocked by same env-var mismatch as current multi-bot, so not a quick fallback. Leave open until PO resolves comms.

## Ghost article drafts (PO review needed — bot comms down so I can't ping)

| Slug | Article | Linear |
|---|---|---|
| `bezrobocie-polska-2024-historyczny-rekord` | OR-145 Labour / unemployment | OR-145 |
| `koszty-obslugi-dlugu-polska-2024` | OR-146 Debt service costs | OR-146 |
| `cofog-wydatki-polska-2023-gdzie-trafi-kazda-zlotowka` | OR-147 COFOG spending breakdown | OR-147 |
| `polska-na-tle-ue-deficyt-dlug-2024` | OR-148 EU fiscal comparison | OR-148 |
| `wzrost-plac-polska-2024` | OR-149 Real wage growth 2024 | OR-149 |
| `polska-demografia-przyrost-naturalny-2024` | OR-150 Demographics | OR-150 |
| `polska-produkcja-przemyslowa-2024` | OR-151 Industrial output | OR-151 |

## Open work (next slot: 07:00 UTC 2026-05-29)

| # | Linear | What | Status |
|---|---|---|---|
| 1 | — | Verify Telegram bots restored (PO action) — if still down, only the outbox file path works for status reporting | Watch |
| 2 | OR-152 | P2 — year-anchor consistency check on remaining public_finance pages (Wydatki, Dochody, UE, Prognozy) | Open |
| 3 | OR-152 | P3 — COFOG legend label overlap on Wydatki section | Open |
| 4 | OR-86 | BDL (GUS) ingestion first run | Blocked — needs `BDL_API_KEY` from PO |
| 5 | — | Theme 2 article #9 candidate (NUTS2 regional wages, or fiscal multiplier study) — but queue already at 7 unpublished drafts | Open |
| 6 | OR-89 | Weekly snapshot (social) | Buildable; publish blocked on OR-90 |

## Linear blocked on PO action

| Issue | What |
|---|---|
| — | **P0 Telegram bot env-var fix** (see run #22 post-mortem for 3 fix options) |
| OR-90 | Instagram token — Meta Developer portal (blocks Theme 4 publishing) |
| OR-79 | Ghost nav link — browser admin session |
| OR-86 | BDL_API_KEY — PO needs to register at api.stat.gov.pl |
| 7 articles | Ghost preview + publish decisions |

## Key technical facts (current)

- DuckDB write-locked while any `dbr serve` is running. `run_daily.sh` and any new mart build must stop all `or-*` dashboards (except telegram bots) — dynamic discovery via `systemctl list-unit-files`.
- `run_daily.sh` non-zero exit → outbox alert. Bot polls `data/telegram-outbox/*.md` every 30s (only `BOT_ROLE=claude` runs the poller). Tested in `/tmp` isolation 2026-05-28 17:02 UTC. Passed silent test 2026-05-28 22:07 UTC.
- **NEW gotcha:** systemd `Environment=FOO=${BAR}` does NOT shell-expand from `EnvironmentFile`. Use literal values, a wrapper script with shell expansion, or change the consumer to read the source-of-truth var name directly.
- dbr `bar` is **horizontal** (metric on x, dim on y). Use `column` for vertical bars.
- Seed dimension_keys are alphabetically sorted and must match Eurostat API exactly.
- OR-152 fix: public_finance Przegląd KPIs anchor on **2025**; all narrative blocks should match.

## Stale feature branches

`feat/OR-95-dbw-hvd-explorer`, `feat/OR-template-clustered-stacked`, `feat/or-114-sustainability-tab-enhancements`, `feat/or-118-analytics-competence-structure`, `feat/or-121-measure-reference-system`, `feat/or-122-chart-visual-config`, `feat/template-one-per-family`, `feat/telegram-claude-bridge` (PR #62 blocked by same env-var issue)
