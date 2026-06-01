# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-06-01 16:25 UTC (run #40c — scroll-edge fade, live-verified) -->

## Run #40c — soft-fade scroll edges so content doesn't slam into header/footer

Follow-up to #40b: with header/footer flush (gap 0), mid-scroll content touched the divider
lines. **Empirically ruled out** scroll-container padding (overflow clips at the padding box —
content paints over the padding; screenshot-verified) and a plain canvas gap (header bg ==
canvas grey → the divider line floats in a same-colour field with an abrupt content slice;
A/B screenshot confirmed it looks worse). **Fix (`38cab4a9`):** `mask-image` linear-gradient
on `#dbr-main-scroll` — content dissolves over the top/bottom 16px (`PAGE_GAP`). Mask is on the
fixed scroll viewport so the fade band stays pinned at the edges; divider lines don't move
(still sidebar-aligned). Verified live (deployed computed `mask-image` + mid-scroll screenshots
on public_finance + demographics — text and charts fade into the chrome, no hard touch). All 16
on HEAD. **Lesson:** overflow containers clip at the padding box, so container padding gives no
mid-scroll inset — use a mask fade for edge breathing room.

## Run #40b — header/footer flush against scroll body (no right-column row gap)

Follow-up to #40: PO wanted the header to "touch the space where the page disappears when
scrolling." The right column grid carried a `PAGE_GAP` (16px) between header/scroll/footer
rows, so the header floated 16px above the scroll-clip line — content vanished in a detached
canvas band. **Fix (`2ef31887`):** right-column grid `gap` PAGE_GAP→0. Header bottom border is
now the scroll-disappear line; footer top likewise (symmetric). Right column = one contiguous
panel mirroring the sidebar. Row edges don't move, so sidebar line-alignment is preserved.
Verified live: header-bottom 72 == scroll-top 72 (gap 0), scroll-bottom 836 == footer-top 836
(gap 0), header-bottom 72 == sidebar-brand-bottom 72 (dy 0), footer-top 836 == sidebar-footer-top
836 (dy 0). Fleet redeployed, all 16 on HEAD.

## Run #40 — kill the dead band between page header and first section anchor

Chrome polish on the whole fleet. The first section `<h2>` carried `section_top_gap` (40px)
as `marginTop` on top of the main canvas's `main_padding` (28px top inset) — stacking into a
~68px gap below the page header (the "strange space"). `section_top_gap` is for separating
sections from each other; on the first section it double-counts. **Fix (`c3c7329e`):** in
`page_shell.py`, zero `marginTop` on the first heading only (`idx == 0`); later sections keep
their gap. Verified live (Playwright, hydrated): header-bottom 72 → first-`<h2>` top 116 =
**44px** (= page_gap 16 + main_padding 28, the natural floating-panel inset; was 84px). Fleet
redeployed + verified all 16 on HEAD. Framework-wide — applies to every current/future dashboard.

## Run #39 — flagship public_finance freshness 2024→2025 (caught by a visual pass)

Quiet run (inbox empty, no Strategic/Todo/In-Progress, 18/18 articles published, 16
dashboards + www 200). Spent it on a visual quality pass of the flagship — and it paid off:
found and fixed a real content bug.

**Bug:** public_finance overview KPI cards have no year filter → resolve **latest-non-null**,
and the warehouse now holds **2025** actuals (balance −7.3 / debt 59.7 / expenditure 50.9 /
interest 2.5 % GDP — all match the rendered cards; body prose already said 2025). But the page
title "Polska 2024 w skrócie", footer "Dane: 2024" and the PL trend section title "1995–2024"
still said **2024**. Run #38 set footer=2024 on the wrong premise the cards showed 2024.

**Fix (`976b1acb`, live-verified):** title + footer + PL trend title → 2025. Verified via
DuckDB (`fact_finance_overview`, `fact_finance_revenue_expenditure` max PL year = 2025) and
live (`_dash-layout` serves all three 2025 strings + hydrated screenshot, 33 charts). **Left at
2024 deliberately (still true):** EU-27 cross-section (most-complete year, 34 vs 33 countries;
2024-specific prose) + COFOG (max PL COFOG year = 2024). Commented correction on **OR-165**.

**Two lessons this run:**
1. **Screenshot the HYDRATED page, not the splash.** The visual-screenshot-reviewer subagent
   returned no verdict — it captured a blank "Loading…" Dash splash (premature) and prod
   chromium crashed on the heavy page (OOM). Working recipe: hit **localhost:<port>** (not
   prod TLS), launch chromium with `--no-sandbox --disable-dev-shm-usage --single-process`,
   `wait_until=domcontentloaded` + a ~3.5s settle, `full_page=False`. `svgs>0` = hydrated.
   Script at `/tmp/shot_pf.py`.
2. **A docs/YAML-only HEAD advance makes the fleet read STALE by stamp though no framework
   code changed.** `redeploy_dashboards.py --verify-only` spins because HEAD `25bcf64e` is
   docs-only and landed after the last restart; live fleet runs `1acfc1a3` (last dbr code
   commit). Don't restart the fleet to chase a docs-only stamp bump — confirm code via direct
   curl of `<meta name="dbr-build">`.

## Current Focus

**16 domain dashboards live. 18 blog articles PUBLISHED. dbr at 22 visual types.**
Fleet stable. Flagship public_finance now freshness-consistent at 2025. No open build in flight.

**Next real build options (none unblocked-and-safe-and-high-value right now):**
- New domain dashboards (crime/agri/business) → BLOCKED on OR-86 BDL key (PO).
- dbr engine features → branch+PR, don't destabilize fleet: OR-165 (footer auto-derive — the
  per-page manual fix keeps recurring; this is the real solution), OR-160 (cross-filter),
  OR-161 (date-range slicer), OR-162 (number formatting).
- Quality passes on live dashboards (hydrated screenshots) — declarative fixes only. The other
  15 dashboards likely have the same footer-understatement OR-165 tracks.

## Live production state (verified run #39)

- **16 Eurostat domain dashboards Live (HTTP 200):** public_finance (8057), labour_market
  (8058), national_accounts (8059), demographics (8060), environment (8061),
  living_conditions (8062), prices (8063), education (8064), transport (8065), science
  (8066), trade (8067), production (8068), health (8069), energy (8070), tourism (8071),
  financial_markets (8072). **Next free port: 8073.**
- **Portal** `/` one card per domain. **Blog** all 18 articles live. **Daily ingestion**
  22:00 UTC (last exit=0). **Autonomous-lead cron** `0 2,7,12,17 * * *` UTC.

## Ops note — fleet redeploy after dbr framework changes (USE THE VERIFIER)

Commit touching `packages/dbr/` (editable install) does NOT auto-update the live fleet — each
`or-<domain>.service` must restart, and `curl` 200 can't tell new code from old. **Commit dbr
code first, then `python3 infra/scheduler/redeploy_dashboards.py`** — restarts all 16, polls
each page's `<meta name="dbr-build">` until == repo HEAD, exits non-zero with STALE/DOWN if any
lag. **Caveat (run #39):** a docs/YAML-only HEAD advance makes the verifier report STALE for
all 16 though no framework code changed — that's expected, don't restart to chase it. `dbr run`
is the path when a dashboard's own YAML changed (rewrites nginx route too; reads YAML from disk
on restart). `systemctl restart or-*` + `daemon-reload` NOPASSWD; `is-active`/`--version` NOT.
Dash answers at `/<domain>/`, not `/`.

## Release pipeline (FIXED + cheap)

- `15b9e8eb`: reviewers strip `ANTHROPIC_API_KEY` → authenticate via Max OAuth. Run STANDALONE
  only (concurrent token use can rate-limit nested `claude -p`).
- `313a6781`: 18 per-slug PUBLISHED stubs → Step 2b sweep skips all in <1s. `--force` to
  re-review. New drafts (no stub) still get full review.

## Open / blocked work

| Linear | What | Status |
|---|---|---|
| OR-165 | dbr auto-derive footer_updated (forecast-aware) | Backlog — engine, branch+PR. Flagship manually fixed to 2025 (#39); rest of fleet still understates |
| OR-86 | BDL/GUS ingestion — gates OR-60/62/63 + regional depth | Backlog — needs `BDL_API_KEY` (PO) |
| OR-60/62/63 | Crime / Business / Agriculture dashboards (ARCHIVED) | Blocked on OR-86; thin Eurostat data |
| OR-159/160/161/162 | dbr features (choropleth[done]/cross-filter/date-slicer/num-fmt) | Backlog — engine, branch+PR |
| OR-153 | Telegram inbound (systemd `${}` non-expansion) | Blocked — PO; outbox works |
| OR-90 | Instagram token (Meta portal) — blocks OR-89 publish | Blocked — PO action |
| OR-79 | Ghost nav "Portal" link — browser admin | Blocked — PO action |
| OR-89 | Weekly snapshot — code ready; publish blocked on OR-90 | cron entry remains |

In Progress + Todo Linear: empty. Article queue: cleared (all 18 live).

## Note for PO

`.env`'s `ANTHROPIC_API_KEY` is an unfunded pay-as-you-go account. Harmless for the release
pipeline (stripped, `15b9e8eb`), but any other code passing it to the SDK fails "credit
balance too low". Consider funding or removing it.

## Key technical facts (current)

- **Footer freshness:** `footer_updated` is hand-set per dashboard, drifts stale; OR-165 tracks
  the engine auto-derive fix. public_finance now at 2025 (#39). KPI cards resolve latest *non-null*.
- **Unbuilt domains gated on BDL (OR-86), not effort** — Eurostat PL too thin for CRM/AGR/BUS.
- **dbr framework changes need fleet restart** (see Ops note above; docs-only HEAD = false STALE).
- **Hydrated screenshot recipe:** localhost:<port>, chromium `--no-sandbox --disable-dev-shm-usage
  --single-process`, settle ~3.5s, `full_page=False`, check `svgs>0`. (`/tmp/shot_pf.py`.)
- **Seed dimension_key must match raw** — query `raw.eurostat_observations` before adding rows.
- **dbt write-lock dance:** stop affected `or-<name>.service` → dbt run → restart.
- **dbr 22 visual types:** area, bar, box, bullet, card, choropleth, column, combo, funnel,
  gauge, heatmap, histogram, line, pie, ribbon, scatter, slicer, small_multiples, tab_group,
  table, treemap, waterfall.
- **dbr `bar` = horizontal** (metric x, dim y); **`column` = vertical bars.**
- Portal homepage = static `infra/nginx/html/index.html`; deploy via
  `docker compose up -d --force-recreate nginx`.

## Discord bot fleet (live)

8 bots, `infra/discord-bot/bot.py`, tokens in `.env`. project-lead (opus), scrum-master
(haiku), dashboard-dev/data-engineer/content-writer/researcher/code-reviewer (sonnet), debug
(haiku). Channels: `#general`, `#daily-standup`, `#dashboard-dev`, `#blockers`, `#linear-feed`.
**Untracked `infra/systemd/or-*-bot.service` + modified `infra/discord-bot/bot.py` + `logs/`
are PO WIP — leave untouched, never commit.**

## Stale feature branches

`feat/OR-95-dbw-hvd-explorer`, `feat/OR-template-clustered-stacked`,
`feat/or-114-sustainability-tab-enhancements`, `feat/or-118-analytics-competence-structure`,
`feat/or-121-measure-reference-system`, `feat/or-122-chart-visual-config`,
`feat/template-one-per-family`, `feat/telegram-claude-bridge` (PR #62).
