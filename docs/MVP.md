# MVP v0.1 — Otwarte Raporty

**Release date:** 2026-03-28
**Version:** v0.1.0

---

## What is Otwarte Raporty

A one-person data media company turning Polish public data into accessible, beautiful, and useful products. Open Reporting publishes data-driven insights about the Polish economy, labour market, demographics, and more — through a public portal, a blog, a mobile app, and social media.

---

## What is in MVP v0.1

### Products

| Product | URL | Technology | Status |
|---------|-----|------------|--------|
| Blog | open-reporting.dev | Ghost 5 CMS | Live |
| Data Portal | portal.open-reporting.dev | Dash (Python) + nginx | Live |
| Data Explorer | portal.open-reporting.dev/explorer/ | Dash (Python) | Live |
| Mobile PWA | portal.open-reporting.dev/app/ | FastAPI + Jinja2 | Live |
| Social | @otwarteraporty (Instagram) | Meta Graph API | Live |

### Data Platform

- **Warehouse**: DuckDB analytical database at `data/warehouse.duckdb`
- **Catalogue**: 222 indicators across 18 domains (PostgreSQL operational DB)
- **Ingestion**: Eurostat (73 verified series, including NUTS2 regional) + NBP FX rates
- **Processing**: dbt project (`open_reporting`) — 22 curated models, 6 seeds
- **Dimensions**: `dim_geo` (Poland + 7 NUTS1 + 17 NUTS2), `dim_domain_detail` (with default aggregation), `dim_calendar`, `dim_source`

### Infrastructure

- Single Hetzner VPS
- Docker Compose: nginx (reverse proxy, SSL), PostgreSQL 16, Ghost 5
- SSL/TLS via Let's Encrypt (certbot)
- Systemd services: `or-labour` (port 8050), `or-explorer` (port 8051), `or-mobile` (port 8052)

### Features

- **Labour dashboard** — unemployment, wages, employment by region and time
- **Data Explorer** — ad-hoc queries across all 222 indicators with dimension hierarchy drill-down, default aggregation per indicator, NUTS2 regional data
- **Mobile PWA** — installable Android app with KPI cards and domain browsing
- **Instagram publishing** — data card generation (Plotly PNG) + Meta Graph API posting

---

## Explicitly Out of Scope for MVP

- Automated test suite
- CI/CD pipeline
- Monitoring and alerting
- Domain-specific dashboards beyond Labour (MAC, ENV, etc.)
- Automated ingestion scheduling (currently manual)
- Ghost blog content (no articles published yet)
- Facebook / Threads / LinkedIn posting
- User accounts or authentication
- BDL (GUS) data ingestion

---

## Known Limitations and Accepted Risks

| Area | Limitation | Risk | Accepted |
|------|-----------|------|---------|
| Ghost admin | Admin account not yet set up — blog cannot be edited | Cannot publish articles | Yes — fix as first post-MVP task |
| Ingestion | No automated scheduling — data must be refreshed manually | Data becomes stale | Yes — automate in Phase 1 |
| Instagram token | Access token expires ~end of May 2026 — manual refresh required | Publishing fails silently | Yes — calendar reminder set |
| DuckDB concurrency | Single-writer lock — dashboards must be stopped before dbt runs | Brief downtime during data refresh | Yes — documented in session memory |
| No tests | Zero automated tests for dashboards, dbt models, or ingestion | Regressions go undetected | Yes — address in Phase 2 |
| Single VPS | No redundancy or failover | Outage = full downtime | Yes — acceptable for MVP scale |

---

## Key Technical Decisions Made During MVP

- **DuckDB over PostgreSQL for analytics** — embedded, no server management, fast for analytical queries, fits single-VPS architecture
- **dbt for transformations** — version-controlled SQL, seed files for reference data, testable
- **Dash (Python) over JavaScript** — all dashboards in Python, no frontend build toolchain
- **Ghost for blog** — managed CMS with built-in editor, themes, newsletter — avoids building a CMS
- **PWA over native app** — installable on Android via "Add to Home Screen", no app store needed
- **Meta Graph API for Instagram** — two-step publish (container → publish), images served from portal nginx
- **Nordic minimal design** — consistent colour palette (`AZURE_1 #4A7FB5`, `BG_PAGE #F7F8FA`) across all products
- **Polish content, English code** — all backend code in English, all user-facing content in Polish
