---
name: composite_knowledge
description: >
  Composite builder skill — fills the `knowledge/` bucket of a target complex skill.
  Reads the target's `_seed.md` (purpose, pre-existing experience, seed sources),
  collects authoritative resources, analyses coverage, synthesises a structured
  knowledge document. Orchestrates the basic skills `/basic_collect`, `/basic_analyze`, `/basic_save`.
  Triggers when: "build the knowledge base for X", "research X for the <skill> skill",
  "we need a KB on X before we start".
user-invocable: true
argument-hint: "<target skill path>"
---

# `composite_knowledge` — build the knowledge bucket for a complex skill

A composite skill that orchestrates `/basic_collect` → `/basic_analyze` → `/basic_save` to
produce `<target>/knowledge/summary.md` plus `<target>/knowledge/raw/` for
a target complex skill. It does no atomic work itself — every collection
or analysis step delegates to a basic skill.

## Inputs

| What | Provided by |
|------|------------|
| Target skill path | Caller — e.g. `.claude/skills/complex_dashboard/` or a `team/knowledge-base/<topic>/` directory |
| `<target>/_seed.md` | The target itself — purpose, out-of-scope, pre-existing experience, seed sources. Read first. |
| Topic scope (fallback) | Caller — one or two sentences. Required if `_seed.md` is missing. |

If `_seed.md` is absent or empty, ask the caller for purpose + seed
sources interactively before starting. Do not synthesise without scope.

## Workflow

1. **Read `_seed.md`** — extract purpose, out-of-scope, pre-existing
   experience, seed sources. Hold these as the priority frame for the
   rest of the workflow.
2. **Scope** — write the specific questions this knowledge document must
   answer. This list becomes the skeleton of §1 (Overview) and §3 (Key
   patterns) of the output.
3. **Tier sources** — identify primary practitioners, standards bodies,
   vendor canon, academic research, case material. Primary > secondary
   > tertiary. The `_seed.md` *Seed sources* go to the top of the queue.
4. **Inventory existing project knowledge** — check `team/knowledge-base/`,
   `team/standards/`, and other `complex_*` skills for material that
   already covers parts of this scope. Reference, do not duplicate.
5. **`/basic_collect`** — invoke the basic `collect` skill against the source
   queue from steps 3+4. Output goes to `<target>/knowledge/raw/`.
   `/basic_collect` draws no conclusions.
6. **`/basic_analyze`** — invoke the basic `analyze` skill on `<target>/knowledge/raw/`
   to assess coverage, source authority, and gaps. If coverage is poor,
   loop back to step 5 with a tightened source list. Proceed when
   coverage is good enough.
7. **Synthesise** — write `<target>/knowledge/summary.md` in the 7-section
   shape below. Every claim cites a source file in `raw/`.
8. **Distil** — pull 3–6 load-bearing rules from `summary.md` up into
   `<target>/SKILL.md`. The SKILL.md stays scannable; depth stays in
   `summary.md`.
9. **`/basic_save`** — invoke the basic `save` skill to commit the produced
   files into the target's bucket. Flag gaps explicitly in §7 of the
   summary.

## Output shape — `summary.md` (7 sections, all mandatory)

An absent section is itself a signal of incomplete synthesis. A short
section is fine; an empty one is not.

1. **Overview** — what this topic is, its scope, key concepts, why it
   matters for this project. 2–4 paragraphs. Written for an intelligent
   reader new to the topic.
2. **Authoritative sources** — the sources that survived the rubric
   below. For each: name, URL, what it covers, why it is authoritative.
   Prefer primary over summaries.
3. **Key patterns and conventions** — how practitioners approach this
   topic. Established patterns, naming conventions, structural decisions
   that are standard in the field. Not opinions — what the field agrees
   on.
4. **Component / API reference** — concrete inventory of what exists:
   functions, classes, configuration options, endpoints, data structures,
   chart types, etc. Include signatures, parameters, usage notes. Verify
   against the current version — do not rely on memory.
5. **Examples** — representative real-world examples or code snippets
   demonstrating key patterns. Each example concrete and runnable.
6. **Decisions and trade-offs** — known choices in this topic area,
   their implications, what the project decided with rationale.
   Format: Decision → Options considered → Choice made → Why.
7. **Gaps and open questions** — what is uncertain, not yet researched,
   or needs validation. Honest. Flag gaps so they can be addressed.

## Quality criteria — source-authority rubric (7 rules + optional 8th)

Every candidate source must pass all seven before entering `raw/`. Waivers
are recorded with an explicit reason at the top of the source file.

1. **Authority** — recognised in its field: standards body, peer-reviewed
   venue, primary practitioner, or vendor canon.
   *Failure mode:* anonymous blog treated as canonical.
2. **Primacy** — primary preferred over secondary. Wikipedia, SEP, blog
   summaries accepted only when primary unavailable, and flagged as
   secondary.
   *Failure mode:* hearsay citation chains with no grounding.
3. **Load-bearing** — answers at least one of the scoped questions
   (step 2). No filler, no "related reading".
   *Failure mode:* bloated `raw/` that hides the actual argument.
4. **Independence / triangulation** — sources collectively span tiers
   (institutional, academic, vendor, practitioner). No single school or
   author dominates.
   *Failure mode:* one worldview masquerading as the field's consensus.
5. **Codifiability** — the valuable content is *explicit*. Tacit content
   is routed to `experience/` externalisation, not `knowledge/raw/`.
   *Failure mode:* fake explicitness — a checklist that is really a feel
   in disguise.
6. **Verifiability** — stable locator: DOI, ISBN, official URL, or
   archived snapshot when the URL is volatile.
   *Failure mode:* "a talk someone gave" citations that cannot be
   re-checked.
7. **Recency** — prefer 2023+ or latest revision, unless foundational
   and evergreen. Foundational picks must state *why* they remain
   current.
   *Failure mode:* stale technical canon; or blind recency that
   discards classics.

**Optional 8th — recommended, not strict:**

- **Licence / accessibility** — can be lawfully quoted and stored in
  `raw/`. Public-domain, Creative Commons, or fair-use scope verified.
  *Failure mode:* paywalled content copied verbatim.

## Output checklist

Before reporting completion:

- [ ] `<target>/_seed.md` was read; its scope and seed sources drove the workflow.
- [ ] `<target>/knowledge/raw/` contains the surviving sources, each with a license note.
- [ ] `<target>/knowledge/summary.md` has all 7 sections; every claim cites a `raw/` file.
- [ ] §7 (Gaps) is honest and non-empty.
- [ ] 3–6 load-bearing rules have been distilled up into `<target>/SKILL.md`.
- [ ] Every `raw/` file passes the 7-rule rubric (or carries a recorded waiver).

## Deeper reading

`references/definition.md` carries the academic grounding for *what
knowledge is* (ESCO/EQF, Bloom, Polanyi, Ryle, DIKW, Nonaka). Optional —
not load-bearing for daily use of this skill.
