---
name: release
description: "Release a completed product. Commits, deploys, documents, and closes the Linear issue. Called from product orchestrator skills after QA passes."
user-invocable: false
---

# Release

Final step for any product. Deploys or publishes the product, documents it,
and closes the issue. Only runs after QA has passed.

Applies to any product type: dashboard, article, research, social content, portal, blog.

## Inputs

- QA report (pass confirmation, known caveats)
- Requirements document (what was built, acceptance criteria)
- Built product (code, content, or other output)

## Agent

Main Claude — deployment steps and documentation.

## Steps

### 1. Commit and PR (code products only)
For products with code (dashboards, portal): run `/review` — spawns evaluators,
auto-commits, pushes branch, opens PR. Present PR URL to PO.

For content products (articles, social): skip this step.

### 2. Publish or deploy

*Dashboards / portal:*
- Merge PR (wait for PO approval)
- Restart service if running as systemd unit
- Verify the product loads at its URL
- Confirm it appears on `portal.open-reporting.dev`

*Articles:*
- Publish to Ghost CMS
- Confirm it appears at `www.open-reporting.dev`

*Social content:*
- Schedule or post via configured social publishing tool

*Research:*
- Commit notebooks and outputs to `products/research/`
- Merge PR

### 3. Release document
Produce a brief release document:
- Product name, type, and domain
- Access point (URL, channel, or location)
- What was built (one-paragraph summary)
- Data sources and refresh cadence (if applicable)
- Known limitations or caveats (from QA report)
- Date released

Save as a comment on the Linear issue, or as a file if the product has a
dedicated folder in `products/`.

### 4. Close
- Linear issue → **Done**
- Update `team/session-memory.md`
- Delete feature branch (code products)

## Output

Product live at its access point. Release document saved. Linear issue closed.
