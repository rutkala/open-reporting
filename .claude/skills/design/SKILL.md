---
name: design
description: >
  Produce a complete design specification for any product. Use after requirements are
  approved, before any implementation begins. Covers backend (data model, semantic layer,
  API) and optionally frontend (layout, charts, interactions) for visual products.
  The build step implements exactly what is specified here — no design decisions during build.
  Triggers when: "design the solution", "create the design spec", "architecture for X",
  "how should we structure the data", "design the dashboard/portal/article".
user-invocable: true
argument-hint: "<product type> for <domain or topic>"
---

# Design

Produces the complete specification for what will be built. Every structural, data, and
visual decision is made here. Build is a pure executor — it reads this document and
implements without making design decisions.

---

## Input

| What | Required |
|------|----------|
| Requirements document | Yes — defines what must be built |
| Supporting resources | As available — knowledge bases, domain research, reference implementations, existing code |

Read all provided inputs before designing anything. The requirements document is the
authoritative source; supporting resources inform the decisions.

---

## Output

A single design document covering all sections relevant to the product type.
