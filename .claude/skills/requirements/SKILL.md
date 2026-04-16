---
name: requirements
description: "Produce a requirements document for any product. Defines purpose, audience, deliverables, and acceptance criteria."
user-invocable: false
---

# Requirements

Defines what the product must be and do. This document is the contract for the build —
QA tests against it and every subsequent step derives its scope from it.

Applies to: dashboard, article, research, social content, portal, blog.

## Input

- Initial request (Linear issue or captured intake from product skill Step 1)
- Domain brief (`products/domain-briefs/{domain}.md`)

## Output

- Requirements document (markdown file on feature branch)
- Approved by PO before next step begins

## Components

| Role | Agent |
|------|-------|
| Author | business-analyst |
| Reviewer | brief-reviewer |

## Steps

1. Read the domain brief and the initial request
2. Draft all mandatory sections (see Instructions)
3. Spawn **brief-reviewer** — fix P1 findings before proceeding; add P2 as caveats
4. Present to PO and wait for explicit approval

## Instructions

The document must contain all seven sections. None can be omitted.

**1. Purpose**
One paragraph. What problem does this product solve? What question does it answer?
What decision or action does it enable?

**2. Target Audience**
Who will use or consume this product? Their role, context, and analytical background.

**3. Deliverables**
What exactly will be produced? Be specific to the product type:
- Dashboard: pages, KPIs, charts, filters
- Article: topic, angle, key claims, format, length
- Social content: platform, format, key message, tone
- Research: research question, methodology, output format

**4. Content Requirements**
Specific elements the product must contain:
- Dashboard: KPI definitions (name, formula, unit, interpretation), chart list per page
- Article: key points, data or evidence required, sources to cite
- Social content: messaging pillars, visual requirements
- Research: hypotheses, data needed, analytical methods

**5. Data Sources**
What data is required? Which warehouse tables, external sources, or research materials?
Note gaps — data needed but not yet available.

**6. Acceptance Criteria**
Specific, testable statements used in QA.
Format: "When [condition], the product [expected result]."
Minimum 3 criteria. Each must be verifiable by a reviewer without ambiguity.

**7. Out of Scope**
Explicitly list what is NOT included in this version.

## Standards

- `team/standards/build/requirements.md`
- `team/knowledge-base/business-analysis/kpi-indicator-design.md` (data-driven products)
