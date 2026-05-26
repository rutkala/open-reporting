# After-Action Review (AAR) — US Army Doctrine & Lineage

**Primary source:** US Army, *TC 25-20: A Leader's Guide to After-Action Reviews*, HQ Department of the Army, Washington DC, September 1993.

**Consulted exposition:** USAID, *After-Action Review Technical Guidance* (Feb 2006, PN-ADF-360), which formalises the four-question model from TC 25-20 for civilian use. URL: https://fs-prod-nwcg.s3.us-gov-west-1.amazonaws.com/s3fs-public/2023-06/usaid-aar-guide.pdf

**Why this source belongs in `experience-base/knowledge/raw/`:** AAR is the most battle-tested operational mechanism for converting a completed event into durable lessons. Where Kolb describes the *cognitive cycle* and Argyris & Schön describe the *theoretical distinctions*, TC 25-20 gives the *concrete ritual*: four questions, ground rules, roles, and feed-forward mechanism. It is the procedural anchor for how a session actually gets written into an experience entry.

---

## 1. Definition and core purpose

An After-Action Review is a structured, facilitated review conducted immediately after a significant event. Its explicit purpose is *organisational learning* — capturing insights while events are fresh and translating them into actionable improvements for future work.

TC 25-20 treats the AAR as a *professional discussion*, not a critique. The subject of scrutiny is the performance of the unit and its processes, not the reputation of individuals.

## 2. The four classic questions

The AAR is organised around four foundational questions (TC 25-20, 1993):

1. **What was supposed to happen?** — establishes the baseline: objectives, plan, success criteria.
2. **What actually happened?** — documents the real outcome, deviations, observable facts, without judgement.
3. **What went well and why?** — identifies successes and the contributing factors (decisions, dynamics, resources, context).
4. **What can be improved and how?** — produces specific, actionable recommendations — not blame.

This four-question frame forces balanced attention to both success and shortfall and keeps the conversation on observable facts and causal factors rather than personalities.

TC 25-20 expands this into a four-phase process:

- **Plan** the AAR (who, when, where, focus).
- **Prepare** (collect observations, rehearse facilitation, prime participants).
- **Conduct** the AAR (walk the four questions, discuss key issues).
- **Follow up** (integrate findings; this is the step most skipped in practice).

## 3. Formal vs informal AARs

- **Informal AAR** — short, often verbal, conducted at team level after routine activity. Low documentation overhead; relies heavily on facilitator skill. Good for quick-cycle learning inside an established team.
- **Formal AAR** — structured, documented, often includes cross-functional participants or outside observers. Used after complex operations, major project completions, or incidents with significant implications. Produces written records linked to organisational systems.

Both serve the same learning function; they differ in scope, stakeholder breadth, and documentation depth.

## 4. No-blame, no-rank ground rules

These are not etiquette — they are *functional requirements* of the method.

- **No-blame orientation:** focus is on systems, processes, and decisions, not individual fault. The question is "what factors led to this outcome," not "who is culpable."
- **No-rank principle:** hierarchy is suspended inside the AAR. Junior participants must be genuinely safe contradicting senior recollections. Facilitators actively solicit input from all levels and prevent high-rank voices from dominating conclusions.

Without both rules, discussion collapses into sanitised, politically safe narratives that hide the real performance drivers. Psychological safety is the load-bearing condition.

## 5. Capturing findings and feeding forward

AARs only create value when insights transition into *organisational memory* and change future practice. TC 25-20 and the USAID guide identify four mechanisms:

1. **Documentation standards** — consistent format: what worked, what didn't, specific recommendations with owners and timelines.
2. **Lessons-learned repositories** — collect AARs across units so patterns across incidents become visible (one team's bottleneck may be a systemic friction).
3. **Integration mechanisms** — findings must reach decision-makers responsible for training, process design, doctrine. Some organisations require operational leaders to formally respond to AAR recommendations, creating accountability.
4. **Knowledge transfer** — pass lessons to teams facing similar situations: new projects reference AARs from comparable work; onboarding surfaces recurring challenges.

The decisive phrase is **intent to change**. An AAR without a mechanism to modify future practice is documentation, not learning.

## 6. Implications for an AI agent's experience base

1. **Use the four-question skeleton as the entry template.** Each experience record should open with What was supposed to happen / What happened / What went well + why / What to improve + how. This is a proven structure for preventing a log that only records outcomes.

2. **Separate observation from interpretation.** TC 25-20's distinction between Q2 (facts) and Q3–4 (interpretation) maps directly to Kolb's CE → RO → AC progression. An entry that conflates them is both harder to revisit and harder to refute.

3. **Enforce no-blame framing even in a single-agent context.** The AI analogue of blame is confirmation bias and post-hoc rationalisation of the chosen path. The experience base's entry format should structurally make it easy to record disconfirming evidence and uncomfortable mistakes without softening.

4. **Feed-forward or it does not count.** Every experience entry must declare its downstream effect: which standard, skill, pattern, or future check it updates. An entry that ends at Q4 ("here is what I'd do differently") without feeding a change artefact is stuck at documentation.

5. **Distinguish informal from formal.** Not every session warrants a full formal entry. A lightweight in-session AAR can live in conversation memory; a formal one — after a complex product build, a failed deployment, or a recurring bug — should be crystallised into the experience base with full documentation discipline.

## Verbatim anchors (from TC 25-20 and USAID exposition)

- AAR is "a structured, facilitated process designed to help teams examine performance following significant events."
- Four questions: "What was supposed to happen? / What actually happened? / What went well and why? / What can be improved and how?"
- Four phases of conducting an AAR: **Plan → Prepare → Conduct → Follow up.**
- "No-blame" and "no-rank" ground rules are prerequisites for the honest participation that the method relies on.
- "An AAR without mechanisms to modify future practice becomes an exercise in documentation rather than learning."
