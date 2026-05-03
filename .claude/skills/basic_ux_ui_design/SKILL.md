---
name: basic_ux_ui_design
description: "UX/UI design artifact. Defines what a frontend design specification is — layout, charts, KPIs, filters, and interactions. Produced by /composite_design and consumed by /composite_build."
user-invocable: false
---

# UX/UI Design

The UX/UI design artifact is the frontend section of the design document. It specifies
every visual and interaction element of the product. The build step implements this exactly —
no design decisions are made during build.

Produced by: `/composite_design` (dashboard-dev agent)
Consumed by: `/composite_build` (dashboard-dev agent)

---

## Location

Embedded in: `products/domain-briefs/{domain}/composite_design.md` (frontend section)
Or standalone: `products/domain-briefs/{domain}/ux-ui.md`

---

## Structure

**Dashboard / visual products:**
1. **Page structure** — list of pages, navigation between them
2. **Page layout** — for each page: filter pane content, section names, chart placement
3. **KPI cards** — for each card: metric name (Polish), formula, unit, comparison, trend direction
4. **Chart specifications** — for each chart:
   - Chart type (must match decision table in `dashboard/references/chart-types.md`)
   - Title (analytical conclusion in Polish, not a description of the chart type)
   - X-axis: field, label (Polish), unit
   - Y-axis: field, label (Polish), unit
   - Series: names (Polish), colours (theme tokens only — from `products/visuals/lib/theme.py`)
   - Data source: warehouse table or semantic model measure
5. **Filter specifications** — for each filter: field, type (dropdown/range/tile/slider), scope (page/global), default value
6. **Interactions** — which filters drive which charts; drill-down behaviour

---

## How to produce

When producing this artifact within `/composite_design`, specify every element below:

**Layout**
- Number of pages and navigation structure
- Grid per page (columns, rows, panel sizes)
- Header, footer, sidebar content and placement
- Filter bar position (top, sidebar, inline)

**Chart specifications** (for each chart in the requirements)
- Chart type and justification (reference `dashboard/references/chart-types.md`)
- X-axis: field, Polish label, format
- Y-axis: field, Polish label, format, scale
- Series: Polish names, specific palette values from `theme.py`
- Reference lines if any (benchmark, target, zero line)
- Polish title stating the analytical conclusion (not the chart type)

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
- Which palette tokens are used where (reference `products/visuals/lib/theme.py`)
- Semantic assignments: positive = X, negative = Y, neutral = Z
- No red/green-only distinctions (colour-blind safe)

**Typography and spacing**
- Title sizes, label sizes, padding conventions (follow Nordic design system)

---

## Quality criteria

- Every chart has a title stating the analytical conclusion, not the chart type
- No dual y-axis charts — use subplots if scales differ
- No pie charts with more than 3 categories
- All labels in Polish with correct diacritics
- Colours from Nordic palette only — no hardcoded hex values
- Max 4–5 series per line chart (Cowan 4±1)
- Every filter has a defined scope and default value

---

## Standards

- `team/standards/build/visualisation.md`
- `dashboard/references/theme.md`
- `dashboard/references/chart-types.md`
- `team/knowledge-base/ux-perception/perception.md`
- `team/knowledge-base/visualization/principles.md`
- Reviewed by: `visualization-reviewer`, `visual-screenshot-reviewer`
