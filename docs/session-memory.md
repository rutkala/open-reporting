# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-06-05 (run #68 — article #19, revenue-side public finance) -->

## Run #68 — Article #19 shipped: revenue-side public-finance piece

Broke a 5-run streak of public_finance dashboard tweaks (#63/#65/#66/#67). The
under-used lever per `docs/roadmap.md` is **content cadence**, and the draft queue was
empty. Audited the 18 published articles: finance was covered on deficit / debt /
debt-service / social spending (COFOG) / EU excessive-deficit — but **nothing on the
revenue side**. Filled that gap; it pairs with the `dochody` dashboard page from #66.

**Angle (grounded in `curated.fact_finance_revenue_expenditure`, not guessed):** PL state
runs on social contributions (15,1% PKB, 2024 — single largest) + consumption taxes/VAT
(14,4%); income taxes D5 only 7,8%; total take 42,8% PKB, ~3,2 pp BELOW EU27 (46,0).

**Process:** content-writer (1 spawn) wrote it → release_pipeline gate **BLOCKED** first
pass (content BLOCK, 2 P1s: unsourced min-wage trend; "14,4% below a 14,2–14,4% max"
self-contradiction). Fixed all findings **directly** (SendMessage unavailable this harness)
incl. domain CONDITIONALs (OFE-2010 timing, Polski Ład 2022 D61 break, VAT-Gap report
covers thru 2022, JPK_VAT causal→coinciding, D5/D29 scope). Re-gate (--force) PASSED:
content PASS, analytical CONDITIONAL, domain CONDITIONAL.

**Live:** https://www.open-reporting.dev/dochody-panstwa-polska-skad-pieniadze-2024/ → 200.
Blog now **19 published articles**.

**Gate logic confirmed:** `gate_passed` blocks only on BLOCK/ERROR; CONDITIONAL = pass.

## KEY OPS MODEL (current — unchanged since #64)
- Dashboards = **static HTML** in `infra/nginx/html/<domain>/index.html` (gitignored build
  artifacts). NO `dbr serve`, NO `or-<domain>.service`, NO ports.
- A dashboard YAML change OR a data refresh needs a **REBUILD** to show:
  single dashboard → `dbr run products/dashboards/<domain>` (build + nginx route + reload).
  Whole fleet / after any `packages/dbr/` edit → commit FIRST, then
  `python3 infra/scheduler/redeploy_dashboards.py` (builds 16 → web root, verifies each
  `<meta dbr-build>` == HEAD; non-zero exit = NOT resolved).
- Build embeds `<meta dbr-build>` = HEAD **at build time** → commit, then rebuild so
  stamp == HEAD (else --verify-only reports STALE).
- Live verify: `curl -s https://portal.open-reporting.dev/<domain>/` → 200 + stamp==HEAD +
  Plotly content. For layout/visual changes, screenshot (Playwright) — curl can't see layout.
- **Page layout is a fixed single-screen canvas with `overflow:hidden`.** Do NOT stack
  full-height rows (clips). Side-by-side widths (e.g. 60/40) within one row are safe.
- **Single scrolling page** with scrollspy nav (sections stacked, `dbr-section-<anchor>`),
  NOT a display:none multi-page app. Below-the-fold charts auto-resize on load (#67).

## Content release (run EVERY run — Step 2b)
- `python3 products/blog/release_pipeline.py` → reviews each unreviewed draft through 3
  reviewers (content + analytical + domain Opus), auto-publishes those with NO BLOCK.
  `gate_passed`: blocks only on BLOCK/ERROR; **CONDITIONAL counts as pass**.
- Re-review a fixed draft: `release_pipeline.py <draft.md> --force` (single article,
  3 reviewers, ~6 min). Published drafts stay in `products/blog/drafts/` (state tracked via
  Ghost slug lookup, not file moves). Review reports: `products/blog/reviews/<slug>-review.md`.
- **19 articles published.** Each run starts with sweep clean unless a new draft was authored.

## dbr visual notes
- **bar = HORIZONTAL** (metric on x). Vertical categorical → use **column**. Bitten 3×.
- **Multi-metric line:** `y: { metric: [a, b, c] }` → one trace per metric. Long PL labels
  wrap to multiple rows once the chart is resized to its card (#67 `_RESIZE_JS`).
- **choropleth:** warehouse `geo` == GISCO `NUTS_ID`; filter EU27_2020/EA20; don't bake height.
- Production visual types only: line, card, bar, column, choropleth. No slicers/tabs/Interval.
- `value_format` fully wired (#65): `options.value_format` on card/column/bar/table.
- Client scripts (live + static parity, `make_app.py`): `_SCROLLSPY_JS`, `_SIDEBAR_TOGGLE_JS`,
  `_RESIZE_JS`. Static export injects all three via `build._document`.

## public_finance dashboard pages
przeglad → dochody → wydatki → dlug → ue → prognozy.

## Engine-tree state
- Clean except known untracked PO/bot WIP (never commit): `infra/discord-bot/bot.py`,
  `infra/systemd/or-*-bot.service`, `logs/`, `.claude/scheduled_tasks.lock`,
  `products/blog/reviews/release-report.md`, stray `open-reporting-full.tar.gz` (root).
- 16 dashboards static; all on HEAD `c9d7a687` (run #67 fleet redeploy). No dbr code change
  this run → no fleet redeploy needed.

## Standing blockers (all PO-side)
- **OR-168** — root-fixed (#64); only `systemctl disable or-{16}` remains (sudo gap).
- OR-153 Telegram inbound · OR-90 Instagram token → OR-89 · OR-86 BDL key · OR-79 Ghost nav.
- On hold under static model: OR-160 cross-filter, OR-161 date-picker (backend-only).

## Lessons
- **When the dashboard vein has been worked several runs running, check the content gap map
  first** (#68): a new article filling a coverage hole + cross-linking a recent dashboard
  page beat a 6th consecutive dashboard polish on marginal value.
- **The publish gate works — let it block, then fix precisely** (#68): the content reviewer
  caught a real self-contradiction and an unsourced trend; domain caught OFE-timing + a
  missing structural break. All fixable inline; re-gate passed.
- **Measure live bounding boxes before re-diagnosing** (#66/#67): the "legend clip" was a
  chart rendering 1084px wide in a 628px card. Playwright bbox, not a pixel-eyeball.
- **The page canvas is fixed-height/overflow-hidden** (#66): never stack full rows.
- **Check whether a backlog item is already half-done before building** (#65).
