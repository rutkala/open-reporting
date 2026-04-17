---
name: collect
description: >
  Gather raw information from sources — web, files, data, APIs — and organise into
  structured notes. Invoked by research and improve when information intake is needed
  before synthesis. This skill gathers; it does not conclude. All interpretation happens
  in the calling skill.
  Triggers when: /research or /improve reaches the information-gathering step.
user-invocable: false
---

# Collect

Gather raw information from sources and synthesise it into structured notes
for the calling skill to use. This is the intake phase — no conclusions yet.

**Called by:** research and improve.

## Input

- Topic and question: what information is needed, and why
- Source hints: known relevant sources, documentation, or repositories to check

## Steps

1. Define what specific information is needed (from the calling skill's context)
2. Search: web (official docs, authoritative publications), codebase, existing KB modules
3. For each source: note what was found and where
4. Synthesise into structured notes — deduplicate, flag contradictions
5. Return notes to the calling skill

<HARD-GATE>
Do NOT draw conclusions here. If you notice a pattern emerging, note it in the raw
output as an observation — but synthesis, evaluation, and recommendation happen in the
calling skill. Premature conclusions in the intake phase bias the synthesis that follows.
</HARD-GATE>

## Rules

- Prefer official sources: government publications, library docs, academic papers, Eurostat, GUS
- Check dates — prefer sources from 2023 onwards unless foundational
- Do not draw conclusions here — synthesis happens in the calling skill
- Note source quality: authoritative / secondary / blog / unknown
- If a source contradicts another, flag both — don't silently discard one
