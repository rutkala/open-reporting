# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-05-31 17:18 UTC (run #33 — fleet redeploy to HEAD dbr layout fix) -->

## Current Focus

**16 domain dashboards live. 18 blog articles PUBLISHED. dbr at 22 visual types.**

**Latest (run #33):** Caught + fixed production drift. Smoke check was green, but
all 16 dashboard services were running `packages/dbr/` code from BEFORE HEAD commit
`2922a4cf` (PO's Playwright-verified "remove sidebar gap strip + visible header chrome"
layout fix, committed 16:38 UTC; services last restarted 16:13–16:16 UTC). dbr is
editable-installed, so a `systemctl restart` picks up new framework code. Rolling-restarted
all 16 → all HTTP 200, all ActiveEnterTimestamp now 17:02–17:18 UTC, fleet == HEAD.
No code change this run; pure ops sync. Channel fully healthy (no I/O degradation).

## Live production state (verified run #33, all HTTP 200)

- **16 Eurostat domain dashboards Live, all on HEAD dbr:** public_finance (8057),
  labour_market (8058), national_accounts (8059), demographics (8060), environment (8061),
  living_conditions (8062), prices (8063), education (8064), transport (8065),
  science (8066), trade (8067), production (8068), health (8069), energy (8070),
  tourism (8071), financial_markets (8072).
- **Portal homepage** `/` — one card per live domain. **Blog** `www.open-reporting.dev`
  — all 18 articles published. **Daily ingestion** 22:00 UTC cron (last exit=0).
  **Autonomous-lead cron** `0 2,7,12,17 * * *` UTC. **Next free dashboard port:** 8073.

## Ops note — fleet redeploy after dbr framework changes

When a commit touches `packages/dbr/` (editable install), the live fleet does NOT
auto-update — each `or-<domain>.service` must be restarted to load new framework code.
Check drift with: `git log -1 --format=%ci -- packages/dbr/` vs
`systemctl show or-<domain>.service -p ActiveEnterTimestamp`. A plain
`sudo systemctl restart or-<domain>.service` suffices (no nginx churn); `dbr run` is
only needed when the dashboard's own YAML changed. Local `/` health-poll is a poor
readiness signal — Dash answers at `/<domain>/`; verify via nginx curl instead.

## Open / blocked work

| Linear | What | Status |
|---|---|---|
| — | release-pipeline skip guard ineffective: per-slug `reviews/<slug>-review.md` "✅ PUBLISHED" stubs never written for the 18 (published via aggregate flow) → Step 2b sweep would re-spawn 54 subprocesses. Write the 18 stubs to make the sweep a cheap no-op | next run, small |
| — | bezrobocie article: Ghost-only draft, no committed source `.md` | content-writer to regenerate source |
| OR-153 | Telegram inbound (systemd `${}` non-expansion) | Blocked — PO; outbox works |
| OR-90 | Instagram token (Meta portal) — blocks OR-89 publish | Blocked — PO action |
| OR-86 | BDL/GUS ingestion | Backlog — needs `BDL_API_KEY` from PO |
| OR-79 | Ghost nav "Portal" link — browser admin | Blocked — PO action |
| OR-89 | Weekly snapshot — code ready; publish blocked on OR-90 | cron entry remains |
| Phase 3 | Data depth: BDL, Finance v2, dbt tests, freshness indicators | Next build focus |

In Progress + Todo Linear: empty. Article queue: cleared (all 18 live).

## Note for PO

`.env`'s `ANTHROPIC_API_KEY` is an unfunded pay-as-you-go account. Harmless for the
release pipeline now (stripped, commit `15b9e8eb`), but any other code passing it to the
SDK will fail with "credit balance too low". Consider funding or removing it.

## Recent commits

| Commit | What |
|---|---|
| `2922a4cf` | fix(dbr): remove sidebar gap strip + visible header chrome (PO; deployed to fleet in #33) |
| `82f59fad` | fix(dbr): add minHeight:0 to main scroll container — footer visible |
| `f9f0f42e` | fix(dbr): Cache-Control no-store on all dashboard nginx routes |
| `04725888` | fix(dbr): widen sidebar gap to 16px, restore footer to white surface |
| `81cc1dff` | fix(dbr): header/footer canvas colour + sidebar gap + full fleet redeploy |
| `15b9e8eb` | fix(blog): strip ANTHROPIC_API_KEY from release-pipeline review subprocess |

## Discord bot fleet (live)

8 bots, `infra/discord-bot/bot.py`, tokens in `.env`. project-lead (opus),
scrum-master (haiku), dashboard-dev/data-engineer/content-writer/researcher/code-reviewer
(sonnet), debug (haiku). Channels: `#general`, `#daily-standup`, `#dashboard-dev`,
`#blockers`, `#linear-feed`.
**Untracked `infra/systemd/or-*-bot.service` + modified `infra/discord-bot/bot.py` +
`logs/` are PO WIP — leave untouched, never commit.**

## Key technical facts (current)

- **dbr framework changes need fleet restart** (see Ops note above).
- **Release pipeline FIXED** (`15b9e8eb`): reviewers strip ANTHROPIC_API_KEY → Max OAuth.
  Run STANDALONE only. Skip guard needs per-slug review stubs (currently absent).
- **Seed dimension_key must match raw** — query `raw.eurostat_observations` before adding
  seed rows. `dbt seed --select eurostat_series` then `dbt run --select stg_eurostat+`.
- **dbt write-lock dance:** stop affected `or-<name>.service` → dbt run → restart.
- **dbr 22 visual types:** area, bar, box, bullet, card, choropleth, column, combo,
  funnel, gauge, heatmap, histogram, line, pie, ribbon, scatter, slicer, small_multiples,
  tab_group, table, treemap, waterfall.
- **dbr `bar` = horizontal** (metric x, dim y); **`column` = vertical bars.**
- KPI cards resolve latest *non-null* value (semantic.py). Use `semantic_query` /
  `_run_latest_query`.
- Portal homepage = static `infra/nginx/html/index.html`; deploy via
  `docker compose up -d --force-recreate nginx`.

## Stale feature branches

`feat/OR-95-dbw-hvd-explorer`, `feat/OR-template-clustered-stacked`,
`feat/or-114-sustainability-tab-enhancements`, `feat/or-118-analytics-competence-structure`,
`feat/or-121-measure-reference-system`, `feat/or-122-chart-visual-config`,
`feat/template-one-per-family`, `feat/telegram-claude-bridge` (PR #62).
