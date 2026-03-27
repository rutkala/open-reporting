# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-03-27 -->

## Current Focus
Brand rename to "Otwarte Raporty", Instagram publishing automation, social media playbook.

## Last Session Summary (2026-03-27)

### What was built/changed:

**Brand rename — "Otwarte Raporty"**
- Explorer, Labour dashboard, Mobile PWA (templates + manifest.json) — display name updated
- Ghost CMS title set via `docker-compose.yml` env var (`title: Otwarte Raporty`) + DB updated directly
- Ghost DB update needed because env var only applies to fresh installs; existing DB value takes precedence

**Instagram publishing**
- Meta Developer account created, app "Otwarte Raporty" (ID: 1334119365407244)
- Instagram Business account @otwarteraporty connected as tester
- Token generated for @otwarteraporty (user ID: 26290813287238381)
- Credentials in `.env`: `INSTAGRAM_APP_ID`, `INSTAGRAM_APP_SECRET`, `INSTAGRAM_ACCESS_TOKEN`
- Token valid ~60 days — refresh via Meta Developer portal → Use cases → Generate token
- Published first test posts: 2×2 KPI card (Wzrost PKB, CPI, Wzrost płac, EUR/PLN)
- Image generation: Plotly → PNG → `infra/nginx/html/` → served at `portal.open-reporting.dev/<file>.png`
- **Important**: use unique filename per post — Instagram caches by URL

**Social playbook**
- `.claude/playbooks/social.md` — full publishing flow, card design rules, caption format, quality gates

**kaleido installed** — for Plotly static PNG export (`pip install kaleido --break-system-packages`)

### Products live:
- `open-reporting.dev` — Ghost blog "Otwarte Raporty"
- `portal.open-reporting.dev` — Dashboards (labour port 8050, explorer port 8051)
- `portal.open-reporting.dev/app/` — Mobile PWA (port 8052)
- Instagram: @otwarteraporty

## Key Technical Facts
- DB (analytical): DuckDB at data/warehouse.duckdb (DUCKDB_PATH env var)
- DB (operational): PostgreSQL localhost:5432 db=reporting user=reporting
- dbt: `cd platform/processing/dbt && DUCKDB_PATH=/opt/open-reporting/data/warehouse.duckdb dbt run --profiles-dir .`
- dbt seed: add `--select <seed_name>` to seed only one file; schema change requires `--full-refresh`
- Harlequin: `harlequin /opt/open-reporting/data/warehouse.duckdb` (run in tmux new-window)
- DuckDB concurrency: stop dashboards before dbt run — `sudo systemctl stop or-explorer or-labour`
- Instagram API: two-step publish (create container → wait 10s → publish)

## Catalogue State
- `catalogue.domain_details`: 222 indicators across 18 domains
- `catalogue.domain_detail_sources`: 483 mappings — Eurostat: 73 verified (2 NUTS2); NBP FX: 4 verified
- `dim_primary_source`: 77 verified mappings — used as Explorer default
- NUTS2 domains: `mac.gdp_per_capita_regional`, `pop.population_regional`

## Open Items
- Domain dashboards: next phase — LAB, MAC, ENV first; standard template (KPI cards, time series, cross-indicator bar)
- Fix BUS: `sts_inpr_a` series_id (try `indic_bt=PROD`)
- BDL ingestion: pending user confirmation on API key
- SDP ingestion: pending user confirmation on data format
- Install dbt-metricflow, migrate products/semantic/ → dbt metrics/
- Ghost admin account setup (not yet created — setup screen not found)
- Ghost nav: add "Portal" link to `portal.open-reporting.dev` (requires Ghost admin)
- Instagram token refresh due ~end of May 2026
- Social: automate weekly Economy Snapshot post
