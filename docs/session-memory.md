# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-06-01 10:50 UTC (chrome line-alignment fix — VERIFIED pixel-exact via Playwright) -->

## Header/footer ↔ sidebar line alignment — DONE, verified pixel-exact (`1acfc1a3`)

Four-iteration saga, finally resolved. PO wanted the header's bottom divider line and the
footer's top divider line to align with the sidebar's two internal divider lines (brand
borderBottom, portal-footer borderTop). Two earlier attempts made it WORSE: `2ccc8e9a`
(removed right-col grid gap — broke the floating look, didn't fix alignment) and `2d84962c`
(full-width header/footer ABOVE/BELOW the sidebar — put the brand line 56px below the header
line: gross misalignment). **Both reverted.**

**Final fix (`0faf543b` + `1acfc1a3`):** back to side-by-side `[sidebar | right-col]`, right-col
= the robust pinned-footer Grid `auto/minmax(0,1fr)/auto` WITH the floating gap restored
(pinned-footer lesson preserved, NOT regressed). Three pixel sources of misalignment killed at
root: (1) sidebar's 1px outer **border** offset its internal lines — removed border+radius, now
a flat BG_SURFACE panel separated by the page gap; (2) brand box was 57px (28px badge + 2×14
padding + 1px border) vs header 56px — trimmed brand padding 14→13px; (3) footer/​sidebar-footer
heights unified to minHeight 48px, both bottom-anchored.

**Lesson — the decisive move that ended the loop: MEASURE, don't trust CSS.** Wrote a Playwright
script (`/tmp/measure_lines.py`) that reads the live rendered `getBoundingClientRect().y` of all
four lines through prod nginx. Result: header-bottom 72 == brand-bottom 72 (Δ0); footer-top 836
== sb-footer-top 836 (Δ0), identical on public_finance + demographics. The 3 prior attempts all
"passed" on eyeballing/geometry-in-my-head and were wrong by 1–56px. For pixel-alignment work,
bounding-box measurement is the only real verification.

## Run #38 — shipped a verified product fix + tracked a real fleet-wide finding

Production healthy (5 dashboards + www 200, ingest exit=0, inbox empty, no
Strategic/Todo/In-Progress). Step 2b sweep = 18/18 skip in <1s (no-op as designed).

**Investigated 17th-domain dashboard, correctly rejected it.** The unbuilt domains are
**data-blocked, not effort-blocked**: Eurostat PL coverage is far too thin — CRM 33 obs
(violent_crime & prison_population END IN 2007; crime_rate only 2022–2024), AGR 26, BUS 25
— vs hundreds-to-hundreds-of-thousands for every live domain. OR-60/62/63 themselves name
GUS BDL/DBW/MS/Policja/MRiRW as sources (never Eurostat). Building on Eurostat = thin,
stale product. Correctly blocked on **OR-86** (`BDL_API_KEY`, PO action). **Lesson: the
remaining enumerated domains are gated on BDL ingestion, not on build effort — do not
re-investigate building them on Eurostat each quiet run.**

**Shipped (product):** public_finance footer `Dane: 2023` → `Dane: 2024` (strictly-true;
2024 fiscal actuals are displayed, page titled "Polska 2024 w skrócie"). dbr validate +
run + verified LIVE (`_dash-layout` serves `Dane: 2024`, 200). Single-dashboard, no dbr
framework change, fleet untouched.

**Tracked (backlog) OR-165** (Improvement+Infra, Low): the WHOLE fleet's `footer_updated`
is hand-set and drifting stale (most say 2023 but have 2025 actuals). Conservative-but-true
so not urgent. Naive max(year) is WRONG — IMF WEO → 2029 forecasts; monthly series → 2026
(it's 2026-06). Fix = engine auto-derive from each page's displayed *actual* (non-forecast)
data; branch+PR+fleet-redeploy when picked.

**Note:** OR-60/62/63 are ARCHIVED (archivedAt 2026-03-20) → `save_comment` rejects them.
Finding recorded in decisions.md + OR-165 description instead.

## Current Focus

**16 domain dashboards live. 18 blog articles PUBLISHED. dbr at 22 visual types.**
Fleet stable (floating-panel layout #34–#36 verified live). No open build in flight.

**Next real build options (none unblocked-and-safe-and-high-value right now):**
- New domain dashboards (crime/agri/business) → BLOCKED on OR-86 BDL key (PO).
- dbr engine features → branch+PR, don't destabilize fleet: OR-165 (footer auto-derive),
  OR-160 (cross-filter), OR-161 (date-range slicer), OR-162 (number formatting).
- Quality passes on live dashboards (visual-screenshot-reviewer) — declarative fixes only.

## Live production state (verified run #38)

- **16 Eurostat domain dashboards Live (HTTP 200):** public_finance (8057), labour_market
  (8058), national_accounts (8059), demographics (8060), environment (8061),
  living_conditions (8062), prices (8063), education (8064), transport (8065), science
  (8066), trade (8067), production (8068), health (8069), energy (8070), tourism (8071),
  financial_markets (8072). **Next free port: 8073.**
- **Portal** `/` one card per domain. **Blog** all 18 articles live. **Daily ingestion**
  22:00 UTC (last exit=0). **Autonomous-lead cron** `0 2,7,12,17 * * *` UTC.

## Ops note — fleet redeploy after dbr framework changes (USE THE VERIFIER)

Commit touching `packages/dbr/` (editable install) does NOT auto-update the live fleet — each
`or-<domain>.service` must restart to load new framework code, and `curl` 200 cannot tell new
code from old. **Commit dbr code first, then `python3 infra/scheduler/redeploy_dashboards.py`**
— restarts all 16, polls each page's `<meta name="dbr-build">` stamp until == repo HEAD, exits
non-zero with STALE/DOWN table if any lag. **Non-zero = NOT resolved.** Targeted:
`redeploy_dashboards.py <domain>`; check-only `--verify-only`. `dbr run` is the path when a
dashboard's own YAML changed (also rewrites nginx route). `systemctl restart or-*` +
`daemon-reload` NOPASSWD; `is-active`/`--version` NOT. Dash answers at `/<domain>/`, not `/`.

## Release pipeline (FIXED + cheap)

- `15b9e8eb`: reviewers strip `ANTHROPIC_API_KEY` → authenticate via Max OAuth. Run STANDALONE
  only (concurrent token use can rate-limit nested `claude -p`).
- `313a6781`: 18 per-slug PUBLISHED stubs → Step 2b sweep skips all in <1s. `--force` to
  re-review. New drafts (no stub) still get full review.

## Open / blocked work

| Linear | What | Status |
|---|---|---|
| OR-165 | dbr auto-derive footer_updated (forecast-aware) | Backlog — engine, branch+PR |
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

- **Footer freshness:** `footer_updated` is hand-set per dashboard, drifting stale; OR-165
  tracks the engine auto-derive fix. Most footers conservative-but-true (year ≤ actual).
- **Unbuilt domains gated on BDL (OR-86), not effort** — Eurostat PL too thin for CRM/AGR/BUS.
- **dbr framework changes need fleet restart** (see Ops note above).
- **Seed dimension_key must match raw** — query `raw.eurostat_observations` before adding seed
  rows. `dbt seed --select eurostat_series` then `dbt run --select stg_eurostat+`.
- **dbt write-lock dance:** stop affected `or-<name>.service` → dbt run → restart.
- **dbr 22 visual types:** area, bar, box, bullet, card, choropleth, column, combo, funnel,
  gauge, heatmap, histogram, line, pie, ribbon, scatter, slicer, small_multiples, tab_group,
  table, treemap, waterfall.
- **dbr `bar` = horizontal** (metric x, dim y); **`column` = vertical bars.**
- KPI cards resolve latest *non-null* value (semantic.py).
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
