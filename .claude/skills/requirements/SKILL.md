---
name: requirements
description: "Produce a requirements document for a dashboard. Defines what to build — KPIs, pages, filters, data sources, acceptance criteria. Called from /dashboard Step 3."
user-invocable: false
---

# Requirements Document

Produces a requirements document that defines exactly what the dashboard must contain.
This document is the contract for the build — QA will test against it in Step 7.

## Inputs

- Initial request from Step 1 (Linear issue or captured intake)
- Domain brief from Step 2 (`products/domain-briefs/{domain}.md`)

## Standards and knowledge

- Read `team/standards/build/requirements.md` before writing
- Read `team/knowledge-base/business-analysis/kpi-indicator-design.md` for KPI definitions

## Agent

**business-analyst** — researches domain context, defines KPIs, writes the document.

## Mandatory sections

The requirements document must contain all of the following. None can be omitted.

### 1. Problem Statement
One paragraph. What question does this dashboard answer? What decision does it support?

### 2. Target Audience
Who will use this dashboard? What is their role? What is their analytical background?

### 3. KPI Definitions
For each KPI:
- Name (Polish label for display)
- Formula or calculation method
- Unit and scale
- Interpretation (what does a high/low value mean?)
- Source indicator(s) from warehouse

### 4. Pages and Structure
For each page:
- Page name and purpose
- Charts on this page (type, data, axes)
- KPI cards on this page
- Filters available

### 5. Data Sources
What data is required? Which warehouse tables or dbt models?
Note any gaps — data that is needed but not yet ingested.

### 6. Acceptance Criteria
Specific, testable statements. Each criterion will be checked in QA.
Format: "When [condition], the dashboard shows [expected result]."

### 7. Out of Scope
Explicitly list what is NOT included in this version.

## Evaluator

After writing, spawn **brief-reviewer** with the document as input.
- BLOCK → fix P1 issues, rewrite affected sections, re-run evaluator
- CONDITIONAL → add P2 findings as caveats in the document
- PASS → proceed

## Output

Save as a markdown file on the feature branch. Present to PO for approval.
