# Open Reporting

A one-person data media company turning Polish public data into accessible,
beautiful, and useful products.

**Live:** [portal.open-reporting.dev](https://portal.open-reporting.dev) · [www.open-reporting.dev](https://www.open-reporting.dev)

---

## What it is

Open Reporting collects public data — budgets, labour market, stock markets,
demographics, and more — processes it, and publishes it as interactive
dashboards and long-form articles.

Polish public data is the starting point. Every domain where open data
exists is in scope.

---

## Live products

| Product | URL | Description |
|---------|-----|-------------|
| Analytical Portal | portal.open-reporting.dev | Interactive Plotly dashboards |
| Blog | www.open-reporting.dev | Data-driven articles (Polish) |

**Current dashboards:**
- State budget (Poland, 2008–2024)
- Regional budgets (16 voivodships)
- GPW stock market (140+ WSE tickers)

---

## Stack

| Layer | Technology |
|-------|-----------|
| Infrastructure | Hetzner VPS CX22, Docker Compose |
| Database | PostgreSQL 16 |
| Dashboards | Python + Plotly (static HTML) |
| Blog | Ghost CMS |
| Reverse proxy | Nginx + Let's Encrypt |
| Data ingestion | Python scripts (GUS BDL API, stooq.com) |

---

## Data sources

- **GUS BDL API** (`bdl.stat.gov.pl`) — Polish regional statistics
- **stooq.com** — Warsaw Stock Exchange historical prices
- More sources added as new topic domains are covered

---

## Project structure

```
ingestion/      data ingestion scripts (GUS BDL, GPW)
processing/     data transformation scripts
charts/         Plotly dashboard generators
  dashboards/   individual dashboard modules
  lib/          shared theme, DB connection
content/        article drafts and assets
nginx/          reverse proxy config
```

---

## Roadmap

See [ROADMAP.md](ROADMAP.md) for phased plan.
See [PRODUCT.md](PRODUCT.md) for full product vision.

---

*Owner: Radek Utkala · Poland · 2026*
