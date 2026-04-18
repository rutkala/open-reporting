---
name: dashboard
description: >
  Dashboard artifact skill. Describes what a dashboard is as an analytical product —
  its purpose, types, components, design principles, and quality criteria. Tool-agnostic:
  applies whether the dashboard is built in Power BI, Tableau, Excel, Python, or any
  other tool. Load this skill when any work targets a dashboard product — designing,
  building, reviewing, or evaluating one.
  Triggers when: "build the dashboard", "design the dashboard", "implement the
  [domain] dashboard", "review the dashboard", or when /develop reaches a dashboard product.
user-invocable: true
---

# Dashboard

A dashboard is a visual display of information needed to monitor performance or understand
a situation at a glance. It presents data from one or more sources, organised to answer
a specific analytical question for a specific audience.

This skill defines WHAT a dashboard is. The process for producing one lives in `/develop`.
How this project builds dashboards technically is documented in `references/`.

---

## Source

Primary sources for this knowledge base: `knowledge-base/summary.md`.
Load it before designing or evaluating any dashboard.

---

## Types

| Type | Primary question | Update frequency | Audience |
|------|-----------------|-----------------|---------|
| **Operational** | What is happening right now? | Real-time or near-real-time | Operations, on-call |
| **Analytical** | Why is this happening? What are the trends? | Daily / weekly / quarterly | Analysts, domain experts |
| **Strategic** | Are we on track toward goals? | Monthly / quarterly | Leadership, stakeholders |

Most Open Reporting dashboards are **analytical** — they support exploration and insight,
not real-time monitoring.

---

## Components

Every dashboard is composed of some combination of these elements:

| Component | Purpose |
|-----------|---------|
| **KPI / Scorecard** | Single key metric with comparison (target, prior period, benchmark) |
| **Chart** | Visual encoding of one or more measures over a dimension (time, category, geography) |
| **Filter / Slicer** | Controls that let the user narrow the data shown (dimension, date range, category) |
| **Context / Narrative** | Text, annotation, or reference lines that explain what the numbers mean |
| **Data attribution** | Source, methodology note, and freshness date — required on every dashboard |

---

## Input

| What | Required |
|------|----------|
| Domain brief | Yes — defines the analytical question, audience, KPIs, and data sources |
| UX/UI design | Yes — defines layout, chart types, filters, and visual hierarchy |
| Data specification | Yes — defines which measures and dimensions are available |

<HARD-GATE>
Do not design or build any dashboard component before the domain brief exists. The
analytical question and audience determine everything downstream: which charts, which
KPIs, which filters, how much detail. Without a domain brief, dashboard decisions have
no grounding.
</HARD-GATE>

---

## Output

A working dashboard that:
- Answers one clear analytical question per page
- Presents KPIs, charts, and filters appropriate to the audience and question
- Includes source attribution and data freshness date
- Uses consistent visual language (colour, typography, layout)

---

## Design principles

**Audience first**
Every design decision — number of charts, level of detail, filter options — follows from
who will use the dashboard and what question they need answered. A dashboard for a policy
analyst is not the same as one for a data journalist.

**One question per page**
Each page or view answers one analytical question. Adding secondary questions creates
cognitive overload and dilutes the main message.

**KPIs set context before charts**
KPI cards at the top establish the overall picture (what is the number, is it good or
bad). Charts below them explain it (why, how, compared to what).

**Filters are navigation, not decoration**
Include only filters the audience will actually use. Every additional filter increases
cognitive load. Prefer pre-filtered views over universal filter panels where possible.

**Titles state conclusions**
A chart titled "Employment 2018–2024" describes. A chart titled "Employment grew 4% in
2024, recovering to pre-pandemic levels" informs. Titles should state what the chart
shows, not just label its contents.

**Source attribution is mandatory**
Every dashboard must state: data source, methodology reference if non-obvious, and
when the data was last updated.

---

## Quality criteria

Before any dashboard is released:
- [ ] Each page answers exactly one analytical question
- [ ] Every chart has a title that states the analytical conclusion
- [ ] KPIs are present and include a comparison value (target, prior period, or benchmark)
- [ ] All filters are necessary — no filter included that the audience will not use
- [ ] Source and freshness date are visible
- [ ] The design was reviewed against the domain brief — every KPI and chart maps to an analytical requirement

---

## Reference files (implementation)

These files describe how dashboards are built in this project's specific stack.
Load them when implementing, not when designing:

| File | When to read it |
|------|----------------|
| `references/template.md` | Before starting any new dashboard — file structure, patterns, how to copy and adapt |
| `references/semantic.md` | Before writing measures.py — Dimension and Measure API, format types, examples |
| `references/components.md` | Before building any chart or UI element — correct function signatures and parameters |
| `references/chart-types.md` | Before choosing a chart type — decision table and hard rules |
| `references/theme.md` | Before writing layout or style code — colour tokens, typography, spacing |
| `knowledge-base/summary.md` | Before designing — dashboard concepts, patterns, best practices |
