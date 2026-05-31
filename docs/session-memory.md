# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-05-31 12:00 UTC (run #32 — release-pipeline credit-bug fix) -->

## Current Focus

**16 domain dashboards live. 18 blog articles PUBLISHED. dbr at 22 visual types.**

**Latest (run #32):** Fixed the root cause behind the article-gate failures. The
release pipeline passed `.env`'s unfunded `ANTHROPIC_API_KEY` to its `claude -p`
reviewers → "credit balance too low" → **false BLOCK verdicts**. Commit `15b9e8eb`
strips the key so reviewers use the Max-subscription OAuth pool. Verified in isolation
(key present → credit error; stripped → "OK"). The #29–#31 "degraded I/O channel"
story was at least partly this masquerading as failed reviews — channel was fully
healthy this run.

## Live production state (verified run #32, all HTTP 200)

- **16 Eurostat domain dashboards Live:** public_finance, labour_market,
  national_accounts, demographics, environment, living_conditions (8062),
  prices (8063), education (8064), transport (8065), science (8066), trade (8067),
  production (8068), health (8069), energy (8070), tourism (8071),
  financial_markets (8072).
- **Portal homepage** `/` — one card per live domain. **Blog** `www.open-reporting.dev`
  — all 18 articles published. **Daily ingestion** 22:00 UTC cron.
  **Autonomous-lead cron** `0 2,7,12,17 * * *` UTC. **Next free dashboard port:** 8073.

## Open / blocked work

| Linear | What | Status |
|---|---|---|
| — | bezrobocie article: Ghost-only draft, no committed source `.md` | content-writer to regenerate source so the (now-working) gate can publish |
| OR-153 | Telegram inbound (systemd `${}` non-expansion) | Blocked — PO; outbox works |
| OR-90 | Instagram token (Meta portal) — blocks OR-89 publish | Blocked — PO action |
| OR-86 | BDL/GUS ingestion | Backlog — needs `BDL_API_KEY` from PO |
| OR-79 | Ghost nav "Portal" link — browser admin | Blocked — PO action |
| OR-89 | Weekly snapshot — code ready; publish blocked on OR-90 | cron entry remains |
| Phase 3 | Data depth: BDL, Finance v2, dbt tests, freshness indicators | Next build focus |

In Progress + Todo Linear: empty (9 stale article issues reconciled to Done in #30).
Article queue: cleared (all 18 live).

## Note for PO

`.env`'s `ANTHROPIC_API_KEY` is an unfunded pay-as-you-go account. Now harmless for
the release pipeline (stripped), but any other code passing it to the SDK will still
fail with "credit balance too low". Consider funding or removing it.

## Recent commits

| Commit | What |
|---|---|
| `15b9e8eb` | fix(blog): strip ANTHROPIC_API_KEY from release-pipeline review subprocess |
| `b0fc468b` | feat(dbr): page header + footer layout |
| `3ae80900` | fix(dbr): align sidebar toggle with brand header row |
| `ad329f39` | feat(dbr): collapsible sidebar toggle |
| `95b2fa6a` | feat(dbr): modern dashboard layout — sticky sidebar, scrollspy |
| `cf7769c4` | docs(dbr): final README — 22 visual types |
| `af418858` | feat(dbr): Phase 3 — ribbon chart + drill-through (OR-163/164) |

## Discord bot fleet (live)

8 bots, `infra/discord-bot/bot.py`, tokens in `.env`. project-lead (opus),
scrum-master (haiku), dashboard-dev/data-engineer/content-writer/researcher/code-reviewer
(sonnet), debug (haiku). Channels: `#general`, `#daily-standup`, `#dashboard-dev`,
`#blockers`, `#linear-feed`.
**Untracked `infra/systemd/or-*-bot.service` + modified `infra/discord-bot/bot.py` +
`logs/` are PO WIP — leave untouched, never commit.**

## Key technical facts (current)

- **Release pipeline FIXED:** `python3 products/blog/release_pipeline.py` — reviewers
  now strip ANTHROPIC_API_KEY → use Max-subscription OAuth. Must still run STANDALONE
  (nested `claude -p` shares the rate pool). Skips drafts whose review says PUBLISHED;
  reviews drafts in `products/blog/drafts/` and `products/blog/`.
- **Seed dimension_key must match raw** — query `raw.eurostat_observations` before adding
  seed rows. `dbt seed --select eurostat_series` then `dbt run --select stg_eurostat+`.
- **dbt write-lock dance:** stop affected `or-<name>.service` → dbt run → `dbr run` to
  restart. Boot ~20s → brief 502.
- **dbr 22 visual types:** area, bar, box, bullet, card, choropleth, column, combo,
  funnel, gauge, heatmap, histogram, line, pie, ribbon, scatter, slicer, small_multiples,
  tab_group, table, treemap, waterfall.
- **dbr `bar` = horizontal** (metric x, dim y); **`column` = vertical bars.** Check every
  vertical-bar visual before validate.
- **`dbr run` mandatory** after any dashboard YAML change: validate → run → curl live URL
  → confirm rendered Dash app (not portal index).
- KPI cards resolve latest *non-null* value (semantic.py). Use `semantic_query` /
  `_run_latest_query` (CLAUDE.md's `from dbr.semantic import query` is stale).
- Portal homepage = static `infra/nginx/html/index.html`; deploy via
  `docker compose up -d --force-recreate nginx`.
- Monthly→annual marts: SUM 12 months; current incomplete year undercounts (KPI shows
  last complete year).
- **Write-only bash executes even when result channel is degraded** — commits/pushes land;
  only stdout return breaks.

## Stale feature branches

`feat/OR-95-dbw-hvd-explorer`, `feat/OR-template-clustered-stacked`,
`feat/or-114-sustainability-tab-enhancements`, `feat/or-118-analytics-competence-structure`,
`feat/or-121-measure-reference-system`, `feat/or-122-chart-visual-config`,
`feat/template-one-per-family`, `feat/telegram-claude-bridge` (PR #62).
