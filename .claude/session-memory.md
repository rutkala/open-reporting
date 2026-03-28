# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-03-28 -->

## Current Focus
MVP v0.1.0 declared complete. Switching to post-MVP agile workflow with Linear issues + feature branches + PRs.

## MVP Status: COMPLETE (v0.1.0 — 2026-03-28)
See `docs/MVP.md` for full declaration and `docs/RELEASE_NOTES.md` for release notes.

**Two remaining gaps (first Linear issues to create):**
1. Ghost admin account setup — blog cannot be managed without it
2. Daily ingestion cron — NBP + Eurostat currently refreshed manually

## Post-MVP Process (CRITICAL — new rules from v0.1.0)
See `docs/CONTRIBUTING.md` for full process. Summary:
- **All work starts as a Linear issue** — no idea goes to code directly
- **Feature branch per issue**: `feat/ORE-XXX-description` from `main`
- **PR required** with `/review` output and standards compliance checklist
- **Never push directly to `main`**
- **Update `docs/RELEASE_NOTES.md`** under "Unreleased" as part of each PR

## Products Live
- `open-reporting.dev` — Ghost blog "Otwarte Raporty"
- `portal.open-reporting.dev` — Labour dashboard (port 8050) + Explorer (port 8051)
- `portal.open-reporting.dev/app/` — Mobile PWA (port 8052)
- Instagram: @otwarteraporty (token expires ~end of May 2026)

## Key Technical Facts
- DB (analytical): DuckDB at data/warehouse.duckdb (DUCKDB_PATH env var)
- DB (operational): PostgreSQL localhost:5432 db=reporting user=reporting
- dbt: `cd platform/processing/dbt && DUCKDB_PATH=/opt/open-reporting/data/warehouse.duckdb dbt run --profiles-dir .`
- dbt seed schema change: requires `--full-refresh`
- DuckDB concurrency: stop dashboards before dbt run — `sudo systemctl stop or-explorer or-labour`
- Instagram API: two-step publish (create container → wait 10s → publish); unique filename per post
- kaleido installed for Plotly PNG export

## Catalogue State
- `catalogue.domain_details`: 222 indicators across 18 domains
- `catalogue.domain_detail_sources`: 483 mappings — Eurostat: 73 verified (2 NUTS2); NBP FX: 4 verified
- NUTS2 domains: `mac.gdp_per_capita_regional`, `pop.population_regional`

## Roadmap (see docs/ROADMAP.md)
Phase 1 — Content & Data depth:
- Ghost admin + first articles
- MAC, LAB, ENV domain dashboards
- BDL ingestion, automated daily cron
- Instagram token refresh (May 2026)

Phase 2 — Quality & Reliability:
- dbt tests, error handling, monitoring

Phase 3 — Growth & Distribution:
- Facebook/Threads posting, more NUTS2, EU27 scope
