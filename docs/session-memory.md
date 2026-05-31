# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-05-31 (run #31) UTC -->

## Current Focus

**16 domain dashboards live. All 18 blog articles PUBLISHED. Article bottleneck CLEARED.**

**ACTIVE: high-latency VPS tool I/O channel — 3 runs running (#29, #30, #31).**
Run #31: QUIET RUN, production VERIFIED healthy. The channel is NOT dead — it flushes in sporadic delayed batches (~6 calls latency). Smoke check eventually came through: public_finance, labour_market, national_accounts, demographics, environment, www all HTTP 200; git clean of own work. Build held off anyway: sporadic flush latency makes a multi-step deploy (dbt write-lock dance, service stop/start) unsafe to drive — cannot observe step N before issuing N+1. Article queue cleared (Step 2b nothing to publish); remaining roadmap PO-blocked. PO latency escalation stands.

## Live production state (last VERIFIED run #28; not re-verifiable #29–#31 due to channel)

- **16 Eurostat domain dashboards — all Live as of run #28:**
  public_finance, labour_market, national_accounts, demographics, environment,
  living_conditions (8062), prices (8063), education (8064), transport (8065),
  science (8066), trade (8067), production (8068), health (8069), energy (8070),
  tourism (8071), financial_markets (8072).
- **Portal homepage:** `/` — one card per live domain.
- **Blog:** `www.open-reporting.dev` — all 18 articles PUBLISHED (commit `6d7b89f4`).
- **Daily ingestion:** 22:00 UTC cron.
- **Autonomous-lead cron:** `0 2,7,12,17 * * *` UTC.
- **Next free dashboard port:** 8073.

## Open / blocked work (all standing blockers PO-side)

| Linear | What | Status |
|---|---|---|
| (infra) | Degraded autonomous tool I/O channel | Blocked — PO; 3 runs running |
| OR-153 | Telegram inbound (systemd `${}` non-expansion) | Blocked — PO; outbox works |
| OR-90 | Instagram token (Meta portal) — blocks OR-89 publish | Blocked — PO action |
| OR-86 | BDL/GUS ingestion | Backlog — needs `BDL_API_KEY` from PO |
| OR-79 | Ghost nav "Portal" link — browser admin | Blocked — PO action |
| OR-89 | Weekly snapshot — code ready; publish blocked on OR-90 | Buildable remainder: cron entry |
| Phase 3 | Data depth: BDL, Finance v2, dbt tests, freshness indicators | Next focus once channel healthy |

**Article queue: CLEARED.** No drafts pending — all 18 live.

## Known infra issue (ACTIVE — TOP PRIORITY FOR PO)

**Degraded autonomous tool I/O — 3 runs running (#29, #30, #31).** `claude -p` subprocess tool results return empty on response and do not flush in-window; reads never complete. Forces quiet runs because all deploy/verify output is unobservable. Autonomous building is idle until fixed.
Suggested PO checks: claude-code version on VPS vs last-known-good; autonomous-lead.sh launcher stdout/stderr piping + any timeout/buffering wrapper; whether interactive `claude` on the VPS shows tool output normally (isolates harness vs subprocess).

## Recent commits

| Commit | What |
|---|---|
| (run #31) | docs: run #31 quiet — tool I/O channel degraded 3rd run, escalated |
| `fe4fea8b` | docs: run #30 addendum — reconcile 9 published article issues to Done |
| `a0d03607` | docs: run #30 quiet — health verified, ingest exit=0, channel flagged |
| `6d7b89f4` | feat(content): publish all 18 articles — pipeline review complete |
| `0c45be26` | docs: session memory — release pipeline shipped, protocol change flagged |
| `cd106eb4` | feat(content): autonomous article release pipeline — 3-reviewer gate |

## Discord bot fleet (live)

8 bots, `infra/discord-bot/bot.py`, tokens in `.env` as `DISCORD_BOT_<NAME>_TOKEN`.
project-lead (opus), scrum-master (haiku), dashboard-dev/data-engineer/content-writer/researcher/code-reviewer (sonnet), debug (haiku).
Service files: `or-discord-<name>-bot.service`. Channels: `#general`, `#daily-standup`, `#dashboard-dev`, `#blockers`, `#linear-feed`.
**Untracked `infra/systemd/or-*-bot.service` + modified `infra/discord-bot/bot.py` + `logs/` are PO WIP — leave untouched, never commit.**

## Key technical facts (current)

- **Release pipeline:** `python3 products/blog/release_pipeline.py` — must run STANDALONE. All 18 drafts published; nothing pending.
- **Seed dimension_key must match raw** — query `raw.eurostat_observations` before adding seed rows. `dbt seed --select eurostat_series` then `dbt run --select stg_eurostat+`.
- **dbt write-lock dance:** stop affected `or-<name>.service` → dbt run → `dbr run` to restart. Boot ~20s → brief 502.
- **dbr `bar` = horizontal** (metric x, dim y); **`column` = vertical bars.** Check every vertical-bar visual before validate.
- **`dbr run` mandatory** after any dashboard YAML change: validate → run → curl live URL → confirm rendered Dash app (not portal index).
- KPI cards resolve latest *non-null* value (semantic.py fix).
- CLAUDE.md's `from dbr.semantic import query` is stale — use `semantic_query` / `_run_latest_query`.
- Portal homepage is static `infra/nginx/html/index.html`; deploy via `docker compose up -d --force-recreate nginx`.
- Line chart multi-metric: `y: { metric: [m1, m2] }` — one trace per metric.
- Monthly→annual marts: SUM 12 months; current incomplete year undercounts (KPI shows last complete year).
- **Write-only bash executes even when the result channel is degraded** — commits/pushes land on disk/remote; only stdout return is broken.

## Stale feature branches

`feat/OR-95-dbw-hvd-explorer`, `feat/OR-template-clustered-stacked`, `feat/or-114-sustainability-tab-enhancements`, `feat/or-118-analytics-competence-structure`, `feat/or-121-measure-reference-system`, `feat/or-122-chart-visual-config`, `feat/template-one-per-family`, `feat/telegram-claude-bridge` (PR #62).
