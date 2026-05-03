# Knowledge — Definition and Methodology

Meta-knowledge about what knowledge *is*, how it is structured, and what this
means for the `knowledge/` folder inside every skill in this project. This file
lives inside the template skill so that every new skill inherits the same
grounded understanding.

---

## 1. Primary definition

The European Qualifications Framework (EQF) defines knowledge, and ESCO adopts
that definition verbatim:

> "Knowledge means the outcome of the assimilation of information through
> learning. Knowledge is the body of facts, principles, theories and practices
> that is related to a field of work or study."
>
> — ESCO Escopedia, *Knowledge* entry (sourced from EQF)

Three load-bearing claims are packed into that sentence:

1. Knowledge is an **outcome** — not raw input; it is what remains after
   information has been assimilated through learning.
2. Knowledge has **content type** — specifically, facts, principles, theories,
   and practices.
3. Knowledge is **bound to a field** — of work or study. Context-free knowledge
   is not what this definition targets.

Sources: `raw/esco-knowledge.md`, `raw/eqf-8-levels.md`.

---

## 2. What knowledge *is*

### 2.1 Content types (ESCO / EQF)

The ESCO/EQF definition names four content types, which are the basic substance
of any knowledge body:

| Type | What it covers |
|---|---|
| **Facts** | Discrete, verifiable truths about the field |
| **Principles** | General rules or laws governing the field |
| **Theories** | Explanatory frameworks for why facts and principles hold |
| **Practices** | Established, codified ways of doing things in the field |

### 2.2 Depth axis (EQF 8 levels)

EQF levels 1–8 describe knowledge **depth** along an independent axis:

- L1–L2 — basic, factual
- L3–L4 — facts + principles + theories (broad contexts)
- L5–L6 — comprehensive / specialised, critical understanding
- L7–L8 — frontier, original thinking, cross-field synthesis

A skill's `knowledge/` may target any depth level; the depth should be stated
explicitly (e.g., "this skill needs L5 knowledge of Plotly — comprehensive,
specialised, with awareness of boundaries").

Source: `raw/eqf-8-levels.md`.

### 2.3 Typology — four alternative taxonomies

Different frameworks partition knowledge differently. All four below are valid
lenses; each is useful for a different purpose.

**By content type (Bloom revised 2001)** — what the knowledge *is about*:

| Type | Definition |
|---|---|
| Factual | Terminology, specific details, discrete elements |
| Conceptual | Relationships, classifications, principles, theories, models |
| Procedural | How to do things — methods, algorithms, techniques |
| Metacognitive | Knowledge of cognition itself and of one's own cognition |

**By codifiability (Polanyi 1966)** — whether it can be written down:

- **Explicit** — formalised, codified, transferable through documents.
- **Tacit** — rooted in experience, resists articulation. "We know more than we
  can tell." An AI model can only consume the explicit half; tacit knowledge
  must first be *externalised* (Nonaka SECI — see §5).

**By mode (Ryle 1949)** — what it is *about*:

- **Knowing that** — propositional content. Fact-shaped.
- **Knowing how** — practical ability. Skill-shaped. Gradable; acquired gradually
  through practice.

**By depth (EQF 1–8)** — how advanced it is (see §2.2).

### 2.4 Parallel definitions

O\*NET (US DOL):
> "Organized sets of principles and facts applying in general domains."

This aligns with the ESCO/EQF formulation: organised, principled, factual,
domain-bound. The two major occupational taxonomies converge on the same core
claim about what knowledge is.

Sources: `raw/bloom-revised-taxonomy.md`, `raw/polanyi-tacit-explicit.md`,
`raw/ryle-knowing-that-knowing-how.md`, `raw/onet-knowledge.md`.

---

## 3. What knowledge *is not*

### 3.1 Not data, not information, not wisdom

The DIKW hierarchy (Ackoff 1989; Rowley 2007) places knowledge between
information and wisdom:

| Level | What it is | Question it answers |
|---|---|---|
| Data | Unorganised symbols, signs, observations | — |
| Information | Contextualised data; has relevance | Who / what / where / when |
| **Knowledge** | Processed information applied in practice | How |
| Wisdom | Evaluated understanding; ethical judgement | Why |

Implications:

- **Data and information are ingredients, not knowledge**. A table of numbers
  is data; a labelled chart is information; a generalisation that explains
  the chart in context is knowledge.
- **Wisdom sits above knowledge**. We do not codify wisdom; we aim to provide
  enough knowledge (and crystallised experience) for a competent actor —
  human or AI — to *exercise* wisdom in context.
- DIKW has critics (Capurro, Weinberger, Frické) who argue the hierarchy is
  not as clean as the pyramid suggests. We use it as a discriminator, not as
  metaphysics.

Source: `raw/dikw-hierarchy.md`.

### 3.2 Not skill, not competence

ESCO's core distinction:

> "The difference lies in the way this knowledge is applied and being put into use."

- **Knowledge** = the content (facts, principles, theories, practices)
- **Skill** = cognitive and practical ability that applies knowledge (EQF)
- **Competence** = knowledge + skill + autonomy/responsibility in context (EQF)

In our skill framework, `knowledge/` holds the content layer; the skill itself
(the `SKILL.md` distillation, plus the `artifact/` vocabulary and the rules in
`experience/`) is the applied layer.

Sources: `raw/esco-knowledge.md`, `raw/eqf-8-levels.md`.

---

## 4. How knowledge relates to experience in our three-layer model

Our skill folder shape is `knowledge/`, `experience/`, `artifact/`. Mapping to
the literature:

| Our layer | Corresponds to |
|---|---|
| `knowledge/` | Explicit knowledge (Polanyi); knowing that (Ryle); factual + conceptual knowledge (Bloom); DIKW Knowledge level |
| `experience/` | Externalised tacit knowledge (Polanyi + Nonaka SECI); codified procedural knowledge (Bloom); crystallised knowing how (Ryle) |
| `artifact/` | The applied output — the skill/competence layer of ESCO; the "practices" bucket of the ESCO definition when codified as reusable parts |

### The SECI move (Nonaka & Takeuchi 1995)

Nonaka's SECI model describes four conversions between tacit and explicit:

| From ↓ \ To → | Tacit | Explicit |
|---|---|---|
| Tacit | Socialisation | **Externalisation** |
| Explicit | Internalisation | Combination |

For an AI consumer the critical move is **externalisation** — turning tacit
practitioner expertise into explicit, codified form. That is exactly what
writing into `experience/` accomplishes. Our framework is a disciplined
externalisation + combination pipeline.

Socialisation (tacit → tacit) is not available to an AI across sessions; the
substitute is thorough externalisation by humans up front.

Source: `raw/nonaka-seci-model.md`.

---

## 5. How knowledge is classified

### 5.1 ISCED-F 2013 (UNESCO)

ESCO classifies knowledge by field using ISCED-F 2013 — UNESCO's 2013
classification of Fields of Education and Training. It has 11 broad fields
(codes 00–10). We do not mandate ISCED-F classification for our skills, but
we name it here as the standard reference for any skill that needs formal
alignment with European qualifications systems.

### 5.2 Occupational taxonomies

O\*NET organises knowledge into 9 major categories (Business & Management,
Manufacturing & Production, Engineering & Technology, Mathematics & Science,
Health Services, Education & Training, Arts & Humanities, Law & Public Safety,
Communications). ESCO and EQF do not prescribe categories at this level;
ISCED-F handles the field partition.

### 5.3 Our practice

Each skill states its field in plain language (e.g., "dashboard design",
"Polish labour-market statistics", "dbt semantic-layer patterns"). We do not
require a formal ISCED-F code; clarity about the field is sufficient for
navigation.

Sources: `raw/isced-f-2013-note.md`, `raw/onet-knowledge.md`,
`raw/esco-knowledge.md`.

---

## 6. Implications for our skill framework

### 6.1 What belongs in `knowledge/`

- **Explicit, codified content** — facts, principles, theories, practices —
  about the skill's field (ESCO definition).
- **Raw sources** in `knowledge/raw/` — PDFs, URL excerpts, book quotes, standards
  documents, reference implementations.
- **A synthesis document** in `knowledge/` (typically `summary.md` per
  this skill's 7-section format) that distils the raw into a structured
  body of facts, principles, theories, and practices.
- **All four Bloom knowledge types** are welcome: factual, conceptual,
  procedural, metacognitive. But note §6.2 on where procedural knowledge
  actually lives in our model.

### 6.2 What does *not* belong in `knowledge/`

- **Tacit knowledge** that has not been externalised. Either externalise it
  into `experience/` or flag it honestly as a gap. Pretending to codify tacit
  knowledge that cannot be codified produces false confidence.
- **Crystallised heuristics, do/avoid rules, templates** — these are
  externalised procedural knowledge; they live in `experience/`. A rule like
  "never use pie charts with more than 3 categories" is *crystallised tacit*,
  not "knowledge" in the ESCO sense.
- **The skill's own output components** — visuals, layout, theme, model
  binding etc. These live in `artifact/`.
- **Raw data or raw information** without synthesis — DIKW puts these *below*
  knowledge. They can sit in `raw/` but the synthesis is what makes the
  bucket actually hold *knowledge*.
- **Wisdom / ethical judgement** — we support wisdom by giving the model
  enough knowledge and experience to exercise it; we do not attempt to write
  it down.

### 6.3 What an AI model consumes

An AI model consumes only **explicit** knowledge (Polanyi). Therefore:

- Everything load-bearing must be written down in explicit prose.
- Tacit expertise of a practitioner must be externalised first — that is the
  SECI externalisation step, and it is the *point* of `experience/`.
- Gaps where tacit knowledge cannot be fully codified must be flagged
  explicitly in a "Gaps and open questions" section, so future iterations
  know where to dig.

### 6.4 Depth discipline

Each skill should be explicit about what EQF depth level it targets. A skill
that needs L3 knowledge of a topic does not benefit from L7 research-frontier
material; conversely, a skill at L7 will be starved by L2 basics. State the
target level in the skill's `SKILL.md` so collection is scoped accordingly.

### 6.5 Quality bar for `knowledge/`

- Every factual claim in the synthesis cites a source in `knowledge/raw/`.
- The synthesis follows the 7-section structure defined in this skill
  (Overview, Authoritative sources, Key patterns, Component/API reference,
  Examples, Decisions, Gaps).
- Tacit-resistance gaps are declared honestly, not smoothed over.
- Sources are primary where available (standards, official docs, peer-reviewed
  work). Secondary summaries (Wikipedia, blog posts) are acknowledged as such.
- Dates checked — prefer 2023+ unless foundational (e.g., Ryle 1949, Polanyi
  1966, Nonaka 1995 are foundational and evergreen).

### 6.6 Source selection criteria

Any candidate source proposed for `knowledge/raw/` must pass this checklist.
The collect phase applies it up front; the analyse-coverage phase re-checks
after the fact. A source that fails a criterion is either rejected, demoted
to "secondary with note", or flagged for replacement. Waivers must be
recorded with a reason.

Each criterion is stated as a **rule** with the **failure mode** it prevents.

1. **Authority** — the source is recognised in its field: a standards body,
   peer-reviewed venue, primary practitioner, or vendor canon.
   *Failure mode:* anonymous blog post treated as canonical.
2. **Primacy** — primary source preferred over secondary. Wikipedia, Stanford
   Encyclopedia of Philosophy, blog summaries are accepted only when the
   primary is unavailable, and must be explicitly flagged as secondary.
   *Failure mode:* hearsay citation chains with no grounding.
3. **Load-bearing** — the source answers at least one of the skill's scoped
   knowledge questions (§7 workflow step 1). No filler, no "related reading".
   *Failure mode:* bloated `raw/` that hides the actual argument.
4. **Independence / triangulation** — sources collectively span tiers
   (institutional, academic, vendor, practitioner). No single school or author
   dominates. *Failure mode:* one worldview masquerading as the field's consensus.
5. **Codifiability (Polanyi)** — the valuable content in the source is
   *explicit*. If the valuable content is tacit, it is routed to `experience/`
   externalisation, not `knowledge/raw/`. *Failure mode:* fake explicitness —
   a checklist that is really a feel in disguise.
6. **Verifiability** — stable locator: DOI, ISBN, official URL, or archived
   snapshot when the URL is volatile. *Failure mode:* "a talk someone gave"
   citations that cannot be re-checked.
7. **Recency discipline** — prefer 2023+ or latest revision, unless the source
   is foundational and evergreen. Foundational picks must state *why* they
   remain current (Tufte 1983, Polanyi 1966, Ryle 1949, Nonaka 1995 are the
   pattern). *Failure mode:* stale technical canon; or blind recency that
   discards classics.

**Optional 8th — recommended, not strict:**

- **Licence / accessibility** — the source can be lawfully quoted and stored
  in `raw/`. Public-domain, Creative Commons, or fair-use scope verified.
  *Failure mode:* paywalled content copied verbatim into the repo.

#### How this integrates with the pipeline

- The collect phase evaluates each candidate against criteria 1–7 (and 8
  where publication matters) before writing to `raw/`.
- The analyse-coverage phase re-checks coverage and demotes or removes
  sources that fail.
- The final `summary.md` cites each source with a one-line note on which
  criteria it satisfies (or which were waived, with reason).

---

## 7. Workflow — how to populate `knowledge/` in a new skill

1. **Scope** — write down the specific questions the knowledge must answer
   (e.g., for `dashboard`: what IS a dashboard, what is it made of, what
   makes one good, how practitioners do it, what to avoid, how it binds to a
   semantic model). This list becomes the skeleton of `summary.md`.
2. **Identify tiers of authoritative sources** — primary practitioners,
   standards bodies, vendor canon, academic research, case material.
3. **Inventory what already exists** — other `complex_*` skills'
   `knowledge/` buckets. Do not duplicate; reference.
4. **Collect** — raw material into `knowledge/raw/`. The collect phase
   gathers without drawing conclusions.
5. **Analyze** — coverage, source quality, gaps. Return to the collect
   phase for targeted gaps; proceed when coverage is good enough.
6. **Synthesise** — write `summary.md` following the 7-section structure
   defined in this skill's `SKILL.md`. Every claim cites a source file in
   `raw/`.
7. **Distil** — pull 3–6 load-bearing rules from `summary.md` up into the
   skill's `SKILL.md`. `SKILL.md` stays scannable; depth stays in `summary.md`.
8. **Flag gaps** — the last section of `summary.md` lists what was not
   covered, what could not be verified, and what remains tacit and
   unexternalised. This is required, not optional.

---

## 8. Sources consumed

All raw sources are stored in `knowledge/raw/`. Full citations:

- **ESCO** — Escopedia, *Knowledge*. https://esco.ec.europa.eu/en/about-esco/escopedia/escopedia/knowledge (retrieved 2026-04-19). See `raw/esco-knowledge.md`.
- **EQF** — European Qualifications Framework, 8-level descriptors. https://en.wikipedia.org/wiki/European_Qualifications_Framework (retrieved 2026-04-19; the official europass.europa.eu URL returned 404). See `raw/eqf-8-levels.md`.
- **O\*NET** — Content Model. https://www.onetcenter.org/content.html (retrieved 2026-04-19). See `raw/onet-knowledge.md`.
- **Anderson & Krathwohl (2001)** — *A Taxonomy for Learning, Teaching, and Assessing: A Revision of Bloom's Taxonomy of Educational Objectives*. New York: Longman. Cognitive Process Dimension verbatim from Wikipedia; Knowledge Dimension reconstructed from canonical formulation. See `raw/bloom-revised-taxonomy.md`.
- **Ryle, Gilbert (1949)** — *The Concept of Mind*. London: Hutchinson. See `raw/ryle-knowing-that-knowing-how.md` (Stanford Encyclopedia of Philosophy).
- **Polanyi, Michael (1966)** — *The Tacit Dimension*. Chicago: University of Chicago Press. See `raw/polanyi-tacit-explicit.md` (Wikipedia).
- **Ackoff, Russell L. (1989)** — "From Data to Wisdom." *Journal of Applied Systems Analysis* 16: 3–9. See `raw/dikw-hierarchy.md`.
- **Rowley, Jennifer (2007)** — "The wisdom hierarchy: representations of the DIKW hierarchy." *Journal of Information Science* 33(2): 163–180. See `raw/dikw-hierarchy.md`.
- **Nonaka, Ikujiro & Takeuchi, Hirotaka (1995)** — *The Knowledge-Creating Company*. Oxford: Oxford University Press. See `raw/nonaka-seci-model.md` (Wikipedia).
- **UNESCO ISCED-F 2013** — partial, UNESCO direct PDF returned 404; notes consolidated in `raw/isced-f-2013-note.md`.

## 9. Open questions and known gaps

- **ISCED-F 2013 detailed field listing** — the 11 broad fields (codes 00–10)
  and their definitions were not successfully fetched. Not load-bearing for
  this definition, but required if a skill ever needs formal ISCED
  classification. Resolve by fetching the UNESCO ISCED-F 2013 manual.
- **Bloom Knowledge Dimension primary-source quotes** — reconstructed from
  canonical formulation; direct quotes from Anderson & Krathwohl 2001 should
  replace the reconstruction if the Knowledge Dimension ever becomes
  load-bearing for a specific decision.
- **Davenport & Prusak (1998)** — identified in the plan but not fetched; the
  SECI + Polanyi + DIKW sources already cover the ground. Fill if an
  operational KM definition is needed.
- **Tacit/untranscribed expertise** — any practitioner expertise that remains
  tacit and was not externalised is, by Polanyi's own argument, absent from
  this framework. Future skills should actively solicit tacit expertise from
  practitioners and externalise it deliberately rather than assume
  documentation alone covers the field.
