---
name: dashboard-code
description: "Build the dashboard Dash application. Translates architecture and UX/UI designs into working code. Called from /dashboard Step 6."
user-invocable: false
---

# Dashboard Code

Builds the working Dash application from the architecture and UX/UI designs.
Does not make design or data model decisions — those are already made. This step is pure implementation.

## Inputs

- Architecture design from Step 4 (data model, components, KPI logic)
- UX/UI design from Step 5 (layout, chart specs, colours, labels)
- `products/dashboards/pilot_template/` — the structural mould

## Standards and knowledge

- Read `team/standards/build/visualisation.md` — chart implementation rules, theme usage
- Read `team/standards/build/storage.md` — query patterns, parameterised SQL
- Read `team/knowledge-base/visualization/charts/` — chart-type specific rules

## Agent

**dashboard-dev** — implements the Dash application.

## Implementation rules

- Copy structure from `products/dashboards/pilot_template/` — do not start from scratch
- Output goes to `products/dashboards/{domain}/`
- All user-facing strings (labels, titles, tooltips) in Polish
- All code, variables, functions, file names in English
- Parameterised queries only — no string concatenation in SQL
- Use `products/visuals/lib/theme.py` for all colour references — no hardcoded hex values
- Use `products/visuals/lib/db.py` for warehouse queries
- Chart components from `products/visuals/components/` where they exist

## File structure

```
products/dashboards/{domain}/
  app.py       ← Dash layout and callbacks
  data.py      ← Data fetching functions (calls db.py)
  measures.py  ← KPI calculation logic (if not in dbt)
```

## Evaluator

After implementation, spawn **code-reviewer** and **visualization-reviewer** in parallel.
- BLOCK on either → fix P1 issues, re-run
- CONDITIONAL → note P2 findings, proceed
- PASS → proceed to QA

## Output

Working Dash application at `products/dashboards/{domain}/app.py`.
