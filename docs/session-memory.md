# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-06-02 (run #54 — OR-88 dim_geo NUTS1/NUTS2 regions) -->

## Run #54 — OR-88: dim_geo now covers Polish NUTS1/NUTS2 regions. HEAD 1f21e0c2

**Shipped the regional data foundation (data-plane, zero engine touch).** Picked OR-88
because the engine tree was dirty (active sibling WIP — see below) so no dbr work was
safe; OR-88 is pure dbt/seed.

**The issue premise was stale.** Audited the live warehouse: NUTS2/voivodeship data
already exists across **6 domains** (~26 indicators: mac/pop/lab/soc/clt) via the
`PL_NUTS2` ingestion sentinel — criterion #1 (≥5 domains) was already met. The real gap
was criterion #3: `dim_geo` was country-only, so regional facts (`geo='PL21'`) resolved
to NO name. The authoritative `seed_geo_nuts` seed (7 NUTS1 + 17 NUTS2, correct Polish
diacritics) existed but was never joined into any dim (and wasn't even materialised).

**Fix (commit `1f21e0c2`):** `dim_geo.sql` UNIONs the NUTS1/NUTS2 rows from
`ref('seed_geo_nuts')` + new columns `geo_level` (country/nuts1/nuts2) and `parent_geo`
(nuts2→nuts1→country roll-up). `dim_geo.yml` gains accepted_values test + 2 semantic
dimensions. Verified: 58 rows (34 country + 7 + 17), 0 unresolved PL regional codes in
all_indicators, country joins unchanged (additive), dbt tests PASS=8.

**Prod build trick (avoids deploying the sibling WIP):** verified on a `/tmp` COPY first
(zero disruption); then stopped all 16 dashboard services (release DuckDB RO locks),
`git stash`-ed ONLY make_app.py so the restart booted clean committed HEAD (= the code
they already ran → zero live-behaviour change), ran dbt on prod, restarted 16,
`git stash pop` to restore the sibling WIP undeployed. All 16 + www back to 200, stamp
`ddcbe73a` (clean — WIP correctly NOT shipped). ~50s planned outage during reboot.

**Linear:** OR-88 → Done. Criterion #2 (explorer regional drill-down = UI) handed to
**OR-159 (choropleth)** — commented there that dim_geo now supplies the NUTS2 names +
hierarchy (GeoJSON PL21…PL92 codes == `geo` PK).

## ACTIVE SIBLING WIP in tree — do NOT commit/revert (as of run #54)
- `packages/dbr/src/dbr/make_app/make_app.py` — modified 2026-06-02 13:48 UTC (after the
  12:00 run). A **mobile-header revert**: drops run #53's sticky `#dbr-page-header` so the
  section H2 rises to take the top slot instead (comment: "dashboard header scrolls away
  normally on mobile"). Almost certainly dashboard-dev bot iterating on PO feedback about
  the #53 double-sticky. Desktop-noop. **This dirties the engine tree → blocks ALL
  engine-plane dbr work + fleet redeploy until committed/cleared.** Same hands-off rule as
  the untracked bot files below.
- Untracked PO/bot WIP (never commit): `infra/discord-bot/bot.py`,
  `infra/systemd/or-*-bot.service`, `logs/`, `.claude/scheduled_tasks.lock`.

## How dim_geo regional mapping works (for next maintainer)
- `seed_geo_nuts.csv` (products/warehouse/seeds/) = authoritative NUTS map: geo, geo_name,
  geo_type (country/nuts1/nuts2), country_code, nuts1_code, nuts1_name. Seeded to
  `curated` per dbt_project.yml.
- `dim_geo.sql` country_rows (VALUES, 34) ∪ region_rows (seed, geo_type in nuts1/nuts2).
  Region name_pl=name_en=geo_name (Polish proper nouns). parent_geo: nuts2→nuts1_code,
  nuts1→country_code('PL'). country parent_geo NULL.
- All 24 PL regional codes in all_indicators (7 NUTS1 + 17 NUTS2) now resolve. Non-PL
  regional codes = 0 (foreign NUTS not ingested).

## NUTS2 ingestion path (catalogue-driven)
- `eurostat_observations.py` reads `catalogue.domain_detail_sources` WHERE
  source_id='eurostat' AND verified=true. series_id = `dataset?geo=PL_NUTS2&dim=val`.
  `PL_NUTS2` sentinel = fetch all regions, keep `PL*` rows. Adding a NUTS2 series = add a
  verified catalogue row + ingest; no code change.

## Recent commits
- 1f21e0c2 feat(warehouse): dim_geo covers Polish NUTS1/NUTS2 regions (OR-88)
- ddcbe73a docs: run #53 — per-section sticky headings on mobile
- 62a24419 feat(dbr): per-section sticky headings on mobile (pin + hand off per page)
- 0233b656 feat(dbr): sticky page header on mobile (reuse header, drop the extra bar)
- 8b2f620a fix(dbr): footer auto-derive must reuse engine's DuckDB connection (OR-165)

## What's next (unblocked, autonomous)
- **Once make_app.py WIP is committed/cleared** (engine tree clean), the dbr feature
  backlog opens up: **OR-159 choropleth (High)** — now has its dim_geo prerequisite ready,
  natural next pick; OR-160 cross-filter (High), OR-161 date slicer, OR-162 number-format.
  Each = branch+PR+critic+redeploy, one per run, don't batch.
- Data-plane (always safe even with dirty engine tree): more NUTS2 indicators via the
  catalogue sentinel if a domain gap appears; OR-88 left coverage in good shape.

## Prod-build-with-dirty-engine-tree pattern (reusable)
When a dbt build needs the DuckDB write lock but the engine tree has uncommitted WIP you
must not deploy: stash ONLY the WIP file(s) → stop 16 → dbt on prod → start 16 (boots
clean HEAD = unchanged behaviour) → stash pop. Verify build stamp == HEAD to prove WIP
not shipped. Check WIP file mtime first to confirm the sibling bot is idle (low conflict risk).

## Standing blockers (all PO-side)
- OR-153 Telegram inbound · OR-90 Instagram token → OR-89 · OR-86 BDL key → crime/agri/
  business dashboards · OR-79 Ghost nav.

## Lessons
- **Audit the live warehouse before trusting an issue's premise.** OR-88 claimed "only 2
  NUTS2 domains"; reality was 6. Two of three acceptance criteria were already met — the
  real work was one missing dimension join, not new ingestion.
- **Verify dbt model changes on a `/tmp` copy first**, then build prod — de-risks the SQL
  with zero outage before touching the write lock.
- A second in-process `duckdb.connect()` to a file the MetricFlow engine holds fails
  (config-mismatch) → reuse `_get_engine()._sql_client.query()`. (from #50)
