---
name: ux-ui
description: "Produce a UX/UI design for a visual product. Defines layout, chart specifications, colour usage, and interaction behaviour."
user-invocable: false
---

# UX/UI Design

Specifies every visual decision for the product. The code step does not make
design decisions — they are all made here.

Applies to: dashboard, portal (any product with a visual interface).

## Input

- Requirements document
- Architecture design (component inventory)

## Output

- UX/UI design document (markdown file on feature branch)

## Components

| Role | Agent |
|------|-------|
| Author | dashboard-dev |

No automated evaluator at design stage — visual-screenshot-reviewer runs in QA
against the rendered product.

## Steps

1. Read requirements document and architecture component inventory
2. Design layout for each page
3. Specify each chart, KPI card, and filter
4. Define colour usage and typography
5. Save design document on feature branch

## Instructions

**Layout**
- Number of pages and navigation structure
- Grid per page (columns, rows, panel sizes)
- Header, footer, sidebar content and placement
- Filter bar position (top, sidebar, inline)

**Chart specifications** (for each chart in component inventory)
- Chart type and justification
- X-axis: field, Polish label, format
- Y-axis: field, Polish label, format, scale
- Series: Polish names, specific palette values from `theme.py`
- Reference lines if any (benchmark, target, zero line)
- Polish title and subtitle

**KPI cards** (for each card)
- Polish metric label
- Value format (number format, unit, decimal places)
- Comparison: vs previous period, vs benchmark, none
- Colour logic: when positive/negative/neutral colouring applies

**Filters** (for each filter)
- Polish label
- Component type: dropdown, multi-select, date range, slider
- Scope: applies to current page only, or all pages
- Default value

**Colour usage**
- Which palette values are used where (reference `products/visuals/lib/theme.py`)
- Semantic assignments: positive = X, negative = Y, neutral = Z
- Confirm no red/green-only distinctions (colour-blind safe)

**Typography and spacing**
- Title sizes, label sizes, padding conventions

## Standards

- `team/standards/build/visualisation.md`
- `team/knowledge-base/ux-perception/perception.md`
- `team/knowledge-base/visualization/principles.md`
- `team/knowledge-base/visualization/ui-principles.md`
