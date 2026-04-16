---
name: ux-ui
description: "Produce a UX/UI design for a dashboard. Defines layout, chart specifications, colour usage, and interaction behaviour. Called from /dashboard Step 5."
user-invocable: false
---

# UX/UI Design

Produces a visual design specification that the dashboard code step uses as its blueprint.
Every visual decision must be made here — the code step does not make design decisions.

## Inputs

- Requirements document from Step 3
- Architecture design from Step 4 (component inventory)

## Standards and knowledge

- Read `team/standards/build/visualisation.md` — Nordic design system, colour palette, chart rules
- Read `team/knowledge-base/ux-perception/perception.md` — pre-attentive attributes, Gestalt, WCAG
- Read `team/knowledge-base/visualization/principles.md` — IBCS, colour semantics, reference lines
- Read `team/knowledge-base/visualization/ui-principles.md` — layout, grid, dashboard types

## Agent

**dashboard-dev** — designs layout, selects chart types, specifies visual details.

## Mandatory sections

### 1. Layout
- Number of pages and navigation structure
- Grid system per page (columns, rows, panel sizes)
- Header and footer content
- Sidebar or top-bar filters placement

### 2. Chart Specifications
For each chart in the component inventory:
- Chart type and justification (why this type for this data)
- X-axis: field, label (Polish), format
- Y-axis: field, label (Polish), format, scale (linear/log)
- Series: names (Polish), colours (specific palette values)
- Reference lines if any
- Title and subtitle (Polish)

### 3. KPI Cards
For each KPI card:
- Metric label (Polish)
- Value format (number format, unit)
- Comparison: vs previous period? vs benchmark?
- Colour semantics: when green/red/neutral

### 4. Filters
For each filter:
- Label (Polish)
- Component type (dropdown, multi-select, date range, slider)
- Scope: applies to one page or all pages
- Default value

### 5. Colour Usage
- Which palette values are used where (reference `theme.py` values)
- Semantic assignments: positive = X, negative = Y, neutral = Z
- Colour-blind safe: confirm no red/green-only distinctions

### 6. Typography and Spacing
- Title sizes
- Label sizes
- Padding and margin conventions

## Evaluator

No automated evaluator at design stage. The visual-screenshot-reviewer runs in Step 7 (QA)
against the rendered dashboard.

## Output

Save as a markdown file on the feature branch.
