# Tech Stack & Environment

## Source of Truth Rules

| What | Where |
| :--- | :--- |
| Product vision, documentation | Linear documents |
| Tasks, status, roadmap | GitHub Issues |
| Code | GitHub (github.com/rutkala/open-reporting) |
| Claude Code working instructions | CLAUDE.md |

> **Rule:** Never duplicate documentation. If it's in Linear, don't copy it to GitHub or anywhere else. (Except for machine-readable config/taxonomy as agreed).

## Stack

| Layer | Technology |
| :--- | :--- |
| Infrastructure | Hetzner VPS CX22, Docker Compose |
| Database | PostgreSQL 16 |
| Dashboards | Python + Plotly (static HTML) |
| Blog | Ghost CMS |
| Reverse proxy | Nginx + Let's Encrypt |
| Data ingestion | Python scripts (GUS BDL API, stooq.com) |
| Project management | GitHub Issues |
| Code hosting | GitHub |

## VPS Access
* **IP:** 91.98.118.153
* **Specs:** Hetzner CX22, 4GB RAM, Ubuntu
* **Repo path:** `/opt/open-reporting`

## API Keys (Managed in local .env)
* **BDL_API_KEY:** GUS BDL API
* **DBW_API_KEY:** GUS DBW API
* **POSTGRES_PASSWORD:** PostgreSQL
* **GHOST_KEY_ID + GHOST_KEY_SECRET:** Ghost Admin API

## Docker Services

| Service | Image | Ports | Purpose |
| :--- | :--- | :--- | :--- |
| postgres | postgres:16-alpine | 5432 | Data warehouse |
| nginx | nginx:alpine | 80, 443 | Reverse proxy + SSL |
| ghost | ghost:5-alpine | 2368 | Blog CMS |
| certbot | certbot/certbot | - | SSL renewal |

## Key Commands
* **Start services:** `cd /opt/open-reporting && docker compose up -d`
* **Regenerate dashboards:** `POSTGRES_PASSWORD=xxx python3 charts/generate.py`
* **Ingest GPW stock data:** `POSTGRES_PASSWORD=xxx python3 ingestion/gpw_ingest.py`
* **Ingest BDL budget data:** `BDL_API_KEY=xxx POSTGRES_PASSWORD=xxx python3 ingestion/budget_ingest.py`
* **Renew SSL:** `./nginx/request_certificate.sh`
