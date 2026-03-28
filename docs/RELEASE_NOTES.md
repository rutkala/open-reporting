# Release Notes

---

## v0.1.0 — MVP (2026-03-28)

### Products launched
- **Blog** — `open-reporting.dev` (Ghost 5, "Otwarte Raporty")
- **Data Portal** — `portal.open-reporting.dev` with Labour dashboard and Data Explorer
- **Mobile PWA** — `portal.open-reporting.dev/app/` — installable Android app
- **Instagram** — `@otwarteraporty` with data card publishing

### Data platform
- DuckDB analytical warehouse with 222 indicators across 18 domains
- Eurostat ingestion (73 verified series) including NUTS2 regional data
- NBP FX rates ingestion (EUR/PLN, USD/PLN, GBP/PLN, CHF/PLN)
- dbt project: 22 curated models, 6 seeds
- Geographic dimension expanded to include NUTS1 (7) + NUTS2 (17) Polish regions

### Explorer enhancements
- Dimension hierarchy drill-down (Period: Year/Quarter/Month; Domain: Group/Domain/Detail)
- Default aggregation per indicator (`default_agg` in `dim_domain_detail`)
- Power BI-style ◄/► drill buttons

### Brand
- Renamed from "Open Reporting" to "Otwarte Raporty" across all products

### Infrastructure
- Single Hetzner VPS, Docker Compose (nginx, PostgreSQL 16, Ghost 5)
- SSL/TLS via Let's Encrypt
- Systemd services for all three portal apps

---

## Unreleased

### Documentation & project hygiene (2026-03-28)
- Expanded `docs/DOMAINS.md` to full 18-domain catalogue with Eurostat themes, GUS equivalents, and subcategories
- Archived all three Linear documents (Domain Taxonomy, Tech Stack & Environment, Data Catalog) — GitHub is now single source of truth for all documentation
- Updated Linear project description (mobile live, Instagram-only social, Polish-first language)
- Rewrote `docs/ARCHITECTURE.md` to reflect current stack (DuckDB/PostgreSQL roles, systemd services, URL structure)
- Rewrote `README.md` with correct product list, live URLs, doc index
- Added `docs/MVP.md`, `docs/ROADMAP.md`, `docs/CONTRIBUTING.md`, `docs/RELEASE_NOTES.md`
- Added `docs/CONTRIBUTING.md` defining post-MVP agile workflow (Linear → feature branch → PR → review → merge)
- Added `.claude/playbooks/social.md` for Instagram publishing flow
- Added `.claude/lessons-learned.md` for continuous process improvement
