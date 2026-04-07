---
name: review-ideas
description: "Review the ideas board, decide which to pursue, and convert accepted ideas into proper Linear issues with full templates."
user-invocable: true
argument-hint: ""
---

# Review Ideas

Go through all ideas in Linear, decide which to accept or reject, and convert accepted ones into proper issues ready for `/kickoff`.

## Step 1 — Fetch ideas

List all Linear issues with label "Idea" (status: Backlog).

If there are no ideas, say so and stop.

## Step 2 — Present ideas for review

Show all ideas as a numbered list:
```
## Ideas Board

1. **{Title}** ({ID})
   {Description — 1–2 sentences}

2. ...
```

Then give your recommendation for each:
- **Recommend accept** — if there is clear value, the data/capability exists or is feasible, and it fits the current phase
- **Recommend defer** — if the idea is good but not Phase 1 priority
- **Recommend reject** — if out of scope, duplicate, or not aligned with product direction

Present all recommendations at once, then ask: *"Which would you like to accept, defer, or reject?"*

## Step 3 — Process decisions

For each **accepted** idea:
1. Identify the issue type (dashboard / ingestion / article / infrastructure) using `team/standards/build/requirements.md`
2. Fill in the full issue template for that type
3. If the idea is large, split into a parent issue (epic) + sub-issues
4. Create the issue(s) in Linear:
   - Label: Feature / Bug / Data / Content / Infra (whichever applies — not Idea)
   - Set status to **Todo**
   - Assign to a milestone if it clearly belongs to Phase 1 / 2 / 3
   - Link sub-issues to parent
   - Set `relatedTo` the original idea issue ID (creates traceable chain)
5. Close the original idea: set to **Canceled**, add comment: *"Converted to {new issue ID(s)}"*

For each **deferred** idea:
- Leave in Backlog with Idea label, add comment: *"Deferred — revisit in Phase {N}"*

For each **rejected** idea:
- Set status to Canceled, add comment with brief reason

## Step 4 — Summary

After processing all decisions, show:
```
## Ideas Review Complete

✅ Accepted → {list of new issue IDs and titles}
⏸ Deferred → {list}
❌ Rejected → {list}
```

Issues marked ✅ are ready for `/kickoff`.
