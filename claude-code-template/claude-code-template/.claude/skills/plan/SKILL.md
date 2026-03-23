---
name: plan
description: "Create an implementation plan before writing code. Analyses the request, identifies affected files, designs the approach, and presents it for user approval. Use before starting complex features, refactors, or multi-file changes."
disable-model-invocation: true
user-invocable: true
argument-hint: "<what to implement>"
---

# Implementation Plan

Create a detailed plan before writing any code. Get user approval, then execute.

## Task
`$ARGUMENTS`

## Step 1 — Understand the Request

1. Parse what the user wants to achieve
2. Identify the scope: single file, single domain, or cross-cutting?
3. Check `.claude/session-memory.md` for relevant context from recent sessions

## Step 2 — Research the Codebase

Before designing, read the relevant code:

1. **Find affected files** — Grep/Glob for the area of code that needs to change
2. **Understand current state** — Read each affected file to understand existing patterns
3. **Identify dependencies** — What other code depends on what you're changing?
4. **Check for existing solutions** — Is there already a utility, pattern, or convention for this?

## Step 3 — Design the Plan

Present a structured plan:

```markdown
# Plan: {title}

## Summary
{1-2 sentence description of what this plan achieves}

## Scope
- **Files to create:** {list}
- **Files to modify:** {list with brief description of changes}
- **Files to delete:** {list, if any}
- **Estimated complexity:** Small (1-3 files) | Medium (4-8 files) | Large (9+ files)

## Approach

### Step 1: {first thing to do}
- {specific change in specific file}
- {why this approach vs alternatives}

### Step 2: {next thing}
- {details}

### Step N: {final step}
- {details}

## API Contract (if applicable)
- **Endpoint:** `METHOD /api/path`
- **Auth:** {who can access}
- **Request:** {shape}
- **Response:** {shape}

## Database Changes (if applicable)
- {migrations, new tables, altered columns}

## Risks & Trade-offs
- {what could go wrong}
- {alternative approaches considered and why rejected}
- {backwards compatibility concerns}

## Testing Strategy
- {how to verify the changes work}

## Open Questions
- {anything you need the user to decide before proceeding}
```

## Step 4 — Wait for Approval

**NEVER start implementing without user approval.**

Present the plan and ask:
- "Does this plan look right? Shall I proceed?"
- If the user suggests changes, update the plan and present again
- Only start coding after explicit approval

## Step 5 — Execute

Once approved:
1. Follow the plan step by step
2. If you discover something unexpected mid-implementation, pause and inform the user
3. If you need to deviate from the plan, explain why before doing so
4. After completing, summarise what was done vs what was planned

## Rules
- **Plans are for the user, not for you** — write them clearly in the user's language
- **Read `.claude/languages.json`** → `agent_language` for which language to write the plan in
- **Don't over-plan simple tasks** — if it's a 1-file, 5-line change, just do it
- **Do plan complex tasks** — multi-file changes, new features, refactors, anything cross-cutting
- **Include line numbers** — when referencing existing code, include file:line
- **Be specific** — "modify the auth middleware" is bad; "add `isSupervisor` check at `auth.js:42`" is good
- **Consider the delegation** — if the plan spans multiple domains, note which agent will handle each part
