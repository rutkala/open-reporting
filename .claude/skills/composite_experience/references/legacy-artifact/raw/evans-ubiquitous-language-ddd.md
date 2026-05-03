# Evans — Domain-Driven Design: Ubiquitous Language and Bounded Context (2003)

**Source:** Evans, E. (2003). *Domain-Driven Design: Tackling Complexity in the Heart of Software.* Reading, MA: Addison-Wesley. ISBN 0-321-12521-5. Consulted via Wikipedia canonical summary and Evans's own *DDD Reference* (2015) where accessible.

**URL (consulted):** https://en.wikipedia.org/wiki/Domain-driven_design

**Why this source belongs in `artifact-base/knowledge/raw/`:** Simon, Parnas, Alexander, and GoF tell us *what* a reusable part is and *how to carve* the vocabulary. Evans adds the load-bearing constraint that the vocabulary must be **linguistically disciplined within a bounded context**. An `artifact/` bucket is not just a collection of parts — it is a *ubiquitous language* local to a skill. Evans also provides the *building-block taxonomy* (Entity / Value Object / Aggregate / Service / Factory / Repository) which is a direct analogue for typing the kinds of reusable parts a skill produces, and the *anti-corruption layer* idea which explains how one skill's vocabulary interfaces with another's without contamination.

---

## 1. Ubiquitous Language

Evans's central insistence: domain experts, users, and developers must share one vocabulary, and that vocabulary must live *inside* the code — class names, method names, module names.

> The structure and language of code must match the business domain according to input from domain experts.

Naming is not decoration. If the class is called `LoanApp` but the expert says *loan application*, the mismatch will silently drift into miscommunication and bugs. In a ubiquitous-language regime, the source code reads back to the domain expert as the domain expert speaks.

For a skill's `artifact/`: the names of parts are the language the skill speaks. A skill whose parts are named `Helper3`, `CommonWidget`, `GenericThing` has no language; it has noise. A skill whose parts are named after the *concepts of its domain* ("kpi_card", "time_series_panel", "comparative_bar") is speaking.

## 2. Bounded Context

> A bounded context is "a specific area within which a domain model is consistent and valid."

Evans rejects the fantasy of a single unified model covering the whole organisation. Instead: split the system into **bounded contexts**, each with its own internal ubiquitous language. Inside a context, every term has one meaning; across contexts, the same term may mean different things, and that is fine as long as the translation happens explicitly at the boundary.

For the skills framework: **each skill is a bounded context.** The `dashboard` skill's meaning of "card" is different from the `semantic-model` skill's meaning of "entity." Pretending the vocabulary crosses skill boundaries unchanged creates semantic collisions.

## 3. Domain Model as shared artefact

The domain model — the *thing* that captures the agreed terms, their relationships, and the rules — is the collaborative output between domain experts and developers. It is the artefact that both can point at. Evans insists this is not separate from the code; the code embodies the model.

In our three-layer skill shape, `artifact/` serves this role: the skill's model, expressed as a vocabulary of reusable parts, shared with everything downstream.

## 4. Tactical building blocks

Evans identifies named kinds of model element. Each is a *type* of part. Summary:

| Building block | Definition |
|---|---|
| **Entity** | Object defined by **identity**, not attributes. Same attributes, different IDs = different things (e.g., airline seat #14A). |
| **Value Object** | Immutable object defined by its **attributes**, no identity. Interchangeable if attributes match (e.g., a date, a money amount). |
| **Aggregate** | Cluster of Entities and Value Objects treated as a consistency unit. Has an **aggregate root** — the only object outsiders may reference. |
| **Service** | Operation that doesn't naturally belong to any single object. Stateless. Models verbs of the domain. |
| **Factory** | Encapsulates complex construction of domain objects. |
| **Repository** | Provides retrieval/storage of domain objects, abstracting the persistence mechanism. |

Not every skill needs all six. But a skill's `artifact/` benefits from *some* typology: naming the *kinds* of part, not only the parts. Flat vocabularies where every part is just "a component" lose the structural discrimination that Evans shows is load-bearing.

## 5. Anti-Corruption Layer

When two bounded contexts must interoperate, Evans introduces an **anti-corruption layer** — an isolation boundary that translates the upstream context's model into the downstream context's own terms.

> The anti-corruption layer "provides your system with functionality of the upstream system in terms of your own domain model."

Without this layer, an external system's vocabulary leaks in and pollutes the local ubiquitous language. Legacy systems and third-party APIs are the typical cases.

For skills: when one skill consumes another skill's artefacts (e.g., the `dashboard` skill using the `semantic-model` skill's outputs), a translation layer should sit at the boundary. The downstream skill never adopts the upstream skill's vocabulary wholesale; it re-expresses in its own terms.

## 6. Strategic vs Tactical DDD

- **Strategic DDD** — macro concerns: context mapping, relationships between bounded contexts, shared kernels, published languages, separate ways.
- **Tactical DDD** — micro concerns: the building blocks inside one context.

For skills: *strategic* concerns live at the portfolio level — how `knowledge-base`, `experience-base`, and `artifact-base` relate; how `dashboard` integrates with `semantic-model`. *Tactical* concerns live inside each skill's `artifact/` — the kinds and instances of parts.

## 7. Implications for an AI skill's artifact vocabulary

1. **Name parts in the domain's words.** The part name is the language. Generic names ("util", "helper", "common") are refusals to name the domain and are a failure of ubiquitous language.

2. **Each skill is a bounded context.** Do not cross vocabulary silently. A term that appears in two skills must mean the same thing in both, or be renamed in at least one.

3. **Type the parts.** Borrow Evans's building-block typology (Entity / Value Object / Aggregate / Service / Factory / Repository) or define an analogue per skill. A flat "everything is a component" vocabulary loses structural discrimination.

4. **Maintain an anti-corruption layer at skill boundaries.** When skill A consumes artefacts from skill B, translate at the boundary. Do not adopt B's vocabulary inside A.

5. **The vocabulary is the shared artefact between experts and builders.** For AI skills, the "expert" is the PO / analyst; the "builder" is the skill + model. The parts must read back to the PO as the domain reads to them.

6. **Strategic vs tactical clarity.** The global skill catalogue is a context map; each skill's `artifact/` is a tactical vocabulary. Keep the two levels distinct.

## Verbatim anchors

- A bounded context is "a specific area within which a domain model is consistent and valid."
- The anti-corruption layer "provides your system with functionality of the upstream system in terms of your own domain model."
- DDD "focuses on: the core domain; creative collaboration between domain practitioners and software practitioners; speaking a ubiquitous language within an explicitly bounded context."
- Building blocks: **Entity, Value Object, Aggregate, Service, Factory, Repository.**
