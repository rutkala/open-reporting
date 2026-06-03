# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-06-03 (run #57 — OR-167 voivodeship GDP map live) -->

## Run #57 — OR-167 voivodeship (NUTS2) GDP-per-capita map live. HEAD 70f8f0e4

**Shipped the first voivodeship choropleth end-to-end** on the National Accounts
dashboard ("Regiony" page) — completing the regional-map arc started in #54
(dim_geo NUTS2) and #56 (poland_nuts2 geo mechanism).

**Data plane (commit 85569855):**
- `fact_macro_regional` — (geo, period_year) grain, restricted to the 17 NUTS2
  voivodeships via `dim_geo.geo_level='nuts2'` (PL-only seed → exactly the 17
  PL2x…PL9x codes; matches bundled `poland_nuts2` NUTS_ID 1:1, no aggregate
  leakage). 425 rows 2000–2024, 17 in 2024. dbt tests PASS=3.
- `macro_regional` semantic model → metric `gdp_per_capita_regional` (Eurostat
  nama_10r_2gdp, EUR_HAB, current-price EUR/capita). Verified 17 regions via
  semantic_query_data with geo + geo__country_name_pl.
- Built on a /tmp COPY first, then promoted via stop-16 → dbt run → restart-16
  lock pattern (run #54).

**Engine fix (branch → critic APPROVE → merge ddc2cd3b, commits 7291111d+f1de9c3e):**
- choropleth baked `fig.layout.height` onto a non-responsive dcc.Graph → map SVG
  overflowed its definite-height flex cell into the next row. Invisible on wide
  EU map (centres w/ vertical margin); tall Poland exposed it (visible overlap).
- Routed through `chart_with_optional_table` like bar/line/area (clears height,
  responsive cell-fill, `.dbr-fill-graph` mobile pin, + CSV download). Fixes the
  latent EU-map overlap too. `options.height` now ignored on desktop (cell-driven).

**Layout (commit 70f8f0e4, YAML):** map+bar side-by-side (52/48) in one row so the
17-region bar gets full viewport-row height — all labels legible (was cramped stacked).

**Verified live (Playwright):** fleet redeploy → all 16 on ddc2cd3b after engine
change. Poland map renders (Warsaw darkest ~45.3k, Lubelskie ~16k, Teal scale),
no overlap (map bottom 545 < bar top 634), all 17 sorted labels show, Warsaw azure.
EU map re-checked, no regression. national_accounts on HEAD 70f8f0e4 (YAML-only).

## Choropleth maintainer notes (updated)
- `packages/dbr/src/dbr/visuals/choropleth.py`. `_BUNDLED_GEOJSON`: name →
  (geojson path, featureidkey, view-or-None). `options.geojson` picks a bundled
  map; poland_nuts2 view=None → fitbounds="locations".
- **Renders as a fill-chart now** (since #57): no baked pixel height; fills its
  flex cell via chart_with_optional_table. Add new maps the same way; don't bake
  fig.layout.height on a geo (it overflows the row — see #57 lesson).
- Design rests on warehouse `geo` == GISCO `NUTS_ID`. YAML must filter aggregate
  codes (EU27_2020/EA20) or they silently drop (a warning logs when they do).

## Recent commits
- 70f8f0e4 feat(national_accounts): map + ranked bar side-by-side on Regiony (OR-167)
- ddc2cd3b Merge OR-167: choropleth fills flex cell (fixes Poland map overlap)
- f1de9c3e docs(dbr): correct choropleth options.height docstring
- 7291111d fix(dbr): choropleth fills its flex cell instead of fixed height (OR-167)
- 85569855 feat(warehouse): voivodeship GDP-per-capita NUTS2 regional map (OR-167)
- 0e462319 docs: run #56 — OR-159 choropleth live (EU deficit map)

## What's next (unblocked, autonomous)
- **More NUTS2 metrics** (data-plane, always safe): only gdp_per_capita_regional
  reaches full 17-NUTS2 coverage cleanly from mac_indicators. Others (employment/
  unemployment/poverty regional) are filtered out of the by-domain intermediates
  — exposing them needs an intermediate change first. A follow-up could add a
  regional page to labour_market once lab_indicators carries the NUTS2 rows.
- dbr feature backlog (engine, branch+PR+critic+redeploy, one per run, don't batch):
  **OR-160 cross-filter (High)**, OR-161 date slicer, OR-162 number-format.

## Engine-tree state
- Clean except known untracked PO/bot WIP (never commit): `infra/discord-bot/bot.py`,
  `infra/systemd/or-*-bot.service`, `logs/`, `.claude/scheduled_tasks.lock`,
  `products/blog/reviews/release-report.md` (regenerated each release sweep).
- NB: 15 non-national_accounts dashboards serve stamp ddc2cd3b (engine HEAD at
  redeploy); the two later commits are national_accounts YAML only — functionally
  current, stamp lag is cosmetic. Next engine change's redeploy resyncs them.

## Prod-build-with-lock pattern (reusable, #54/#57)
dbt build needing the DuckDB write lock: build on a /tmp COPY to verify → stop 16
→ dbt run+test on prod → restart 16 → verify rows + stamp. ~1 min planned outage.

## Standing blockers (all PO-side)
- OR-153 Telegram inbound · OR-90 Instagram token → OR-89 · OR-86 BDL key →
  crime/agri/business dashboards · OR-79 Ghost nav.

## Lessons
- **A "verified clean" wide map can mask a layout bug a tall map exposes.** The EU
  choropleth had the identical row overlap since #56 but transparent margins hid
  it; Poland filling the frame made it visible. Measure adjacent-row bounding
  boxes — don't trust the eye on one geography.
- **A registered/used visual can still be subtly broken.** choropleth rendered on
  the EU page but was opting out of the layout cascade the whole time.
- **Plotly built-in geo scope can't match Eurostat alpha-2** (only ISO-3 / names).
  EU maps use bundled GISCO geojson keyed on NUTS_ID == our `geo`.
