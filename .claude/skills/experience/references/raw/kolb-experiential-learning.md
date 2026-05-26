# Kolb — Experiential Learning Cycle

**Source:** Kolb, D. A. (1984). *Experiential Learning: Experience as the Source of Learning and Development.* Englewood Cliffs, NJ: Prentice Hall. Exposition via McLeod, S. (Simply Psychology) summary of Kolb (1984).

**URL (consulted):** https://www.simplypsychology.org/learning-kolb.html

**Why this source belongs in `experience-base/knowledge/raw/`:** Kolb formalises *how* experience turns into knowledge. His four-stage cycle (do → reflect → conceptualise → test) is the canonical procedural model for extracting transferable rules from a concrete incident — exactly the operation an AI agent performs when it converts a session into an experience entry. Pairs with Argyris & Schön (which asks *what* the learning is) by answering *what the workflow of extraction looks like*.

---

## 1. Definition of learning

> "Learning is the process whereby knowledge is created through the transformation of experience." (Kolb 1984, p. 38)

> "Knowledge results from the combination of grasping and transforming experience." (Kolb 1984, p. 41)

Knowledge is *not* transferred or absorbed. It is *constructed* by working on experience.

## 2. The four-stage cycle

Kolb models learning as a continuous cycle of four modes. All four are needed for robust learning; a learner may enter at any point.

**1. Concrete Experience (CE)** — the learner encounters a tangible situation (novel or reinterpreted). Hands-on engagement. The raw input.

**2. Reflective Observation (RO)** — the learner examines what occurred against existing knowledge. "Inconsistencies between experience and prior understanding prove particularly important during this reflective phase." Dissonance is the signal.

**3. Abstract Conceptualisation (AC)** — through reflection, the learner forms new ideas or modifies existing concepts. Mental models are revised. This is the step that produces the transferable artefact.

**4. Active Experimentation (AE)** — the learner applies the new concept in real or simulated settings, testing it and generating fresh experience. This closes the loop and restarts it.

> "Effective learning is seen when a person progresses through a cycle of four stages."

No single stage suffices. Skipping RO gives unreflective action; skipping AC gives reflection without codification; skipping AE leaves concepts untested.

## 3. Two dimensions, four learning styles

Kolb arranges the four modes on two intersecting axes:

- **Processing continuum (how we approach tasks):** Active Experimentation (doing) ↔ Reflective Observation (watching).
- **Perception continuum (how we grasp information):** Concrete Experience (feeling) ↔ Abstract Conceptualisation (thinking).

The four quadrant combinations yield four learning styles:

| Style | Combination | Preference |
|---|---|---|
| **Diverging** | CE + RO | Feel & watch — multi-perspective, imaginative, idea generation |
| **Assimilating** | AC + RO | Think & watch — logical, concise, concepts over people |
| **Converging** | AC + AE | Think & do — practical problem-solving, technical application |
| **Accommodating** | CE + AE | Feel & do — intuition and hands-on over analysis |

The styles describe preferred entry points and dominant modes; they do *not* exempt a learner from completing the cycle.

## 4. Intellectual lineage

- **Kurt Lewin** — action-reflection cycle in social psychology; Kolb's cyclical structure descends directly from Lewin's feedback-loop model of experiential learning.
- **John Dewey** — education as a dialectic of *doing* and *thinking*; experience is the substrate of learning.
- **Jean Piaget** — constructivism: learners actively build understanding through assimilation and accommodation of experience.

Kolb's synthesis: learning is the *dialectic between doing and thinking,* grounded in experience.

## 5. Implications for an AI agent's experience base

1. **Every entry must traverse all four stages.** A log that records only what happened (CE) is not an experience entry — it is a diary. A usable experience entry must go further: reflect against prior expectations (RO), crystallise a revised rule or pattern (AC), and specify how the rule will be tested in future work (AE). If any stage is missing, the entry is incomplete.

2. **Dissonance is the trigger.** Kolb's RO stage specifically flags *inconsistencies* between expectation and outcome as the most learning-rich signal. An AI experience base should preferentially capture incidents where the model's prior expectation diverged from the actual result — those are the entries that change theory-in-use.

3. **Conceptualisation must produce a transferable artefact.** AC is where a single incident becomes a rule, template, or heuristic usable in a different context. An entry stuck at RO ("I reflected and it felt off") has no downstream value. The AC output is what gets promoted into standards, skills, or patterns.

4. **Close the loop.** AE says: a lesson is not trusted until re-used. Experience entries should therefore record *when and how the conceptualisation was tested afterwards,* with a later annotation confirming or revising the rule. Without AE, the experience base silently accumulates untested theories.

## Verbatim anchors

- "Learning is the process whereby knowledge is created through the transformation of experience." (1984, p. 38)
- "Knowledge results from the combination of grasping and transforming experience." (1984, p. 41)
- "Effective learning is seen when a person progresses through a cycle of four stages." (Simply Psychology summary)
