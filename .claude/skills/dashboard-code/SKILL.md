---
name: dashboard-code
description: "Build the dashboard Dash application. Pure implementation — translates architecture and UX/UI designs into working code."
user-invocable: false
---

# Dashboard Code

Builds the working Dash application. No design or data model decisions are made here —
those are already specified. This step is pure implementation.

## Input

- Architecture design (data model, component inventory, KPI calculation logic)
- UX/UI design (layout, chart specs, colours, Polish labels)

## Output

- Working Dash application at `products/dashboards/{domain}/`
- Passes code-reviewer and visualization-reviewer before QA

## Components

| Role | Agent |
|------|-------|
| Author | dashboard-dev |
| Code reviewer | code-reviewer |
| Visualization reviewer | visualization-reviewer |

code-reviewer and visualization-reviewer run in parallel after implementation.

## Steps

1. Read architecture design and UX/UI design in full
2. Copy structure from `products/dashboards/pilot_template/`
3. Implement data layer (`data.py`)
4. Implement measures (`measures.py`) if KPI logic not in dbt
5. Implement layout and callbacks (`app.py`)
6. Spawn **code-reviewer** and **visualization-reviewer** in parallel
7. Fix P1 findings from either reviewer; note P2 findings
8. Verify dashboard runs locally before handing to QA

## Instructions

**File structure**
```
products/dashboards/{domain}/
  app.py        ← Dash layout and callbacks
  data.py       ← Data fetching (calls products/visuals/lib/db.py)
  measures.py   ← KPI logic not handled in dbt (if needed)
```

**Implementation rules**
- Copy from `products/dashboards/pilot_template/` — do not start from scratch
- All user-facing strings (labels, titles, tooltips, axis labels) in Polish
- All code identifiers (variables, functions, files, routes) in English
- Parameterised queries only — no string concatenation in SQL
- Colour references via `products/visuals/lib/theme.py` — no hardcoded hex values
- Warehouse queries via `products/visuals/lib/db.py`
- Chart components from `products/visuals/components/` where they exist

**Verification before handoff**
Run the app locally: `PYTHONPATH=/opt/open-reporting python3 products/dashboards/{domain}/app.py`
Confirm it loads without errors before proceeding to QA.

## Standards

- `team/standards/build/visualisation.md`
- `team/standards/build/storage.md`
- `team/knowledge-base/visualization/charts/` (chart-type specific rules)
