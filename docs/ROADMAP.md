# Roadmap — Post-MVP

All work follows the process in `CONTRIBUTING.md`. Every item is a Linear issue before any work starts.

**Live backlog and progress:** [Linear — Open Reporting](https://linear.app/open-reporting/project/open-reporting-a1e9c36ff5be)

---

## Phase 1 — Content & Data Depth
*Fill the products with value.*

- Ghost blog operational, first articles published
- Domain dashboards: MAC (macroeconomics), LAB (labour), ENV (environment)
- Data pipeline automated: daily cron, BDL ingestion, NUTS2 expansion
- Social media automated: weekly Economy Snapshot, token refresh

## Phase 2 — Quality & Reliability
*Make the platform trustworthy and maintainable.*

- dbt tests: fact/dimension constraints, referential integrity
- Dashboard error handling: meaningful messages, no blank pages
- Ingestion failure alerts and centralised structured logging
- Health check endpoints, data freshness indicators

## Phase 3 — Growth & Distribution
*Reach more users, cover more data.*

- Social: Facebook Page, Threads API, automated social calendar
- Data: European scope (EU27 macro), historical depth, SDP source
- Portal: all 18 domain dashboards, cross-domain comparison, search
- Infrastructure: CI/CD pipeline, staging environment
