# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-05-31 02:00 UTC -->

## Current Focus

**16 domain dashboards live. All 18 blog articles PUBLISHED. Article bottleneck CLEARED.**
Run #30 (2026-05-31 02:00 UTC): QUIET RUN. Verified all 16 dashboards + www = 200, inbox empty, git clean of own work. Did NOT build — VPS tool I/O channel degraded for the 2nd consecutive run (#29 + #30): tool results buffer/return empty, flush in delayed batches; some reads never flushed in-window. Driving a multi-step deploy (dbt run / dbr run / curl verify) through an unobservable channel risks a half-applied production change, so held off. Escalated the recurring I/O issue to PO. Article release queue is fully published, so Step 2b had nothing to publish (pipeline not spawned — save shared rate pool).

## Live production state

- **16 Eurostat domain dashboards — all Live ✓ (HTTP 200 verified run #30):**
  public_finance, labour_market, national_accounts, demographics, environment,
  living_conditions (8062), prices (8063), education (8064), transport (8065),
  science (8066), trade (8067), production (8068), health (8069), energy (8070),
  tourism (8071), financial_markets (8072).
- **Portal homepage:** `/` — Live ✓ (per OR-155, one card per live domain; may need refresh as count grows).
- **Blog:** `www.open-reporting.dev` — Live ✓; **all 18 articles PUBLISHED** (commit `6d7b89f4`).
- **Daily ingestion:** 22:00 UTC cron. Services all serving 200 (ingest exit code not definitively read run #30 due to channel, but no breakage).
- **Autonomous-lead cron:** `0 2,7,12,17 * * *` UTC.
- **Next free dashboard port:** 8073.

## Open / blocked work (all standing blockers PO-side)

| Linear | What | Status |
|---|---|---|
| OR-153 | Telegram inbound (systemd `${}` non-expansion) | Blocked — PO; outbox works |
| OR-90 | Instagram token (Meta portal) — blocks OR-89 publish | Blocked — PO action |
| OR-86 | BDL/GUS ingestion | Backlog — needs `BDL_API_KEY` from PO |
| OR-79 | Ghost nav "Portal" link — browser admin | Blocked — PO action |
| OR-89 | Weekly snapshot — code ready; publish blocked on OR-90 | Buildable remainder: cron entry |
| Phase 3 | Data depth: BDL, Finance v2, dbt tests, freshness indicators | Next focus |

**Article queue: CLEARED.** No drafts pending — all 18 live.

## Known infra issue (ACTIVE)

**Degraded autonomous tool I/O — 2 runs running (#29, #30).** `claude -p` subprocess tool results buffer/return empty on immediate response, flushing in delayed batches; some reads never flush in-window. Forces quiet runs because deploy output is unobservable. PO flagged via outbox. Check VPS harness pipe buffering / claude-code version before relying on next build run.

## Recent commits

| Commit | What |
|---|---|
| `6d7b89f4` | feat(content): publish all 18 articles — pipeline review complete |
| `0c45be26` | docs: session memory — release pipeline shipped, protocol change flagged |
| `cd106eb4` | feat(content): autonomous article release pipeline — 3-reviewer gate |
| `5c2b20f9` | docs: session memory — 16 dashboards live, Phase 2 complete |
| `b3e50ad5` | feat(content): financial markets article — exchange rate history PLN |

## Discord bot fleet (live)

8 bots, `infra/discord-bot/bot.py`, tokens in `.env` as `DISCORD_BOT_<NAME>_TOKEN`.
project-lead (opus), scrum-master (haiku), dashboard-dev/data-engineer/content-writer/researcher/code-reviewer (sonnet), debug (haiku).
Service files: `or-discord-<name>-bot.service`. Channels: `#general`, `#daily-standup`, `#dashboard-dev`, `#blockers`, `#linear-feed`.
**Untracked `infra/systemd/or-*-bot.service` + modified `infra/discord-bot/bot.py` + `logs/` are PO WIP — leave untouched, never commit.**

## Key technical facts (current)

- **Release pipeline:** `python3 products/blog/release_pipeline.py` — must run STANDALONE (nesting in active session hits Max rate limits). All 18 drafts now published; nothing pending.
- **Seed dimension_key must match raw** — query `raw.eurostat_observations` before adding seed rows. `dbt seed --select eurostat_series` then `dbt run --select stg_eurostat+`.
- **dbt write-lock dance:** stop affected `or-<name>.service` → dbt run → `dbr run` to restart. Boot ~20s → brief 502.
- **dbr `bar` = horizontal** (metric x, dim y); **`column` = vertical bars.** Check every vertical-bar visual before validate.
- **`dbr run` mandatory** after any dashboard YAML change: validate → run → curl live URL → confirm rendered Dash app (not portal index).
- KPI cards resolve latest *non-null* value (semantic.py fix).
- CLAUDE.md's `from dbr.semantic import query` is stale — use `semantic_query` / `_run_latest_query`.
- Portal homepage is static `infra/nginx/html/index.html`; deploy via `docker compose up -d --force-recreate nginx`.
- Line chart multi-metric: `y: { metric: [m1, m2] }` — one trace per metric.
- Monthly→annual marts: SUM 12 months; current incomplete year undercounts (KPI shows last complete year).

## Stale feature branches

`feat/OR-95-dbw-hvd-explorer`, `feat/OR-template-clustered-stacked`, `feat/or-114-sustainability-tab-enhancements`, `feat/or-118-analytics-competence-structure`, `feat/or-121-measure-reference-system`, `feat/or-122-chart-visual-config`, `feat/template-one-per-family`, `feat/telegram-claude-bridge` (PR #62).
