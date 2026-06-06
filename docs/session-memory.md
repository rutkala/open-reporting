# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-06-06 (run #71 — closed OR-168 Urgent P1: OOM resolved by static architecture) -->

## Run #71 — Closed OR-168 (Urgent/Infra): VPS OOM fleet-cull resolved by architecture

The standing-blocker list was stale. OR-168 had been carried for three runs (#68–#70) as
PO-blocked ("needs swap" / "systemctl disable — sudo gap"). Re-verified against live state:
both framings are obsolete. The static-HTML migration (the OR-168 work itself) removed the
OOM vector entirely, and the 16 units are **already disabled**. Closed → Done.

**Verification (run #71):** no `dbr serve`/dash processes; all 16 `or-<domain>.service` =
`active=inactive enabled=disabled`; all 16 domains 200 (static HTML, stamp c9d7a687); `free -h`
= 1.5 GiB available (vs ~256 MiB under the old fleet); nginx 7d log = 72 502s ALL on 02–03 Jun
(runs #46/#58), most recent 2026-06-03 12:00:13, **zero since**. No PO swap/RAM action needed —
criterion #1's durable-mechanism clause is met, strictly stronger than the swap stopgap.

**Loose end (zero risk):** 16 leftover `/etc/systemd/system/or-<domain>.service` files remain on
disk, disabled+inactive. Removal needs `rm` (outside NOPASSWD allowlist) → optional cosmetic
cleanup, not a blocker.

**Lesson:** the standing-blockers list can rot. An item fixed at the root in #64 kept being
recopied as PO-blocked on a stale remediation framing. Re-verify blockers against live state
periodically instead of recopying.

## KEY OPS MODEL (current — unchanged since #64)
- Dashboards = **static HTML** in `infra/nginx/html/<domain>/index.html` (gitignored build
  artifacts). NO `dbr serve`, NO `or-<domain>.service` running, NO ports. Confirmed #71: all 16
  units inactive+disabled, no dashboard processes, 1.5 GiB free.
- A dashboard YAML change OR a data refresh needs a **REBUILD** to show:
  single dashboard → `dbr run products/dashboards/<domain>` (build + nginx route + reload).
  Whole fleet / after any `packages/dbr/` edit → commit FIRST, then
  `python3 infra/scheduler/redeploy_dashboards.py` (builds 16 → web root, verifies each
  `<meta dbr-build>` == HEAD; non-zero exit = NOT resolved).
- Live verify: `curl -s https://portal.open-reporting.dev/<domain>/` → 200 + stamp + Plotly
  content. For layout/visual changes, screenshot (Playwright) — curl can't see layout.
- **Page layout is a fixed single-screen canvas with `overflow:hidden`.** Do NOT stack
  full-height rows (clips). Side-by-side widths (e.g. 60/40) within one row are safe.

## Content release (run EVERY run — Step 2b)
- `python3 products/blog/release_pipeline.py` → reviews each unreviewed draft through 3
  reviewers (content + analytical + domain Opus), auto-publishes those with NO BLOCK.
  `gate_passed`: blocks only on BLOCK/ERROR; **CONDITIONAL counts as pass**.
- Re-review a fixed draft: `release_pipeline.py <draft.md> --force` (single article).
  Published drafts stay in `products/blog/drafts/` (state via Ghost slug lookup, not file moves).
- **20 articles published.** Each run starts with sweep clean unless a new draft was authored.

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
- 16 dashboards static; all on stamp c9d7a687 (#67). No dbr code change since → no fleet
  redeploy needed.

## Standing blockers (all PO-side — re-verified #71)
- OR-153 Telegram inbound · OR-90 Instagram token → OR-89 · OR-86 BDL key · OR-79 Ghost nav.
- On hold under static model: OR-160 cross-filter, OR-161 date-picker (backend-only).
- **CLOSED #71: OR-168** (OOM — resolved by static architecture; no PO swap needed).
- Canceled #70: OR-110/112/113 (finance-v2, app.py-era — superseded by public_finance dbr).

## Followup (minor, deferred)
- CLAUDE.md Development Commands shows a stale DuckDB snippet (`from dbr.semantic import query`)
  — use `duckdb.connect(read_only=True)`. Too trivial to warrant a flagged CLAUDE.md edit alone.
- 16 leftover `or-<domain>.service` unit files on disk (disabled, zero risk) — `rm` needs sudo
  outside allowlist; optional PO-assisted cleanup.
