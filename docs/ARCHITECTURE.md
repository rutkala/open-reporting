# Open Reporting — Architecture

## Infrastructure

Single Hetzner VPS running Docker Compose. No Kubernetes, no cloud-managed databases — simple by design for a one-person operation.

## Docker Services

```yaml
Services:
  nginx     → port 80/443  — Reverse proxy, static file serving
  postgres  → port 5432    — Internal only (not exposed)
  ghost     → port 2368    — Internal only (proxied via nginx)
```

All services defined in `docker-compose.yml`. Configuration in `nginx/conf.d/`.

## Directory Layout

```
/opt/open-reporting/
├── charts/
│   ├── dashboards/         ← One Python module per dashboard
│   ├── lib/
│   │   ├── db.py           ← PostgreSQL connection + query helper
│   │   └── theme.py        ← Plotly theme: C (colours), apply(), page()
│   └── generate.py         ← Entry point: imports and calls all dashboards
├── ingestion/              ← ETL scripts (one per data source)
├── processing/             ← Data transformation scripts
├── nginx/
│   ├── conf.d/             ← Virtual host configs (committed)
│   └── html/               ← Static output (dashboards, assets)
├── content/                ← Ghost CMS data volume (gitignored)
├── .claude/                ← Claude Code config
├── docs/                   ← Project documentation (this folder)
├── .env                    ← Secrets (gitignored)
├── .env.example            ← Template for secrets (committed)
└── docker-compose.yml
```

## Database

PostgreSQL 16. Two schema layers:

| Schema | Purpose | Naming |
|--------|---------|--------|
| `raw` | Raw ingested data, preserve source structure | `raw.{source}_{entity}` |
| `public` | Processed, analysis-ready data | `public.{domain}_{metric}` |

Connection via `psycopg2`. DSN from `POSTGRES_PASSWORD` env var.

## Dashboard Pipeline

```
Data Source API
      ↓
ingestion/{source}_ingest.py    [raw schema]
      ↓
processing/{domain}_transform.py [public schema]  (optional)
      ↓
charts/dashboards/{name}.py     [reads public schema]
      ↓
charts/generate.py              [orchestrates all dashboards]
      ↓
nginx/html/dashboards/{name}.html  [served by nginx]
```

## Secrets Management

| Variable | Purpose |
|----------|---------|
| `POSTGRES_PASSWORD` | PostgreSQL superuser password |
| `BDL_API_KEY` | GUS BDL API key |
| `GHOST_DATABASE_PASSWORD` | Ghost CMS DB password |

All secrets in `.env` (gitignored). `.env.example` committed as reference.

## SSL / TLS

Certificates managed by certbot (Let's Encrypt). Stored in `/etc/letsencrypt/` on host, mounted into nginx container. Renewal via `renew-certs.sh`.

## Deployment

No CI/CD. Manual deploy:
```bash
git pull origin main
docker compose up -d
POSTGRES_PASSWORD=xxx python3 charts/generate.py
```
