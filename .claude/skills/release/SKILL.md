---
name: release
description: "Produce a release document and deploy a completed dashboard. Final step in /dashboard pipeline."
user-invocable: false
---

# Release

Deploys the dashboard and produces a release document. Only runs after QA has passed.

## Inputs

- QA report from Step 7 (pass confirmation, any known caveats)
- Requirements document from Step 3 (accepted criteria, scope)
- Built dashboard at `products/dashboards/{domain}/app.py`

## Agent

Main Claude — deployment steps and documentation.

## Steps

### 1. Commit and open PR
Run `/review` — spawns evaluators, auto-commits, pushes branch, opens PR.
Present PR URL to PO.

### 2. Merge
Wait for PO to approve and merge the PR.

### 3. Deploy
After merge:
- Restart the dashboard service if running as systemd unit
- Verify the dashboard loads at its URL
- Confirm it appears on `portal.open-reporting.dev`

### 4. Release document
Produce a release document containing:
- Dashboard name and domain
- Access URL
- What was built (summary of pages, KPIs)
- Data sources and refresh cadence
- Known limitations or caveats (from QA report)
- Date released

Save release document on the feature branch before merge, or as a comment on the Linear issue.

### 5. Close
- Linear issue → **Done**
- Update `team/session-memory.md` with what was completed
- Delete feature branch

## Output

Live dashboard at its URL. Release document saved. Linear issue closed.
