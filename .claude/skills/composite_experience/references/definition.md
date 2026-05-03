# Experience — Definition and Methodology

Meta-knowledge about what *experience* is, how it is structured, and what this
means for the `experience/` folder inside every skill in this project. This file
lives inside the `experience-base` skill so that every new skill inherits the
same grounded understanding. Companion to `knowledge-base/knowledge/knowledge-definition.md`.

---

## 1. Primary definition

Drawing on Kolb (1984), Argyris & Schön (1978), and Davenport & Prusak (1998),
*experience* is defined in this project as:

> **Experience is the accumulated, framed record of prior action — what was
> done, what was observed, what was expected, how expectation diverged from
> outcome, and the revised rule this episode implies.**

The operative phrase is **framed experience** (Davenport & Prusak 1998):

> "Knowledge is a fluid mix of framed experience, values, contextual information,
> and expert insight that provides a framework for evaluating and incorporating
> new experiences and information."

Three load-bearing claims:

1. Experience is **retrospective** — it exists only after an action has been
   taken and its consequences observed.
2. Experience is **interpretive** — raw logs are *data*, not experience. An
   experience record requires the observer to *frame* the episode: what was
   expected, what actually happened, what rule it implies.
3. Experience is **tacit-originating but explicit-rendered** — it begins in
   the practitioner's head (Polanyi's tacit dimension) and becomes a usable
   artefact only when it is **externalised** (Nonaka's SECI model, §4).

Sources: `raw/kolb-experiential-learning.md`, `raw/davenport-prusak-working-knowledge.md`,
`raw/argyris-schon-theories-of-action.md`, `raw/polanyi-tacit-explicit.md`,
`raw/nonaka-seci-model.md`.

---

## 2. What experience *is*

### 2.1 The four modes of an experience entry (Kolb 1984)

Kolb's cycle maps directly onto the minimum structure of an experience record:

| Kolb stage | In an experience entry | What it captures |
|---|---|---|
| Concrete Experience (CE) | *What happened* | The event — observed facts, no interpretation |
| Reflective Observation (RO) | *Expectation vs outcome* | Where the expected frame diverged from reality |
| Abstract Conceptualisation (AC) | *Revised rule / pattern* | The transferable lesson, stated as a rule |
| Active Experimentation (AE) | *How it will be tested* | The next situation where the revised rule will be validated |

> "Effective learning is seen when a person progresses through a cycle of four stages." (Kolb 1984)

Skipping any stage produces a diminished entry (see §6.2).

### 2.2 Two loop levels (Argyris & Schön 1978)

Every experience entry should declare its loop level:

- **Single-loop** — strategy is adjusted; governing goal stays the same.
  *"Do X instead of Y, still pursuing goal G."*
- **Double-loop** — the governing variable itself is revised.
  *"Goal G was wrong; the real goal is G'."*

Double-loop entries are rarer and more valuable. Mislabelling a double-loop
correction as single-loop is a silent corruption: the governing variable stays
broken while strategy thrashes around it.

### 2.3 Two moments of reflection (Schön 1983)

| Moment | When it happens | Artefact |
|---|---|---|
| **Reflection-in-action** | Mid-task, while the situation is still unfolding | Session-local correction; fragment in conversation memory |
| **Reflection-on-action** | After the task is complete | A durable experience entry |

The experience base primarily stores the *reflection-on-action* record, but it
should be retrievable *during future work* in a way that supports
*reflection-in-action* on similar situations. That is, entries are indexed by
**trigger conditions** (situation shape) as well as by topic.

### 2.4 Surprise as the capture signal (Schön 1983)

Reflection is triggered by **surprise** — a unique case, an unstable situation,
a conflict of values, or an outcome that contradicted expectation. Without
surprise, routine proceeds on autopilot and there is nothing worth writing down.

This means: an experience entry whose CE equals the prior expectation exactly is
almost never worth keeping. The entries worth writing are the ones where the
prior expectation was wrong or incomplete.

### 2.5 The four AAR questions (US Army TC 25-20, 1993)

The US Army's After-Action Review gives the canonical *ritual* for converting an
event into a record:

1. **What was supposed to happen?** — expectation.
2. **What actually happened?** — observed fact.
3. **What went well and why?** — the success pattern and its causes.
4. **What can be improved and how?** — the forward rule.

The AAR's four-question sequence is this project's recommended template for a
formal experience entry (see §6.1).

### 2.6 The SECI conversions (Nonaka & Takeuchi 1995)

Experience entries are the output of two SECI moves:

- **Externalisation** (tacit → explicit) — the act of writing a tacit judgement
  ("I felt it was wrong because…") into propositional prose.
- **Combination** (explicit → explicit) — promoting recurring rules into
  standards, skills, or patterns once enough entries accumulate.

Socialisation (tacit → tacit) is **not available** to an AI across sessions —
the model cannot apprentice. Internalisation (explicit → tacit) corresponds,
for an AI, to repeated use of the entry in context.

---

## 3. What experience *is not*

### 3.1 Not raw logs

A session transcript, a git log, a terminal output, or a command history is
*data* (DIKW). Adding timestamps and context makes it *information*. It
becomes *experience* only when the observer frames it: states the expectation,
identifies the divergence, extracts the rule. A folder of raw logs is not an
experience base.

### 3.2 Not knowledge

Knowledge (per the `knowledge-base` skill) is declarative, external, and field-wide
— *what the field knows*. Experience is procedural, local, and internal —
*what we have learned by doing*. The two feed each other: experience entries
may elevate to standards (which then become reference knowledge for future
work); knowledge frames the expectation against which experience is read.

### 3.3 Not narrative for its own sake

An entry that reads as storytelling with no transferable rule has failed at
Kolb's AC stage. The test: can a future reader (or future model) extract an
action-relevant rule from this entry without re-deriving it? If no, the entry
is incomplete.

### 3.4 Not a blame log

AAR doctrine is explicit: the subject is *systems, processes, and decisions*,
not individuals. The AI analogue of blame is confirmation bias and post-hoc
rationalisation of the path actually taken. Entries that soften failure into
success or rationalise away disconfirming evidence pollute the experience
base and propagate the same mistake into future work.

---

## 4. How experience relates to knowledge and assets in our three-layer model

The three-layer shape — `knowledge/`, `experience/`, `assets/` — distributes
the substance:

| Our layer | Corresponds to |
|---|---|
| `knowledge/` | Explicit knowledge (Polanyi); knowing that (Ryle); factual + conceptual (Bloom); DIKW Knowledge |
| `experience/` | **Externalised tacit knowledge** (Polanyi + Nonaka SECI); crystallised procedural knowledge (Bloom); codified *knowing how* (Ryle); framed experience (Davenport & Prusak) |
| `assets/` | The applied resources the skill points to — code modules, themes, fixtures; the ESCO *skill* / *competence* layer |

### The externalisation move

For an AI, the load-bearing SECI step is **externalisation** — turning tacit
practitioner expertise into explicit prose. `experience/` is where that
externalisation lives. Without it, an AI has no apprenticeship substitute
(socialisation is unavailable) and cannot internalise practitioner feel.

### The combination move

When several entries converge on the same rule, the rule should be **combined
upward** into:

- a `team/standards/build/` or `team/standards/evaluation/` rule,
- a section of a skill's `SKILL.md`,
- a test or check in the pipeline.

Unpromoted rules silently duplicate in the experience base.

Sources: `raw/polanyi-tacit-explicit.md`, `raw/nonaka-seci-model.md`,
`raw/davenport-prusak-working-knowledge.md`.

---

## 5. How experience is structured

### 5.1 Informal vs formal entries (AAR)

Not every reflection warrants a full entry. Borrowing the AAR distinction:

- **Informal** — an in-session correction, a quick note, a lesson that
  changes the next three minutes of work. May live in conversation memory
  or a lightweight scratch note.
- **Formal** — a durable, structured entry written to `experience/`. Used
  after a complex product build, a failed deployment, a recurring bug, or
  a surprising outcome. Produces a re-usable artefact.

The experience base stores **formal** entries. Informal corrections are
valuable but too numerous to archive individually.

### 5.2 The entry shape

Every formal entry in `experience/` has this skeleton:

```
# <short title — the rule, not the event>

**Date:** YYYY-MM-DD
**Situation type:** <class of situation; used as retrieval key>
**Loop level:** single-loop | double-loop

## Expected
<what was supposed to happen — CE + Argyris's "espoused theory">

## Observed
<what actually happened — no interpretation>

## Surprise
<where expectation diverged, or why the case was unique/unstable/value-conflicted>

## Rule
<the revised, transferable rule — AC stage; single sentence possible>

## How to test
<the next situation where this rule will be validated — AE stage>

## Promotion target (if any)
<standard, skill section, or check this rule should be combined into>

## Sources / links
<related commits, PRs, session notes, prior entries>
```

### 5.3 Retrieval keys

Entries must be retrievable by **situation type**, not only by topic. Schön's
*reflection-in-action* requires that a similar-looking situation cue the prior
entry in-flight. That means the **Situation type** field is a first-class
index, maintained as a small controlled vocabulary per skill.

---

## 6. Implications for our skill framework

### 6.1 What belongs in `experience/`

- **Formal framed entries** following the §5.2 shape.
- **Crystallised do/avoid rules** derived from multiple entries, grouped by
  topic (e.g., `experience/rules/aggregation.md`).
- **Templates and patterns** distilled from recurring entries — the AC output
  generalised into a reusable shape.
- **A situation-type index** if entries grow beyond a handful.

### 6.2 What does *not* belong in `experience/`

- **Raw session logs** — these are data, not experience. Archive elsewhere
  if needed.
- **Field-wide facts or theories** — these are knowledge; they belong in
  `knowledge/`.
- **Re-usable output parts** (charts, layouts, components) — these are the
  skill's asset vocabulary; they belong in `assets/`.
- **Unpromoted rationalisations** — an entry that softens failure into success
  corrupts the base and must be rewritten or removed.
- **Entries missing Kolb stages** — an entry without expectation (CE gap),
  without divergence (RO gap), without a rule (AC gap), or without a test
  plan (AE gap) is incomplete and should be flagged for completion rather
  than archived as-is.

### 6.3 What an AI model consumes

An AI model consumes **only explicit** content (Polanyi). Therefore:

- Every tacit judgement must be externalised in prose before it is usable.
- The entry's *Rule* field must be action-relevant and self-contained — a
  future model should be able to apply the rule without needing the full
  narrative context.
- Entries that remain implicit ("you just have to feel it") are not usable
  by the AI and must be either externalised further or routed into the
  knowledge base (to cite human practitioner sources) rather than faked in
  `experience/`.

### 6.4 Depth and scope discipline

Experience is **skill-local**. An entry about Plotly layout behaviour belongs
in the `dashboard` skill's `experience/`, not in a shared pool. Cross-skill
lessons that prove durable should be promoted to `team/standards/` via the
combination move (§4) — they become knowledge once standardised.

### 6.5 Quality bar for `experience/`

- Every formal entry has the full §5.2 skeleton filled — no section empty.
- Each entry declares its **loop level** explicitly.
- The **Rule** is a single transferable sentence, not a paragraph of
  narrative.
- Disconfirming evidence is preserved, not edited out (AAR no-blame).
- Entries that have been promoted into a standard reference the standard
  and can be retired or compacted.
- Stale entries (contradicted by later work, superseded by a standard) are
  marked superseded, not silently deleted.

### 6.6 Entry-quality criteria

Any candidate entry proposed for `experience/` must pass this checklist before
being merged. This is the experience-base analogue of `knowledge-definition.md` §6.6
source-selection criteria — but it grades the *entry* rather than an *external
source*, because experience content is produced internally, not collected.

Each criterion is stated as a **rule** with the **failure mode** it prevents.

1. **Surprise present** — the entry is triggered by a divergence between
   expectation and outcome, a unique case, or a value conflict. No-surprise
   entries are diary, not experience.
   *Failure mode:* a log of routine work inflated into an "entry".
2. **Full Kolb cycle** — CE, RO, AC, AE are all populated. No stage skipped.
   *Failure mode:* narration without a transferable rule; rule without a plan
   to test; test plan without grounding in an observed event.
3. **Loop level declared** — single-loop or double-loop explicit.
   *Failure mode:* double-loop correction mislabelled as single-loop, leaving
   the governing variable broken.
4. **Frame stated** — what frame / assumption was operative at the time. Schön's
   problem-setting requirement: capture the frame that produced the surprise,
   not only the outcome.
   *Failure mode:* an entry that presents its conclusion as the obvious one,
   hiding the frame that made it non-obvious.
5. **No-blame / no-rationalisation** — the entry records disconfirming evidence
   honestly. Failures are not softened. The chosen path is not retrofitted
   into "the right call all along".
   *Failure mode:* confirmation-biased entry that propagates the same mistake.
6. **Transferability** — the Rule is a sentence a future reader can apply in a
   *different* instance of the same situation type, without re-deriving it.
   *Failure mode:* the entry reads as a story about one project, usable
   nowhere else.
7. **Retrievability** — the entry declares its situation type using the skill's
   controlled vocabulary, so it can be recalled mid-task in future work.
   *Failure mode:* the entry is forgotten because nothing triggers its recall.
8. **Promotion path** — if the rule is likely to recur across situations, the
   entry names the standard, skill section, or check into which it should be
   combined. If not yet ready for promotion, the entry flags "local for now".
   *Failure mode:* rules accumulate in `experience/` and never influence
   standards; knowledge base never compounds.

#### How this integrates with the pipeline

- At time of writing: the author fills the §5.2 skeleton and self-checks
  against criteria 1–7. Criterion 8 (promotion) is revisited periodically,
  not per-entry.
- At periodic review: rules that have fired multiple times are promoted into
  standards (combination move); contradicted entries are marked superseded;
  stale entries with no promotion path and no recurrence are compacted.

---

## 7. Workflow — how to populate `experience/` in a new skill

1. **Seed the situation-type vocabulary** — list the classes of situation this
   skill recurrently faces (e.g., for `dashboard`: *ambiguous KPI spec*,
   *over-long series*, *failed colour contrast*, *cross-filter dead-end*).
   This vocabulary doubles as the retrieval index.
2. **Start empty** — a new skill has no earned experience. Do not invent
   entries from imagined scenarios; this produces plausible-sounding but
   unvalidated rules. Empty is honest; fabricated is harmful.
3. **Capture on surprise** — during real work, when outcome diverges from
   expectation, write a formal entry following §5.2. Apply criteria §6.6.
4. **Classify** — tag the entry with situation type and loop level.
5. **Periodically combine** — when 2–3 entries converge on the same rule,
   promote the rule to a standard, a skill section, or a check. Mark the
   source entries as *promoted* with a link to the standard.
6. **Periodically prune** — mark superseded entries superseded; compact
   obsolete ones. An entry contradicted by a later entry is *information*
   about the evolution of the rule, not garbage — keep it with a supersession
   marker if it remains instructive.
7. **Cross-skill promotion** — when a rule proves durable across skills,
   move it up to `team/standards/`. At that point it becomes *knowledge* for
   future skills (see `knowledge-definition.md` §4 on the knowledge/experience
   split).

---

## 8. Sources consumed

All raw sources are stored in `knowledge/raw/`. Full citations:

- **Polanyi, Michael (1966)** — *The Tacit Dimension*. Chicago: University of Chicago Press. Also referenced in `knowledge-base`. See `raw/polanyi-tacit-explicit.md`.
- **Argyris, C. & Schön, D. A. (1978)** — *Organizational Learning: A Theory of Action Perspective*. Reading, MA: Addison-Wesley. Consulted via Smith / infed.org exposition. See `raw/argyris-schon-theories-of-action.md`.
- **Schön, D. A. (1983)** — *The Reflective Practitioner: How Professionals Think in Action*. New York: Basic Books. Consulted via Saffer's summary notes. See `raw/schon-reflective-practitioner.md`.
- **Kolb, D. A. (1984)** — *Experiential Learning: Experience as the Source of Learning and Development*. Englewood Cliffs, NJ: Prentice Hall. Consulted via Simply Psychology exposition. See `raw/kolb-experiential-learning.md`.
- **US Army (1993)** — *TC 25-20: A Leader's Guide to After-Action Reviews*. HQ Department of the Army. Consulted via USAID AAR Technical Guidance (Feb 2006). See `raw/us-army-after-action-review.md`.
- **Nonaka, Ikujiro & Takeuchi, Hirotaka (1995)** — *The Knowledge-Creating Company*. Oxford: Oxford University Press. Also referenced in `knowledge-base`. See `raw/nonaka-seci-model.md`.
- **Davenport, T. H. & Prusak, L. (1998)** — *Working Knowledge: How Organizations Manage What They Know*. Boston: Harvard Business School Press. Consulted via Mindtools exposition. See `raw/davenport-prusak-working-knowledge.md`.

## 9. Open questions and known gaps

- **Schön primary-text quotes with page numbers** — current entry uses
  secondary exposition; direct quotes from Schön (1983) would strengthen §2.3
  and §2.4. Resolve by fetching the archived PDF of the full text when needed.
- **Argyris & Schön 1996 *Organizational Learning II*** — the 1996 follow-up
  refines several 1978 claims. Not fetched; not load-bearing for current
  definitions; fill if double-loop implementation patterns become load-bearing.
- **Empirical AAR literature outside the military** — healthcare, aviation,
  and wildfire services all adapted AAR with their own findings. Not
  consulted; fill if a domain-specific AAR pattern is needed.
- **How to measure experience-base health** — the definition names quality
  criteria for individual entries but does not specify a *base-level* metric
  (coverage, recurrence detection, promotion rate). Candidate for a follow-up
  pass once enough entries exist to measure against.
- **Tacit AI judgement** — the analogue of tacit practitioner expertise inside
  a language model (pattern-matching beyond explicit rules) is not well
  characterised. Any entry relying on "the model should notice X" is a
  candidate externalisation-gap and should be flagged rather than assumed.
