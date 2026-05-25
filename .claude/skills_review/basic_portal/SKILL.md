---
name: basic_portal
description: "Portal product context. Loaded when working on portal.open-reporting.dev — the analytical dashboard delivery channel. Defines what the portal is, how dashboards are registered, and what standards apply."
user-invocable: true
---

# Portal

The portal is the public-facing delivery channel for analytical dashboards at
`portal.open-reporting.dev`. It aggregates all domain dashboards and provides
a unified entry point for users.

This skill defines WHAT the portal is. The process for any portal work lives in `/composite_develop`.
For dashboard-specific work, also load `/complex_dashboard`.

---

## Technology stack

| Layer | Technology |
|-------|-----------|
| Framework | Python + Dash |
| Delivery | nginx reverse proxy |
| Dashboards | Served as systemd services |
| Source | `products/portal/` |

## Active services

| Dashboard | Port | Domain |
|-----------|------|--------|
| Labour | 8050 | Labour market |
| Explorer | 8051 | Data explorer |
| Mobile | 8052 | Mobile-optimised |
| Finance | 8053 | Public finance |

---

## Input

| Artifact | Location | Produced by |
|----------|----------|-------------|
| Dashboard product | `products/dashboards/{domain}/` | `/complex_dashboard` + `/composite_build` |
| nginx config | `infra/nginx/conf/` | Infrastructure |

---

## Output

| Deliverable | Location |
|-------------|----------|
| Dashboard accessible at URL | `portal.open-reporting.dev/{domain}` |
| Portal index updated | `infra/nginx/html/` |

---

## Registration process

To add a new dashboard to the portal:
1. Dashboard passes smoke test and code review
2. Add systemd service to `infra/systemd/`
3. Register route in nginx config (`infra/nginx/conf/`)
4. Reload nginx: `docker compose up -d --force-recreate nginx`
5. Verify at `portal.open-reporting.dev`

---

## Quality gates

- [ ] Dashboard loads at its URL with no 502/504 errors
- [ ] Portal index links to the new dashboard
- [ ] Mobile layout verified (OR-108 scope)

---

## Standards

- `docs/visualization/building.md`
- Infrastructure config in `infra/`
