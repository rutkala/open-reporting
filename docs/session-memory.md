# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-06-07 (run #72 — shipped OR-171 dbr design refresh; flagged foreign Antigravity workstream) -->

## Run #72 — Shipped OR-171 (dbr design refresh) + flagged a foreign workstream

Started with a NOT-clean tree: two foreign workstreams new since #71, neither from PO channels
(Telegram inbox empty, no Strategic label).

1. **dbr design overhaul** — `ORIGINAL_REQUEST.md` ("Integrity mode: benchmark", 2026-06-06 19:56Z).
   Uncommitted edits to `packages/dbr/{theme.yaml, make_app.py, build.py}` + throwaway scripts
   (`verify_mobile_layout.py`, `fix_and_test.py`, `lin_*.py`, `build_temp/`). `PROJECT.md` claimed
   milestones DONE but nothing was committed/deployed — claims were hallucinated.
2. **"Antigravity V2" pivot** — commit `00e7b85e` removed telegram+discord bots; uncommitted
   `docs/ROADMAP.md` rewrite ("Open Reporting V2 — AI-Native Media Company", "Author: Antigravity
   Project Lead") + untracked `infra/nginx/html/team.html`, `infra/scheduler/team_workspace_feed.py`.
   **Contradicts CLAUDE.md (8-bot Discord fleet). LEFT UNTOUCHED — flagged to PO for direction.**

**Action:** finished workstream 1 (verified sound: builds clean, renders well across line/KPI/
choropleth/bar, contrast improves, glassmorphism subtle). Committed ONLY the 3 dbr files via
PR #67 → main `19f6a4b2`. `redeploy_dashboards.py` rebuilt all 16 (exit 0, stamps PASS); live
URLs 200 + stamp `19f6a4b2`; Playwright confirms live render. OR-171 → Done. No reviewer spawn
(styling-only, verified). Left ROADMAP/bot-removal/scripts alone (not mine; one-logical-change).

**OPEN QUESTION FOR PO:** is the Antigravity pivot (bot removal + ROADMAP V2 + team-feed) sanctioned
— retire CLAUDE.md + the Discord fleet — or a rogue session to revert? Blocked on PO direction.

## KEY OPS MODEL (current)
- Dashboards = **static HTML** in `infra/nginx/html/<domain>/index.html` (gitignored build artifacts).
  NO `dbr serve`, NO `or-<domain>.service` running, NO ports. 16 units inactive+disabled, ~1.5 GiB free.
- YAML/data change → rebuild to show: single → `dbr run products/dashboards/<domain>`;
  fleet / any `packages/dbr/` edit → commit FIRST, then `python3 infra/scheduler/redeploy_dashboards.py`
  (builds 16 → web root, verifies `<meta dbr-build>` == HEAD; non-zero exit = NOT resolved).
- Live verify: `curl -s .../<domain>/` → 200 + stamp + Plotly. Layout/visual → Playwright screenshot.
- **Page = fixed single-screen canvas `overflow:hidden`.** Don't stack full-height rows (clips).
  Side-by-side widths (60/40) within one row are safe.
- **Current dbr HEAD stamp: `19f6a4b2`** (#72 design refresh). All 16 on it.

## dbr design system (post-#72, OR-171)
- Theme tokens now exposed as `:root` CSS custom properties via `get_css_vars()` in make_app.py;
  both static (`build.py`) and live Dash (`_INDEX_STRING`) paths inject them. Edit colours/spacing
  in `theme.yaml` → rebuild; CSS uses `var(--teal-primary)` etc.
- Palette: Slate/Tailwind (teal `#3B8B94`, azure `#3A6FA4`, canvas `#F8FAFC`, text `#1E293B`).
  16px card radius, soft shadow, 24/32px spacing, glassmorphism (backdrop-blur) + hover-lift.

## dbr visual notes
- **bar = HORIZONTAL** (metric on x). Vertical categorical → use **column**. Bitten 3×.
- choropleth: warehouse `geo` == GISCO `NUTS_ID`; filter EU27_2020/EA20; don't bake height.
- Production visual types only: line, card, bar, column, choropleth. No treemap/donut/slicers/tabs.
- `value_format` fully wired (#65). Below-the-fold charts auto-resize on load (#67 `_RESIZE_JS`).

## public_finance dashboard pages
przeglad → dochody → wydatki → dlug → ue → prognozy.

## Content release (run EVERY run — Step 2b)
- `python3 products/blog/release_pipeline.py` → reviews unreviewed drafts through 3 reviewers
  (content + analytical + domain Opus), auto-publishes those with NO BLOCK (CONDITIONAL = pass).
- Re-review fixed draft: `release_pipeline.py <draft.md> --force`. State via Ghost slug lookup.
- **20 articles published.** Sweep clean unless a new draft was authored.

## Engine-tree state (CAUTION — currently dirty with foreign WIP)
- Uncommitted/untracked foreign WIP NOT to commit blindly: `docs/ROADMAP.md` (Antigravity rewrite),
  `infra/nginx/html/team.html`, `infra/scheduler/team_workspace_feed.py`, `ORIGINAL_REQUEST.md`,
  `PROJECT.md`, `fix_and_test.py`, `lin_finish.py`, `lin_reset.py`, `verify_mobile_layout.py`,
  `build_temp/`, `logs/`, `products/blog/reviews/release-report.md`, `.claude/scheduled_tasks.lock`.
- The 3 dbr files from the overhaul are now COMMITTED (#72). 16 dashboards static, all stamp `19f6a4b2`.

## Standing blockers (all PO-side)
- OR-153 Telegram inbound · OR-90 Instagram token → OR-89 · OR-86 BDL key · OR-79 Ghost nav.
- On hold under static model: OR-160 cross-filter, OR-161 date-picker (backend-only).
- **NEW #72:** Antigravity-pivot direction (bot removal + ROADMAP V2) — needs PO decision.

## Followup (minor, deferred)
- CLAUDE.md Development Commands shows a stale DuckDB snippet (`from dbr.semantic import query`)
  — use `duckdb.connect(read_only=True)`. Too trivial to warrant a flagged CLAUDE.md edit alone.
- 16 leftover `or-<domain>.service` unit files on disk (disabled, zero risk) — `rm` needs sudo.
