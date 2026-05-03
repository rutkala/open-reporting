---
name: basic_release_summary
description: "Release summary artifact. Defines what a release document is — what was built, where it lives, data sources, known limitations, and date. Produced by /composite_release."
user-invocable: false
---

# Release Summary

A release summary documents what was built and deployed. It is the permanent record
of the product at a point in time — useful for audits, handoffs, and the PO's reference.

Produced by: `/composite_release` (via `/write`)
Saved as: comment on the Linear issue, or file in the product folder.

---

## Location

Linear issue comment, or: `products/{product-type}/{domain}/release-{date}.md`

---

## Structure

```markdown
# Release: {Product Name}

**Date:** {release date}
**Issue:** OR-XXX
**Type:** Dashboard | Article | Research | Social content | Portal

## What was built

{One paragraph in plain language. What the product does, for whom, and what question it answers.}

## Access point

{URL, channel, or file path where the product is available.}

## Data sources

| Source | Table / Location | Refresh cadence |
|--------|-----------------|-----------------|
| {source name} | {warehouse table or URL} | {daily/monthly/static} |

## Known limitations

{Items from the QA checklist marked NOT TESTABLE, or P2 findings deferred.
Write "None" if clean.}

## Dependencies

{Any ingestion jobs, dbt models, or services the product depends on.}
```

---

## Quality criteria

- Access point must be a real, working URL or path — not a placeholder
- Data sources must list the actual warehouse tables used
- Known limitations must come from the QA checklist — not invented here
- "None" is acceptable for limitations — but must be explicit
