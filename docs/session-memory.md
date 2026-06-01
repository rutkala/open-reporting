# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-06-01 02:05 UTC (run #37 — release-sweep no-op stubs + Linear board reconciliation) -->

## Run #37 — cleared two pieces of standing debt (housekeeping run)

Production fully healthy (all 16 dashboards + www 200, ingest exit=0, channel healthy).
Inbox empty; no Strategic/Todo/In-Progress; no safe unblocked build right after the
#34–#36 layout stabilization. Spent the run clearing two deferred-debt items, both
complete and verifiable:

1. **Step 2b sweep is now a sub-second no-op** (commit `313a6781`). The release-pipeline
   skip guard checks `reviews/<slug>-review.md` for "✅ PUBLISHED"; those per-slug files
   never existed (the 18 were published via the aggregate flow), so every run's Step 2b
   would re-spawn 18×3 reviewer subprocesses for zero gain. Verified all 18 article URLs
   HTTP 200, then wrote a stub per slug. Pipeline now skips all 18 in <1s, 0 subprocesses.
   **Also resolved:** the bezrobocie/or-145 "Ghost-only draft, regenerate" followup from
   #32 — it's actually live (200) with a committed source `drafts/or-145-labour.md`.
2. **Linear board reconciliation** — moved 10 stale shipped dashboard tickets Backlog→Done
   (OR-53/54/58/64/65/66/68/81/82 + OR-75 epic), each 1:1 to a live domain. Comment on
   OR-75. Left open: OR-60 Crime, OR-63 Agriculture (not built); OR-62 Business/Industry
   (mapping uncertain).

**Lesson:** when a "standing followup" recurs across 3+ post-mortems and is small +
verifiable, just do it on the next quiet run instead of re-flagging it.

## Current Focus

**16 domain dashboards live. 18 blog articles PUBLISHED. dbr at 22 visual types.**
Floating-panel layout (#34–#36) verified live, all 16 on HEAD. No open build in flight.

**Next real build** (none unblocked-and-safe this run): Phase 3 data depth — OR-86 BDL
ingestion (needs PO `BDL_API_KEY`), or a dbr engine feature (OR-159 choropleth [already a
visual type]/OR-160 cross-filter/OR-161 date-range slicer — all `packages/dbr/`, branch+PR,
do NOT destabilize the just-stabilized fleet). New domain dashboards OR-62/60/63 if wanted.

## Live production state (verified run #37 — all 16 HTTP 200)

- **16 Eurostat domain dashboards Live:** public_finance (8057), labour_market (8058),
  national_accounts (8059), demographics (8060), environment (8061), living_conditions
  (8062), prices (8063), education (8064), transport (8065), science (8066), trade (8067),
  production (8068), health (8069), energy (8070), tourism (8071), financial_markets (8072).
- **Portal** `/` one card per domain. **Blog** all 18 articles live. **Daily ingestion**
  22:00 UTC (last exit=0). **Autonomous-lead cron** `0 2,7,12,17 * * *` UTC.
  **Next free dashboard port:** 8073.

## Ops note — fleet redeploy after dbr framework changes (USE THE VERIFIER)

A commit touching `packages/dbr/` (editable install) does NOT auto-update the live fleet —
each `or-<domain>.service` must restart to load new framework code, and a `curl` 200 cannot
tell new code from old. **Commit dbr code first, then `python3
infra/scheduler/redeploy_dashboards.py`** — restarts all 16, polls each page's
`<meta name="dbr-build">` stamp until == repo HEAD, exits non-zero with a STALE/DOWN table
if any lag. **Non-zero exit = NOT resolved.** Targeted: `redeploy_dashboards.py <domain>`;
check-only: `--verify-only`. `dbr run` is the path when a dashboard's own YAML changed (it
also rewrites the nginx route). Sudo `systemctl restart or-*` + `daemon-reload` are
NOPASSWD; `is-active`/`--version` are NOT. Dash answers at `/<domain>/`, not `/`.

## Release pipeline (FIXED + now cheap)

- `15b9e8eb`: reviewers strip `ANTHROPIC_API_KEY` → authenticate via Max OAuth. Run
  STANDALONE only (concurrent token use can rate-limit the nested `claude -p` calls).
- `313a6781`: 18 per-slug PUBLISHED stubs written → Step 2b sweep skips all in <1s, 0
  subprocesses. Use `--force` to re-review. New drafts (no stub) still get full review.

## Open / blocked work

| Linear | What | Status |
|---|---|---|
| OR-153 | Telegram inbound (systemd `${}` non-expansion) | Blocked — PO; outbox works |
| OR-90 | Instagram token (Meta portal) — blocks OR-89 publish | Blocked — PO action |
| OR-86 | BDL/GUS ingestion | Backlog — needs `BDL_API_KEY` from PO |
| OR-79 | Ghost nav "Portal" link — browser admin | Blocked — PO action |
| OR-89 | Weekly snapshot — code ready; publish blocked on OR-90 | cron entry remains |
| OR-159/160/161/162 | dbr features (choropleth/cross-filter/date-slicer/num-format) | Backlog — engine plane, branch+PR |
| OR-62/60/63 | Business/Industry, Crime, Agriculture dashboards | Backlog — not built |

In Progress + Todo Linear: empty. Article queue: cleared (all 18 live).

## Note for PO

`.env`'s `ANTHROPIC_API_KEY` is an unfunded pay-as-you-go account. Harmless for the release
pipeline now (stripped, `15b9e8eb`), but any other code passing it to the SDK fails with
"credit balance too low". Consider funding or removing it.

## Recent commits

| Commit | What |
|---|---|
| `313a6781` | chore(blog): 18 per-slug PUBLISHED review stubs — Step 2b sweep is a no-op |
| `48fee2ad` | docs: run #36 — footer contrast fix note + layout lesson |
| `67d1cef3` | fix(dbr): darken page canvas so footer (and all cards) are clearly visible |
| `c93bbee7` | docs: run #35 — floating-panel layout note + lesson |
| `085b2a8d` | feat(dbr): floating-panel layout — uniform inset + visible footer |
| `83bf2e29` | docs: codify verified-redeploy discipline |
| `2353c430` | fix(dbr): raise redeploy health budget to 140s for slow demographics boot |
| `c893ca57` | feat(dbr): build-SHA stamp + verified redeploy |

## Discord bot fleet (live)

8 bots, `infra/discord-bot/bot.py`, tokens in `.env`. project-lead (opus),
scrum-master (haiku), dashboard-dev/data-engineer/content-writer/researcher/code-reviewer
(sonnet), debug (haiku). Channels: `#general`, `#daily-standup`, `#dashboard-dev`,
`#blockers`, `#linear-feed`.
**Untracked `infra/systemd/or-*-bot.service` + modified `infra/discord-bot/bot.py` +
`logs/` are PO WIP — leave untouched, never commit.**

## Key technical facts (current)

- **dbr framework changes need fleet restart** (see Ops note above).
- **Seed dimension_key must match raw** — query `raw.eurostat_observations` before adding
  seed rows. `dbt seed --select eurostat_series` then `dbt run --select stg_eurostat+`.
- **dbt write-lock dance:** stop affected `or-<name>.service` → dbt run → restart.
- **dbr 22 visual types:** area, bar, box, bullet, card, choropleth, column, combo,
  funnel, gauge, heatmap, histogram, line, pie, ribbon, scatter, slicer, small_multiples,
  tab_group, table, treemap, waterfall.
- **dbr `bar` = horizontal** (metric x, dim y); **`column` = vertical bars.**
- KPI cards resolve latest *non-null* value (semantic.py).
- Portal homepage = static `infra/nginx/html/index.html`; deploy via
  `docker compose up -d --force-recreate nginx`.

## Stale feature branches

`feat/OR-95-dbw-hvd-explorer`, `feat/OR-template-clustered-stacked`,
`feat/or-114-sustainability-tab-enhancements`, `feat/or-118-analytics-competence-structure`,
`feat/or-121-measure-reference-system`, `feat/or-122-chart-visual-config`,
`feat/template-one-per-family`, `feat/telegram-claude-bridge` (PR #62).
