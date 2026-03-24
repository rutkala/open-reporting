# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-03-24 -->

## Current Focus
Repo restructure complete. Next: first new dashboard from Linear backlog, or ingestion pipeline.

## Last Session Summary (2026-03-24)
Full repo reorganisation into 4 top-level areas + products layer:
- `infra/` — nginx (conf, certs, html web root)
- `platform/` — processing/ (ingestion TBD)
- `products/` — semantic/, visuals/, dashboards/, portal/, blog/, mobile/, social/
- `.claude/` — team (unchanged)
- Root: docker-compose.yml, .env, README.md, CLAUDE.md, .gitignore (all stay at root)

Built semantic layer + Dash dashboard (labour domain):
- `products/semantic/` — YAML domain models + Python engine (ibis + pandas)
- `products/semantic/labour/model.yml` — facts, dimensions, measures, KPIs, sections
- `products/visuals/lib/` — db.py (psycopg2), theme.py (Nordic Plotly template)
- `products/dashboards/rynek_pracy/app.py` — Dash app, fully driven by semantic model
- `products/dashboards/rynek_pracy/static.py` — static HTML generator
- `products/dashboards/generate.py` — runner for static generation
- `infra/nginx/html/` — nginx web root (output of static.py goes here)
- nginx proxies `/dash/` → localhost:8050

## Key Technical Facts
- DB: PostgreSQL, host=localhost:5432, db=reporting, user=reporting
- Dash served at portal.open-reporting.dev/dash/ via nginx reverse proxy
- Static HTML served from infra/nginx/html/ (nginx root /usr/share/nginx/charts)
- PYTHONPATH=/opt/open-reporting required for all python3 commands
- load_dotenv(override=True) + lazy _dsn() pattern for DB connections
- Semantic layer: products.semantic.query(metric_id, domain="labour")

## Open Items
- Build ingestion pipeline (platform/ingestion/) — no scripts yet
- Populate products/visuals/labour/ with reusable chart components
- Flesh out products/portal/ as a proper delivery layer
- Review and update docs/ folder (ARCHITECTURE.md refs are stale)
- First Linear issue implementation
