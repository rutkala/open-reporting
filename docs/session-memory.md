# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-05-29 07:15 UTC -->

## Current Focus

**Autonomous-lead schedule runs ON the VPS** via radek's crontab at 02/07/12/17 UTC. Each run reads state from disk + Linear + Telegram inbox/outbox; ships work end-to-end (code + deploy + verify); writes a post-mortem; posts a Telegram report.

Run #23 (07:00 UTC, 2026-05-29): Closed **OR-152 P2/P3** — re-anchored public_finance Wydatki to 2024 COFOG (newly arrived in warehouse) + fixed the COFOG trend legend overlap. Escalated the still-unresolved Telegram comms outage to **OR-153** (Urgent/Infra) — the one PO-reachable channel, since outbox alerts can't be delivered while the bot is down.

## Collaboration model (current)

PO does **feedback + new-idea direction only**. Claude owns all VPS development, deploy, infra. Bypass-permissions is on for radek. See `~/.claude/projects/-opt-open-reporting/memory/feedback_autonomous_ops_on_vps.md`.

## Live production state

- **Public finance:** `portal.open-reporting.dev/public_finance/` — Live ✓ (Wydatki on 2024 COFOG; trend legend fixed, run #23)
- **Labour market:** `portal.open-reporting.dev/labour_market/` — Live ✓
- **National accounts:** `portal.open-reporting.dev/national_accounts/` — Live ✓
- **Demographics:** `portal.open-reporting.dev/demographics/` — Live ✓
- **Environment:** `portal.open-reporting.dev/environment/` — Live ✓
- **Blog:** `www.open-reporting.dev` — Live ✓
  - Articles 2–8 (OR-145..OR-151) — **In Ghost as DRAFTS**, awaiting PO preview
- **Daily ingestion:** 2026-05-28 12:00 + 22:00 both exit=0. Alert path silent on success (correct).
- **Autonomous-lead cron:** `0 2,7,12,17 * * *` UTC.
- **Telegram bots:** **DOWN** — all 7 `or-*-bot` services inactive. Root cause = systemd `Environment=TELEGRAM_BOT_TOKEN=${TELEGRAM_CLAUDE_BOT_TOKEN}` does not shell-expand. Tracked as **OR-153** (Urgent). Source-tree files (bot.py + 7 `or-*-bot.service`) remain uncommitted PO WIP — do not touch.

## Comms deadlock (important)

Outbox→PO delivery is dead (the claude bot is the poller). So outbox reports + OR-76 ingest alerts cannot reach PO while bots are down. **Linear is the only working PO channel** — use it for anything PO must see (this is why OR-153 exists, not just a decisions.md note). Run #22's mistake was flagging the P0 only in the outbox/decisions.md.

## Recent commits

| Commit | What |
|---|---|
| `e89360d2` | fix(public_finance): OR-152 P2/P3 — Wydatki 2024 re-anchor + trend legend overlap |
| `8bdb235a` | docs: run #22 post-mortem + OR-152 P1 dług narrative fix |
| `7e6c2058` | docs: run #21 post-mortem |
| `ca5ece47` | feat(content): OR-151 industrial output article (8th Theme 2) |
| `1fd7b9dc` | feat(ingestion): OR-76 — alert PO via Telegram outbox on daily-ingest failure |

## Open PRs

- **#62 (draft) `feat/telegram-claude-bridge`** — single-bot Claude-responder rewrite. ALSO blocked by the same env-var mismatch. Leave open until PO resolves comms (see OR-153).

## Ghost article drafts (PO preview needed — comms down, can't ping)

`bezrobocie-polska-2024-historyczny-rekord` (OR-145), `koszty-obslugi-dlugu-polska-2024` (OR-146), `cofog-wydatki-polska-2023-gdzie-trafi-kazda-zlotowka` (OR-147), `polska-na-tle-ue-deficyt-dlug-2024` (OR-148), `wzrost-plac-polska-2024` (OR-149), `polska-demografia-przyrost-naturalny-2024` (OR-150), `polska-produkcja-przemyslowa-2024` (OR-151).

## Open work (next slot: 12:00 UTC 2026-05-29)

| # | Linear | What | Status |
|---|---|---|---|
| 1 | OR-153 | Telegram comms fix (3 options in issue) | Blocked — PO action |
| 2 | OR-86 | BDL (GUS) ingestion first run | Blocked — needs `BDL_API_KEY` from PO |
| 3 | OR-90 | Instagram token (Meta portal) — blocks Theme 4 publishing | Blocked — PO action |
| 4 | OR-79 | Ghost nav link — browser admin | Blocked — PO action |
| 5 | 7 drafts | Ghost preview + publish decisions | Blocked — PO + comms |
| 6 | OR-89 | Weekly snapshot (social) | Buildable; publish blocked on OR-90 |
| 7 | — | Next visual-screenshot-review target (labour_market or demographics) for a QUIET RUN | Open |

## Key technical facts (current)

- COFOG 2024 now in `curated.fact_finance_cofog` (PL: social 18,3 / economic 6,1 / health 6,1 / education 5,6 / gen-services 5,2 / defence 2,9; total 49,3% GDP).
- DuckDB write-locked while any `dbr serve` runs; read-only connections are fine for verification queries. Mart builds must stop all `or-*` dashboards first (run_daily.sh pattern, dynamic discovery).
- dbr `bar` is **horizontal** (metric x, dim y); use `column` for vertical bars.
- dbr line charts: `label_endpoints: true` has NO collision avoidance — converging series get overlapping labels. For >2 series that converge, prefer a legend (drop `label_endpoints` + `highlight`). Engine label-nudging would be a `packages/dbr/` PR.
- systemd `Environment=FOO=${BAR}` does NOT expand; `${BAR}` DOES expand in `ExecStart=`. Shell-wrapper ExecStart is the clean fix.
- Seed dimension_keys are alphabetically sorted, must match Eurostat API exactly.

## Stale feature branches

`feat/OR-95-dbw-hvd-explorer`, `feat/OR-template-clustered-stacked`, `feat/or-114-sustainability-tab-enhancements`, `feat/or-118-analytics-competence-structure`, `feat/or-121-measure-reference-system`, `feat/or-122-chart-visual-config`, `feat/template-one-per-family`, `feat/telegram-claude-bridge` (PR #62).
