---
name: basic_research
description: "Research the technical approach for a task before implementing. Searches web, official docs, and codebase. Forms ONE recommendation and proceeds — does not present options for the PO to choose from."
user-invocable: true
argument-hint: "<what to research>"
---

# Technical Research

Investigate the best technical approach. Form a recommendation. Proceed.

## Task
`$ARGUMENTS`

---

## Step 1 — Understand What Needs Deciding

Before searching, define clearly:
- What technical question needs answering?
- What are the constraints? (existing stack, performance requirements, maintainability)
- Are there existing patterns in this codebase already?

Check first:
- `docs/` for relevant standards
- Existing code for patterns already in use
- `.claude/session-memory.md` for recent relevant context

---

## Step 2 — External Research

Invoke `/basic_collect` to gather raw information from official documentation, web sources, and the codebase. `/basic_collect` handles intake without drawing conclusions — synthesis happens in Step 3.

Search for:
- Official documentation for relevant libraries, APIs, frameworks
- Known issues, limitations, and gotchas
- Production-grade examples from authoritative sources

Prefer official docs over blog posts. Check dates — prefer recent sources (2023+).

Note: If the task involves a **business domain** (Public Finance, Labour, Health, etc.), produce a domain brief following the `domain-input` artifact format — see `.claude/skills/basic_domain_input/SKILL.md` for the research steps and output structure.

---

## Step 3 — Form ONE Recommendation

Do not present a list of options for the PO to choose from. Evaluate options internally and arrive at one recommendation.

The recommendation should be grounded in:
- Technical fit with the existing stack (DuckDB, dbt, Dash, Python)
- Alignment with standards in `docs/`
- What authoritative sources recommend for this problem type
- Maintainability and simplicity

---

## Step 4 — Present Findings (internal reference, not user-facing)

Structure findings as a working note for planning:

```
## Research: {topic}

### Problem
{What technical question was being answered}

### What I found
{Key findings — what's possible, what the constraints are, relevant library behavior}

### Recommendation
{One approach, with plain-language reasoning}

### Risks or unknowns
{Anything that needs validating during implementation}

### Sources
{Links to documentation or examples used}
```

This note informs `/composite_plan` — it is not a presentation for PO approval. The PO sees the plan, not the research notes.

---

## Step 5 — Share if relevant

If research reveals a significant scope change, an unexpected constraint, or a trade-off the PO should be aware of — share it in plain language along with the proposed path forward before the caller proceeds.

Otherwise the findings feed directly into `/composite_plan` without requiring PO input.
