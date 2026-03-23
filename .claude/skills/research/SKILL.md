---
name: research
description: "Research how to implement a task before planning. Searches the web, reads documentation, explores the codebase for existing patterns, and presents findings with a clear recommendation for user approval."
user-invocable: true
argument-hint: "<what to research>"
---

# Research & Analysis

Investigate the best approach before writing any code. Present findings in plain language for user approval.

## Task
`$ARGUMENTS`

## Step 1 — Understand the Question

Before researching, define clearly:
- What specific question needs answering?
- What would a good answer look like?
- Are there existing patterns in this codebase to check first?

## Step 2 — Check the Codebase First

Before going to the web:
- Search for existing patterns, utilities, or conventions already in the project
- Check `.claude/session-memory.md` for relevant context from recent sessions
- Check `docs/` for relevant architecture or data source documentation

## Step 3 — External Research

Search for:
- Official API documentation for relevant data sources
- Library documentation (Plotly, psycopg2, pandas, Ghost API, etc.)
- Real examples of similar implementations
- Known issues, limitations, or gotchas

Use web search and web fetch tools. Prefer official docs over blog posts. Check publication dates — prefer recent sources.

## Step 4 — Present Findings

Present in plain business language. Lead with the recommendation, follow with evidence.

```
## Research: {topic}

### What we're trying to solve
{1 paragraph — the problem in plain language}

### What I found
{Summary of key findings — what's possible, what's not, what the options are}

### Options

**Option A: {name}**
- What it is: {plain description}
- Pros: {list}
- Cons: {list}

**Option B: {name}**
- What it is: {plain description}
- Pros: {list}
- Cons: {list}

### My recommendation
**Option {X}** — {plain-language reason why, focused on your goals not technical elegance}

### Risks or unknowns
{Anything that could go wrong or needs validating during implementation}

### Sources
{Links to key documentation or examples used}
```

## Step 5 — Wait for Approval

Do NOT proceed to planning until the user:
- Approves the recommendation, OR
- Chooses a different option, OR
- Asks for more research on a specific point

Once approved, proceed with `/plan` using the chosen approach.
