---
name: improve
description: >
  Extract lessons from completed work and convert them into concrete improvements to
  standards, skills, and processes. Run after a release or explicitly when an area needs
  improvement. Produces a written improvement plan, not a conversation.
  Triggers when: "improve X", "extract lessons", "what can we do better", "update the
  standards", or after a release cycle completes.
user-invocable: true
argument-hint: "<optional: area to focus on>"
---

# Improve

Structured feedback loop. Extracts lessons from completed work and converts them into
concrete, written improvements. The output is an improvement plan — specific changes to
skills, processes, or standards with clear rationale.

---

## Input

| What | Required |
|------|----------|
| Completed work | Yes — a release, a build cycle, or a specific area to review |
| Focus area | Optional — narrows scope; if omitted, review recent work broadly |

---

## Output

An improvement plan listing proposed changes with rationale and specific file edits.

---

## Steps

1. **Gather lessons** — review completed work for what went wrong, what was slow, what was unclear
2. **Identify patterns** — classify each item:
   - Recurring (happened more than once) → strong candidate for a standard or skill update
   - Novel but significant → capture as a lesson
   - Already covered by an existing rule that wasn't followed → skill clarity issue
3. **Generate improvements** — for each actionable item: what specific change would prevent recurrence?
4. **Produce the improvement plan** — list of proposed changes, each with: what to change, which file, and why
5. Present plan to PO and wait for explicit approval

<HARD-GATE>
Do NOT apply any changes to skills or processes without explicit PO approval of the
improvement plan. Collecting lessons and proposing changes is safe — applying them without
approval is not, because it silently changes how every future work is done.
</HARD-GATE>

6. Apply approved changes

---

## Rules

- Improvements must be specific and actionable — "be more careful" is not an improvement; "add a pre-flight check to the build step" is
- Recurring issues that caused rework or visible defects take priority over style preferences
- Every proposed change must name the exact file and section to update
