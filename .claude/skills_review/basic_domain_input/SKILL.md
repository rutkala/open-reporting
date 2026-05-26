---
name: basic_domain_input
description: "Domain input artifact. Defines what a domain brief is and how to produce it — the structured research document that grounds all design and requirements work in how practitioners actually analyse a domain."
user-invocable: false
---

# Domain Input

A domain input (domain brief) is the research foundation for any product in a specific
business or economic domain. It documents how practitioners in that domain think, what
KPIs they use, what questions they ask, and what authoritative sources say.

Produced by: `/basic_research` (invoked by `/composite_document`)
Consumed by: `/composite_document`, `/composite_design`, any domain-specific product skill

---

## Location

`products/domain-briefs/{domain}/domain-brief.md`

---

## Structure

Every domain brief must contain:

1. **Domain overview** — what this domain covers, key actors, key questions practitioners ask
2. **Authoritative sources** — publications, statistical agencies, methodological frameworks used
3. **Key indicators** — canonical KPIs used by practitioners, with definitions and units
4. **Analytical patterns** — what comparisons, breakdowns, and time horizons are standard
5. **Polish context** — what is specific to Poland: GUS methodology, structural breaks, known data quality issues
6. **Data availability** — which indicators exist in the warehouse; which need ingestion

---

## How to produce

When `/basic_research` is invoked for domain research (by `/composite_document`), follow these steps:

### Step 0 — Check existing KB module

Before any web research, check `docs/README.md` for an existing domain module:
- If a module exists (e.g. `docs/public-finance/principles.md`): read it first. Use it as the foundation — skip or abbreviate what it already covers. Fill only the gaps with targeted web research.
- If no module exists: proceed with full research, then consider whether findings warrant creating a new module (raise with PO after the brief).

### Step 1 — Define domain scope

Clarify before searching:
- What economic/social/policy area does this domain cover?
- Who are the practitioners? (economists, statisticians, policy analysts, journalists)
- What level? (national, regional, EU, global)
- What is the Polish context? (regulated, published, or analyzed specifically for Poland)

### Step 2 — Research authoritative sources

Search and read:
- **Official statistics:** Eurostat Statistics Explained, GUS methodology and publications, IMF/World Bank/OECD domain reports, relevant Polish ministry publications
- **Standard frameworks:** how do international organisations structure analysis of this domain? What decompositions and comparisons are standard?
- **Dashboard precedents:** OECD Data, World Bank Open Data, Eurostat dashboards, national statistical portals

Prefer primary sources (official publications, methodology papers) over secondary summaries. Check dates — prefer 2023+.

### Step 3 — Identify standard KPIs

For each KPI practitioners actually use:
- Name (English + Polish if known)
- Definition (how calculated)
- Standard presentation (% of GDP, per capita, index, etc.)
- Typical breakdowns (region, sector, demographic, time period)
- Why it matters

Focus on what is genuinely standard in the field, not what is easy to compute.

### Step 4 — Identify analytical angles

What questions do analysts, policymakers, and citizens ask about this domain?
These become the tabs, sections, and charts of any dashboard in this domain.

### Step 5 — Identify visualization conventions

What chart types do experts use? Time series, waterfall, stacked bar, maps, comparison charts?
What periods are standard (annual, quarterly, monthly)?

### Step 6 — Produce the domain brief

Write using this template:

```
## Domain Brief: {Domain Name}

### What this domain is
{2–3 sentences: definition, scope, Polish context}

### Key practitioners and their questions
{Who analyses this domain, what questions they ask}

### Standard KPIs
| KPI | Definition | Unit | Standard breakdown |
|-----|-----------|------|-------------------|

### Standard analytical angles
1. {angle 1 — headline metric + trend}
2. {angle 2 — composition / breakdown}
3. {angle 3 — comparison / benchmark}
4. {angle 4 — specific domain question}

### Visualization conventions
{Chart types and layouts standard in authoritative publications}

### Data dimensions available in warehouse
{Which curated columns map to these KPIs}

### Gap analysis
{KPIs that are standard but not yet in the warehouse}

### Sources consulted
{Links to authoritative publications used}
```

### Step 6.5 — Gate: brief review

After writing the brief, spawn `brief-reviewer`:
- **BLOCK** → fix P1 issues, revise, re-run reviewer
- **CONDITIONAL** → add P2 findings to a Notes / Caveats section, then proceed
- **PASS** → proceed

---

## Quality criteria

- Every indicator cites an authoritative source (Eurostat, GUS, IMF, ministry)
- No indicators invented without practitioner precedent
- Polish structural breaks documented (methodological changes in time series)
- Data availability status confirmed against warehouse, not assumed

---

## Standards

- `docs/business-analysis/principles.md`
- `docs/analytical-methods/principles.md`
- `docs/business-analysis/reviewing.md`
