---
name: qa-checklist
description: "QA checklist artifact. Defines what a quality assessment report is — acceptance criteria results, evaluator findings, and a final PASS/FAIL verdict."
user-invocable: false
---

# QA Checklist

A QA checklist is the structured output of the `/evaluate` step. It records the result
of testing every acceptance criterion and aggregates evaluator agent findings into
a single PASS/FAIL verdict.

Produced by: `/evaluate` (via `/write`)
Consumed by: `/release` (PASS required to proceed)

---

## Location

`products/domain-briefs/{domain}/qa-checklist.md`
Or as a comment on the Linear issue.

---

## Structure

```markdown
# QA Checklist — {Product Name}

**Verdict:** PASS | FAIL
**Date:** {date}
**Tested by:** {agent/person}

## Acceptance Criteria

| # | Criterion | Result | Notes |
|---|-----------|--------|-------|
| 1 | {criterion from requirements doc} | PASS/FAIL/NOT TESTABLE | {observed vs expected if FAIL} |

## Evaluator Findings

### code-reviewer
{P1/P2/P3 findings or "No findings"}

### visualization-reviewer
{findings or "Not applicable"}

### [other agents as relevant]

## Known Limitations

{Items marked NOT TESTABLE with reason, or P2/P3 findings deferred to next iteration}

## Sign-off

- [ ] All acceptance criteria PASS or NOT TESTABLE (with reason)
- [ ] All P1 evaluator findings resolved
- [ ] P2 findings documented in Known Limitations
```

---

## Quality criteria

- Every criterion from requirements doc must appear — none can be silently skipped
- FAIL requires: criterion reference, observed behaviour, expected behaviour
- NOT TESTABLE requires: why it cannot be verified
- Verdict is FAIL if any criterion is FAIL (NOT TESTABLE does not block release)
