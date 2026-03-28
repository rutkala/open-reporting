---
name: capture-idea
description: "Capture an idea from the current conversation into the Linear ideas board. No template required — title and brief description is enough."
user-invocable: true
argument-hint: "<optional: short title or description of the idea>"
---

# Capture Idea

Save an idea to the Linear ideas board without any formal requirements. Ideas are reviewed later via `/review-ideas` before becoming issues.

## Step 1 — Determine the idea

If `$ARGUMENTS` is provided, use it as the basis for the idea title and description.

If `$ARGUMENTS` is empty, look at the current conversation for the most recent idea or feature suggestion being discussed.

## Step 2 — Create the Linear issue

Create a Linear issue with:
- **Title**: short, clear title (max 60 chars)
- **Description**: 2–4 sentences — what the idea is, what problem it solves or value it adds. No acceptance criteria, no technical detail required.
- **Status**: Backlog
- **Label**: Idea
- **Team**: Open-reporting

## Step 3 — Confirm to user

Respond with a single line:
```
💡 Idea captured: "{title}" — [{ID}]({Linear URL})
```

Do NOT ask follow-up questions. Do NOT start implementing. The idea sits in the backlog until `/review-ideas`.
