# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-06-01 (run #43 — FIXED-canvas pages: distribute/fill/align, live-verified) -->

## Run #43 — fixed-canvas pages (distribute, fill, align, real edge space). HEAD 4159fc6c, all 16 verified

PO feedback on #42: (1) edge "shadow" should be real space; (2) visuals must align left+right
across rows; (3) distribute content vertically — no overlapping pages, one page per anchor;
(4) make pages FIXED at the layout level — jump via anchors and/or scroll.

**Engine (`page_shell.py` + `compiler.py` + `_render.py`, commit before content):**
- **Fixed pages**: section = exactly one viewport (`height:100%` + `overflow:hidden`),
  `scrollSnapType: y mandatory`. Verified: snapped page 764px visible, all others **0px** —
  no overlap, one page per anchor.
- **Vertical distribution**: flex-column page body splits leftover height across *grow* rows;
  KPI/slicer rows + chart+table rows keep natural height. Grow (chart) rows have a **260px
  readable floor** (`_MIN_GROW_ROW_HEIGHT`); if a page needs more, the body scrolls internally
  while staying a one-viewport tile (still only one page visible). `overflowY:auto` on body.
- **Charts fill**: no-table chart cards clear fixed height + render a responsive graph that
  fills the cell (`_card_render_mode` in `_render.py`). **Chart WITH a companion table keeps
  fixed height and stacks the table beneath** (filling collapses the chart) — and the compiler
  marks those rows non-grow. Fill cards `overflow:hidden` so an over-dense cell never paints
  over its neighbour (was the old UE overlap mess). This makes the engine safe for the other
  15 dashboards' inline tables without touching their content.
- **Horizontal alignment**: `%` item widths → flex-grow ratio with 0 basis (`_item_flex`),
  not `flex:0 0 <pct>`. Old form summed bases to 100% + added gaps → each row overflowed by a
  different amount (KPI right 1604, 2-chart 1572, 1-chart 1556, some clipped past canvas). Now
  every row fills exactly [left,right]; all rows align edge-to-edge (verified L280 R1556).
- **Edge space**: removed the top/bottom mask-fade (#40c) — it read as a shadow. Fixed pages
  don't scroll content under the chrome at rest, so the page's own MAIN_PADDING is clean space.

**Content (`public_finance`)**: dropped 7 inline companion tables (up to 54 rows — overflow a
fixed canvas), replaced with `download: true` (Pobierz CSV). Charts now fill the page.

**Live-verified** (Playwright 1600×900): all 5 pf pages clean + screenshotted (KPIs aligned,
charts fill, space below header, snap isolates one page); labour_market (has tables) + demographics
spot-checked — 1 page on screen, no overlap. All 16 serve HEAD `4159fc6c`.

**Known tradeoff**: pages authored with 2+ tall chart rows (≥2×260px + headings) exceed an
880px window and scroll internally a little; they fit fully on ≥1080p monitors. Reducing rows
per page (content authoring) removes the internal scroll — per-dashboard follow-up if wanted.
The other 15 dashboards keep their inline tables (engine renders them natural-height, safe) —
they can be migrated to the download pattern later for a cleaner fixed-canvas look.

## Run #42 — Power BI–style full-viewport pages + full-width canvas (shipped, all 16 verified)

`/goal`: each sidebar anchor should behave like a Power BI page — full-viewport, click-to-show-
fully, pages stacked with up/down scroll; and kill the oversized right gap.

**Shipped (`6989a42c`, follows `55f5895e`):**
- **Page model** (`page_shell.py`): each section now renders as a `dbr-section-<anchor>` wrapper
  with `minHeight:100%` (resolves against the scroll container's definite grid-track height),
  `scrollSnapAlign:start`; container gets `scrollSnapType: y proximity` (proximity, not mandatory
  — tall pages must stay freely scrollable, never trapped). Dropped the single `<html.Main>`
  wrapper and the `1440px` `main_max_width` cap → canvas spans full width, leaving only
  `MAIN_PADDING` as the inset (44px right, symmetric with the sidebar↔canvas side). All H2
  headings now `marginTop:0` (each sits at its own page top).
- **Nav-click snap** (`make_app.py` scrollspy JS): click scrolls the whole `dbr-section-<anchor>`
  wrapper flush to the container top via `getBoundingClientRect` math (offsetParent-robust), so
  the page opens fully like a default view. Scrollspy active-state still keyed on `h2[id]`.
- Id namespace: section wrappers are `dbr-section-*` (the chrome already owns `dbr-page-header/
  -footer` — keeping them distinct avoids collision).

**Live-verified (Playwright, 1600×900 public_finance):** right inset 44px (was a big void from
the 1440 cap); all 5 section pages ≥ container height 764; nav click → page-top offset 0px
(flush snap); screenshots confirm full-width charts + clean page-open. **This supersedes/cleans
up the dangling #41 uncommitted page-model WIP** — now a reviewed, committed, fleet-deployed
version. All 16 serve HEAD `6989a42c`.

**Note (judgment):** charts keep their own fixed heights — they fill width but do not vertically
stretch to fill a page (heterogeneous row content makes auto-stretch fragile; Power BI itself
hand-lays-out). Full-width fill + viewport-height pages was the robust read of "cover full page
space". Revisit per-visual vertical-fill only if PO asks.

## Run #41 — quiet run: production verified, uncommitted dbr WIP flagged (no mutation)

Inbox empty, no Strategic/Todo/In-Progress, 18/18 articles published (sweep clean no-op), 16
dashboards + www HTTP 200, ingest exit=0. Tool channel healthy.

**Found new uncommitted engine-plane WIP — NOT mine, NOT touched:** working tree carries an
edit to `packages/dbr/src/dbr/layout/page_shell.py` (mtime 16:44 UTC) layering a full-viewport
**scroll-snap "page model"** on top of committed `38cab4a9` (the #40c mask-fade). It's the
in-flight continuation of the interactive #40/#40b/#40c layout-polish session — **PO's active
interactive WIP.** Did not commit (unreviewed engine code, fails the review gate) and did not
revert (live experimental work).

**Production integrity confirmed:** all 16 services booted **16:18 UTC** (before the 16:44
edit); live `public_finance` serves stamp `38cab4a9` with **no `scrollSnap` token** → the
page-model is NOT live and won't deploy unless a service restarts. Daily cron only *ensures
running* (won't restart live units), so the landmine is dormant. **Consequence: any `dbr run`
/ `redeploy_dashboards.py` would push the unreviewed page-model fleet-wide — so I avoided all
dbr redeploys this run.** PO must finish+commit (then gate + redeploy) or stash/discard it
before any autonomous run can safely redeploy dashboards again.

## Recent layout-polish lineage (interactive #40 series, committed)

- `c3c7329e` #40 — zero `marginTop` on first section heading (kill dead band under header).
- `2ef31887` #40b — right-column grid `gap` PAGE_GAP→0; header/footer flush against scroll body.
- `38cab4a9` #40c — `mask-image` linear-gradient fade on `#dbr-main-scroll` top/bottom 16px so
  content dissolves into the chrome instead of touching divider lines. **All 16 on this HEAD.**
  Lesson: overflow containers clip at the padding box — use a mask fade for edge breathing room.
- `976b1acb` #39 — flagship public_finance freshness 2024→2025 (title/footer/trend; KPI cards
  resolve latest-non-null, warehouse has 2025 actuals). EU-27 + COFOG left at 2024 (true).

## Current Focus

**16 domain dashboards live. 18 blog articles PUBLISHED. dbr at 22 visual types.** Fleet stable
on `38cab4a9`. No open build in flight. Next safe build is gated: dashboards need the dbr tree
clean (PO WIP above) or new data (OR-86 BDL key).

**Next real build options (none unblocked-safe-high-value right now):**
- New domains (crime/agri/business) → BLOCKED on OR-86 BDL key (PO); Eurostat PL too thin.
- dbr engine features → branch+PR: OR-165 (footer auto-derive — recurring manual fix, real
  solution), OR-160 (cross-filter), OR-161 (date-slicer), OR-162 (num-fmt).
- Quality passes on live dashboards (hydrated screenshots, declarative fixes) — but a dbr
  redeploy is unsafe until the page_shell WIP is resolved.

## Live production state (verified run #41)

- **16 Eurostat dashboards Live (HTTP 200):** public_finance (8057), labour_market (8058),
  national_accounts (8059), demographics (8060), environment (8061), living_conditions (8062),
  prices (8063), education (8064), transport (8065), science (8066), trade (8067), production
  (8068), health (8069), energy (8070), tourism (8071), financial_markets (8072). Next port 8073.
- Portal `/` one card per domain. Blog all 18 live. Daily ingestion 22:00 UTC (last exit=0).
  Autonomous-lead cron `0 2,7,12,17 * * *` UTC.

## Ops note — fleet redeploy after dbr changes (USE THE VERIFIER)

Editable-installed `packages/dbr/` does NOT auto-update the live fleet; `curl` 200 can't tell
new code from old. **Commit dbr code first, then `python3 infra/scheduler/redeploy_dashboards.py`**
— restarts all 16, polls each `<meta name="dbr-build">` until == HEAD, exits non-zero (STALE/DOWN)
if any lag. Caveat: a docs/YAML-only HEAD advance makes the verifier report STALE for all 16
though no framework code changed — expected, don't restart to chase it; confirm via direct curl.
`dbr run` is the path when a dashboard's own YAML changed. `systemctl restart or-*` + `daemon-reload`
NOPASSWD; `is-active`/`--version` NOT. Dash answers at `/<domain>/`, not `/`.

## Release pipeline (FIXED + cheap)

- `15b9e8eb`: reviewers strip `ANTHROPIC_API_KEY` → Max OAuth auth. Run STANDALONE only.
- `313a6781`: 18 per-slug PUBLISHED stubs → Step 2b sweep skips all in <1s. `--force` to
  re-review; new drafts (no stub) still get full review.

## Open / blocked work

| Linear | What | Status |
|---|---|---|
| OR-165 | dbr auto-derive footer_updated (forecast-aware) | Backlog — engine, branch+PR. Flagship at 2025; rest understates |
| OR-86 | BDL/GUS ingestion — gates OR-60/62/63 + regional depth | Backlog — needs `BDL_API_KEY` (PO) |
| OR-60/62/63 | Crime / Business / Agriculture dashboards (ARCHIVED) | Blocked on OR-86; thin Eurostat data |
| OR-159/160/161/162 | dbr features (choropleth done / cross-filter / date-slicer / num-fmt) | Backlog — engine, branch+PR |
| OR-153 | Telegram inbound (systemd `${}` non-expansion) | Blocked — PO; outbox works |
| OR-90 | Instagram token (Meta portal) — blocks OR-89 publish | Blocked — PO action |
| OR-79 | Ghost nav "Portal" link — browser admin | Blocked — PO action |

In Progress + Todo Linear: empty. Article queue: cleared (all 18 live).

## Key technical facts (current)

- **`.env` `ANTHROPIC_API_KEY` is unfunded** — harmless for release pipeline (stripped), but any
  other code passing it to the SDK fails "credit balance too low". Fund or remove.
- **Footer freshness** hand-set per dashboard, drifts stale (OR-165). KPI cards = latest non-null.
- **Hydrated screenshot recipe:** localhost:<port>, chromium `--no-sandbox --disable-dev-shm-usage
  --single-process`, settle ~3.5s, `full_page=False`, check `svgs>0`. (`/tmp/shot_pf.py`.)
- **Seed dimension_key must match raw** — query `raw.eurostat_observations` before adding rows.
- **dbt write-lock dance:** stop affected `or-<name>.service` → dbt run → restart.
- **dbr `bar` = horizontal** (metric x, dim y); **`column` = vertical bars.**
- Portal homepage = static `infra/nginx/html/index.html`; deploy via `docker compose up -d
  --force-recreate nginx`.

## Untracked / WIP — leave untouched, never commit

- **`packages/dbr/.../page_shell.py` (MODIFIED) — PO interactive scroll-snap page-model WIP (#41).**
  Fleet-wide landmine until resolved; do not redeploy dbr while present.
- `infra/discord-bot/bot.py` (modified) + untracked `infra/systemd/or-*-bot.service`
  (gemini/opencode/claude/discord-test/…) + `logs/` + `.claude/scheduled_tasks.lock` — PO bot WIP.

## Discord bot fleet (live)

8 bots, `infra/discord-bot/bot.py`. project-lead (opus), scrum-master (haiku),
dashboard-dev/data-engineer/content-writer/researcher/code-reviewer (sonnet), debug (haiku).
Channels: `#general`, `#daily-standup`, `#dashboard-dev`, `#blockers`, `#linear-feed`.

## Stale feature branches

`feat/OR-95-dbw-hvd-explorer`, `feat/OR-template-clustered-stacked`,
`feat/or-114-sustainability-tab-enhancements`, `feat/or-118-analytics-competence-structure`,
`feat/or-121-measure-reference-system`, `feat/or-122-chart-visual-config`,
`feat/template-one-per-family`, `feat/telegram-claude-bridge` (PR #62).
