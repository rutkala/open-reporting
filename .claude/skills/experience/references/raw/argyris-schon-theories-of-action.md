# Argyris & Schön — Theories of Action, Single-Loop / Double-Loop Learning

**Source:** Argyris, C., & Schön, D. A. (1978). *Organizational Learning: A Theory of Action Perspective.* Reading, MA: Addison-Wesley. Synthesis and quotations via Smith, M. K. (infed.org) secondary exposition of Argyris & Schön (1974, 1978, 1996).

**URL (consulted):** https://infed.org/dir/welcome/chris-argyris-theories-of-action-double-loop-learning-and-organizational-learning/

**Why this source belongs in `experience-base/knowledge/raw/`:** Argyris & Schön's distinction between *espoused theory* (what people say they do) and *theory-in-use* (what they actually do), and between single-loop and double-loop learning, is the canonical framework for turning experience into revised action. It is the theoretical backbone for why an AI agent's experience base must capture not only what was done, but whether the underlying governing variables themselves should change.

---

## 1. Theories of action: espoused theory vs theory-in-use

Argyris & Schön argue that every actor operates from two distinct theories:

- **Espoused theory** — the explanations people give when asked how they act: the theory they consciously endorse.
- **Theory-in-use** — the implicit mental map that actually governs behaviour.

> "When someone is asked how he would behave under certain circumstances, the answer he usually gives is his espoused theory of action for that situation … However, the theory that actually governs his actions is this theory-in-use."

Theory-in-use is inferred from three observable elements of any action:

1. **Governing variables** — dimensions the actor tries to keep within acceptable limits.
2. **Action strategies** — moves used to keep those variables in range.
3. **Consequences** — intended and unintended results of the strategies.

Effectiveness emerges only when espoused theory and theory-in-use are congruent.

## 2. Model I and Model II

**Model I** is the default theory-in-use most people exhibit under problematic conditions. Its governing values:

- Achieve the purpose as defined by the actor
- Win, do not lose
- Suppress negative feelings
- Emphasise rationality

Model I produces unilateral control, defensive relationships, limited information validity, and little public testing of ideas. It *inhibits* genuine learning.

**Model II** is an alternative orientation emphasising:

- Valid information
- Free and informed choice
- Internal commitment
- Public testing of evaluations, illustrated with directly observable data
- Minimally defensive relationships

Most people *espouse* Model II values when asked, yet *operate* predominantly from Model I. Closing this gap is itself a learning task.

## 3. Single-loop and double-loop learning

Learning, for Argyris & Schön, begins with the **detection and correction of error** (1978: 2). Two response modes:

**Single-loop learning** — error is detected and corrected in ways that let the organisation carry on its present policies or achieve its present objectives. Governing variables stay fixed; only action strategies change. Analogy: a thermostat adjusting to restore a set temperature.

**Double-loop learning** — "error detected and corrected in ways that involve the modification of an organisation's underlying norms, policies and objectives." Governing variables themselves are questioned and possibly restructured.

Single-loop learning ≈ *efficiency within a frame.*
Double-loop learning ≈ *questioning the frame.*

Double-loop learning becomes increasingly necessary as environments grow more uncertain and complex — yet Model I reasoning patterns systematically suppress it.

## 4. From individual to organisational learning

Learning becomes *organisational* only when encoded beyond a single head. Argyris & Schön introduce **organisational maps** — "shared descriptions of the organisation which individuals jointly construct and use to guide their own inquiry." These maps are the organisation's memory and constitute its collective theory-in-use.

> "For organizational learning to occur, learning agents' discoveries, inventions, and evaluations must be embedded in organizational memory." (1978: 19)

> "If it is not encoded in the images that individuals have, and the maps they construct with others, then 'the individual will have learned but the organization will not have done so.'"

When members operate from Model I, they create **Organisational I (O-I)** systems — self-fulfilling, self-reinforcing, escalating-error feedback loops that protect existing assumptions.

The rarer **Organisational II (O-II)** system enables collective double-loop learning through shared Model II practices: participation, public testing, honest inquiry.

## 5. Implications for an AI agent's experience base

1. **Capture both theories.** An experience log must record not just the espoused rationale ("I chose X because Y") but also the inferred theory-in-use (what the actual action + consequence pattern reveals).
2. **Distinguish loop levels.** Each entry should note whether the lesson is a single-loop correction (adjust strategy, keep goal) or a double-loop revision (governing value itself was wrong).
3. **Externalise for organisational memory.** A lesson held only in a single model's working context is not organisational learning. It must be crystallised into a durable, shared artefact (standards, skills, patterns) — the AI equivalent of an organisational map.
4. **Guard against Model I defaults.** Model I's "win, don't lose, save face" pattern has an AI analogue: confirmation bias toward the chosen approach, post-hoc rationalisation of outcomes, suppression of disconfirming evidence. An experience base worth trusting must structurally resist this — by requiring disconfirmable tests, explicit surfacing of conflicting evidence, and a place for failure data that is not rhetorically softened.

## Verbatim anchors

- "learning involves the detection and correction of error" (Argyris & Schön 1978: 2)
- "learning agents' discoveries, inventions, and evaluations must be embedded in organizational memory" (1978: 19)
- Single-loop: error corrected so "the organization [can] carry on its present policies or achieve its present objectives."
- Double-loop: error corrected "in ways that involve the modification of an organization's underlying norms, policies and objectives."
