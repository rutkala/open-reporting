# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-05-28 08:45 UTC -->

## Current Focus

**Autonomous-lead schedule moved from cloud to VPS.** The cloud RemoteTrigger is disabled — it could only ship YAML/SQL but couldn't deploy, so dashboards and articles piled up unactivated. New schedule runs ON the VPS via radek's crontab, where the agent has full access to `dbt`, `dbr`, `systemctl`, `docker`, and the live URLs. Same 02/07/12/17 UTC cadence, same prompt structure (adapted), but every run can now ship complete end-to-end work.

Recovery just completed: OR-52, OR-55, OR-83 dashboards deployed; all 6 article drafts pushed to Ghost (drafts, awaiting PO review). Two new bar→column bug fixes shipped (OR-52, OR-55 — same pattern bit three dashboards).

## Collaboration model (current)

PO does **feedback + new-idea direction only**. Claude owns all VPS development, deploy, infra, commands. Bypass-permissions is on for radek. See `~/.claude/projects/-opt-open-reporting/memory/feedback_autonomous_ops_on_vps.md`.

## Live production state

- **Public finance:** `portal.open-reporting.dev/public_finance/` — Live ✓
- **Labour market:** `portal.open-reporting.dev/labour_market/` — Live ✓
- **National accounts:** `portal.open-reporting.dev/national_accounts/` — Live ✓ (deployed 2026-05-28 by PO session)
- **Demographics:** `portal.open-reporting.dev/demographics/` — Live ✓ (deployed 2026-05-28 by PO session)
- **Environment:** `portal.open-reporting.dev/environment/` — Live ✓ (deployed 2026-05-28 by PO session)
- **Blog:** `www.open-reporting.dev` — Live ✓
  - Article 1 (SGP/Maastricht) — Published ✓
  - Articles 2–7 (OR-145..OR-150) — **In Ghost as DRAFTS**, awaiting PO preview + publish approval
- **Daily ingestion:** cron `0 22 * * *` UTC, last run exit=0
- **Autonomous-lead cron:** `0 2,7,12,17 * * *` UTC → `infra/scheduler/autonomous-lead.sh`

## Recent commits

| Commit | What |
|---|---|
| `d1f2a4d` | feat(scheduler): VPS autonomous-lead launcher + prompt |
| `83524bd` | fix(demo): bar→column for OR-55 natural-increase visual |
| `0823cbe` | fix(macro): bar→column for OR-52 vertical-bar visuals |
| `24612f5` | docs: cloud-run #19 post-mortem |
| `5368422` | feat(content): OR-150 demographics article draft |
| `4e35a28` | feat(data): OR-86 BDL ingestion module |
| `c4d210e` | feat(content): OR-149 wages article draft |
| `796e0eb` | feat(dashboard): OR-83 ENV dashboard YAML + infra |
| `8f4328d` | feat(data): OR-83 ENV mart + semantic layer |
| `6fda803` | feat(content): OR-148 EU fiscal article draft |
| `b0598ab` | feat(demo): OR-55 dashboard mart + YAML |
| `ad1e34a` | feat(macro): OR-52 dashboard mart + YAML |

## Ghost article drafts (PO review needed)

| Slug | Article | Linear |
|---|---|---|
| `bezrobocie-polska-2024-historyczny-rekord` | OR-145 Labour market / unemployment | OR-145 |
| `koszty-obslugi-dlugu-polska-2024` | OR-146 Debt service costs | OR-146 |
| `cofog-wydatki-polska-2023-gdzie-trafi-kazda-zlotowka` | OR-147 COFOG spending breakdown | OR-147 |
| `polska-na-tle-ue-deficyt-dlug-2024` | OR-148 EU fiscal comparison | OR-148 |
| `wzrost-plac-polska-2024` | OR-149 Real wage growth 2024 | OR-149 |
| `polska-demografia-przyrost-naturalny-2024` | OR-150 Demographics | OR-150 |

PO reviews in Ghost admin (`www.open-reporting.dev/ghost/`). Tell Claude which to publish; flip via `publish_to_ghost.py --publish`.

## Open work (next autonomous slot: 12:00 UTC)

| # | Linear | What | Status |
|---|---|---|---|
| 1 | OR-87 | `sts_inpr_a` indic_bt=PROD fix | Code shipped; `sts_inpr_a` not in raw — needs `loader.py` + ingestion backfill + `dbt run` to activate |
| 2 | OR-86 | BDL (GUS) ingestion | Code shipped; needs `BDL_API_KEY` (PO must register at api.stat.gov.pl/Home/BdlApi) |
| 3 | — | Theme 2 article #8 | Macro/national_accounts pair article — next content slot |
| 4 | OR-76 | Pipeline robustness | Retries, alerting |
| 5 | OR-89 | Weekly snapshot (social) | Buildable; publish blocked on OR-90 |

## Linear blocked on PO action

| Issue | What |
|---|---|
| OR-90 | Instagram token — Meta Developer portal (blocks all of Theme 4 publishing) |
| OR-79 | Ghost nav link — browser admin session |
| OR-86 | BDL_API_KEY — needs PO registration at api.stat.gov.pl |

## Architecture

**Schedule:** cron at `0 2,7,12,17 * * *` UTC fires `/opt/open-reporting/infra/scheduler/autonomous-lead.sh`, which pipes `infra/scheduler/lead-protocol-prompt.md` into `claude -p --model opus` with a 75-min timeout. Logs to `data/logs/autonomous-lead-YYYY-MM-DD-HH.log`.

**Auth:** Claude CLI uses `~/.claude/.credentials.json` (OAuth, auto-refreshes). Permission bypass on globally via `~/.claude/settings.json` (`defaultMode: bypassPermissions`).

**Sudo NOPASSWD allowlist for radek:**
- `systemctl restart|start|stop|status|enable or-*`
- `systemctl daemon-reload`
- `cp /opt/open-reporting/infra/systemd/*.service /etc/systemd/system/`

**Port assignments:** public_finance=8057, labour_market=8058, national_accounts=8059, demographics=8060, environment=8061. Next: 8062.

## Cloud trigger

`trig_01TqBcSxS3SzQn7BtSTiDmif` — DISABLED (last fired 2026-05-28 07:01 UTC, never pushed because its run errored/ran out of time). Config preserved as record. Direct delete not available via the in-session API; PO can delete via claude.ai web UI if desired (functionally a no-op now).

## Key technical facts (current)

- DuckDB write-locked while any `dbr serve` is running. To run dbt: `sudo systemctl stop or-<name>.service`, run dbt, `sudo systemctl start`.
- dbr `bar` is **horizontal** (metric on x, dim on y). Use `column` for vertical bars (categorical x, metric y). Has bitten OR-52 macro, OR-55 demographics; verify every vertical-bar visual before `dbr run`.
- Seed dimension_keys are canonically sorted alphabetically and must match `raw.eurostat_observations.dimension_key` exactly — query before guessing.
- OR-150 article: TFR 2023 = 1.16, natural increase = −3.7/1000 (verified).
- OR-148 article: Poland 2024 deficit = 6.5% GDP (Eurostat EDP April 2026).
- OR-87 fix: `sts_inpr_a` needs ingestion backfill — raw table has zero rows for it currently.

## Stale feature branches (pre-autonomous; do not merge/delete without PO)

`feat/OR-95-dbw-hvd-explorer`, `feat/OR-template-clustered-stacked`, `feat/or-114-sustainability-tab-enhancements`, `feat/or-118-analytics-competence-structure`, `feat/or-121-measure-reference-system`, `feat/or-122-chart-visual-config`, `feat/template-one-per-family`
