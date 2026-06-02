# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-06-02 (run #45 — labour_market EU-27 data + ranking fix, OR-166) -->

## Run #45 — fix labour_market only-Poland EU pages + mis-ranking. HEAD 05719c6e

**The flagship bug found & fixed this run.** labour_market's "Polska na tle UE-27" page (+
the bezrobocie EU-unemployment chart) rendered a **single Poland bar** and mis-ranked it.
Two root causes, both fixed:
1. **Data** — Eurostat `lfsa_ergan`/`lfsa_argan`/`une_rt_a` were pinned `geo=PL` in the
   catalogue → only Poland ever ingested. Widened to `geo=ALL_GEOS` (CSV seed
   `products/database/data/domain_detail_sources.csv` + live PG catalogue), re-ingested,
   rebuilt `fact_labour_overview` → now **35–37 geos/yr**. KPIs + PL trends filter
   `geo:PL` so non-breaking.
2. **Aggregation** — the EU bars lacked `dual_year`, so `agg:average` averaged each country
   over its whole history (PL → ~66.8, mis-ranked 2nd-worst). Added `dual_year:true` →
   latest-2-years cross-section; **PL now ranks correctly 13th (78.8% 2025)**.

Layout: ue → side-by-side 50/50 (no clip); bezrobocie → side-by-side trends + full-width
ranking; inline 27-row tables → `download:true`. Commits `ce2dca37` (data) + `05719c6e`
(dashboard), pushed. OR-166 (Bug+Data) closed Done. Live-verified 1600×900: 0px clip,
correct PL rank, KPIs 78.8/64.3/3.1, all 16 dashboards + www HTTP 200.

**Ops note:** re-ingest needs the DuckDB write lock (held by or-education.service, whose
MainPID *is* the dbr-serve process). Used the run_daily pattern: stop 16 → ingest →
`dbt run --select stg_eurostat lab_indicators fact_labour_overview fact_labour_wages` →
restart 16. 16 services booting at once take ~30s to all answer 200 — poll, don't trust
the first check.

## Resolved this run
- **#44's "other 15 dashboards clip" worry was overstated.** A fleet-wide Playwright
  clip-sweep showed **only labour_market** clipped; the other 15 are clean (≤6px SVG
  artifact). No further fill-restructure pass needed.
- The only-Poland EU-comparison bug was **labour-specific** — only labour_market &
  public_finance have 27-country EU visuals, and pf already used `dual_year` + ALL_GEOS.

## Lessons
- A "200 OK + no clip" page can still be **misleading**: always screenshot a comparison
  chart and sanity-check that the highlighted entity sits where the data says it should.
- `dual_year:true` is what makes a dbr cross-section bar **point-in-time**; without it,
  `agg:average` silently averages over all history → wrong rankings for series with
  uneven history lengths. Any new EU/cross-section ranking bar needs `dual_year` (or an
  explicit year filter).
- dbr `bar` is horizontal — correct for country rankings (metric x, country y).

## Recent commits
- 05719c6e fix(dashboards): labour_market EU pages — correct ranking + fixed-canvas fill
- ce2dca37 fix(data): widen labour EU-comparison series to ALL_GEOS
- 401b9a35 style(dbr): lighten dashboard canvas background #E4EAF0 -> #EDF1F6
- 0a19fbdf docs: run #44 — no internal scroll + public_finance fill-restructure
- ccd1cfe4 feat(dashboards): public_finance — one fill-row per page so charts fill

## What's next
- **OR-165** (open): fleet-wide `footer_updated` auto-derive from displayed actual
  (non-forecast) year — engine-plane, branch+PR+fleet-redeploy.
- **Other dashboards may share the dual_year gap** on any single-year cross-section bar —
  spot-check if a future page looks mis-ranked. (Only labour/pf have EU rankings today.)
- Phase-3 data depth (OR-86, BDL) blocked on PO `BDL_API_KEY`.

## Standing blockers (all PO-side)
- OR-153 Telegram inbound · OR-90 Instagram token → OR-89 · OR-86 BDL key · OR-79 Ghost nav
- Known untracked PO/bot WIP in tree (do not commit): `infra/discord-bot/bot.py`,
  `infra/systemd/or-*-bot.service`, `logs/`, `.claude/scheduled_tasks.lock`.
