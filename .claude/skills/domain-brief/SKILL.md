---
name: domain-brief
description: "Research a business/economic domain before any design work. Finds how practitioners analyze this domain, what KPIs they use, what questions they ask, and what authoritative publications say. Produces a domain brief that drives dashboard design, indicator selection, and data modelling."
user-invocable: true
argument-hint: "<domain name, e.g. 'Public Finance' or 'Labour Market'>"
---

# Domain Brief

Research how experts in this domain analyze data. Design decisions come AFTER this research, not before.

## Domain
`$ARGUMENTS`

---

## Step 0 — Check for existing domain module

Before doing any web research, check `team/analytics/INDEX.md` for an existing domain module:
- If a module exists for this domain (e.g. `team/analytics/domains/public-finance.md`): **read it first**. Use it as the foundation — skip or abbreviate the web research steps it already covers. Note any gaps the module doesn't address and fill those with targeted web research.
- If no module exists: proceed with full research below, then consider whether findings warrant creating a new module (raise with PO after the brief).

---

## Step 1 — Define the Domain Scope

Before searching, clarify:
- What is this domain? What economic/social/policy area does it cover?
- Who are the practitioners? (economists, statisticians, policy analysts, journalists, finance ministers, etc.)
- What level are we targeting? (national, regional, EU, global)
- What is the Polish context? (is this domain regulated, published, or analyzed specifically for Poland?)

---

## Step 2 — Research Authoritative Sources

Search for and read:

**Official statistical publications:**
- Eurostat Statistics Explained pages for this domain
- GUS (Central Statistical Office of Poland) methodology and publications
- IMF, World Bank, OECD reports for this domain (e.g., IMF Fiscal Monitor for Public Finance)
- Relevant Polish ministry publications (MF for finance, MPiPS for labour, MZ for health)

**Standard analytical frameworks:**
- How do international organizations structure analysis of this domain?
- What decompositions, breakdowns, and comparisons are standard?
- What time horizons are used? (annual, quarterly, long-term trends)

**Dashboard and visualization precedents:**
- How do central banks, statistical offices, and policy institutions visualize this domain?
- What does a well-designed Public Finance / Labour / Health dashboard look like?
- Look for: OECD Data, World Bank Open Data, Eurostat dashboards, national statistical portals

Use web search and web fetch for each source. Prefer primary sources (official publications, methodology papers) over secondary summaries.

---

## Step 3 — Identify Standard KPIs

Extract the metrics that practitioners in this domain actually use. For each KPI:
- Name (in English and Polish if known)
- Definition (how is it calculated?)
- Standard presentation (as % of GDP, per capita, index, etc.)
- Typical breakdowns (by region, sector, demographic group, time period)
- Why it matters (what decision or question does it inform?)

Focus on what is genuinely standard, not what is easy to compute from available data.

---

## Step 4 — Identify Analytical Angles

What questions do analysts, journalists, policymakers, and citizens ask about this domain?

Examples for Public Finance:
- Is the budget in deficit or surplus? How has it changed over time?
- What is the composition of revenue (taxes, contributions, other)?
- How does Poland's fiscal position compare to EU/Eurozone peers?
- Is public debt sustainable? What is the trajectory?

These questions become the tabs, sections, and charts of the dashboard.

---

## Step 5 — Identify Visualization Conventions

What chart types do experts use for this domain?
- Time series vs. cross-sectional
- Waterfall charts for budget composition
- Stacked bars for breakdown
- Maps for geographic analysis
- Comparison charts (Poland vs EU average)
- Which periods are standard (annual, quarterly, monthly)?

---

## Step 6 — Produce the Domain Brief

Write a structured brief:

```
## Domain Brief: {Domain Name}

### What this domain is
{2–3 sentences: definition, scope, Polish context}

### Key practitioners and their questions
{Who analyzes this domain, what questions do they ask}

### Standard KPIs
| KPI | Definition | Unit | Standard breakdown |
|-----|-----------|------|-------------------|
| ...

### Standard analytical angles
1. {angle 1 — headline metric + trend}
2. {angle 2 — composition / breakdown}
3. {angle 3 — comparison / benchmark}
4. {angle 4 — specific domain question}

### Visualization conventions
{What chart types and layouts are standard in authoritative publications}

### Data dimensions available in warehouse
{Which of our curated.all_indicators / curated.mart_{domain} columns map to these KPIs}

### Gap analysis
{KPIs that are standard but not yet in our data — note for future ingestion}

### Sources consulted
{Links to authoritative publications used}
```

---

## Step 7 — Use the Brief

The domain brief informs:
- Dashboard design: what tabs, KPIs, and charts are appropriate for this domain
- Data modelling: which indicators belong in `dim_domain_detail` and what the mart's domain hierarchy should be
- Gold mart design: what derived metrics and categorical columns make sense

After completing the brief, use it as the basis for design proposals. Share the brief (or its key findings) with the PO when presenting a design — not necessarily for approval, but to show the domain grounding behind the decisions. The PO can then challenge the interpretation, add context from their knowledge of the product's audience, or confirm the direction.

The brief is a starting point for discussion, not a final specification. If the PO has specific domain knowledge or preferences that differ from what the research suggests, that is valuable input — incorporate it.
