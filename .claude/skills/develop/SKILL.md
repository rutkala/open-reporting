---
name: develop
description: >
  Full product development pipeline. Orchestrates the mandatory sequence: document →
  design → build → evaluate → release → improve. Use when starting work on any product
  from scratch or from a Linear issue. Applies to any product type: dashboard, portal,
  mobile app, article, knowledge base, research, social content.
  Triggers when: "develop X", "build the product", "start work on OR-XXX", or when a
  Linear issue is ready to implement.
user-invocable: true
argument-hint: "<OR-XXX or product type>"
---

# Develop

Full product development pipeline. Mandatory steps in sequence — none can be skipped.
Each step produces an artifact that the next step depends on.

---

## Input

| What | Required |
|------|----------|
| Linear issue or product description | Yes — defines what to build |
| Product type | Yes — determines which steps apply |

---

## Output

Working product at its target location, with artifacts from each step: requirements,
design, built product, QA report, release document.

---

## Steps

1. **Document** — produce the requirements artifact; gate: PO approves before proceeding
2. **Design** — produce the design artifact; gate: PO approves before proceeding; skip if the product has no data or visual layer
3. **Build** — implement from the design; skip if the product has no code deliverable
4. **Evaluate** — assess against requirements; gate: all criteria pass before release; failures return to build
5. **Release** — deploy or publish; gate: PO confirms deployment
6. **Improve** — extract lessons and produce improvement plan after release

---

## Rules

- Steps 1 and 2 require explicit PO approval before the next step starts
- Step 4 must pass fully — no partial releases
- Before starting any step, check if its artifact already exists and is current — if so, skip and proceed
- If the Linear issue is provided: read it in full, extract product type, domain, and problem statement, summarise to PO before starting
- If no issue exists: ask the PO for product type, domain, business problem, audience, and constraints — then create a Linear issue before proceeding
