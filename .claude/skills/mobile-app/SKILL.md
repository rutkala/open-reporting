---
name: mobile-app
description: "Mobile app product context. Loaded when working on mobile-optimised dashboards (OR-108). Defines what the mobile product is, its layout constraints, and how it differs from the desktop dashboard."
user-invocable: true
---

# Mobile App

The mobile product is a mobile-optimised version of the analytical dashboards,
served at port 8052. It uses the same data layer as desktop dashboards but
applies a responsive, touch-friendly layout.

This skill defines WHAT the mobile product is. The process lives in `/develop`.
For the underlying dashboard components, also load `/dashboard`.

Linear: OR-108

---

## Technology stack

| Layer | Technology |
|-------|-----------|
| Framework | Python + Dash (mobile-optimised layout) |
| Port | 8052 |
| Source | `products/dashboards/mobile/` |
| Data layer | Shared with desktop dashboards (same DuckDB + dbt) |

---

## Input

| Artifact | Location | Produced by |
|----------|----------|-------------|
| Desktop dashboard | `products/dashboards/{domain}/` | `/dashboard` |
| Requirements document | `products/domain-briefs/{domain}/requirements.md` | `/document` |

---

## Output

| Deliverable | Location |
|-------------|----------|
| Mobile Dash app | `products/dashboards/mobile/app.py` |
| Accessible at | `portal.open-reporting.dev` (port 8052) |

---

## Mobile layout rules

- Single-column layout — no side-by-side charts on mobile
- KPI cards stack vertically
- Charts full-width, minimum height 300px
- No hover-dependent interactions — touch-friendly alternatives only
- Filter pane collapses to a drawer on mobile (not fixed sidebar)
- Font size minimum 14px for readability on small screens

---

## Quality gates

- [ ] Layout renders correctly at 375px width (iPhone SE)
- [ ] Layout renders correctly at 768px width (tablet)
- [ ] No horizontal scroll on any screen size
- [ ] Touch targets minimum 44×44px
- [ ] Smoke test passes on mobile app port

---

## Standards

- `team/standards/build/visualisation.md`
- `dashboard/references/theme.md` (shared Nordic theme)
