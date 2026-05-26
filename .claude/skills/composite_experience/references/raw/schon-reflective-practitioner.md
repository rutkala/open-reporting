# Schön — The Reflective Practitioner (1983)

**Source:** Schön, D. A. (1983). *The Reflective Practitioner: How Professionals Think in Action.* New York: Basic Books. ISBN 0-465-06878-2. Consulted via Saffer's summary notes on Schön (1983).

**URL (consulted):** https://odannyboy.medium.com/notes-on-donald-sh%C3%B6ns-the-reflective-practitioner-e67f753879d8

**Why this source belongs in `experience-base/knowledge/raw/`:** Schön provides the missing piece between "accumulated experience" and "applicable judgement." Where Kolb describes a deliberate *post-hoc* cycle and AAR describes a *post-event* ritual, Schön describes the *in-flight* thinking an expert does while the situation is still unfolding — *reflection-in-action*. For an AI agent that must often adjust approach mid-session, this is the theoretical frame for that mid-flight correction. Also contains the sharpest critique of the "theory → practice → result" pipeline that an AI could otherwise default to (Schön's *Technical Rationality*).

---

## 1. Knowing-in-action vs knowledge-in-action

Schön distinguishes:

- **Knowing-in-action** — the tacit, intuitive, spontaneous know-how that enables skilful performance. Pattern recognition, judgement, execution, all happening without conscious deliberation. This is the working layer of an experienced practitioner.
- **Knowledge-in-action** — the attempt to *describe* knowing-in-action in propositional form. A theory about what the practitioner does.

Most professional work operates at the tacit layer until routine is disrupted.

## 2. Reflection-in-action

The core Schönian move. Thinking about what one is doing *while doing it*.

> "When the phenomenon at hand eludes the normal categories of knowledge-in-practice, presenting itself as unique or unstable, the practitioner may surface and criticize his initial understanding of the phenomenon, construct a new description of it, and test the new description by an on-the-spot experiment." (Schön 1983)

The practitioner conducts a "reflective conversation with the situation": they make a move, observe how the situation responds ("talks back"), and adjust. Actor and observer simultaneously. This is what distinguishes experts from novices — experts reformulate their frame in real time without pausing work.

## 3. Reflection-on-action

Retrospective thinking *after* practice concludes. Analyse what happened, why it succeeded or failed, what principles governed the decisions. Reflection-on-action then updates future knowing-in-action.

Schön's two concepts map cleanly to two loci in an experience base:

- **Reflection-in-action** → session-local correction; the agent changes course mid-task because something surprised it.
- **Reflection-on-action** → the post-session experience entry; a durable artefact capturing what was learned.

## 4. Surprise as the trigger

Reflection is not continuous. It is triggered by **surprise** — a unique case, an unstable situation, a conflict of values, or an outcome that contradicts expectation. Without surprise, knowing-in-action carries on autopilot.

Schön's signature phrase: practitioners deal with "complexity, uncertainty, instability, uniqueness, and value conflict" — the messy, ill-framed part of professional life that routine methods cannot resolve.

## 5. Critique of Technical Rationality

Schön explicitly rejects the model where scientific theory is developed abstractly and then *applied* to specific problems to yield unambiguous results. Technical Rationality assumes:

- the problem is given,
- the relevant theory is settled,
- application is mechanical.

In real professional practice (design, medicine, urban planning, teaching, engineering debugging), none of these hold. Problems are not pre-defined; they must be *constructed* through **problem setting** — deciding what decisions matter, what ends to pursue, which means fit. *Framing* the problem is itself the hard part; the "technical solution" is trivial once the frame is right.

> "Increasingly we have become aware of the importance to professional practice of phenomena … which do not fit the model of Technical Rationality." (Schön 1983)

## 6. Handling uncertainty, uniqueness, and value conflict

Reflective practitioners do not seek universal solutions. They employ **iterative experimentation**:

- reframe the situation,
- make a move (a "chess-like" action),
- observe how the situation talks back,
- revise the frame,
- try again.

Criteria for a good frame: solves the problem as set, yields satisfactory outcomes, is coherent, aligns with fundamental values, sustains ongoing inquiry.

Competing schools of thought legitimately offer different frames. Schön advocates **frame analysis** — conscious awareness that the practitioner actively *constructs* their reality of the problem, and can shift frames deliberately.

## 7. Implications for an AI agent's experience base

1. **The experience base must cover both layers.** Reflection-on-action is the written entry. Reflection-in-action is harder: it is the ability to recognise mid-task that the current frame is wrong. The experience base supports the latter by being retrievable *during* work, not only after it — entries must be indexable by trigger conditions ("this looks like X" → recall the prior X episode), not only by topic.

2. **Surprise is the capture signal.** An entry worth writing is one where expectation diverged from outcome. The schema should make the *prior expectation* explicit so that the surprise is legible — otherwise the entry reads as simple narration.

3. **"Problem setting" is first-class.** An experience entry should capture *how the problem was framed*, not only how it was solved. Schön's core insight is that the frame, not the technique, determines the outcome. The experience base becomes a library of good and bad frames applied to recurring situation types.

4. **Avoid the Technical-Rationality trap.** The temptation is to treat knowledge as self-executing: "the standard says X, therefore do X." Schön insists that in genuine practice, the standard must first be *interpreted for this situation*. The experience base must record when a standard was bent, overridden, or reframed — those entries are more valuable than entries where the standard applied cleanly.

5. **Frames are plural.** An entry that presents its conclusion as the single correct interpretation is suspect. Useful entries preserve competing frames considered and the reason for the chosen one — so a future reader (human or model) can re-evaluate under a different frame if the situation warrants.

## Verbatim anchors

- "Knowing-in-action" — the tacit, spontaneous know-how of skilled practice.
- "When the phenomenon at hand eludes the normal categories of knowledge-in-practice, presenting itself as unique or unstable, the practitioner may surface and criticize his initial understanding of the phenomenon, construct a new description of it, and test the new description by an on-the-spot experiment." (Schön 1983)
- Professional practice deals with "complexity, uncertainty, instability, uniqueness, and value conflict."
- "Increasingly we have become aware of the importance to professional practice of phenomena … which do not fit the model of Technical Rationality." (Schön 1983)
