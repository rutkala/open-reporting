# Architecture

Single Hetzner VPS, Docker Compose. Simple by design for a one-person operation.

---

## Infrastructure

```
Docker Compose services:
  nginx     → 80/443   — Reverse proxy, SSL termination, static files
  postgres  → 5432     — Internal only — Ghost CMS operational DB
  ghost     → 2368     — Internal only — Blog CMS (proxied via nginx)

Host processes (systemd):
  or-labour   → port 8050 — Labour dashboard (Dash)
  or-explorer → port 8051 — Data Explorer (Dash)
  or-mobile   → port 8052 — Mobile PWA (FastAPI)
```

SSL/TLS via Let's Encrypt (certbot). Certificates in `/etc/letsencrypt/`, mounted into nginx.

---

## Data Architecture

Two databases, two roles:

| Database | Technology | Role |
|----------|-----------|------|
| Analytical warehouse | DuckDB (`data/warehouse.duckdb`) | All data queries, dashboards, Explorer, mobile |
| Operational DB | PostgreSQL 16 | Ghost CMS only |

### DuckDB Schema Layout

| Schema | Purpose | Naming |
|--------|---------|--------|
| `raw` | Raw ingested data — source structure preserved | `raw.{source}_{entity}` |
| `curated` | dbt-transformed, analysis-ready | `curated.{domain}_{metric}` |

### PostgreSQL

Used only by Ghost CMS. No analytics run against it.

---

## Data Pipeline

```
Source APIs (Eurostat, NBP, ...)
    ↓
platform/ingestion/to_raw/          → raw.{source}_{entity} (DuckDB)
    ↓
platform/processing/dbt/            → curated.* (DuckDB, via dbt)
    ↓
products/visuals/lib/               → shared query helpers
    ↓
products/dashboards/    → Labour (port 8050), Explorer (port 8051)
products/mobile/        → Mobile PWA (port 8052)
```

### Key dbt Models

- `curated.all_indicators` — conformed wide fact table (all sources, sparse dim1–dim4 columns)
  - `curated.stg_eurostat` — Eurostat staging (73 series, 37 indicators, national + NUTS2)
  - `curated.stg_nbp` — NBP staging (4 FX rate indicators, daily)
  - `curated.stg_dbw` — GUS DBW HVD staging (69 indicators, 568k rows, annual, with dimension labels)
- `curated.dim_domain_detail` — indicator catalogue (305 rows, 18 domains)
- `curated.dim_source` — source registry (eurostat, nbp, dbw)
- `curated.dim_geo` — geographic hierarchy (PL + 7 NUTS1 + 17 NUTS2)
- `curated.dim_calendar` — monthly spine 1995–2029

**Rule**: dashboards and the Explorer query `curated.*` only — never `raw.*` directly.

---

## URL Structure

| URL | Serves |
|-----|--------|
| `open-reporting.dev` | Redirects to `www.open-reporting.dev` |
| `www.open-reporting.dev` | Ghost blog |
| `portal.open-reporting.dev` | Static HTML (nginx web root) |
| `portal.open-reporting.dev/labour/` | Labour dashboard (port 8050) |
| `portal.open-reporting.dev/explorer/` | Data Explorer (port 8051) |
| `portal.open-reporting.dev/app/` | Mobile PWA (port 8052) |

---

## Secrets

All in `.env` (gitignored). See `.env.example` for the full list.

Key variables:
- `DUCKDB_PATH` — path to warehouse.duckdb
- `POSTGRES_PASSWORD` — PostgreSQL password (Ghost only)
- `INSTAGRAM_APP_ID`, `INSTAGRAM_APP_SECRET`, `INSTAGRAM_ACCESS_TOKEN` — Meta API

---

## Deployment

No CI/CD (post-MVP). Manual deploy:
```bash
git pull origin main
docker compose up -d --force-recreate nginx  # if nginx config changed
sudo systemctl restart or-labour or-explorer or-mobile  # if app code changed
```

dbt refresh (stop dashboards first — DuckDB single-writer):
```bash
sudo systemctl stop or-explorer or-labour
cd platform/processing/dbt
DUCKDB_PATH=/opt/open-reporting/data/warehouse.duckdb dbt run --profiles-dir .
sudo systemctl start or-explorer or-labour
```
