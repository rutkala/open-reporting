# Frost — Atomic Design (2016)

**Source:** Frost, B. (2016). *Atomic Design.* Self-published (Brad Frost Web). Available online at https://atomicdesign.bradfrost.com/.

**URL (consulted):** https://atomicdesign.bradfrost.com/chapter-2/ (Chapter 2 — Atomic Design Methodology).

**Why this source belongs in `artifact-base/knowledge/raw/`:** Frost provides the most concrete, modern, widely-adopted formulation of a **scale hierarchy** for a reusable-parts vocabulary. Where Alexander gave us the pattern, GoF gave us the catalogue form, and Evans gave us the language discipline, Frost gives us the **granularity stratification** — Atoms → Molecules → Organisms → Templates → Pages — that makes a design system legible and composable. Every contemporary design system (Material, Polaris, Carbon, Lightning) uses a near-identical stratification. For an AI skill's `artifact/`, this is the practical model for *how many levels* the vocabulary should have and *what each level names*.

---

## 1. Why chemistry

Frost surveyed other fields — industrial design, architecture (Alexander) — and settled on chemistry because it provides a **natural hierarchy with universal vocabulary**:

> "Atomic elements combine together to form molecules. These molecules can combine further to form relatively complex organisms."

The point is not that UI literally is chemistry. The point is that the stratification — *smallest self-contained unit → combinations → complex functional units → layout frames → filled instances* — is a shape that lets designers talk about a design system without ambiguity of scale.

## 2. The five stages

### 2.1 Atoms

> "Atoms are the foundational building blocks … basic HTML elements like form labels, inputs, and buttons that can't be broken down further without ceasing to be functional."

Key tests for an atom:

- Self-contained — functions on its own.
- Irreducible — breaking it further destroys its function.
- Has properties that influence downstream use.

### 2.2 Molecules

> "Molecules are relatively simple UI components formed when atoms bond together."

Canonical example: label + input + button = search form.

A molecule has **purpose** — a single job it does. It is the smallest unit that a designer talks about in task-oriented language ("the search form") rather than element-oriented language ("the input").

### 2.3 Organisms

> "Organisms are more complex components built from molecules and atoms."

Example: a header with logo + navigation + search form. An organism is a distinct section of an interface — a recognisable functional unit with enough structure that it stands as a complete part of the layout on its own.

### 2.4 Templates

> "Templates place components into layouts while articulating underlying content structure."

Templates drop the chemistry metaphor deliberately (to stay legible to non-technical stakeholders). A template is the **skeleton** — image sizes, character lengths, placement relationships — *without* real content. It emphasises structure over content.

### 2.5 Pages

> "Pages are concrete instances where real representative content replaces placeholders."

Pages bring the system to life. They test whether the underlying patterns survive real variation — actual headline lengths, real data, permission variations, edge cases.

## 3. Not linear — cyclical

Frost is explicit:

> "Atomic design is emphatically not a linear process, but rather a mental model to help us think of our user interfaces as both a cohesive whole and a collection of parts at the same time."

Designers should **not** build all atoms first, then all molecules, then all organisms. They should work across scales concurrently, zooming in and out — refining an atom when designing a page, or promoting a one-off detail to a reusable molecule when the pattern recurs.

For an AI skill's `artifact/`: the vocabulary is not built bottom-up in one pass. Parts are discovered and promoted as assemblies reveal recurrence. Build is cyclical; the hierarchy is a *lens*, not a *pipeline*.

## 4. Templates vs Pages — structure vs content

The separation is the load-bearing one for systems thinking:

> "Content needs to be structured and structuring alters your content."

The template defines the structure the design system supports; the page instantiates it with real content and surfaces where the structure fails. A template with pretty placeholder text and a page with a 200-character real headline can show the design to be broken in ways no atom-level review would catch.

For AI skills: this is the `artifact/`-vs-assembly distinction. The `artifact/` defines structures (parts and templates); assemblies in `products/` instantiate them with real data and surface real-world breakages.

## 5. Systems, not pages

Frost's deeper agenda is a shift in orientation:

> "Build systems, not pages."

One-off pages solve one-off problems. A system solves the recurring problem of how a family of pages should look, work, and evolve. The atomic stratification is the discipline that makes a system possible — otherwise designers default to building individual pages and calling the accumulation "a design system."

## 6. Adaptability

Frost emphasises the methodology is **not rigid**. GE Design renamed the stages ("Principles, Basics, Components, Templates, Features, Applications"). Any taxonomy that:

- has a clear hierarchy,
- stratifies by composition scale,
- distinguishes structure from content,
- enables teams to talk precisely about where a thing lives,

qualifies. The names matter less than the discipline.

## 7. Implications for an AI skill's artifact vocabulary

1. **Stratify by scale.** Parts exist at multiple granularities. Flattening them into "components/" loses information. A skill's `artifact/` benefits from at least three levels — atom / molecule / organism analogue — even if it does not reach five.

2. **Atoms are irreducible.** A part is an atom only if breaking it further destroys function. Do not decompose for decomposition's sake.

3. **Molecules carry purpose.** The lowest level at which the vocabulary names a *task* is the molecule level. Below that, parts are substrates; at that level, they become named affordances.

4. **Templates separate structure from content.** Parts that define the shape of a composition without committing to specific content are valuable in themselves. They are the reusable layout contracts.

5. **Pages / assemblies are where the vocabulary meets reality.** A vocabulary that has never been used in a real assembly is a hypothesis. Only instantiation reveals whether the parts actually compose.

6. **Cyclical, not linear.** Do not build the whole vocabulary upfront. Let recurrence in assemblies pull parts into the vocabulary. Promote when the same shape has been assembled more than once.

7. **Name the levels.** The skill's `artifact/` declares its stratification — chosen names (atom/molecule/organism, or a domain analogue) — so every part knows its rank and how it composes.

## Verbatim anchors

- "Atoms are the foundational building blocks … basic HTML elements … that can't be broken down further without ceasing to be functional."
- "Molecules are relatively simple UI components formed when atoms bond together."
- "Organisms are relatively complex components that form discrete sections of an interface."
- Templates "articulate the design's underlying content structure."
- Pages are "concrete instances" that test the system against real content.
- "Atomic design is not a linear process, but rather a mental model to help us think of our user interfaces as both a cohesive whole and a collection of parts at the same time."
- "Build systems, not pages."
