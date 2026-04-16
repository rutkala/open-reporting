---
name: requirements
description: "Produce a requirements document for any product. Defines purpose, audience, deliverables, and acceptance criteria. Called from product orchestrator skills."
user-invocable: false
---

# Requirements Document

Defines what the product must be and do. This document is the contract for the build —
QA tests against it. Every subsequent step derives its scope from this document.

Applies to any product type: dashboard, article, research, social content, portal, blog.

## Inputs

- Initial request (Linear issue or captured intake from product skill Step 1)
- Domain brief (`products/domain-briefs/{domain}.md`) — provides domain context

## Standards and knowledge

- Read `team/standards/build/requirements.md`
- For knowledge-intensive products (dashboard, research): also read
  `team/knowledge-base/business-analysis/kpi-indicator-design.md`

## Agent

**business-analyst** — defines scope, writes the document.

## Mandatory sections

All sections are required. The content of each adapts to the product type.

### 1. Purpose
One paragraph. What problem does this product solve? What question does it answer?
What decision or action does it enable?

### 2. Target Audience
Who will use or consume this product? What is their role and context?
What is their level of analytical or domain knowledge?

### 3. Deliverables
What exactly will be produced? Be specific.

*For dashboards:* pages, KPIs, charts, filters
*For articles:* topic, angle, key claims, format, length
*For social content:* platform, format, key message, tone
*For research:* research question, methodology, output format

### 4. Content Requirements
What must the product contain? List the specific elements.

*For dashboards:* KPI definitions (name, formula, unit, interpretation), chart specifications per page
*For articles:* key points to cover, data or evidence required, sources
*For social content:* messaging pillars, visual requirements
*For research:* hypotheses, data required, analytical methods

### 5. Data Sources
What data is required to produce this product?
Which warehouse tables, external sources, or research materials?
Note any gaps — data needed but not yet available.

### 6. Acceptance Criteria
Specific, testable statements used in QA.
Format: "When [condition], the product [expected result]."
Minimum 3 criteria. Each must be verifiable by a reviewer.

### 7. Out of Scope
Explicitly list what is NOT included in this version.
This prevents scope creep during build.

## Evaluator

Spawn **brief-reviewer** with the document as input.
- BLOCK → fix P1 issues, revise, re-run before proceeding
- CONDITIONAL → add P2 findings as caveats, proceed
- PASS → proceed

## Output

Markdown file saved on the feature branch. Present to PO for approval before
the next step begins.
