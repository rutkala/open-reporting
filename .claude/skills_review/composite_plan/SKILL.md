---
name: composite_plan
description: "Create an implementation plan before writing code. Analyses the request, identifies affected files, designs the approach, and presents it for user approval in plain business language. Use before starting any non-trivial task."
user-invocable: true
argument-hint: "<what to implement>"
---

# Implementation Plan

Design the implementation approach and present it for user approval before writing any code.

## Task
`$ARGUMENTS`

## Step 1 — Understand the Request

1. What does the user want to achieve? (business outcome, not technical task)
2. Check `.claude/session-memory.md` for relevant context
3. Check `docs/` for relevant architecture or data source context
4. Identify scope: single file, single domain, or cross-cutting?

## Step 2 — Research the Codebase

Read the relevant existing code:
1. Find affected files — search for the area that needs to change
2. Understand current patterns — read each affected file
3. Identify dependencies — what depends on what you're changing?
4. Check for existing solutions — is there already a utility or pattern for this?

## Step 3 — Present the Plan

**Lead with the business outcome. Technical details come second.**
The user must be able to make a decision without reading any code.

```
# Plan: {title}

## What this will deliver
{1-2 sentences in plain language — what the user will be able to see or do when this is done}

## What will change
- New: {list any new files, pages, data, features in plain terms}
- Modified: {list what changes and why, in plain terms}
- Removed: {list anything being deleted, if any}

## Complexity
{Small — a few hours | Medium — a full session | Large — multiple sessions}

## Steps
1. {plain description of first step}
2. {plain description of second step}
N. {plain description of final step}

## Data & database changes
{Plain description of any new data being stored, schemas created, or queries changed. "None" if not applicable.}

## Risks
{What could go wrong, in plain language. "None identified" if straightforward.}

## Open questions
{Anything the user needs to decide before I start. "None — I have everything I need." if clear.}
```

## Step 3.5 — Pre-presentation review (before presenting to user)

After writing the plan, spawn **both** review agents **in parallel** using two Agent tool calls in the same message, **before presenting to the user**.

Pass the plan text as the `$PLAN` variable to both agents.

**Agent A — `architecture-critic`**
Reads `docs/data-architecture/reviewing.md` (its rule book) plus `docs/data-engineering/storage.md`, `ingestion.md`, `processing.md`, and `visualisation.md` for context. Evaluates layer contracts, schema naming, and coupling risks.

**Agent B — `analytical-validator`**
Reads `docs/analytical-methods/reviewing.md` (its rule book) plus `docs/analytical-methods/principles.md` for context. Evaluates statistical and methodological soundness.

**Agent C — `domain-specialist`** *(if domain dashboard or domain indicator work)*
Reads `docs/{domain}.md` and evaluates KPI selection, framing, and benchmark correctness.
Pass `$PLAN` as `$INPUT`. Only invoke if the plan involves domain-specific indicator selection or dashboard design.

Skip Agent A if the plan touches no data layer (e.g. a pure UI or config change).
Skip Agent B if the plan contains no analytical design (e.g. a pure infrastructure or tooling change).
Skip Agent C if the plan is not domain-specific (e.g. infrastructure, tooling, or generic feature work).

**Handling findings:**
- Any agent returns **BLOCK** → fix the design flaw, update the plan, re-run before presenting
- Any agent returns **CONDITIONAL** → add the findings to the plan's **Risks** section, then present to user
- All return **APPROVE** → present normally

The user should only see structurally, analytically, and domain-correct plans.

## Step 4 — Wait for Approval

**NEVER start implementing without explicit user approval.**

- Present the plan and ask: *"Does this look right? Shall I proceed?"*
- If the user suggests changes, update the plan and present again
- Only confirm once approved — execution is the caller's responsibility

**Terminal state:** When the user approves, return control to the caller. `/composite_plan` does not implement — it plans. The caller (`/composite_kickoff`, `/composite_develop`, or inline work) decides what happens next.

## Rules
- **Business language first** — the user is the product owner, not a developer
- **No code in the plan** — describe what will be built, not how
- **Don't over-plan simple tasks** — a 1-file, 5-line change needs no formal plan, just do it
- **Do plan complex tasks** — anything multi-file, cross-cutting, or data-touching
- **Read `.claude/languages.json`** → `agent_language` for the language to write the plan in
