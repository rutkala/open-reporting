# Artifact — Definition and Methodology

Meta-knowledge about what *artifact* is, how it is structured, and what this
means for the `artifact/` folder inside every skill in this project. This file
lives inside the `artifact-base` skill so that every new skill inherits the
same grounded understanding. Companion to
`knowledge-base/knowledge/knowledge-definition.md` and
`experience-base/knowledge/experience-definition.md`.

---

## 1. Primary definition

Drawing on Simon (1969), Alexander (1977), Parnas (1972), Gamma et al. (1994),
Evans (2003), and Frost (2016), an *artifact* in this project is defined as:

> **An artifact is a purposeful, named, composable part — an interface between
> an inner mechanism and an outer environment — that solves a recurring
> problem in a context, within the bounded vocabulary of the skill that
> produces it.**

Six load-bearing claims, each traceable to one of the six sources:

1. **Purposeful and interface-shaped** — Simon (1969): "The real nature of the
   artifact is the interface." An artifact exists *for* a goal, mediating
   between an inner mechanism and an outer environment.
2. **Shaped by information hiding** — Parnas (1972): each artifact owns *one*
   design decision likely to change, exposing only the interface needed to
   use it.
3. **Pattern-form, recurring problem** — Alexander (1977): the part captures
   the **core of a solution** to a **recurring problem in a context,** and
   permits many non-identical instantiations.
4. **Composable, not inherited** — Gamma et al. (1994): parts combine through
   interfaces, not through shared implementation. *Program to an interface,
   not an implementation. Favour composition over inheritance.*
5. **Named in the domain's vocabulary** — Evans (2003): part names are the
   skill's **ubiquitous language** inside its **bounded context.** Generic
   names ("util", "helper") are a failure to name the domain.
6. **Stratified by scale** — Frost (2016): the vocabulary has levels
   (atom → molecule → organism → template → page, or a domain analogue).
   Flat vocabularies lose structural discrimination.

Sources: all six files in `raw/`.

---

## 2. What an artifact *is*

### 2.1 Interface, not object (Simon)

An artifact is the **interface** between:

- its **inner environment** (mechanism, substance, organisation), and
- its **outer environment** (contexts where it will be assembled and used).

> "The real nature of the artifact is the interface." (Simon 1969)

Fit of inner to outer is the quality bar. An internally elegant part that
misfits its assembly contexts is a worse artifact than an ugly part that
fits cleanly.

### 2.2 Four essential elements (GoF, in Alexandrian form)

Every artifact entry has:

1. **Name** — the shared-vocabulary handle (Evans: ubiquitous language).
2. **Problem (in context)** — the recurring tension, scoped to a context class.
3. **Solution** — the arrangement of elements that resolves the tension.
4. **Consequences** — what is gained, what is given up, what new constraints arise.

The Consequences field is mandatory. A part without stated consequences is a
recommendation, not an artifact.

### 2.3 Owns one hidden decision (Parnas)

A well-formed artifact owns *one* design decision likely to change. Everything
else about it is either interface (public) or irrelevant to users. When that
one decision changes, ideally *one file* changes.

Parts that own two decisions will decompose badly on first change. Split them
early.

### 2.4 Generative, not template (Alexander)

> "You can use the solution a million times over, without ever doing it the
> same way twice." (Alexander 1977)

A part is rightly under-specified. It leaves degrees of freedom open for the
assembling context to resolve. Over-specification — locking every parameter —
collapses the pattern into a rigid template and destroys generativity.

### 2.5 Typed by role (Evans)

An artifact is some *kind* of thing. Evans's tactical building blocks
(Entity / Value Object / Aggregate / Service / Factory / Repository) are one
typology; domain-specific analogues exist (Frost's atom/molecule/organism;
dashboard's kpi/chart/panel/layout). Flat vocabularies where every part is
"a component" lose structural discrimination.

### 2.6 Stratified by scale (Frost)

> "Atomic design is a mental model to help us think of our user interfaces as
> both a cohesive whole and a collection of parts at the same time." (Frost 2016)

Parts exist at multiple granularities:

- **Irreducible** — breaking further destroys function.
- **Purposeful combinations** — smallest unit with a task-level name.
- **Functional sections** — complete sub-assemblies.
- **Structures / templates** — skeleton without content.
- **Instances** — filled with real content / data.

A skill's `artifact/` declares its stratification and names each level.

---

## 3. What an artifact *is not*

### 3.1 Not an arbitrary file

A file that has been used once, in one place, is a **prototype**, not an
artifact. Alexander's recurrence rule: the problem must recur and the core
solution must survive at least one re-instantiation before the part earns
artifact status. Unused "just in case" parts are dead weight.

### 3.2 Not a template

Templates parameterise identical instances. Artifacts (as patterns) generate
non-identical instances whose core is preserved and whose surface adapts.
Parts over-specified to the point of fixing every parameter have collapsed
into templates and should be demoted or re-designed.

### 3.3 Not the skill's knowledge or experience

- `knowledge/` holds *what the field knows* (declarative, external).
- `experience/` holds *what doing it has taught us* (procedural, local).
- `artifact/` holds *the reusable parts the skill produces* (the skill's
  own vocabulary of outputs).

Knowledge informs the design of an artifact; experience sharpens it over
iterations; but neither is an artifact. Conflating them pollutes all three
layers.

### 3.4 Not a leaky abstraction

A part that requires its users to understand its internals has failed at
information hiding (Parnas) and at "program to an interface" (GoF). The
cost of the part exceeds its benefit. Either narrow the interface or
redesign the part.

### 3.5 Not a cross-skill universal

Each skill is a **bounded context** (Evans). A term that looks the same in
two skills may mean different things in each. Artifacts do not auto-promote
across skill boundaries — they require an **anti-corruption layer** if one
skill consumes another skill's parts.

---

## 4. How artifact relates to knowledge and experience in our three-layer model

| Our layer | Corresponds to |
|---|---|
| `knowledge/` | Explicit, external, field-wide (ESCO/EQF) |
| `experience/` | Externalised tacit lessons from doing (Polanyi + Nonaka + Kolb + Schön) |
| `artifact/` | **The skill's own vocabulary of reusable parts** — its ubiquitous language (Evans), its pattern language (Alexander), its stratified system (Frost), its information-hiding modules (Parnas), its purposeful interfaces (Simon), in the pattern form (GoF) |

### The flow between layers

1. **Knowledge informs artifact design.** What the field considers well-formed
   components, canonical patterns, proven interfaces — these shape what a
   well-formed artifact looks like before the skill starts producing them.
2. **Experience sharpens artifact design.** Each time an assembly reveals a
   poorly-fitting or over-specified part, the entry in `experience/`
   (framed under the experience-base discipline) feeds back into a revised
   artifact.
3. **Artifacts publish the skill's externalised form.** Downstream consumers
   (other skills, products, agents) talk to the skill through its artifacts.
   The artifact vocabulary is the skill's public face.

---

## 5. How artifact is structured

### 5.1 Scale stratification (Frost, adapted)

Every skill's `artifact/` declares its stratification. A minimum of **three
levels** is recommended; five is typical when UI is involved. Names may be
borrowed from Frost or defined per-skill domain.

| Level | Test | Examples |
|---|---|---|
| **Primitive** | Irreducible; breaking destroys function | a color token, a data-type adapter, a single Plotly trace builder |
| **Compound** | Smallest unit with a task-level name | a KPI card, a query-with-filters, a chart-with-legend |
| **Section** | Complete, functional sub-assembly | a filter panel, a header, a comparison block |
| **Structure** | Layout skeleton without content | a dashboard page layout, a report template, a section grid |
| **Instance** | Filled with real content, lives outside `artifact/` | an actual product page (in `products/`) |

Instance-level artefacts do not live in `artifact/`; they live in the consuming
product. `artifact/` stops one level above the instance.

### 5.2 Typology (Evans, adapted)

Within each level, parts are further typed by **role** — the kind of thing
they are. A skill must declare its typology. Examples:

- **dashboard skill**: visual / control / layout / model-binding / theme.
- **data-engineering skill**: ingestor / transformer / mart / check / semantic-measure.
- **research skill**: data-loader / model / diagnostic / plot.

Flat "component" vocabularies are rejected. The typology is the vocabulary's
spine.

### 5.3 The entry shape

Every part in `artifact/` is documented with this skeleton (Alexandrian form,
with GoF's fourth element and Evans's typing):

```
# <part name — in the skill's ubiquitous language>

**Level:** <primitive | compound | section | structure>
**Type / Role:** <skill-specific; e.g., visual / control / layout>
**Owns decision:** <the one changeable design decision this part hides>
**Status:** prototype | artifact | deprecated

## Context
Where this part applies. The situation class. Outer environment.

## Problem
The recurring tension this part resolves. What goes wrong without it.

## Solution
The part itself — interface, shape, behaviour. What a caller sees. NOT the
internal implementation.

## Forces / trade-offs
The tensions the solution navigates; what it optimises for; what it accepts
as cost.

## Consequences
What is gained, what is given up, what new constraints this part introduces
into any assembly that uses it.

## Related parts
- Composes with: <larger parts that assemble this one>
- Composed from: <smaller parts this one uses>
- Alternatives: <peer parts that solve the same problem differently>

## Instances
Known uses across skills and products. First use = prototype; second use
promotes to artifact.
```

### 5.4 Retrieval and composability

Parts are indexed by:

- **Level** (for scale-appropriate retrieval),
- **Type/Role** (for role-appropriate retrieval),
- **Context** (for situation-appropriate retrieval),
- **Problem keyword** (for pain-point retrieval).

The cross-links between parts (*composes with / composed from / alternatives*)
are at least as important as the individual entries (Alexander: the
connections are more meaningful than the nodes).

---

## 6. Implications for our skill framework

### 6.1 What belongs in `artifact/`

- **Formal pattern entries** following the §5.3 shape.
- **A typology declaration** — the skill's roles and levels.
- **A scale-stratification declaration** — named levels used.
- **Cross-reference maps** — relationships between parts (composes-with,
  alternatives, deprecated predecessors).

### 6.2 What does *not* belong in `artifact/`

- **One-off scripts** — use once, discard or keep in the product. Not an
  artifact until recurrence justifies promotion.
- **Field knowledge** — belongs in `knowledge/`.
- **Lessons from doing** — belong in `experience/`.
- **Rigid templates** — artifacts are generative; fully-parameterised
  templates indicate the pattern collapsed.
- **Universal utilities** — a true cross-skill primitive belongs to
  `team/standards/` or a shared library, not to a single skill's `artifact/`.

### 6.3 What an AI model consumes

An AI model consumes **explicit** artifact definitions (Polanyi). Therefore:

- Every part's interface must be explicit: signature, inputs, outputs,
  constraints.
- Every part's *consequences* must be explicit — what it commits assemblies
  to.
- Implicit "just use it, you'll see how" parts are unusable by the AI and
  fail the Polanyi test. Either externalise further or flag as gap.

### 6.4 Depth and scope discipline

Artifacts are **skill-local**. A part belongs to one skill's `artifact/`. Cross-
skill reuse happens either by:

- **Promotion to `team/standards/`** — the part becomes knowledge for other
  skills (it is standardised and no longer the skill's private vocabulary);
  or
- **Anti-corruption layer** (Evans) — consumer skill translates producer
  skill's vocabulary at the boundary, not by adopting it silently.

Silent cross-skill adoption breaks both bounded contexts.

### 6.5 Quality bar for `artifact/`

- Every part has all §5.3 sections populated.
- Every part names *one* hidden decision (Parnas).
- Every part's **Consequences** field is honest — costs, not only benefits.
- Every part has **Level**, **Type/Role**, and **Status** declared.
- Parts marked *artifact* status have been used ≥ 2 times (Alexander recurrence).
- Parts marked *deprecated* name their successor.
- Generic names ("utility", "helper", "common", "base") are rejected;
  names must belong to the skill's ubiquitous language (Evans).
- Interface reveals as little as possible (Parnas + GoF).

### 6.6 Part-quality criteria

Any candidate entry proposed for `artifact/` must pass this checklist. This is
the artifact-base analogue of `knowledge-definition.md` §6.6 (source-selection)
and `experience-definition.md` §6.6 (entry-quality) — but it grades *candidate
reusable parts*, because artifacts are produced internally by the skill.

Each criterion is stated as a **rule** with the **failure mode** it prevents.

1. **Purpose named** — the part states the goal it serves and the outer
   environment it fits. *Failure mode:* a pretty component no-one can explain
   the purpose of.
2. **Recurrence demonstrated** — the underlying problem has appeared ≥ 2 times
   in real assemblies before the part is promoted from prototype to artifact.
   *Failure mode:* speculative "might be useful" parts clogging the vocabulary.
3. **One hidden decision** — exactly one design decision likely to change is
   owned by this part. *Failure mode:* a multi-decision part that cannot absorb
   change cleanly.
4. **Narrow interface** — the public surface reveals as little as possible;
   internals are not leaked. *Failure mode:* a leaky abstraction that forces
   users to know the implementation.
5. **Composable by interface** — relates to other parts via interface, not via
   shared implementation or inheritance of internals. *Failure mode:* a part
   whose use requires knowing its parent class or sibling internals.
6. **Generative, not template** — the part permits multiple non-identical
   instantiations by leaving appropriate degrees of freedom. *Failure mode:*
   a fully-parameterised template masquerading as a pattern.
7. **Named in ubiquitous language** — the name uses the skill's domain
   vocabulary, not generic filler. *Failure mode:* "util.py", "helper.py",
   "common.py", "base.py".
8. **Level and role declared** — the part's scale level and kind/role are
   stated. *Failure mode:* flat "component" pile with no structural spine.
9. **Consequences honest** — trade-offs, costs, and new constraints are
   stated. *Failure mode:* marketing copy disguised as documentation.
10. **Cross-links present** — composes-with, composed-from, and alternatives
    are named. *Failure mode:* isolated parts with no language-level
    relationships.

#### How this integrates with the pipeline

- At time of proposal: author fills the §5.3 skeleton; self-checks against
  criteria 1–10.
- At promotion (prototype → artifact): second-use evidence is cited; criteria
  1, 2, 3, 6 re-checked.
- At periodic review: parts that have acquired responsibilities (violating
  criterion 3) are split; parts with leaky interfaces (criterion 4) are
  narrowed; deprecated parts with no users are retired.

---

## 7. Workflow — how to populate `artifact/` in a new skill

1. **Declare the typology** — the kinds of part this skill produces
   (visual / control / layout / model-binding / theme, or equivalent). This
   declaration is itself an artifact-level decision.
2. **Declare the stratification** — the levels used (primitive / compound /
   section / structure, or a domain analogue).
3. **Start empty** — a new skill has no earned artifacts. Do not fabricate
   parts from imagined assemblies. Parts earn their place through recurrence
   in real work.
4. **Prototype on first use** — when a new shape appears, build it in the
   consuming product. Do not promote yet. Mark status *prototype*.
5. **Promote on recurrence** — when the same shape is needed again, extract
   the reusable part into `artifact/`. Apply §5.3 entry shape; pass §6.6
   criteria. Status becomes *artifact*.
6. **Periodically consolidate** — when two parts converge, merge or state
   their distinction sharply. When a part's decision has leaked into others,
   re-narrow the interface. When a part is obsolete, mark *deprecated* with
   a successor link.
7. **Promote upward on cross-skill recurrence** — if the part proves useful
   across skills (validated through an anti-corruption layer at first), move
   it to `team/standards/` or a shared library. It then exits the skill's
   private vocabulary and becomes shared knowledge.

---

## 8. Sources consumed

All raw sources are stored in `knowledge/raw/`. Full citations:

- **Simon, H. A. (1969, rev. 1981, 1996)** — *The Sciences of the Artificial.* Cambridge, MA: MIT Press. See `raw/simon-sciences-of-the-artificial.md`.
- **Parnas, D. L. (1972)** — "On the Criteria To Be Used in Decomposing Systems into Modules." *Communications of the ACM,* 15(12), 1053–1058. See `raw/parnas-information-hiding.md`.
- **Alexander, C., Ishikawa, S., Silverstein, M., et al. (1977)** — *A Pattern Language: Towns, Buildings, Construction.* Oxford University Press. Companion: Alexander, C. (1979). *The Timeless Way of Building.* Oxford University Press. See `raw/alexander-pattern-language.md`.
- **Gamma, E., Helm, R., Johnson, R., & Vlissides, J. (1994)** — *Design Patterns: Elements of Reusable Object-Oriented Software.* Reading, MA: Addison-Wesley. See `raw/gang-of-four-design-patterns.md`.
- **Evans, E. (2003)** — *Domain-Driven Design: Tackling Complexity in the Heart of Software.* Reading, MA: Addison-Wesley. See `raw/evans-ubiquitous-language-ddd.md`.
- **Frost, B. (2016)** — *Atomic Design.* Self-published. See `raw/frost-atomic-design.md`.

## 9. Open questions and known gaps

- **Direct primary-text reading of Simon, Parnas, Alexander, and Evans** —
  current entries are built on secondary summaries with verbatim anchors
  preserved. Primary reading with exact page numbers would strengthen the
  quoted sections but is not load-bearing for the definition.
- **Parnas's later work** — *A Rational Design Process* (1986) and the
  information-hiding module papers of the 1980s refine the 1972 argument and
  are not yet consulted. Fill if the *module structure* (not just
  decomposition criterion) becomes load-bearing.
- **POSA / Buschmann et al. (1996)** — *Pattern-Oriented Software
  Architecture* extended GoF to architectural patterns. Not consulted; add
  if architectural-scale artefacts (not just component-scale) become
  load-bearing.
- **Modern design-system references** — Material, Carbon, Polaris, Spectrum.
  Not consulted; all follow Frost's stratification with minor relabeling.
  Add one as case-study if concrete role-naming conventions become
  load-bearing.
- **Conway's Law** — the proposition that system structure reflects the
  communicating structures that produced it. Not yet consulted but relevant
  to why a skill's `artifact/` reflects the skill's own ownership structure.
- **Cost of abstraction** — Graham's and Norvig's critique of GoF (patterns
  indicate missing language features) is noted in the GoF source but not
  developed. Relevant to when a part *should not* be introduced. Candidate
  for a follow-up pass.
- **How to measure artifact-base health** — the definition names per-part
  quality criteria but does not specify vocabulary-level metrics (coverage,
  reuse rate, deprecation ratio, cross-skill promotion frequency).
  Candidate follow-up once enough parts exist.
