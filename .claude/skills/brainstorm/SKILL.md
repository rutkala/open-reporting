---
name: brainstorm
description: "Generate ideas, options, or angles on a topic. Atomic action — invoked by document, design, plan, and improve when divergent thinking is needed before converging on a solution."
user-invocable: true
argument-hint: "<topic or question to brainstorm>"
---

# Brainstorm

Generate a structured set of ideas, options, or angles on a topic. Output is divergent —
the goal is quantity and variety. The calling skill converges on one direction afterward.

## Task
`$ARGUMENTS`

## Steps

1. Clarify the question: what decision or problem is being explored?
2. Generate 5–10 distinct options, angles, or approaches — cover the range, include unconventional ones
3. For each: one sentence on what it is, one sentence on its key trade-off
4. Do NOT recommend one yet — that happens in the calling skill's next step

<HARD-GATE>
Do NOT converge on a recommendation here. If you find yourself preferring one option,
return all options anyway — the calling skill converges. Brainstorming that secretly
recommends one option defeats the purpose: the caller needs the full range to make a
good decision, and premature convergence is exactly the bias this skill exists to prevent.
</HARD-GATE>

## Rules

- Breadth over depth at this stage — avoid elaborating any single idea too far
- Include at least one option that challenges the obvious framing
- Label clearly: "Option A", "Option B", etc. — makes it easy to reference
- If context from a domain brief or requirements doc is available, use it to keep ideas grounded

## Output

A numbered list of options/angles with brief descriptions.
Passed back to the calling skill for convergence.
