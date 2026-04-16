---
name: release
description: "Release a completed product. Deploys or publishes, documents, and closes the Linear issue. Runs after QA passes."
user-invocable: false
---

# Release

Deploys or publishes the product, produces a release document, and closes the issue.
Only runs after QA has fully passed.

Applies to: dashboard, article, research, social content, portal, blog.

## Input

- QA report (pass confirmation, known caveats)
- Requirements document (what was built)
- Built product (code, content, or other output)

## Output

- Product live at its access point
- Release document saved
- Linear issue closed

## Components

| Role | Agent |
|------|-------|
| Author | main Claude |

## Steps

1. Confirm QA report shows full pass
2. Commit and open PR (code products only) — see Instructions
3. Publish or deploy the product — see Instructions
4. Produce release document
5. Close Linear issue and clean up

## Instructions

**Step 2 — Commit and PR (code products: dashboards, portal)**
Run `/review` — spawns evaluators, auto-commits, pushes branch, opens PR.
Present PR URL to PO. Wait for merge approval.

Content products (articles, social, research) skip this step.

**Step 3 — Publish or deploy by product type**

*Dashboard / portal:*
- Merge PR after PO approval
- Restart service if running as systemd unit
- Verify the product loads at its URL
- Confirm it appears on `portal.open-reporting.dev`

*Article:*
- Publish to Ghost CMS
- Confirm it appears at `www.open-reporting.dev`

*Social content:*
- Schedule or post via social publishing tool

*Research:*
- Commit notebooks and outputs to `products/research/`
- Merge PR

**Step 4 — Release document**
Contents:
- Product name, type, domain
- Access point (URL, channel, or file path)
- What was built (one paragraph)
- Data sources and refresh cadence (if applicable)
- Known limitations or caveats (from QA report)
- Date released

Save as a comment on the Linear issue, or as a file in the product's folder.

**Step 5 — Close**
- Linear issue → **Done**
- Update `team/session-memory.md`
- Delete feature branch (code products)

## Standards

- `team/standards/build/requirements.md` (release criteria section)
