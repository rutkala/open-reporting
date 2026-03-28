# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-03-28 -->

## Current Focus
Post-MVP cleanup complete. Ready to start first post-MVP Linear issues (Ghost admin, daily cron).

## MVP Status: COMPLETE (v0.1.0 — 2026-03-28)
See `docs/MVP.md` for full declaration and `docs/RELEASE_NOTES.md` for release notes.

**First Linear issues to create (post-MVP):**
1. Ghost admin account setup — blog cannot be managed without it
2. Daily ingestion cron — NBP + Eurostat currently refreshed manually

## Documentation State (clean as of 2026-03-28)
- All docs in `docs/` on GitHub — single source of truth
- Linear documents archived (Domain Taxonomy, Tech Stack, Data Catalog) — all point to GitHub
- Linear project description updated (mobile live, Instagram only, Polish-only language)
- `docs/DOMAINS.md` — fully expanded to 18 domains with Eurostat themes + GUS equivalents

## Post-MVP Process (CRITICAL — new rules from v0.1.0)
See `docs/CONTRIBUTING.md` for full process. Summary:
- **All work starts as a Linear issue** — no idea goes to code directly
- **Feature branch per issue**: `feat/OR-XXX-description` from `main`
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

## Linear Issues (Phase 1 — all Todo)
Epics: OR-74 (Blog), OR-75 (Dashboards), OR-76 (Data), OR-77 (Social)
Sub-issues: OR-78 to OR-90 — see Linear for full list
Urgent: OR-78 (Ghost admin), OR-85 (daily cron), OR-90 (Instagram token by 2026-05-20)

## Workflow (post-MVP) — 4 stages
1. `/capture-idea` — idea from chat → Backlog (Idea label)
2. `/review-ideas` — convert ideas to proper issues → Backlog
3. `/sprint` — pick issues from Backlog → Todo
4. `/kickoff` — plan → implement → PR → Done
