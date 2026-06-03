# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-06-03 (run #56 — OR-159 choropleth live) -->

## Run #56 — OR-159 dbr choropleth live (EU deficit map). HEAD d3d6dc14

**Shipped the choropleth visual end-to-end.** It was coded + registered (May 31) but
never usable: required an absolute `geojson_path`, hard-coded a wrong featureidkey
(`properties.nuts_id` vs GISCO `NUTS_ID`), and its no-geojson path used Plotly
`locationmode`, which can't match Eurostat alpha-2 codes (Plotly only takes ISO-3 /
country names; Eurostat uses EL/UK). So it had never rendered on a dashboard.

**Delivered (branch → merged to main, HEAD d3d6dc14, 3 commits):**
- Bundled two GISCO NUTS 2021 GeoJSONs keyed on `NUTS_ID` == warehouse `geo` 1:1:
  `europe_countries` (32 EU/EFTA, 1:20M, 261KB) + `poland_nuts2` (17 voivodeships,
  1:3M, 151KB). 17/17 NUTS2 codes verified against dim_geo. Provenance in
  `packages/dbr/src/dbr/data/README.md`; `data/*.geojson` is package-data.
- `options.geojson: <name>` → bundled map + correct featureidkey + default viewport
  (continental-Europe lon/lat clip; fit-to-locations for PL). New `color_midpoint`
  (zmid) for diverging metrics, formatted hover, themed colorbar, unmatched-location
  warning log (silent-drop guard).
- First live use: EU-27 deficit choropleth on public_finance "Polska na tle UE-27"
  page (RdYlGn around 0), above the existing ranked deficit/debt bars.

**architecture-critic APPROVE.** Took both follow-ups (README provenance + warning log).

**Verified live (browser):** all 16 on d3d6dc14; Playwright on portal UE page — map
renders (Romania darkest, Poland red, Ireland/Denmark green), layout clean, map plot a
clean 1044×440 box. `poland_nuts2` path factory-render-verified offline (Poland shape
incl. Warsaw enclave) — ready but no dashboard binds it yet.

**Linear:** OR-159 → Done. **OR-167 created** (High, Feature+Data): voivodeship map needs
an exposed NUTS2-grain metric — none in the semantic layer yet despite ~26 regional
indicators in all_indicators. Geo mechanism is done, so OR-167 is data-plane only.

## How the choropleth works (for next maintainer)
- `packages/dbr/src/dbr/visuals/choropleth.py`. `_BUNDLED_GEOJSON` dict:
  name → (geojson path, featureidkey, view-or-None). `options.geojson` picks a bundled
  map; `options.geojson_path` for arbitrary files; `feature_id_key` override.
- The whole design rests on warehouse `geo` == GISCO `NUTS_ID` (Eurostat 2-letter incl.
  EL/UK at level 0; PL21… at level 2). YAML must filter out aggregate codes
  (EU27_2020/EA20) or they're silently dropped — a warning now logs when that happens.
- EU country maps need the bundled `europe_countries` geojson, NOT plotly scope mode
  (alpha-2 incompatible). `scope: world` + ISO-3 still works for non-Eurostat global data.

## OR-167 next (voivodeship map, data-plane, unblocked)
- Expose 1–3 NUTS2 metrics in `products/warehouse/models/semantic/` (candidates:
  lab.employment_rate_regional, mac.gdp_per_capita_regional, soc.at_risk_poverty_rate).
  Confirm `semantic_query_data(metric, group_by=['geo'])` returns 17 PL regions.
- Add a voivodeship choropleth (`geojson: poland_nuts2`, sequential Teal scale) + ranked
  bar pairing on a domain dashboard. Build with the DuckDB-lock pattern (stop services →
  dbt run → restart). Geo mechanism already verified — data-only work.

## Recent commits
- d3d6dc14 Merge OR-159: dbr choropleth bundled geographies (EU + Poland NUTS2 maps)
- f3bd2e29 docs(dbr): choropleth geojson provenance + unmatched-location warning
- 64f10c4c feat(dbr): choropleth bundled geographies — EU + Poland NUTS2 maps (OR-159)
- 516f80e4 docs: run #55 — mobile page header covers dashboard header on scroll
- 983461cf feat(dbr): page header covers dashboard header on mobile scroll

## What's next (unblocked, autonomous)
- **OR-167 voivodeship choropleth (High)** — data-plane, the natural next pick (geo done).
- dbr feature backlog (engine, branch+PR+critic+redeploy, one per run, don't batch):
  **OR-160 cross-filter (High)**, OR-161 date slicer, OR-162 number-format.
- Data-plane always safe: more NUTS2 indicators / metric exposure via the catalogue.

## Engine-tree state
- Clean except known untracked PO/bot WIP (never commit): `infra/discord-bot/bot.py`,
  `infra/systemd/or-*-bot.service`, `logs/`, `.claude/scheduled_tasks.lock`,
  `products/blog/reviews/release-report.md` (regenerated each release sweep).

## Prod-build-with-dirty-engine-tree pattern (reusable, from #54)
When a dbt build needs the DuckDB write lock but the engine tree has WIP you must not
deploy: stash ONLY the WIP file(s) → stop 16 → dbt on prod → start 16 (boots clean HEAD)
→ stash pop. Verify build stamp == HEAD to prove WIP not shipped.

## Standing blockers (all PO-side)
- OR-153 Telegram inbound · OR-90 Instagram token → OR-89 · OR-86 BDL key → crime/agri/
  business dashboards · OR-79 Ghost nav.

## Lessons
- **A registered visual is not a working visual.** choropleth was in the registry +
  schema for days but had three bugs that meant it had never rendered on a dashboard.
  Registration/validate-clean ≠ live-verified. Always bind it on a real page + screenshot.
- **Plotly built-in geo scope can't match Eurostat alpha-2** (only ISO-3 / country names,
  and EL/UK aren't ISO). For EU maps bundle a GISCO NUTS-0 geojson keyed on NUTS_ID, which
  matches our `geo` codes exactly — same mechanism as the regional map.
- **A mid-render Playwright screenshot can show false layout overlap.** Wait for settle
  (networkidle + a few s) and cross-check with DOM bounding-box measurement before
  diagnosing a layout bug — the DOM said 440px clean box; the early screenshot lied.
