---
name: release
description: >
  Release a completed product. Use only after evaluate returns a full PASS — never before.
  Deploys or publishes, produces a release document, and closes the Linear issue.
  Applies to any product type: dashboard, portal, article, research, social content.
  Triggers when: "release this", "deploy it", "publish the article", "ship it",
  "push to production", or when /develop reaches the release step and QA has passed.
user-invocable: true
argument-hint: "<product type>"
---

# Release

Deploys or publishes the product, produces a release document, and closes the issue.
Only runs after evaluation has fully passed.

---

## Input

| What | Required |
|------|----------|
| Quality Confirmation | Yes — must show full PASS before proceeding |
| Built product | Yes — code, content, or other output ready to deploy |

<HARD-GATE>
Do not proceed unless the QA report shows a full PASS on all acceptance criteria. Any
criterion marked FAIL means the product is not ready — return to build with the failure
list. A product that has not fully passed evaluation must never reach release.
</HARD-GATE>

---

## Output

- Product live at its access point
- Release document saved

---

## Steps

1. Confirm QA report shows full PASS
2. Deploy or publish the product at its designated access point
3. Verify the product is accessible and working after deployment
4. Produce the release document (see structure below)

---

## Release document

Save as a comment on the Linear issue or as a file in the product's folder.

Required contents:
- Product name, type, domain
- Access point (URL, channel, or file path)
- What was built (one paragraph)
- Data sources and refresh cadence (if applicable)
- Known limitations or caveats (from QA report)
- Date released