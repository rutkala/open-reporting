---
name: _template
description: >
  Starting shape for a new COMPLEX skill. Not user-invocable — copy this
  folder to `.claude/skills/complex_<new-skill>/`, fill in `_seed.md`,
  draft `SKILL.md`, then invoke `/composite_knowledge <new-skill>` to
  populate the `knowledge/` bucket. Simple skills do NOT use this template.
user-invocable: false
---

# `_template` — Scaffold for a Complex Skill

A complex skill carries three buckets alongside its `SKILL.md`:

- **`knowledge/`** — domain resources synthesised into a knowledge
  document. Populated by invoking `/composite_knowledge <new-skill>`.
- **`experience/`** — lessons captured over time as the skill is used.
  Populated by invoking `/composite_experience <new-skill>` after a real
  surprising or value-conflicted event.
- **`artifact/`** — passive placeholder for assets the skill needs:
  images, settings, fixtures, generated outputs. No builder skill —
  just a folder where assets live.

## How to start a new complex skill

1. `cp -r .claude/skills/_template/ .claude/skills/complex_<new-skill>/`
2. **Update the frontmatter** in `complex_<new-skill>/SKILL.md`:
   replace `name: _template` with `name: complex_<new-skill>` and
   rewrite the `description:` to describe the new skill. The folder
   name and the `name:` field must match — otherwise the skill loads
   under the wrong name.
3. Fill in `complex_<new-skill>/_seed.md` (purpose, out-of-scope,
   pre-existing experience, seed sources). This is the input the
   `composite_knowledge` builder reads first.
4. Replace the body of `complex_<new-skill>/SKILL.md` with a minimal
   draft describing what the skill does and the problem it solves.
5. Invoke `/composite_knowledge complex_<new-skill>` — it reads
   `_seed.md`, runs `/basic_collect` and `/basic_analyze`, and writes
   a synthesised knowledge document into
   `complex_<new-skill>/knowledge/`.
6. Over time, as real lessons emerge from using the skill, invoke
   `/composite_experience complex_<new-skill> <event>` to add framed
   entries to `complex_<new-skill>/experience/`.
7. Add assets to `complex_<new-skill>/artifact/` directly as needed.

## When NOT to use this template

A `basic_` skill (one atomic action — `/basic_commit`, `/basic_save`, `/basic_collect`)
or a `composite_` skill (an orchestrator referencing other skills —
`/composite_develop`, `/composite_kickoff`, `/composite_knowledge`) is a single `SKILL.md`,
no buckets. Do not copy this template for those — just create the
single file directly.

## Files in this scaffold

- `SKILL.md` — this file. Replace with the new skill's own SKILL.md.
- `_seed.md` — input form for the new skill (filled in step 2 above).
- `knowledge/` — empty; populated by `composite_knowledge`.
- `experience/` — empty; appended to over time by `composite_experience`.
- `artifact/` — empty; populated directly with assets as needed.
