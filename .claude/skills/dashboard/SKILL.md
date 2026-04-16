---
name: dashboard
description: "Build a complete domain dashboard. Product orchestrator — invokes component skills in mandatory sequence."
user-invocable: true
argument-hint: "<optional: OR-123 or domain name e.g. labour-market>"
---

# Dashboard

Full pipeline for a domain dashboard. Mandatory steps in sequence — none can be skipped.

## Input

- Linear issue (OR-XXX) or domain name, or nothing (intake mode)

## Output

- Working Dash application at `products/dashboards/{domain}/`
- Requirements document, architecture design, UX/UI design, QA report, release document

## Components

| Step | Skill | Agent |
|------|-------|-------|
| Domain brief | `/domain-brief` | business-analyst |
| Requirements | `/requirements` | business-analyst |
| Architecture | `/architecture` | data-engineer + dashboard-dev |
| UX/UI design | `/ux-ui` | dashboard-dev |
| Dashboard code | `/dashboard-code` | dashboard-dev |
| QA | `/qa` | analytical-validator, visual-screenshot-reviewer, code-reviewer, domain-specialist |
| Release | `/release` | main Claude |

## Steps

1. **Initial request** — identify domain and issue (see Instructions)
2. **Domain brief** — run `/domain-brief {domain}` if `products/domain-briefs/{domain}.md` is missing or outdated
3. **Requirements** — run `/requirements` → gate: PO approves before proceeding
4. **Architecture** — run `/architecture` → gate: PO approves before proceeding
5. **UX/UI design** — run `/ux-ui`
6. **Dashboard code** — run `/dashboard-code` (requires Steps 4 and 5 complete)
7. **QA** — run `/qa` → gate: all criteria pass before release; failures return to Step 6
8. **Release** — run `/release` → gate: PO confirms deployment

## Instructions

**If $ARGUMENTS is an OR-XXX issue ID:**
Fetch the Linear issue. Extract domain name, problem statement, target audience, constraints.
Summarise in plain language. Confirm with PO before proceeding.

**If $ARGUMENTS is a domain name or empty:**
Enter intake mode. Ask the PO one at a time:
1. What domain or topic is this dashboard about?
2. What business problem or question should it answer?
3. Who will use it — and what decisions will they make with it?
4. Are there specific KPIs or metrics you know must be included?
5. Any known constraints (data sources, scope limits)?
Summarise back to PO, confirm. Create Linear issue (label: Feature, status: In Progress).

**Gates:**
Steps 3 and 4 require explicit PO approval before the next step starts.
Step 7 must pass fully — no partial releases.

**Reuse:**
Before running any component skill, check if its output already exists for this domain.
If it exists and is current, skip that step and proceed.

## Standards

None at orchestrator level — standards are loaded by each component skill.
