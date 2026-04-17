# Dashboard Knowledge Base

## 1. Overview

A dashboard is a single screen that brings together a small set of metrics, along with
enough context to support a decision or monitor a situation. It compresses raw data into
ranked lists, trends, and clear status indicators — enabling users to move from questions
to action rapidly.

Dashboards are a display medium, not a data product. The data behind them can come from
any source (warehouse, API, spreadsheet). The tool used to build them (Power BI, Tableau,
Python/Dash, Excel, Looker) is irrelevant to what a well-designed dashboard must contain.

Good dashboard design shortens the gap between a question and the next action.

---

## 2. Authoritative sources

| Source | URL / Path | What it covers |
|--------|-----------|----------------|
| Stephen Few — Information Dashboard Design | https://www.analyticspress.com/idd.php | Foundational: definition, design principles, common mistakes, perceptual rules |
| IBCS Standards 1.2 | https://www.ibcs.com/ibcs-standards-1-2/ | SUCCESS formula, semantic notation, chart type standards, scenario notation |
| IBCS Wikipedia | https://en.wikipedia.org/wiki/International_Business_Communication_Standards | IBCS overview, three pillars, governance |
| DataCamp — Dashboard Design | https://www.datacamp.com/tutorial/dashboard-design-tutorial | Dashboard types, layout patterns, chart selection, common mistakes, accessibility |
| Yellowfin BI — Design Principles | https://www.yellowfinbi.com/blog/key-dashboard-design-principles-analytics-best-practice | 10 design principles, 5-second rule, cognitive load |

---

## 3. Key patterns and conventions

### Dashboard types

| Type | Primary question | Cadence | Audience | Key design element |
|------|-----------------|---------|----------|--------------------|
| **Strategic** | Are we on track toward goals? | Monthly / quarterly | Leadership, stakeholders | Comparisons vs. baselines, annotations |
| **Analytical** | Why is this happening? What are the trends? | Ad-hoc / deep dive | Analysts, domain experts | High interactivity, filters, drill-downs |
| **Operational** | What is happening right now? | Real-time / minute | Operations, on-call | Big status, alerts, low latency |
| **Tactical** | Are we hitting this week's targets? | Daily / weekly | Managers, squad leads | Progress vs. targets, ownership clarity |
| **Explanatory** | What does this mean? (storytelling) | As-needed | Broad audiences, external | Narrative-driven, minimal controls |

Most Open Reporting dashboards are **analytical** — they support exploration and insight
from Polish public data, not real-time monitoring.

### Visual hierarchy (Z-pattern scanning)
Users scan dashboards top-left → top-right → bottom-left → bottom-right. Content must be
ordered accordingly:

- **Top:** Status, KPIs, targets — answers "are we on track?"
- **Middle:** Trends and comparisons — explains the movement
- **Bottom:** Details, breakdowns, attribution

### Layout patterns

**Top-rail** — KPIs and filters in a horizontal header, charts below
- Best for: "Are we on track?" strategic / tactical questions
- Pros: KPIs in prime real estate; visible filters
- Cons: Can feel tall on small screens

**Left-rail (sidebar)** — navigation and filters in a vertical column, charts to the right
- Best for: Analytical dashboards with frequent view switching or many filters
- Pros: Stable navigation; more vertical chart space
- Cons: Sidebar consumes width; below-fold content ignored

### The five-second rule
Users should grasp the main insight within five seconds of viewing the dashboard. If they
cannot, the layout, hierarchy, or clarity needs improvement.

### Cognitive load limit
5–9 visuals and 5–9 KPIs per dashboard page maximum. More creates overwhelm and dashboard
avoidance. Secondary metrics belong in drill-down views, not the main page.

---

## 4. Component / API reference

### KPI / Scorecard

The primary instrument for communicating the headline number.

| Element | Required | Notes |
|---------|---------|-------|
| Label | Yes | Clear, descriptive — not a column name |
| Value | Yes | Formatted with unit and scale |
| Comparison | Yes | Δ vs. target, prior period, or benchmark |
| Δ (absolute) | Yes | Absolute difference from reference |
| Δ% (relative) | Recommended | Relative difference from reference |
| Trend indicator | Recommended | ▲/▼ or sparkline |
| Timestamp | Yes | When was this data last updated |

IBCS rule: every KPI must display absolute variance (Δ) and relative variance (Δ%) against a reference scenario (plan or prior year). This allows immediate assessment of magnitude and direction.

### Charts

| Data situation | Chart type | Notes |
|---------------|-----------|-------|
| Change over time | Line or column | Line for continuous; column for discrete periods |
| Ranking | Horizontal bar | Sort descending; easier label readability |
| Composition over time | Stacked column or area | 100% variant for share; absolute for volume |
| Variance / bridge | Waterfall | Explains how a base value becomes a final value |
| Part-to-whole (static) | Stacked bar | Max 5–6 categories; avoid pie charts |
| Distribution | Histogram or box plot | For spotting outliers and spread |
| Relationship / correlation | Scatter plot | Add trend line to clarify direction |
| Progress vs. goal | Bullet chart | Compact: value + target + qualitative bands |
| Geography — rates | Choropleth map | Colour encodes value per region |
| Geography — counts | Dot / bubble map | Size encodes quantity |
| Precise values | Table | Freeze key columns; add sparklines for trend |

**Avoid:** Pie charts with more than 3 slices, dual-axis charts (distort comparisons, create false correlations), 3D effects (distort values), rainbow colour palettes.

### Filters / Slicers

| Filter type | When to use |
|-------------|-------------|
| Dropdown | Single-select from a long list |
| Multi-select / checklist | Multiple simultaneous selections from a short list |
| Tile / button group | Single-select from 3–7 visually prominent options |
| Range / slider | Numeric or date range selection |
| Date picker | Specific date or period selection |

Filter design rules:
- Place global filters above content (top-rail) or in a stable sidebar (left-rail)
- Show what is currently applied — hidden filter states cause confusion
- Ship with safe defaults so the first view is immediately useful
- 5 precise filters beats 15 vague ones — filter count is a design decision, not a feature

### Context and narrative

Every metric needs four context layers (DataCamp):
1. **Comparison** — target, prior period (YoY), or benchmark
2. **Scope** — units, active date range, active filters
3. **Freshness** — exact timestamp of last data update
4. **Nuance** — small notes where the number needs qualification ("Refunds excluded", "VAT included")

Titles should state the analytical conclusion, not just label the chart:
- Weak: "Employment 2018–2024"
- Strong: "Employment grew 4% in 2024, returning to pre-pandemic levels"

### Data attribution

Every dashboard must include:
- Source name(s) and publication/methodology reference
- Data freshness date (when the underlying data was last updated)
- Any material methodological notes (what is excluded, how rates are calculated)

---

## 5. Examples

### Inverted pyramid content structure
```
┌─────────────────────────────────────────────┐
│  KPI row: Unemployment 5.1%  ▲ +0.3pp YoY  │  ← Status / answer
│  KPI row: Employment rate 74.2%  ▼ -0.1pp  │
├─────────────────────────────────────────────┤
│  Line chart: Employment trend 2018–2024     │  ← Why / context
│  Stacked column: Employment by sector       │
├─────────────────────────────────────────────┤
│  Table: Regional breakdown                  │  ← Details
│  Source: GUS — updated Q4 2024             │
└─────────────────────────────────────────────┘
```

### Chart-to-question mapping
```
Question                          → Chart
-------------------------------------------
"Is the trend up or down?"        → Line chart
"Which region is largest?"        → Horizontal bar (sorted)
"How does this compare to plan?"  → Bullet chart / KPI with Δ
"What explains the change?"       → Waterfall chart
"How are we distributed?"         → Histogram or box plot
"Is there a relationship?"        → Scatter plot
"What's the regional pattern?"    → Choropleth map
```

### IBCS scenario notation
```
Actuals (AC):     ████  solid dark fill
Prior year (PY):  ░░░░  solid lighter fill
Plan (PL):        □□□□  outlined / hollow
Forecast (FC):    ╱╱╱╱  hatched fill
```

Variance labels: Δ for absolute difference, Δ% for relative difference.

---

## 6. Decisions and trade-offs

**No pie charts for multi-category data**
Decision: use horizontal bar charts (sorted descending) instead of pie charts for
part-to-whole comparisons with more than 3 categories.
Why: human visual system cannot accurately compare arc lengths or angles; sorted bars
allow direct length comparison. Both IBCS and Stephen Few recommend this consistently.

**No dual y-axis**
Decision: never place two differently-scaled measures on a single chart with two y-axes.
Why: dual axis allows the author to manipulate the apparent correlation between two
unrelated series by scaling independently. Split into two vertically aligned panes instead.

**Every KPI includes a comparison value**
Decision: a KPI displayed without a reference (target, prior period, or benchmark) is
incomplete — it provides no basis for evaluation.
Why: a number alone has no meaning. "Unemployment 5.1%" is a fact; "Unemployment 5.1%,
down 0.3pp from last year, still above 4.5% pre-pandemic baseline" is intelligence.

**Titles state conclusions, not descriptions**
Decision: chart and page titles must communicate what the data shows, not what the chart
is of.
Why: label-only titles force users to interpret the chart themselves. Conclusion-first
titles guide interpretation and reduce cognitive load — especially for non-analyst audiences.

**Cognitive load cap: 5–9 elements**
Decision: 5–9 visuals and 5–9 KPIs per page maximum.
Why: research on working memory limits (Cowan 4±1, Miller 7±2) shows that exceeding this
causes viewers to stop processing individual elements and abandon the dashboard. Additional
metrics belong in drill-down views.

**IBCS scenario notation for multi-scenario charts**
Decision: when a chart shows actuals alongside plan or forecast, apply IBCS fill-style
notation (solid/outlined/hatched) to distinguish measured from projected data.
Why: users must immediately distinguish what is real from what is a target or projection.
IBCS notation conveys this without extra labels or legends.

---

## 7. Gaps and open questions

- **Interaction design patterns** not fully covered — cross-filtering (clicking a chart
  element filters other charts on the page), pattern-matching callbacks, and drill-through
  navigation are standard in modern dashboards but not detailed here.

- **Mobile / responsive design** — dashboard design for small screens requires different
  layout priorities (single-column, swipeable sections, larger tap targets). Not covered.

- **Accessibility beyond contrast** — keyboard navigation, screen reader support for charts,
  ARIA roles, and focus management are referenced in sources but not fully synthesised here.

- **Dashboard governance** — version history, ownership, audit trails, and scheduled
  review processes (are metrics still relevant?) referenced in sources but not detailed.

- **Storytelling / explanatory dashboards** — the narrative structure for explanatory
  dashboards (Setup → Change → Next Step) warrants its own section with examples from
  public reporting contexts.
