# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-06-06 (run #69 — article #20, regional inequality) -->

## Run #69 — Article #20 shipped: regional inequality (Polska A / Polska B)

Continued the In Progress item OR-170 (the draft `or-170-regiony.md` was authored on disk
last run, awaiting the gate). Ran the Step 2b sweep → it BLOCKED on first pass
(content BLOCK + domain BLOCK; analytical CONDITIONAL).

**Topic:** regional GDP per capita inequality, NUTS2 2000–2024, from
`curated.fact_macro_regional`. β-convergence (relative) vs widening absolute gap.

**The real BLOCK (domain):** core thesis claimed "all seventeen regions grew faster than
the capital" — **false**. Queried `fact_macro_regional` directly: four of the 16 non-capital
regions grew SLOWER than Warszawski stołeczny (×4.27): Warmińsko-Mazurskie ×4.24,
Kujawsko-Pomorskie ×4.14, Lubuskie ×4.11, Zachodniopomorskie ×3.85. Correct = 12 of 16.
**Content BLOCK:** migration passage made an unsupported causal claim (no migration data).

**Fixed all inline (0 spawns):** corrected the count in lead + growth section (named all four
laggards with real multiples); reframed migration as explicit hypothesis; trimmed headline
13→12 words; added PL91/PL92 retrospective-disaggregation + ESA2010 caveats; added
σ-convergence naming, post-2016-concentrated timeline note, EU peer-dispersion benchmark,
and PL92 commuter-effect note. Re-gate (--force) PASSED: content CONDITIONAL, analytical
PASS, domain CONDITIONAL.

**Live:** https://www.open-reporting.dev/polska-a-polska-b-nierownosci-regionalne-pkb-2024/ → 200.
Blog now **20 published articles**. OR-170 → Done.

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
- Re-review a fixed draft: `release_pipeline.py <draft.md> --force` (single article,
  3 reviewers, ~6 min). Published drafts stay in `products/blog/drafts/` (state tracked via
  Ghost slug lookup, not file moves). Review reports: `products/blog/reviews/<slug>-review.md`.
- `strip_verification_comment` strips the internal `<!-- WERYFIKACJA ... -->` block before
  Ghost render — internal checklists never ship.
- **20 articles published.** Each run starts with sweep clean unless a new draft was authored.

## Lesson (run #69)
- **Verify universal quantifiers ("all N", "every region") against the warehouse before
  gating** — the brief feeding a draft asserted "all 17 regions faster than the capital";
  a `fact_macro_regional` query found four exceptions. Don't trust briefed aggregate claims;
  query the source. (Pattern from #68: let the gate block, then fix precisely + inline.)

## dbr visual notes
- **bar = HORIZONTAL** (metric on x). Vertical categorical → use **column**. Bitten 3×.
- **choropleth:** warehouse `geo` == GISCO `NUTS_ID`; filter EU27_2020/EA20; don't bake height.
- Production visual types only: line, card, bar, column, choropleth. No slicers/tabs/Interval.
- `value_format` fully wired (#65): `options.value_format` on card/column/bar/table.
- Below-the-fold charts auto-resize on load (#67 `_RESIZE_JS`).

## public_finance dashboard pages
przeglad → dochody → wydatki → dlug → ue → prognozy.

## Engine-tree state
- Clean except known untracked PO/bot WIP (never commit): `infra/discord-bot/bot.py`,
  `infra/systemd/or-*-bot.service`, `logs/`, `.claude/scheduled_tasks.lock`,
  `products/blog/reviews/release-report.md`.
- 16 dashboards static; all on HEAD from run #67 fleet redeploy. No dbr code change in #68/#69
  → no fleet redeploy needed.

## Standing blockers (all PO-side)
- **OR-168** — root-fixed (#64); only `systemctl disable or-{16}` remains (sudo gap).
- OR-153 Telegram inbound · OR-90 Instagram token → OR-89 · OR-86 BDL key · OR-79 Ghost nav.
- On hold under static model: OR-160 cross-filter, OR-161 date-picker (backend-only).
