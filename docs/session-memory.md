# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-06-06 (run #70 — QUIET RUN: backlog grooming + data-quality) -->

## Run #70 — QUIET RUN: groomed 3 stale finance-v2 issues + data-quality check

No actionable un-blocked build work this run. Roadmap Themes 1–3 essentially complete
(16 domain dashboards live, 20 articles published); remaining backlog is PO-blocked,
static-deferred, or stale. Per the "Nothing-to-do" protocol → grooming (b) + data check (c).

**Git hygiene at smoke check:** tree showed 68 `D` entries under `docs/visualization/` paired
with untracked dirs (benign index desync from a bot directory-recreate). Verified all 68
on-disk files byte-identical to HEAD, then `git checkout HEAD -- docs/visualization` → clean.

**Canceled 3 obsolete finance issues** (all target the retired `products/dashboards/finance/app.py`,
replaced by the `public_finance` dbr dashboard): **OR-110** (v2 programme), **OR-112**
(expenditure tab), **OR-113** (debt-management tab). Valuable subset already lives on
Wydatki/Dług/Dochody pages; remaining asks need a treemap primitive (not in production set:
line/card/bar/column/choropleth) and MF granular debt-structure data we don't ingest. Each got
a rationale comment pointing to the live replacement.

**Data-quality (DuckDB direct, read-only):** 56 datasets / 98,091 obs / latest 2026-S1 / fetched
2026-06-05 22:08 UTC; all 21 `curated.fact_*` tables populated. No anomalies. NOTE: CLAUDE.md's
`from dbr.semantic import query` snippet is stale — use `duckdb.connect(read_only=True)` directly.

## KEY OPS MODEL (current — unchanged since #64)
- Dashboards = **static HTML** in `infra/nginx/html/<domain>/index.html` (gitignored build
  artifacts). NO `dbr serve`, NO `or-<domain>.service`, NO ports.
- A dashboard YAML change OR a data refresh needs a **REBUILD** to show:
  single dashboard → `dbr run products/dashboards/<domain>` (build + nginx route + reload).
  Whole fleet / after any `packages/dbr/` edit → commit FIRST, then
  `python3 infra/scheduler/redeploy_dashboards.py` (builds 16 → web root, verifies each
  `<meta dbr-build>` == HEAD; non-zero exit = NOT resolved).
- Live verify: `curl -s https://portal.open-reporting.dev/<domain>/` → 200 + stamp==HEAD +
  Plotly content. For layout/visual changes, screenshot (Playwright) — curl can't see layout.
- **Page layout is a fixed single-screen canvas with `overflow:hidden`.** Do NOT stack
  full-height rows (clips). Side-by-side widths (e.g. 60/40) within one row are safe.

## Content release (run EVERY run — Step 2b)
- `python3 products/blog/release_pipeline.py` → reviews each unreviewed draft through 3
  reviewers (content + analytical + domain Opus), auto-publishes those with NO BLOCK.
  `gate_passed`: blocks only on BLOCK/ERROR; **CONDITIONAL counts as pass**.
- Re-review a fixed draft: `release_pipeline.py <draft.md> --force` (single article).
  Published drafts stay in `products/blog/drafts/` (state via Ghost slug lookup, not file moves).
- **20 articles published.** Each run starts with sweep clean unless a new draft was authored.

## Lesson (run #70)
- **At smoke check, a `D`+untracked pairing on a whole directory is usually a benign index
  desync, not lost work.** Verify on-disk content == HEAD (`cmp` loop) BEFORE acting, then
  `git checkout HEAD -- <dir>` restores tracking with zero content change. Don't panic-commit.

## dbr visual notes
- **bar = HORIZONTAL** (metric on x). Vertical categorical → use **column**. Bitten 3×.
- **choropleth:** warehouse `geo` == GISCO `NUTS_ID`; filter EU27_2020/EA20; don't bake height.
- Production visual types only: line, card, bar, column, choropleth. No treemap/donut/slicers/tabs.
- `value_format` fully wired (#65). Below-the-fold charts auto-resize on load (#67 `_RESIZE_JS`).

## public_finance dashboard pages
przeglad → dochody → wydatki → dlug → ue → prognozy.

## Engine-tree state
- Clean except known untracked PO/bot WIP (never commit): `infra/discord-bot/bot.py`,
  `infra/systemd/or-*-bot.service`, `logs/`, `.claude/scheduled_tasks.lock`,
  `products/blog/reviews/release-report.md`.
- 16 dashboards static; all on HEAD from #67 fleet redeploy. No dbr code change since → no
  fleet redeploy needed.

## Standing blockers (all PO-side)
- **OR-168** — root-fixed (#64); only `systemctl disable or-{16}` remains (sudo gap).
- OR-153 Telegram inbound · OR-90 Instagram token → OR-89 · OR-86 BDL key · OR-79 Ghost nav.
- On hold under static model: OR-160 cross-filter, OR-161 date-picker (backend-only).
- Canceled #70: OR-110/112/113 (finance-v2, app.py-era — superseded by public_finance dbr).
