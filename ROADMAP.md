# Open Reporting — Roadmap

**Last updated: March 2026**

---

## Phase 1 — MVP ✅ (done)

Goal: something live, end-to-end, real data, real URL.

- [x] VPS provisioned (Hetzner CX22)
- [x] Docker Compose stack: Postgres, Nginx, Ghost, Certbot
- [x] SSL on portal.open-reporting.dev and www.open-reporting.dev
- [x] GUS BDL ingestion — voivodship budgets (16 regions)
- [x] National budget ingestion (2008–2024)
- [x] GPW stock market ingestion (140+ tickers, stooq.com)
- [x] 4 interactive Plotly dashboards (state budget, regional budgets, GPW, portal home)
- [x] Ghost CMS blog with 2 Polish articles
- [x] GitHub repo connected, SSH auth from VPS

---

## Phase 2 — Foundation (current)

Goal: more data, more content, automated updates, visible online.

**Data & dashboards**
- [ ] GUS BDL — unemployment rate by voivodship
- [ ] GUS BDL — average wages by voivodship
- [ ] GUS BDL — GDP per capita by voivodship
- [ ] Add Labour Market dashboard to portal
- [ ] Automated daily/weekly ingestion (cron or simple scheduler)

**Content**
- [ ] 2 more Polish articles (labour market, regional GDP)
- [ ] English versions of existing articles (AI-assisted)
- [ ] Basic SEO: meta tags, sitemap, Open Graph

**Distribution**
- [ ] LinkedIn page for Open Reporting
- [ ] First LinkedIn post with a chart from the portal

---

## Phase 3 — Monetization

Goal: first paying users or sponsors.

- [ ] Newsletter (Substack or self-hosted)
- [ ] Subscription system (Ghost memberships)
- [ ] Premium content tier (1–2 paywalled reports)
- [ ] Sponsorship outreach (think tanks, data providers)
- [ ] Social media workflow: data → chart → post (semi-automated)

---

## Phase 4 — Scale

Goal: sustainable audience and revenue, richer products.

- [ ] Mobile app (React Native or PWA)
- [ ] YouTube / video content workflow
- [ ] Data science layer: forecasts, anomaly detection, rankings
- [ ] Public API (rate-limited, subscription tier)
- [ ] dbt transformations for data warehouse
- [ ] Consider team / contributors

---

## Backlog (unscheduled ideas)

- Electoral data dashboard (Sejm voting patterns)
- Demographics dashboard (population pyramid by region)
- Health data (NFZ, GUS)
- Public procurement data (UZP)
- EU funds absorption by region
- Crime statistics dashboard
- Air quality / environment indicators
- Education outcomes by region

---

*See PRODUCT.md for full vision.*
