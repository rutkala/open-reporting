# Parnas — On the Criteria To Be Used in Decomposing Systems into Modules (1972)

**Source:** Parnas, D. L. (1972). "On the Criteria To Be Used in Decomposing Systems into Modules." *Communications of the ACM,* 15(12), 1053–1058.

**URL (consulted):** https://wstomv.win.tue.nl/edu/2ip30/references/criteria_for_modularization.pdf (stable re-host of the CACM paper).

**Why this source belongs in `artifact-base/knowledge/raw/`:** Parnas provides the operational criterion for *how to carve up a reusable vocabulary*. Given Simon's definition of an artifact as an interface, Parnas tells us *where the interface line should go*: around the design decisions most likely to change. This is the most cited operational rule in modular design, and it directly answers the question every skill's `artifact/` bucket must answer: "what is a part, and why this part and not a different partition?"

---

## 1. The two decomposition strategies

Parnas contrasts two ways of splitting a system into modules:

- **Modularisation 1 — flowchart-based.** Each module is a step in the processing sequence: input, parse, sort, format, output. The decomposition mirrors the path of data through the program.
- **Modularisation 2 — information-hiding.** Each module is built around a **design decision likely to change**. Internals are hidden behind a stable interface.

Parnas argues Modularisation 1 looks natural but produces brittle systems: when a design decision changes (e.g., storage format, algorithm, representation), multiple flowchart modules must all be touched because the decision leaks across their boundaries.

## 2. The core rule

> Each module should be characterised by "its knowledge of a design decision which it hides from all others … its interface or definition chosen to reveal as little as possible about its inner workings."

Operational form: **decompose around design decisions that are likely to change.** Each module owns one such decision. Everything else sees only the interface, never the decision.

This inverts the intuitive order. The question is not "what are the steps of the computation?" but "what are the hard, changeable decisions, and how do I make each one invisible to the rest?"

## 3. Module as *work assignment*

Parnas's definition is operational, not just structural:

> A module is "a work assignment."

A module is a unit of *responsibility* — assigned to a programmer or team. This reframe means the decomposition criterion is also a project-management criterion: a well-decomposed system is one where a change request maps to *one* work assignment, which maps to *one* team, which owns *one* hidden decision.

The implication for our skills: an `artifact/` part is not just a file — it is a unit of ownership. One part, one concern, one place to change it when the concern changes.

## 4. Three benefits claimed

1. **Managerial** — teams work independently because stable interfaces let work parallelise without coordination overhead.
2. **Product flexibility** — when requirements shift, changes localise inside the module that owns the affected decision; cascading edits across many modules disappear.
3. **Comprehensibility** — a developer need not understand the whole system. Understanding an interface plus the local implementation is enough.

These benefits compound with each other: parallel work, local change, and bounded comprehension all reinforce each other. A system that gives up on information hiding typically loses all three at once.

## 5. Why "hidden decision" beats "processing step"

A processing-step module exposes implementation details across boundaries — the next step needs to know the format produced by the previous one. A hidden-decision module exposes only the interface; the decision that backs it can change without ripple.

Stable design philosophies outlast specific requirements. Organising around decisions-likely-to-change is therefore more resilient than organising around the current processing flow.

## 6. The KWIC index example

Parnas's running example is a Key-Word-In-Context index:

- **Modularisation 1** splits by data journey: input, parse, store, sort, format, output.
- **Modularisation 2** splits by hidden decisions: one module owns the *storage representation,* another owns the *ordering algorithm,* another owns *input format,* another owns *output format.*

When the storage representation changes, only one module is touched. Under Modularisation 1, everything downstream of storage would need to change.

## 7. Implications for an AI skill's artifact vocabulary

1. **Carve the vocabulary around decisions likely to change, not around "steps."** A skill's `artifact/` should enumerate the *hard, mutable choices* the skill has had to make — theme, layout algorithm, semantic-model binding, error-handling policy, locale strategy — and give each its own part.

2. **Each part owns exactly one decision.** A part that owns two decisions (e.g., "colour palette AND chart-type mapping") will decompose badly on first change. Split it early.

3. **Interfaces reveal as little as possible.** The part's public surface should be the narrowest shape that lets it be assembled — not its implementation, not its internal options, not its rationale. Rationale goes in docs, not in the interface.

4. **A part is a work assignment.** When you ask "who owns this part," the answer must be one person (or one sub-skill). If ownership is diffused, the part is wrong.

5. **Changeability is the quality bar.** When a decision changes, ideally *one file* changes. If a change ripples across multiple parts, the decomposition has leaked.

6. **Stable interface, flexible interior.** Parts can be rewritten internally at any time. Their interface is a promise; breaking it breaks assemblies. Version the interface if it must evolve.

## Verbatim anchors

- Every module is characterised by "its knowledge of a design decision which it hides from all others, with its interface or definition chosen to reveal as little as possible about its inner workings."
- A module is "a work assignment."
- Decompose by "design decisions that are likely to change." (p. 1053)
- "One can make the change by modifying only one module." (p. 1053)
