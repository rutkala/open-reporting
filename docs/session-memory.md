# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-06-05 (run #67 — OR-169 Plotly resize-on-load fix) -->

## Run #67 — OR-169 shipped: Plotly resize-on-load fixes clipped legends fleet-wide

The Dochody line legend clip filed in #66 turned out to be a **general chart-sizing
bug**, not a legend-config issue. Fixed it at the engine root; benefits all 16 dashboards.

**Root cause (found by measuring live bounding boxes, not eyeballing):** below-the-fold
Plotly charts bake a too-wide width at `Plotly.newPlot` time — the card hasn't reached its
final flex width when the chart first renders — and never resize. The SVG overflows its
fixed-width `overflow:hidden` card and clips on the right. revenue_trend SVG was **1084px
in a 628px card**. The horizontal legend never wrapped → last labels vanished. The same
defect silently clipped the right *data* edge of every below-the-fold chart. Confirmed on
**live production**.

**Shipped (PR #66 squash-merged, HEAD `c9d7a687`):** added `_RESIZE_JS` to `make_app.py`,
wired into BOTH the live Dash `_INDEX_STRING` and the static export `build._document`
(live/static parity). Forces `Plotly.Plots.resize` on every `.js-plotly-plot` after layout
settles (300ms post-DOMContentLoaded, 200ms post-load) + debounced (150ms) on window
resize. Once sized to the card, Plotly **auto-wraps** the horizontal legend to multiple
rows — no schema change, no per-chart option.

**Rejected:** `legend: right` (vertical) — grows horizontally, always overflows a
fixed-width overflow:hidden card and gets clipped entirely (built, measured failing,
reverted). Side-by-side fixed-canvas constraint stands.

**Verified live (Playwright bbox):** revenue_trend SVG 1084→628px (== card), legend 2 rows,
0 labels overflow; live stamp == HEAD. redeploy_dashboards.py: all 16 on HEAD, exit 0.
code-reviewer PASS (1 P3 on timing-constant comments, addressed).

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
- **It is a single scrolling page** with scrollspy nav (sections stacked, `dbr-section-<anchor>`),
  NOT a display:none multi-page app. Charts below the fold now auto-resize on load (#67).

## dbr visual notes
- **bar = HORIZONTAL** (metric on x). Vertical categorical → use **column**. Bitten 3×.
- **Multi-metric line:** `y: { metric: [a, b, c] }` → one trace per metric, labelled by
  metric.label, shown in legend. Long PL labels now **wrap to multiple rows** once the chart
  is resized to its card (#67 `_RESIZE_JS`) — no longer clip.
- **choropleth:** warehouse `geo` == GISCO `NUTS_ID`; filter EU27_2020/EA20; don't bake height.
- Production visual types only: line, card, bar, column, choropleth. No slicers/tabs/Interval.
- `value_format` fully wired (OR-162): `options.value_format` on card/column/bar/table +
  table `formats:` + theme `formats:` presets.
- Client scripts (live + static parity, in `make_app.py`): `_SCROLLSPY_JS`,
  `_SIDEBAR_TOGGLE_JS`, `_RESIZE_JS`. Static export injects all three via `build._document`.

## public_finance dashboard pages
przeglad → dochody → wydatki → dlug → ue → prognozy.

## Engine-tree state
- Clean except known untracked PO/bot WIP (never commit): `infra/discord-bot/bot.py`,
  `infra/systemd/or-*-bot.service`, `logs/`, `.claude/scheduled_tasks.lock`,
  `products/blog/reviews/release-report.md`, stray `open-reporting-full.tar.gz` (root).
- 16 dashboards static; all rebuilt on HEAD `c9d7a687` (run #67 fleet redeploy).

## Standing blockers (all PO-side)
- **OR-168** — root-fixed (#64); only `systemctl disable or-{16}` remains (sudo gap).
- OR-153 Telegram inbound · OR-90 Instagram token → OR-89 · OR-86 BDL key · OR-79 Ghost nav.
- On hold under static model: OR-160 cross-filter, OR-161 date-picker (backend-only).

## Content
- 18 articles published; release sweep clean (0 drafts). Run `release_pipeline.py` each run.

## Lessons
- **Measure live bounding boxes before re-diagnosing** (#66, #67): the "legend clip" was
  actually a chart that rendered 1084px wide in a 628px card. Playwright bbox readout, not a
  pixel-eyeball, found it. A vertical legend "fix" made it worse — measuring caught that too.
- **A below-the-fold Plotly chart needs an explicit resize** (#67): it sizes to a stale/wide
  container at newPlot and never reflows on its own. `Plotly.Plots.resize` after layout settles.
- **The page canvas is fixed-height/overflow-hidden** (#66): never stack full rows; verify the
  WHOLE rendered card is visible.
- **Check whether a backlog item is already half-done before building** (#65).
