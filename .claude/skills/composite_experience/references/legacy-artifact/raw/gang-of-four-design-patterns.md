# Gamma, Helm, Johnson, Vlissides — Design Patterns (1994)

**Source:** Gamma, E., Helm, R., Johnson, R., & Vlissides, J. (1994). *Design Patterns: Elements of Reusable Object-Oriented Software.* Reading, MA: Addison-Wesley. ISBN 0-201-63361-2. Foreword by Grady Booch. Commonly known as "GoF." Consulted via Wikipedia canonical summary.

**URL (consulted):** https://en.wikipedia.org/wiki/Design_Patterns

**Why this source belongs in `artifact-base/knowledge/raw/`:** GoF is the translation of Alexander's pattern-language idea into software. It proves the form generalises from architecture into code, and it gives the four-element template (Name / Problem / Solution / Consequences) that every artifact entry can follow. Its two core principles — *program to an interface, not an implementation* and *favour composition over inheritance* — are the operational rules for how reusable parts in a skill's `artifact/` should be *usable* by assemblies without leaking internals. GoF also demonstrates the discipline of *cataloguing* patterns (23 named, categorised, cross-referenced) — the same discipline a skill's `artifact/` vocabulary should apply to itself.

---

## 1. The four essential elements of a pattern

Every GoF pattern is documented with:

1. **Pattern name** — a shared-vocabulary handle. Naming is how the pattern enters discourse.
2. **Problem** — the design situation in which the pattern applies; the recurring tension.
3. **Solution** — the arrangement of elements (classes, objects, relationships) that resolve the tension. Described abstractly, not as one instantiation.
4. **Consequences** — the results and trade-offs. What is gained, what is given up, what new constraints the pattern introduces.

The fourth element is the one often dropped by imitators and the one that matters most: every artifact imposes costs, and a pattern without its consequences field is a recommendation, not a pattern.

## 2. Three categories

GoF partitions 23 patterns into three functional groups:

- **Creational (5)** — object creation concerns: *Abstract Factory, Builder, Factory Method, Prototype, Singleton.*
- **Structural (7)** — composition of classes and objects into larger structures: *Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy.*
- **Behavioural (11)** — communication and responsibility distribution between objects: *Chain of Responsibility, Command, Interpreter, Iterator, Mediator, Memento, Observer, State, Strategy, Template Method, Visitor.*

The categorisation itself is a reusable artifact. For a skill's `artifact/`, the same discipline applies: parts should be grouped by concern axis — construction, composition, interaction — not dumped into one pile.

## 3. Two core design principles

GoF's two principles back the entire catalogue. These are the operational rules that make parts *composable*.

### 3.1 "Program to an interface, not an implementation."

Clients should depend on abstract interfaces, not on concrete classes. Consequences:

- the client works with any implementation that satisfies the interface,
- internal changes inside an implementation do not propagate to clients,
- polymorphism and dynamic binding become usable.

This is the same insight Parnas (1972) gave as *information hiding*, restated as a coding rule.

### 3.2 "Favour object composition over class inheritance."

Inheritance is **white-box reuse** — the subclass sees the parent's internals; changes to the parent ripple into subclasses; encapsulation is broken.

Composition is **black-box reuse** — composed objects expose only their interfaces; they can be swapped dynamically; internals stay hidden.

GoF's warning:

> Inheritance "breaks encapsulation" — subclass implementations become bound to parent implementations, forcing cascading changes.

Inheritance is still useful, but bounded: "works best when adding functionality to existing components while reusing most existing code." Outside that narrow case, compose.

For an AI skill's artifact vocabulary: parts relate by composition (one part *uses* another) far more than by inheritance (one part *specialises* another). A vocabulary dominated by "variant subclasses" is a vocabulary that will become brittle.

## 4. Debt to Alexander

GoF explicitly credits Christopher Alexander's *A Pattern Language* (1977) as the structural inspiration. The Alexandrian form (name / context / problem / solution / related) is preserved; the domain is reshaped from buildings to object-oriented software. This cross-domain survival is evidence that the pattern-language form is a real artefact, not an architectural idiosyncrasy — exactly why it belongs in the foundation of any `artifact/` bucket.

## 5. Parsimony warning

The authors caution:

> "Dynamic, highly parameterised software is harder to understand and build than more static software."

Patterns exist to control complexity, not multiply it. A pattern applied where a direct solution suffices is anti-economical. This is the GoF restatement of Simon's satisficing: enough structure to absorb change, not so much that the structure itself becomes the burden.

## 6. Later critiques

- **Paul Graham:** patterns indicate missing language abstractions — a language powerful enough would make the pattern invisible.
- **Peter Norvig:** 16 of the 23 patterns are simplified or dissolved by features in Lisp / Dylan.
- **The authors themselves (2005):** would refactor, add Dependency Injection and Null Object, possibly drop Singleton.

The lesson is not that GoF is wrong but that an artifact vocabulary is *language-relative*. What is a pattern in one technology may be a built-in primitive in another. A skill's `artifact/` must state its host environment, and reevaluate periodically as that environment evolves.

## 7. Implications for an AI skill's artifact vocabulary

1. **Every part has four elements: Name / Problem / Solution / Consequences.** The consequences field is mandatory, not optional. A part without consequences is marketing.

2. **Categorise by concern, not by file type.** GoF's three-way split (creational / structural / behavioural) is a worked example; each skill picks the axes that fit its vocabulary. Lumping everything into "components/" or "helpers/" is a failure mode.

3. **Parts expose interfaces, not implementations.** This is the Parnas rule made operational. Other parts (and external assemblies) depend only on the interface.

4. **Compose, don't inherit.** When a new part is "like an existing one but different," the default is composition. Inheritance is a narrow specialisation tool, not the default building block.

5. **Restraint.** Introduce a pattern only when the recurring problem warrants it. A direct solution that fits cleanly is better than a pattern applied to absorb hypothetical future change.

6. **Host environment explicit.** The vocabulary's parts are relative to a technology stack. State the host (Dash + Plotly, dbt, DuckDB, etc.) and revisit patterns when the host evolves.

## Verbatim anchors

- Four pattern elements: **Name, Problem, Solution, Consequences.**
- "Program to an interface, not an implementation."
- "Favour object composition over class inheritance."
- Inheritance "breaks encapsulation."
- "Dynamic, highly parameterised software is harder to understand and build than more static software."
