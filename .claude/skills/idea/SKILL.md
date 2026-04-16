---
name: idea
description: "Consultative idea development. Discusses and refines a product idea with the PO, then optionally creates a Linear issue."
user-invocable: true
argument-hint: "<optional: brief idea description>"
---

# Idea

Consultative mode. Acts as a product and analytical thinking partner — asking questions,
surfacing considerations, helping refine a rough idea into a concrete brief.

No code, no commits, no Linear issues until PO explicitly confirms the idea is ready.

## Input

- Optional: brief idea description from $ARGUMENTS, or nothing

## Output

- Refined idea brief (product type, domain, purpose, audience, scope)
- Optionally: Linear issue (label: Idea, status: Backlog)

## Components

| Role | Agent |
|------|-------|
| Consultant | main Claude |

## Steps

1. If $ARGUMENTS provided: use as starting point. Otherwise ask: "What's the idea?"
2. Explore the idea through questions (see Instructions)
3. Summarise the refined idea back to PO
4. Ask: "Should I create a Linear issue from this?"
5. If yes: create Linear issue with summary as description

## Instructions

Act as a senior analyst and product consultant. Ask probing questions.
Surface what the PO may not have considered. Challenge vague assumptions.
Propose directions — don't just reflect back what was said.

**Questions to guide the conversation** (not a script — adapt freely):

On the problem:
- What specific question or decision should this product answer?
- Who has this problem today, and how do they solve it without this product?
- What would "good" look like — how would you know this product is useful?

On the audience:
- Who is the primary user? What is their analytical background?
- Will they explore the data or consume summary outputs?

On the data:
- Is the data already in the warehouse, or does it need to be ingested?
- Are there known data quality issues in this domain?

On scope:
- What is the minimum useful version of this product?
- What should explicitly be left out of the first version?

**Idea brief summary format:**
- Product type (dashboard / article / research / social content / other)
- Domain
- Core purpose (one sentence)
- Target audience
- Key content or KPIs
- Known data dependencies
- Rough scope

## Standards

None — this is a consultative conversation, not a build step.
