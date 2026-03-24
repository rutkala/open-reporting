# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-03-24 -->

## Current Focus
Platform layer fully structured. Next: first ingestion script, or first Linear issue.

## Last Session Summary (2026-03-24)
Designed and built the full `platform/` folder structure through architectural discussion:

```
platform/
├── sources/              → Source catalogue (YAML metadata per source)
├── ingestion/
│   ├── to_landing/       → Fetch external files → data/landing/
│   └── to_raw/           → Parse landing files + API fetchers → raw schema
├── database/
│   ├── raw/              → DDL for raw.* tables
│   ├── curated/          → DDL for curated.* tables
│   └── migrations/       → Ordered SQL migration files
└── processing/           → dbt models: raw.* → curated.*
```

Also decided:
- `data/` at repo root (git-ignored entirely) — runtime data, not committed
- `data/landing/` — file landing zone for Excel, PDF, CSV sources
- Processing tool: **dbt-core** (recommended, not yet implemented)
- Existing `platform/processing/bdl_labour_process.py` left in place — migration to dbt is future work

## Previous Session Summary (2026-03-24)
Full repo reorganisation into 4 top-level areas + products layer:
- `infra/` — nginx (conf, certs, html web root)
- `platform/` — processing/ (ingestion TBD)
- `products/` — semantic/, visuals/, dashboards/, portal/, blog/, mobile/, social/

Built semantic layer + Dash dashboard (labour domain):
- `products/semantic/` — YAML domain models + Python engine (ibis + pandas)
- `products/semantic/labour/model.yml` — facts, dimensions, measures, KPIs, sections
- `products/visuals/lib/` — db.py (psycopg2), theme.py (Nordic Plotly theme)
- `products/dashboards/rynek_pracy/app.py` — Dash app, fully driven by semantic model
- `products/dashboards/rynek_pracy/static.py` — static HTML generator
- `infra/nginx/html/` — nginx web root (output of static.py goes here)

## Key Technical Facts
- DB: PostgreSQL, host=localhost:5432, db=reporting, user=reporting
- Dash served at portal.open-reporting.dev/dash/ via nginx reverse proxy
- Static HTML served from infra/nginx/html/ (nginx root /usr/share/nginx/charts)
- PYTHONPATH=/opt/open-reporting required for all python3 commands
- load_dotenv(override=True) + lazy _dsn() pattern for DB connections
- Semantic layer: products.semantic.query(metric_id, domain="labour")

## Open Items
- Write first source YAML catalogue (platform/sources/)
- Write first ingestion script (platform/ingestion/to_raw/ or to_landing/)
- Migrate bdl_labour_process.py → dbt model in platform/processing/
- Populate products/visuals/labour/ with reusable chart components
- Flesh out products/portal/ as a proper delivery layer
- Review and update docs/ folder (ARCHITECTURE.md refs are stale)
- First Linear issue implementation
