---
name: experience
description: >
  Composite builder skill — adds a framed entry to the `experience/` bucket of a
  target complex skill. Triggered by a real surprising, unique, or value-conflicted
  event during the target skill's use. Frames the event into Expected / Observed /
  Surprise / Rule, classifies single- vs double-loop, applies the 8-rule quality
  gate, and saves the entry.
  Triggers when: "capture the lesson from X", "we should remember this", "write an
  experience entry for X".
user-invocable: true
argument-hint: "<target skill path> <triggering event>"
---

# `experience` — add a framed entry to a complex skill's experience bucket

A composite skill that turns a real episode into a structured, retrievable
entry under `<target>/experience/<YYYY-MM-DD>-<slug>.md`. It does no
fabrication — every entry must be triggered by an actual event during the
target skill's use, not by an imagined scenario.

## Inputs

| What | Provided by |
|------|------------|
| Target skill path | Caller — e.g. `.claude/skills/complex_<name>/` |
| Triggering event | Caller — concrete description of the surprise, failure, value conflict, or unique case being framed |
| Situation type | Caller or inferred — the class of situation this entry indexes under (used as retrieval key) |

If the triggering event is vague ("things went wrong"), pause and ask
for specifics before writing. Vague entries become diary, not
experience.

## Workflow

1. **Verify a real event** — confirm the entry is triggered by something
   that actually happened (a divergence between expectation and outcome,
   a unique case, or a value conflict). Reject imagined scenarios.
2. **Identify situation type** — name the class of situation this entry
   belongs to (e.g. for a dashboarding skill: *ambiguous KPI spec*,
   *over-long series*, *failed colour contrast*). Reuse the target's
   existing situation-type vocabulary if one exists; extend it if not.
3. **Frame** — fill in the 7-field skeleton below (Expected / Observed /
   Surprise / Rule / How to test / Promotion target / Sources). The
   *frame* — the assumption operative at the time — must be visible in
   the Expected field.
4. **Classify loop level** — single-loop (correcting an action under an
   unchanged governing variable) or double-loop (changing the governing
   variable itself). Mislabelling double-loop as single-loop leaves the
   real cause unaddressed.
5. **Run the 8-rule quality gate** — see Quality criteria below. Reject
   entries that fail any of rules 1–7. Rule 8 (promotion path) is
   revisited periodically rather than per-write.
6. **Save the entry** — write `<target>/experience/<YYYY-MM-DD>-<slug>.md`
   following the entry skeleton below. If a situation-type index file
   exists at `<target>/experience/index.md`, append the new entry to
   it; otherwise create one.
7. **Periodic combination** *(deferred, not per-call)* — when 2–3 entries
   converge on the same rule, the rule is promoted to a standard, a
   skill section, or a check. Source entries are marked *promoted* with
   a link.

## Output shape — entry skeleton (mandatory unless marked optional)

```
# <short title — the rule, not the event>

**Date:** YYYY-MM-DD
**Situation type:** <class of situation; used as retrieval key>
**Loop level:** single-loop | double-loop

## Expected
What was supposed to happen — the prior frame, the espoused plan. Capture
the assumption that was operative, not only the outcome.

## Observed
What actually happened. Facts, not interpretation. Disconfirming evidence
preserved.

## Surprise
Where expectation diverged from outcome, or why the case was unique /
unstable / value-conflicted. Without surprise, no entry worth keeping.

## Rule
The revised, transferable rule. One sentence where possible. Applicable
to a *different* future instance of the same situation type, without
re-deriving.

## How to test
The next situation where this rule will be validated. An entry with no
test plan silently accumulates untested theory.

## Promotion target *(if any)*
Standard, skill section, or check this rule should be combined into when
it recurs. *Local for now* is an acceptable answer; blank is not.

## Sources / links
Related commits, PRs, session notes, prior entries, standards referenced.
```

## Quality criteria — 8-rule gate

Every entry passes all eight, or is rejected / revised / deferred.

1. **Surprise present** — triggered by divergence between expectation
   and outcome, a unique case, or a value conflict. No-surprise entries
   are diary.
   *Failure mode:* routine work inflated into an "entry".
2. **Full cycle populated** — Expected / Observed / Surprise / Rule /
   How to test all populated. No stage skipped.
   *Failure mode:* narration without a transferable rule; rule without
   a plan to test.
3. **Loop level declared** — single-loop or double-loop explicit.
   *Failure mode:* double-loop correction mislabelled as single-loop,
   leaving the governing variable broken.
4. **Frame stated** — the assumption operative at the time is visible
   in Expected.
   *Failure mode:* the entry presents its conclusion as the obvious
   one, hiding the frame that made it non-obvious.
5. **No-blame / no-rationalisation** — disconfirming evidence
   preserved; failures not softened; chosen path not retrofitted into
   "the right call all along".
   *Failure mode:* confirmation-biased entry that propagates the same
   mistake.
6. **Transferability** — the Rule is applicable in a *different*
   instance of the same situation type, by a reader who lacks full
   narrative context.
   *Failure mode:* the entry reads as a story about one project,
   usable nowhere else.
7. **Retrievability** — situation type uses the target skill's
   controlled vocabulary, so the entry is recallable mid-task in
   future work.
   *Failure mode:* entry forgotten because nothing triggers its recall.
8. **Promotion path declared** — the entry names a combination target
   (standard, skill section, check), or explicitly marks itself *local
   for now*. Blank is not acceptable.
   *Failure mode:* rules accumulate in `experience/` and never
   influence standards; the knowledge base never compounds.

## Operational rules

- **No fabrication** — entries describe real events. Imagined-scenario
  entries are rejected outright.
- **Supersession, not deletion** — a contradicted entry is marked
  *superseded* with a link to the newer one. The original stays as a
  record of how the rule evolved.
- **Promotion retires entries** — once a rule is combined into a
  standard, the source entries are marked *promoted* and compacted to
  a one-line reference.
- **Skill-local scope** — entries belong to one target skill's
  `experience/`. Cross-skill patterns are promoted up to
  `docs/`, at which point they become *knowledge* (input to
  future `/knowledge` runs).

## Output checklist

Before reporting completion:

- [ ] The entry was triggered by a real event, not an imagined scenario.
- [ ] All 7 fields of the skeleton are populated; none skipped.
- [ ] Loop level is declared and matches the actual change made.
- [ ] The 8-rule gate has been walked; rules 1–7 pass; rule 8 is at
      least *local for now*.
- [ ] The entry is saved at `<target>/experience/<date>-<slug>.md`.
- [ ] The situation type matches the target's controlled vocabulary
      (or extends it deliberately).

## Deeper reading

`references/definition.md` carries the academic grounding for *what
experience is* (Kolb's experiential learning cycle, Argyris & Schön's
single/double-loop, Schön's reflective practice, the US Army AAR ritual,
Nonaka's SECI externalisation, Polanyi's tacit/explicit split, Davenport
& Prusak's framed experience). Optional — not load-bearing for daily
use of this skill.
