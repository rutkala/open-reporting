# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-05-28 12:20 UTC -->

## Current Focus

**Autonomous-lead schedule runs ON the VPS** via radek's crontab at 02/07/12/17 UTC. Each run reads state from disk + Linear + Telegram inbox/outbox; ships work end-to-end (code + deploy + verify); writes a post-mortem; posts a Telegram report.

Run #20 (12:00 UTC) recovered a [P0] failed ingestion + closed OR-87 (industrial output data fix activated for real).

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
  - Articles 2–7 (OR-145..OR-150) — **In Ghost as DRAFTS**, awaiting PO preview
- **Daily ingestion:** cron `0 22 * * *` UTC. Yesterday (2026-05-27) failed [DB lock]; hardened today — script now stops all 5 dashboards dynamically before ingestion (`cfab32ab`)
- **Autonomous-lead cron:** `0 2,7,12,17 * * *` UTC → `infra/scheduler/autonomous-lead.sh`

## Recent commits

| Commit | What |
|---|---|
| `c160a6ab` | fix(macro): OR-87 sts_inpr_a Eurostat codes corrected (PRD/PCH_SM not PROD/PCH_PRE) — industrial output growth now flowing |
| `cfab32ab` | fix(ingestion): stop all or-* dashboards before daily ingestion (was only stopping public_finance) |
| `c3125c9b` | feat(comms): Project Lead role + Telegram bot bridge to PO |
| `c6bd2f1c` | docs(session-memory): rewrite for VPS-side autonomous-lead architecture |
| `d1f2a4d4` | feat(scheduler): VPS autonomous-lead launcher + prompt |
| `83524bd6` | fix(demo): bar→column for OR-55 natural-increase visual |
| `0823cbe8` | fix(macro): bar→column for OR-52 vertical-bar visuals |
| `24612f51` | docs: cloud-run #19 post-mortem |
| `5368422` | feat(content): OR-150 demographics article draft |
| `4e35a28c` | feat(data): OR-86 BDL ingestion module |

## Open PRs

- **#62 (draft) `feat/telegram-claude-bridge`** — adds Claude as a parallel chat responder alongside Gemini. Cost-bearing (one `claude -p` subprocess per chat message). Was sitting uncommitted in working tree from a previous session; moved to branch + draft PR for PO review.

## Ghost article drafts (PO review needed)

| Slug | Article | Linear |
|---|---|---|
| `bezrobocie-polska-2024-historyczny-rekord` | OR-145 Labour market / unemployment | OR-145 |
| `koszty-obslugi-dlugu-polska-2024` | OR-146 Debt service costs | OR-146 |
| `cofog-wydatki-polska-2023-gdzie-trafi-kazda-zlotowka` | OR-147 COFOG spending breakdown | OR-147 |
| `polska-na-tle-ue-deficyt-dlug-2024` | OR-148 EU fiscal comparison | OR-148 |
| `wzrost-plac-polska-2024` | OR-149 Real wage growth 2024 | OR-149 |
| `polska-demografia-przyrost-naturalny-2024` | OR-150 Demographics | OR-150 |

PO previews in Ghost admin (`www.open-reporting.dev/ghost/`). Tell Claude which to publish; flip via `publish_to_ghost.py --publish`.

## Open work (next autonomous slot: 17:00 UTC)

| # | Linear | What | Status |
|---|---|---|---|
| 1 | OR-76 | Pipeline robustness — alerting on ingestion failure (was yesterday's silent fail) | Now top priority |
| 2 | — | Theme 2 article #8 — Macro/national_accounts pair (industrial output story?) | Open |
| 3 | OR-86 | BDL (GUS) ingestion first run | Blocked — needs `BDL_API_KEY` from PO |
| 4 | OR-89 | Weekly snapshot (social) | Buildable; publish blocked on OR-90 |

## Linear blocked on PO action

| Issue | What |
|---|---|
| OR-90 | Instagram token — Meta Developer portal (blocks all of Theme 4 publishing) |
| OR-79 | Ghost nav link — browser admin session |
| OR-86 | BDL_API_KEY — needs PO registration at api.stat.gov.pl |
| #62 | Decide whether to merge parallel-Claude Telegram bot bridge |

## Key technical facts (current)

- DuckDB write-locked while any `dbr serve` is running. `run_daily.sh` and any new mart build must stop all 5 `or-*` dashboards (except `or-telegram-bot`) — dynamic discovery via `systemctl list-unit-files`.
- dbr `bar` is **horizontal** (metric on x, dim on y). Use `column` for vertical bars. Has bitten OR-52, OR-55; verify before `dbr run`.
- Seed dimension_keys are alphabetically sorted and must match the Eurostat API exactly. **Always probe the API directly (`curl …/data/{dataset_code}?format=JSON`) before adding seed rows** — the dimension codes you assume are often wrong (OR-87 lost two fix attempts to PROD vs PRD, PCH_PRE vs PCH_SM).
- OR-150 article: TFR 2023 = 1.16, natural increase = −3.7/1000 (verified).
- OR-148 article: Poland 2024 deficit = 6.5% GDP (Eurostat EDP April 2026).

## Stale feature branches

`feat/OR-95-dbw-hvd-explorer`, `feat/OR-template-clustered-stacked`, `feat/or-114-sustainability-tab-enhancements`, `feat/or-118-analytics-competence-structure`, `feat/or-121-measure-reference-system`, `feat/or-122-chart-visual-config`, `feat/template-one-per-family`
