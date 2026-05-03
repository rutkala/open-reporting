---
name: basic_analyze
description: >
  Analyze collected material before writing. Assesses coverage, source authority, and gaps.
  Use when you have raw collected material and need to know what you have, what is missing,
  and whether it is sufficient to write from.
  Triggers when: "analyze what we have", "check coverage", "assess the sources",
  "what are the gaps in the collected material".
user-invocable: true
argument-hint: "<collected material path or description>"
---

# Analyze

Assesses collected material before synthesis begins. The goal is to know what you have,
what is missing, and whether it is good enough to write from — before committing to writing.

---

## Input

| What | Provided by |
|------|------------|
| Collected material | Raw files, notes, scraped content — already gathered |
| Artifact type | Caller — what artifact is being produced (defines what "sufficient coverage" means) |

---

## Output

A short assessment covering:

1. **Coverage** — which angles and sections of the target artifact are well-supported by the collected material, and which are thin
2. **Source quality** — are sources authoritative and current? Flag anything that is a secondary summary, undated, or unreliable
3. **Gaps** — specific topics or questions from the brainstorm that the collected material does not answer
4. **Recommendation** — proceed to `/basic_save`, or return to `/basic_collect` for a targeted pass on specific gaps

---

## How to assess

- Map collected material against the artifact structure (from the artifact skill) — section by section
- For each section: is there enough to write from, or just surface-level coverage?
- Check source dates — prefer recent primary sources; flag anything older than 3 years unless foundational
- Flag contradictions between sources — note them explicitly rather than silently picking one
- Minor gaps: flag for the Gaps section in the artifact, proceed to `/basic_save`
- Major gaps (a full section unsupported): return to `/basic_collect` with a targeted scope
