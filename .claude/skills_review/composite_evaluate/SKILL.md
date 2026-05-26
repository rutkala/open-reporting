---
name: composite_evaluate
description: >
  Evaluate a completed product for quality, correctness, and compliance with requirements.
  Use after build completes, before any release attempt. Applies to any product type:
  dashboard, portal, mobile app, article, knowledge base, research, social content.
  Triggers when: "evaluate the product", "QA this", "is it ready", "run the checks",
  "test before release", or when /composite_develop reaches the evaluate step.
user-invocable: true
argument-hint: "<product type>"
---

# Evaluate

Structured quality assessment of a completed product before release. Checks every
acceptance criterion, verifies the product works as specified, and produces a QA report.

---

## Input

| What | Required |
|------|----------|
| Built product | Yes — running app, written content, or other output |
| Requirements | Yes — source of acceptance criteria |

---

## Output

A QA report covering every acceptance criterion: PASS / FAIL / NOT TESTABLE per item.

- **PASS** — all criteria met, product is ready for release
- **FAIL** — one or more criteria not met; return to build with exact failure list
- **NOT TESTABLE** — criterion cannot be verified with available tools; flag for PO awareness, do not mark as PASS

---

## Steps

1. Read the requirements — extract every acceptance criterion as a numbered list
2. For each criterion: test it against the built product, mark PASS / FAIL / NOT TESTABLE
3. For code products: verify the product starts and runs without errors
4. For visual products: verify charts render, filters respond, data matches design document
5. For written content: verify coverage, accuracy, language quality, and format compliance
6. Compile the QA report — one entry per criterion with observed result and verdict
7. If any FAIL: list exact failures (criterion ref + observed vs expected) and return to build
8. If all PASS or NOT TESTABLE: product is ready for release

---

## Assessment rules

**FAIL requires:**
- Which criterion failed (reference number)
- What was observed
- What was expected

**NOT TESTABLE requires:**
- Which criterion cannot be verified
- Why it cannot be verified with available tools

**Do not guess or assume.** If you cannot observe the result of a criterion, mark it NOT TESTABLE — never PASS.
