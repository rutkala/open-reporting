# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-06-05 (run #66 — OR-111 revenue page shipped) -->

## Run #66 — OR-111 shipped: Public Finance revenue page ("dochody")

Filled the biggest gap in the flagship dashboard — it had deficit/debt/expenditure/EU/
forecast pages but **no revenue page**. Fully in my control (static, no PO blocker).

**Shipped (HEAD `03ce4515`, pushed to main):** new `dochody` page "Skąd państwo bierze
pieniądze?", inserted between overview and expenditure. Two charts:
- **revenue_trend** — multi-metric line: total revenue + social contributions + indirect
  taxes + income taxes, PL 1995–2025, all % PKB.
- **eu_revenue** — peer-benchmark bar, Poland highlighted vs 8 curated EU peers
  (V4 + DE + SE/FR high anchors + RO/IE low). Poland ~44% PKB = mid-low.

Re-scoped OR-111 from the retired `app.py` (donut/scatter, not in the static visual set)
to dbr line+bar. Reused existing `finance_revenue_expenditure` metrics — no new data.

**Visual review (live Playwright screenshots) caught + fixed two real defects:**
- Full 27-country EU bar was illegible at half-width and **Poland's highlighted bar lost
  its label** → curated to 9 peers; Poland now labelled + highlighted.
- Widened line to 60% (EU bar 40%) so its legend renders.
Decoded the served Plotly arrays to confirm the line spans 1995–2025 (total ends 43.6) —
an apparent ~2012 cutoff was a pixel misread; data was always complete.

**Rejected:** `label_endpoints` (long PL labels clip at right under card `overflow:hidden`);
stacked full-width rows (page is a **fixed single-screen canvas, `overflow:hidden`** —
stacking clipped both charts, hid Poland). Side-by-side is the only all-visible layout.

**Known minor → filed OR-169:** at 60% width the 4-series line legend clips the 4th label
(line-legend wrap limitation, engine plane). Queued, not forced under time pressure.

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

## dbr visual notes
- **bar = HORIZONTAL** (metric on x). Vertical categorical → use **column**. Bitten 3×.
- **Multi-metric line:** `y: { metric: [a, b, c] }` → one trace per metric, labelled by
  metric.label, shown in legend. Long PL labels overflow a narrow legend (see OR-169).
- **bar `highlight` + 27 categories at half-width** thins y-tick labels — the highlighted
  category can lose its label. Curate the category set for narrow slots.
- **choropleth:** warehouse `geo` == GISCO `NUTS_ID`; filter EU27_2020/EA20; don't bake height.
- Production visual types only: line, card, bar, column, choropleth. No slicers/tabs/Interval.
- `value_format` fully wired (OR-162): `options.value_format` on card/column/bar/table +
  table `formats:` + theme `formats:` presets.

## public_finance dashboard pages (post #66)
przeglad → **dochody (NEW)** → wydatki → dlug → ue → prognozy.

## Engine-tree state
- Clean except known untracked PO/bot WIP (never commit): `infra/discord-bot/bot.py`,
  `infra/systemd/or-*-bot.service`, `logs/`, `.claude/scheduled_tasks.lock`,
  `products/blog/reviews/release-report.md`, stray `open-reporting-full.tar.gz` (root).
- 16 dashboards static; public_finance on stamp == HEAD (03ce4515). Others on their last
  build commit (normal — only rebuilt on their own YAML/data change).

## Standing blockers (all PO-side)
- **OR-168** — root-fixed (#64); only `systemctl disable or-{16}` remains (sudo gap).
- OR-153 Telegram inbound · OR-90 Instagram token → OR-89 · OR-86 BDL key · OR-79 Ghost nav.
- On hold under static model: OR-160 cross-filter, OR-161 date-picker (backend-only).
- OR-169 line-legend wrap (engine; queued from #66).

## Content
- 18 articles published; release sweep clean (0 drafts). Run `release_pipeline.py` each run.

## Lessons
- **Screenshot, then verify pixels against the source data before re-diagnosing** (#66): an
  apparent line cutoff at ~2012 was a misread — decoding the served Plotly arrays proved
  1995–2025 complete. Don't act on a pixel read alone.
- **The page canvas is fixed-height/overflow-hidden** (#66): never stack full rows; it clips
  silently (hid the highlighted country). Verify the WHOLE rendered card is visible.
- **27 categories don't fit a half-width bar** (#66): curate to a legible peer set so the
  highlighted item keeps its label.
- **Check whether a backlog item is already half-done before building** (#65).
- **A "no-op" must be byte-exact** (#65).
