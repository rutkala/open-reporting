---
name: basic_requirements
description: "Requirements document artifact. Defines what a requirements document is — the contract for what the product must be and do. Produced by /composite_document and consumed by /composite_design and all product skills."
user-invocable: false
---

# Requirements

The requirements document defines what the product must be and do. Every subsequent step
derives its scope from it — design implements what it says, QA tests against it,
and release confirms it was delivered.

Produced by: `/composite_document`
Consumed by: `/composite_design`, `/composite_build`, `/composite_evaluate`, all product skills

---

## Location

`products/domain-briefs/{domain}/basic_requirements.md`

---

## Structure

Every requirements document must contain all seven sections. None can be omitted.

**1. Purpose**
One paragraph: what question or decision this product answers, and why it matters now.
Grounds the product in a real analytical or user need — not just "a dashboard showing X".

**2. Target audience**
Who will use this product. Their analytical background. What decisions they make with it.
Determines the level of complexity, annotation needed, and language register.

**3. Deliverables**
Exact list of what will be produced:
- Dashboard: URL, pages, KPIs, charts, filters
- Article: topic, angle, key claims, format, length
- Social content: platform, format, key message
- Research: research question, methodology, output format

**4. Content requirements**
What must be in the product:
- KPIs and metrics (with Polish labels and unit)
- Key analytical angles (from domain brief)
- Mandatory comparisons, breakdowns, or time horizons
- Any specific user interactions (filters, drill-downs, highlights)

**5. Data sources**
For each data source:
- Name and location (warehouse table or external source)
- Availability status (exists / needs ingestion)
- Known quality issues or gaps

**6. Acceptance criteria**
Numbered list. Each criterion must be testable — observable and verifiable without ambiguity.
Format: "When [condition], the product [shows/does X]."
Minimum 3 criteria. No vague criteria ("looks good", "is fast").

**7. Out of scope**
Explicit list of what this version does NOT include.
Prevents scope creep during build and QA.

---

## Quality criteria

- Every acceptance criterion is independently verifiable
- No criterion uses vague language ("appropriate", "reasonable", "fast")
- Data sources have availability status confirmed against the warehouse
- Out of scope is explicit — does not rely on what is absent to imply exclusion

---

## Standards

- `team/standards/build/requirements.md`
- `team/knowledge-base/business-analysis/kpi-indicator-design.md`
- Reviewed by: `brief-reviewer`
