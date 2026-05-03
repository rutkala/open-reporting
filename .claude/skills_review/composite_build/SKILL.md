---
name: composite_build
description: >
  Implement a product from its design document. Pure execution — reads the design spec
  and builds exactly what is specified. No design decisions are made here.
  Applies to any product type: dashboard, portal, mobile app, article, knowledge base,
  research notebook, social content.
  Triggers when: "build it", "implement the design", "start coding", or when /composite_develop
  reaches the build step.
user-invocable: true
argument-hint: "<product type>"
---

# Build

Implements the product. The design document specifies everything — this step builds it.
No design decisions are made here. If anything in the design document is unclear or
missing, stop and raise it before writing any code.

---

## Input

| What | Required |
|------|----------|
| Product Specification | Yes — complete specification of what to build |

<HARD-GATE>
Before writing any code: confirm the design document exists and is complete. If it is
missing, has TBD sections, or is ambiguous in any area you are about to implement —
stop immediately. Flag the specific gap and wait for clarification. Do NOT infer, guess,
or fill gaps from context. The design document is the contract — build only what it specifies.
</HARD-GATE>

---

## Output

Working product at the location specified in the design document, verified locally before
handing to the next step.

---

## Steps

1. Read the Product Specification in full before writing any code
2. Implement what the Product Specification specifies, section by section
3. Verify the product works locally — starts without errors, produces the expected output
4. Fix any issues found during verification
