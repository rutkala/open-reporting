---
name: composite_knowledge
description: >
  Composite builder skill — produces a structured knowledge document for a target topic.
  Primary use: fills the `knowledge/` bucket of a complex skill (reads `_seed.md`).
  Also usable for any other target that needs a structured knowledge synthesis —
  team knowledge bases, research topics, domain primers. Multi-phase workflow:
  scope → tier sources → collect → analyse coverage → synthesise → save.
  Triggers when: "build the knowledge base for X", "research X", "we need a KB on X".
user-invocable: true
argument-hint: "<target path> [topic scope]"
---

# `composite_knowledge` — build a structured knowledge document

A composite skill that runs a multi-phase workflow (scope → tier
sources → collect → analyse coverage → synthesise → save) to produce
`<target>/summary.md` plus `<target>/raw/` for any target that needs a
structured knowledge synthesis.

**Primary use** is filling the `knowledge/` bucket of a complex skill,
where the target reads `<complex_skill>/_seed.md` for purpose and seed
sources. **Other valid targets** include team knowledge bases, research
topic folders, domain primers, or any directory that needs a codified
knowledge synthesis. The workflow is the same; only the input form
(seed file vs. caller-provided scope) differs.

## What this builds

An **explicit, codified body of facts, principles, theories, and
practices about a defined field** — the ESCO/EQF definition of
knowledge (see `references/definition.md`). DIKW positions this above
data and information: raw sources in `<target>/raw/` are the
data/information layer; the synthesis in `<target>/summary.md` is what
makes the folder actually hold *knowledge*.

When the target is a complex skill, this composite fills the **explicit**
layer of the three-layer model. Tacit content (rules of thumb, war
stories, gut calls) is not knowledge in the ESCO sense and routes to
`<complex_skill>/experience/` via `/composite_experience`. Applied
output (visuals, settings, fixtures) lives in `<complex_skill>/assets/`.
For non-complex-skill targets, only the knowledge layer is produced;
the experience and assets layers do not apply.

## Inputs

| What | Provided by |
|------|------------|
| Target path | Caller — usually `.claude/skills/complex_<name>/knowledge/`, but can be any directory (e.g. `team/knowledge-base/<topic>/`, `products/research/<topic>/`, ad-hoc) |
| Seed input | Either `<complex_skill>/_seed.md` (complex-skill case) OR caller-provided scope: purpose, out-of-scope, pre-existing experience, seed sources |
| Topic scope (fallback) | Caller — one or two sentences. Required if no seed file exists. |
| Depth target (EQF 1–8) | Caller or seed file — L3–4 = broad context; L5–6 = comprehensive/specialised; L7–8 = frontier. Scopes how deep the collect phase goes. Default: L5 if unstated. |

If neither a `_seed.md` nor caller-provided scope is available, ask the
caller for purpose + seed sources interactively before starting. Do not
synthesise without scope.

## Workflow

1. **Frame the scope** — if the target is a complex skill, read
   `<complex_skill>/_seed.md` and extract purpose, out-of-scope,
   pre-existing experience, seed sources. Otherwise use the caller-
   provided scope (purpose + seed sources, plus depth target if stated).
   Hold the extracted frame as the priority for the rest of the workflow.
2. **Scope** — write the specific questions this knowledge document must
   answer. This list becomes the skeleton of §1 (Overview) and §3 (Key
   patterns) of the output.
3. **Tier sources** — identify primary practitioners, standards bodies,
   vendor canon, academic research, case material. Primary > secondary
   > tertiary. Seed sources from step 1 (whether from `_seed.md` or
   caller-provided) go to the top of the queue.
4. **Inventory existing knowledge** — check other `complex_*` skills'
   `knowledge/` buckets for material that already covers parts of this
   scope. Reference, do not duplicate.
5. **Collect** — fetch the queued sources into `<target>/raw/`, one
   file per source. Note the source URL/locator, retrieval date, and
   licence/accessibility at the top of each file. **Hard gate: draw no
   conclusions in this phase.** If a pattern emerges while reading,
   record it as an observation in the source file, not as a synthesis.
   Premature conclusions here bias the synthesis that follows. If a
   source contradicts another already in `raw/`, flag both — do not
   silently discard one.
6. **Analyse coverage** — walk `<target>/raw/` against the scoped
   questions from step 2. For each question: is there enough material
   to write a substantive answer, or only surface coverage? Tier
   sources by authority (institutional / academic / vendor / practitioner)
   and check independence. If coverage is poor on a question, loop back
   to step 5 with a tightened source list. Proceed when every scoped
   question has at least one authoritative source backing it; minor
   gaps are acceptable and go into §7.
7. **Synthesise** — write `<target>/summary.md` in the 7-section
   shape below. Every claim cites a source file in `raw/`. Synthesise —
   do not copy-paste raw material; rewrite into clear prose for a
   reader who has not seen `raw/`. Gaps identified in step 6 go into
   §7, not into guesses inside the body.
8. **Distil (complex-skill targets only)** — pull 3–6 load-bearing rules
   from `summary.md` up into `<complex_skill>/SKILL.md`. The SKILL.md
   stays scannable; depth stays in `summary.md`. Other targets skip this
   step — `summary.md` stands alone.
9. **Save and commit** — write the produced files (`raw/*`, `summary.md`,
   and any updated `SKILL.md`) into the target's bucket and stage for
   commit. Flag gaps explicitly in §7 of the summary.

## Output shape — `summary.md` (7 sections, all mandatory)

An absent section is itself a signal of incomplete synthesis. A short
section is fine; an empty one is not.

1. **Overview** — what this topic is, its scope, key concepts, why it
   matters for this project. 2–4 paragraphs. Written for an intelligent
   reader new to the topic. State the **field** (in plain language, e.g.
   "Polish labour-market statistics", "dbt semantic-layer patterns")
   and the **EQF depth target** the skill needs.
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

- [ ] Scope was framed: for complex-skill targets, `<complex_skill>/_seed.md` was read; for other targets, caller-provided scope was captured. Either way it drove the workflow.
- [ ] §1 (Overview) names the **field** in plain language and the **EQF depth target**.
- [ ] `<target>/raw/` contains the surviving sources, each with a license note.
- [ ] `<target>/summary.md` has all 7 sections; every claim cites a `raw/` file.
- [ ] §7 (Gaps) is honest and non-empty; tacit content that resisted codification is flagged for `/composite_experience` (complex-skill targets) or recorded as an open question (other targets) rather than smoothed over.
- [ ] For complex-skill targets only: 3–6 load-bearing rules have been distilled up into `<complex_skill>/SKILL.md`.
- [ ] Every `raw/` file passes the 7-rule rubric (or carries a recorded waiver).

## Deeper reading

`references/definition.md` is the underlying authority for this skill —
it synthesises the academic grounding (ESCO/EQF, Bloom, Polanyi, Ryle,
DIKW, Nonaka SECI) into the operational definitions used here. The
`raw/` sources beneath it are the primary citations. Read when the
operational rules above feel arbitrary or when extending the skill.
