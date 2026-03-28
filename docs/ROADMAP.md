# Roadmap — Post-MVP

All work after v0.1.0 follows the process defined in `CONTRIBUTING.md`:
every item below must become a Linear issue before any work starts.

---

## Phase 1 — Content & Data Depth
*Priority: fill the products with value*

### Blog
- [ ] Set up Ghost admin account
- [ ] Add "Portal" link to Ghost navigation
- [ ] Publish first article (data-driven, Polish)

### Portal
- [ ] MAC domain dashboard (GDP, investment, trade)
- [ ] LAB domain dashboard (unemployment, wages — dedicated, richer than current)
- [ ] ENV domain dashboard (emissions, energy)
- [ ] Standard dashboard template (KPI cards + time series + cross-indicator bar)

### Data
- [ ] Automate daily ingestion (NBP + Eurostat cron)
- [ ] BDL (GUS) ingestion — budget, regional data
- [ ] Fix BUS domain: `sts_inpr_a` series_id (`indic_bt=PROD`)
- [ ] Expand NUTS2 coverage beyond 2 current domains

### Social
- [ ] Automate weekly Economy Snapshot post (cron + Plotly card)
- [ ] Instagram token auto-refresh before May 2026 expiry

---

## Phase 2 — Quality & Reliability
*Priority: make the platform trustworthy and maintainable*

### Testing
- [ ] dbt tests for fact/dimension constraints (not null, unique, referential integrity)
- [ ] Smoke tests for Explorer and Labour dashboard query paths
- [ ] Ingestion validation tests (row count, date range, null checks)

### Error handling
- [ ] Meaningful error messages in dashboards (not blank pages)
- [ ] Ingestion failure alerts (email or log monitoring)
- [ ] Query timeout protection in Explorer

### Operations
- [ ] Centralised structured logging (JSON format, single log sink)
- [ ] Health check endpoints for all services
- [ ] Data freshness indicator in dashboard footer

---

## Phase 3 — Growth & Distribution
*Priority: reach more users, more data*

### Social
- [ ] Facebook Page posting (same card format as Instagram)
- [ ] Threads API posting
- [ ] Automated social calendar (weekly schedule)

### Data
- [ ] SDP data source (once format confirmed)
- [ ] European scope: extend to EU27 for macro indicators
- [ ] Historical depth: backfill pre-2000 data where available

### Portal
- [ ] Domain deep-dive dashboards (all 18 domains)
- [ ] Cross-domain comparison view
- [ ] Search across all indicators

### Infrastructure
- [ ] CI/CD pipeline (GitHub Actions — dbt test + lint on PR)
- [ ] Staging environment
- [ ] Automated SSL renewal monitoring
