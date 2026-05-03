# Simon — The Sciences of the Artificial (1969)

**Source:** Simon, H. A. (1969, revised 1981, 1996). *The Sciences of the Artificial.* Cambridge, MA: MIT Press. Consulted via Davies' canonical summary of Simon 1969.

**URL (consulted):** http://www.jimdavies.org/summaries/simon1969-a.html

**Why this source belongs in `artifact-base/knowledge/raw/`:** Simon gives the load-bearing *definition* of an artifact that the rest of our framework depends on. An artifact is not merely a made thing — it is a **purposeful interface between an inner and an outer environment**. This single reframe forces every reusable part of a skill to be evaluated on *fit with its outer environment* (the contexts where it will be assembled), not only on internal elegance. It also provides the philosophical ground for the claim that `artifact/` is a distinct layer from `knowledge/` and `experience/`: artifacts live in the *normative* realm of "how things ought to be," not the *descriptive* realm of "how things are."

---

## 1. Primary definition: artifact as interface

Simon's signature reframe:

> "The real nature of the artifact is the interface."

An artifact is not the object per se. It is the **interface** between:

- an **inner environment** — the substance and organisation of the object itself (its mechanism), and
- an **outer environment** — the context in which it must operate (the demands, constraints, and goals it must satisfy).

The artifact's effectiveness depends on the **successful adaptation** of the two environments to one another. Good design is the matching of inner to outer; bad design is mismatch regardless of how elegant either side is in isolation.

For the experience-base/knowledge-base split we already have:

- `knowledge/` and `experience/` describe the *inner environment* of the skill — what it knows and what it has learned.
- `artifact/` describes the *interface* — the reusable parts whose shape must fit the outer environment where they will actually be used.

## 2. Four defining properties of artifacts

From Simon's characterisation:

1. **Synthesised, not naturally occurring** — artifacts are made.
2. **May imitate natural appearance** but remain fundamentally contingent on choice.
3. **Characterised in terms of functions, goals, and adaptation** — not by material, not by form alone.
4. **Discussion blends imperative and descriptive language** — "this *is* what it does" and "this is what it *should* do" are co-present.

The third point is the one most often missed by software developers: a component is fully specified only once its *function*, *goal*, and *adaptation* to the outer environment are stated.

## 3. Natural science vs science of the artificial

> "The science of the artificial is really the science (analytic or descriptive) of engineering (synthetic or prescriptive)."

- **Natural science** studies phenomena governed by necessity — how things *are*.
- **Science of the artificial** studies phenomena contingent on purpose — how things *ought* to be.

Engineering, medicine, business, architecture, and design are all concerned with the normative question. An artifact that cannot be evaluated *against the goal it was made for* has been stripped of the thing that makes it an artifact.

For our framework: every entry in `artifact/` must name the goal the part was designed for. "What is it?" is incomplete; "what is it *for*?" is mandatory.

## 4. Hierarchy and near-decomposability

Simon's Chapter 4 (often cited independently as "The Architecture of Complexity"):

> "Complexity takes the form of hierarchy."

Hierarchical systems evolve faster than non-hierarchical ones because "the many subsystems form as many intermediate stable stages in the process." Near-decomposability means subsystems exhibit short-term independence while remaining long-term interdependent in aggregate.

Implication for reusable parts:

- A well-formed artifact vocabulary is **near-decomposable** — parts compose without each one needing to know the internals of the others.
- The vocabulary naturally stratifies: low-level parts are reused by many higher-level parts; changes inside a low-level part do not cascade upward so long as the interface is preserved.
- This is the structural foundation for Brad Frost's *Atomic Design* (atoms → molecules → organisms → …), GoF design patterns, and Alexander's pattern language.

## 5. Bounded rationality and satisficing

Designers do not compute globally optimal artifacts — they *satisfice*. Near-decomposability is what makes this tractable: local optimisation of a subsystem yields a workable global solution without requiring full system information.

Implication for an AI skill building artifacts: the goal is not the theoretically perfect component. It is the component whose interface satisfies the goal in the outer environment *well enough*, at a composable boundary, with bounded internal complexity.

## 6. Simulation as design understanding

Simon treats **simulation** — running the interface against varying outer environments — as the method for predicting artifact behaviour and making tacit design knowledge explicit.

For us: an `artifact/` part is better-understood when it has been exercised in multiple assemblies, not only designed in isolation. "Use it in several skills before trusting it" is the Simon-derived discipline.

## 7. Implications for an AI skill's artifact vocabulary

1. **Every artifact must name its goal and its outer environment.** "What is it for" and "where does it live" are not optional metadata — they are constitutive of the artifact itself.
2. **Inner–outer fit is the quality criterion.** An internally elegant part that misfits its contexts is a worse artifact than an ugly one that fits.
3. **The vocabulary should be near-decomposable.** Parts should compose through interfaces, not through internal knowledge of each other. Changes inside one part should not propagate upward when the interface holds.
4. **Normative-descriptive hybrid is the native register.** Artifact documentation legitimately says both "this is what it does" and "this is what it ought to do." That is not sloppy — it reflects the thing's nature.
5. **Satisficing over perfection.** Parts are published when they meet the goal well enough at a composable boundary, not when theoretically optimal.
6. **Simulation validates the interface.** A part is not trusted until it has been used in more than one assembly. First use is a prototype; second and third uses make it an artifact.

## Verbatim anchors

- "The real nature of the artifact is the interface."
- Artifacts are "characterized in terms of functions, goals, adaptation."
- "The science of the artificial is really the science (analytic or descriptive) of engineering (synthetic or prescriptive)."
- "Complexity takes the form of hierarchy."
- Engineering, medicine, business, architecture, and painting are concerned with "how things ought to be."
