---
name: save
description: >
  Synthesise collected material into an artifact and write it to disk. Use when collected
  and analysed material is ready and the artifact structure is known.
  Triggers when: "write it up", "save the output", "produce the artifact", "synthesise and save".
user-invocable: true
argument-hint: "<artifact type> to <output path>"
---

# Save

Synthesises collected and analysed material into the target artifact structure and writes
it to the specified output path. Pure execution — no research, no decisions about what to
include beyond what was gathered and assessed in prior steps.

---

## Input

| What | Provided by |
|------|------------|
| Collected material | Raw files, notes — already gathered |
| Analysis | Coverage map, gaps, source quality notes — already assessed |
| Artifact structure | Artifact skill — defines sections, format, quality criteria |
| Output path | Caller — where to write the result |

---

## How to write

- Follow the artifact skill's structure exactly — do not invent sections or skip required ones
- Synthesise — do not copy-paste raw collected content; rewrite into clear, useful prose
- Cite sources — every factual claim should trace back to collected material
- Gaps flagged in `/analyze` go into the artifact's Gaps section — do not fill them with guesses
- Write for the consumer of the artifact, not for the collector: assume they haven't seen the raw material

---

## Output

The artifact file(s) written to the specified output path, structured per the artifact skill.
