# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-05-28 17:10 UTC -->

## Current Focus

**Autonomous-lead schedule runs ON the VPS** via radek's crontab at 02/07/12/17 UTC. Each run reads state from disk + Linear + Telegram inbox/outbox; ships work end-to-end (code + deploy + verify); writes a post-mortem; posts a Telegram report.

Run #21 (17:00 UTC): shipped OR-76 ingestion-failure alerting + OR-151 industrial output article (8th in Theme 2 cohort).

## Collaboration model (current)

PO does **feedback + new-idea direction only**. Claude owns all VPS development, deploy, infra. Bypass-permissions is on for radek. See `~/.claude/projects/-opt-open-reporting/memory/feedback_autonomous_ops_on_vps.md`.

## Live production state

- **Public finance:** `portal.open-reporting.dev/public_finance/` — Live ✓
- **Labour market:** `portal.open-reporting.dev/labour_market/` — Live ✓
- **National accounts:** `portal.open-reporting.dev/national_accounts/` — Live ✓
- **Demographics:** `portal.open-reporting.dev/demographics/` — Live ✓
- **Environment:** `portal.open-reporting.dev/environment/` — Live ✓
- **Blog:** `www.open-reporting.dev` — Live ✓
  - Article 1 (SGP/Maastricht) — Published ✓
  - Articles 2–8 (OR-145..OR-151) — **In Ghost as DRAFTS**, awaiting PO preview
- **Daily ingestion:** cron `0 22 * * *` UTC. 2026-05-27 failed [DB lock]; hardened `cfab32ab`. **NEW:** any non-zero exit now writes alert to `data/telegram-outbox/<UTC>-ingest-FAIL.md` (commit `1fd7b9dc`, OR-76). Tonight is first live test of both.
- **Autonomous-lead cron:** `0 2,7,12,17 * * *` UTC → `infra/scheduler/autonomous-lead.sh`
- **Telegram bots:** new multi-bot architecture running live (`or-claude-bot`, `or-gemini-bot`, `or-opencode-bot` services active). Source-tree files (bot.py rewrite + 7 new `or-*-bot.service`) uncommitted — PO's in-progress work, do not touch.

## Recent commits

| Commit | What |
|---|---|
| `ca5ece47` | feat(content): OR-151 industrial output article (8th Theme 2) — PL +0.5%/+2.5% vs DE -4.6% divergence story |
| `1fd7b9dc` | feat(ingestion): OR-76 — alert PO via Telegram outbox on daily-ingest failure |
| `efd256f0` | docs: run #20 post-mortem |
| `c160a6ab` | fix(macro): OR-87 sts_inpr_a Eurostat codes corrected (PRD/PCH_SM not PROD/PCH_PRE) |
| `cfab32ab` | fix(ingestion): stop all or-* dashboards before daily ingestion |
| `c3125c9b` | feat(comms): Project Lead role + Telegram bot bridge to PO |

## Open PRs

- **#62 (draft) `feat/telegram-claude-bridge`** — earlier single-bot attempt to add Claude as parallel chat responder. **Likely superseded** by PO's new multi-bot architecture. Re-evaluate next run.

## Ghost article drafts (PO review needed)

| Slug | Article | Linear |
|---|---|---|
| `bezrobocie-polska-2024-historyczny-rekord` | OR-145 Labour / unemployment | OR-145 |
| `koszty-obslugi-dlugu-polska-2024` | OR-146 Debt service costs | OR-146 |
| `cofog-wydatki-polska-2023-gdzie-trafi-kazda-zlotowka` | OR-147 COFOG spending breakdown | OR-147 |
| `polska-na-tle-ue-deficyt-dlug-2024` | OR-148 EU fiscal comparison | OR-148 |
| `wzrost-plac-polska-2024` | OR-149 Real wage growth 2024 | OR-149 |
| `polska-demografia-przyrost-naturalny-2024` | OR-150 Demographics | OR-150 |
| `polska-produkcja-przemyslowa-2024` | OR-151 Industrial output (NEW) | OR-151 |

PO previews in Ghost admin (`www.open-reporting.dev/ghost/`). Tell Claude which to publish.

## Open work (next autonomous slot: 02:00 UTC 2026-05-29)

| # | Linear | What | Status |
|---|---|---|---|
| 1 | — | **Verify tonight's 22:00 UTC ingestion succeeds AND alert path is intact** (first live test of `cfab32ab` + `1fd7b9dc`) | Watch |
| 2 | OR-151 | Pre-publish multi-agent review (content + analytical + domain Opus) when PO previews | Open |
| 3 | OR-86 | BDL (GUS) ingestion first run | Blocked — needs `BDL_API_KEY` from PO |
| 4 | OR-89 | Weekly snapshot (social) | Buildable; publish blocked on OR-90 |
| 5 | — | Theme 2 article #9 candidate (NUTS2 regional wages, or fiscal multiplier study) | Open |

## Linear blocked on PO action

| Issue | What |
|---|---|
| OR-90 | Instagram token — Meta Developer portal (blocks Theme 4 publishing) |
| OR-79 | Ghost nav link — browser admin session |
| OR-86 | BDL_API_KEY — PO needs to register at api.stat.gov.pl |
| #62 | Decide whether to close (likely superseded by new multi-bot architecture) |

## Key technical facts (current)

- DuckDB write-locked while any `dbr serve` is running. `run_daily.sh` and any new mart build must stop all `or-*` dashboards (except telegram bots) — dynamic discovery via `systemctl list-unit-files`.
- **NEW:** `run_daily.sh` non-zero exit → outbox alert. Bot polls `data/telegram-outbox/*.md` every 30s (only `BOT_ROLE=claude` runs the poller). Tested 2026-05-28 17:02 UTC in `/tmp` isolation.
- dbr `bar` is **horizontal** (metric on x, dim on y). Use `column` for vertical bars.
- Seed dimension_keys are alphabetically sorted and must match Eurostat API exactly. Always probe API directly before adding seed rows (OR-87 burned two attempts on PROD vs PRD, PCH_PRE vs PCH_SM).
- OR-151 article: PL industrial output 2024 +0.5%, 2025 +2.5%; DE 2024 -4.6%; PL long-term avg 2001-2019 +5.1%. All Eurostat sts_inpr_a verified.

## Stale feature branches

`feat/OR-95-dbw-hvd-explorer`, `feat/OR-template-clustered-stacked`, `feat/or-114-sustainability-tab-enhancements`, `feat/or-118-analytics-competence-structure`, `feat/or-121-measure-reference-system`, `feat/or-122-chart-visual-config`, `feat/template-one-per-family`, `feat/telegram-claude-bridge` (PR #62 likely superseded)
