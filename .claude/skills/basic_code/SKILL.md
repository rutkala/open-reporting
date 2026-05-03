---
name: basic_code
description: >
  Write code given a complete specification. Invoked by build and test when implementation
  is needed. Reads the spec and implements exactly — no design decisions are made here.
  Never use this skill without a complete, unambiguous specification. If the spec has gaps,
  stop and return to /composite_design before continuing.
  Triggers when: /composite_build or /composite_test reaches the implementation step with a full spec ready.
user-invocable: false
---

# Code

Implement code from a specification. Pure execution — the design document or test
specification provides all decisions. This skill writes; it does not design.

**Called by:** build and test.

## Input

- Specification: what to implement (from design doc, test spec, or calling skill)
- Target location: file paths, modules, or components to create or modify
- Product context: loaded by the calling skill (e.g. dashboard/SKILL.md)

## Steps

<HARD-GATE>
If any part of the specification is ambiguous, missing, or leaves an implementation
decision open — stop. Flag the specific ambiguity. Do NOT make implementation decisions;
those belong to /composite_design. Implementing under ambiguity creates code that cannot be
reviewed against any contract and that will likely need to be rewritten.
</HARD-GATE>

1. Read the specification in full before writing any code
2. Check for existing patterns — read related files before creating new ones
3. Implement exactly what the spec says — if anything is ambiguous, stop and flag it
4. Self-check: does the implementation match the spec? Any hardcoded values, missing error handling at boundaries?
5. Return the implemented files to the calling skill

## Rules

- English for all code identifiers (functions, variables, file names, routes)
- Polish for all user-facing strings (labels, titles, tooltips)
- Parameterised queries only — no string interpolation in SQL
- No hardcoded configuration — use env vars or config files
- No imports from `platform/` in `products/` — shared layer is `products/visuals/lib/` only
- Follow existing file structure and naming conventions in the target location

## Standards

- `team/standards/build/storage.md` (database work)
- `team/standards/build/processing.md` (dbt models)
- `team/standards/build/measures.md` (semantic layer)
- Product skill standards (loaded by calling skill)
