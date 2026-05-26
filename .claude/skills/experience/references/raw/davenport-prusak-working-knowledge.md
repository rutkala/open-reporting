# Davenport & Prusak — Working Knowledge (1998)

**Source:** Davenport, T. H., & Prusak, L. (1998). *Working Knowledge: How Organizations Manage What They Know.* Boston: Harvard Business School Press. ISBN 0-87584-655-6. Consulted via Mindtools exposition.

**URL (consulted):** https://www.mindtools.com/aq7u1c3/thomas-davenport-and-larry-prusak-working-knowledge

**Why this source belongs in `experience-base/knowledge/raw/`:** Davenport & Prusak are the canonical practitioner reference on how organisations *capture, codify, and circulate* knowledge — especially knowledge derived from experience. Their definition of knowledge as "a fluid mix of framed experience, values, contextual information, and expert insight" is the most-cited operational definition in KM literature. They also identify the specific failure modes (over-reliance on technology, tacit knowledge that won't codify, missing incentive structures) that an AI experience base must actively design against.

---

## 1. Definition of knowledge

Davenport & Prusak (1998) define knowledge as:

> "a fluid mix of framed experience, values, contextual information, and expert insight that provides a framework for evaluating and incorporating new experiences and information."

Knowledge:

- **originates and is applied in the minds of knowers**
- in organisations **becomes embedded not only in documents or repositories but also in routines, processes, practices, and norms**
- is **broader, deeper, and richer than data or information**

The crucial phrase for the experience base is "**framed experience**." Experience alone is raw; it becomes knowledge only once framed — interpreted, contextualised, and made applicable to new situations.

## 2. The data → information → knowledge hierarchy

Davenport & Prusak insist on the progression:

- **Data** — raw facts and observations.
- **Information** — data organised, processed, given context.
- **Knowledge** — requires human interpretation, judgement, and experience.

Their warning: organisations routinely confuse *information systems* with *knowledge management*, and treat documents-in-a-repository as if they were knowledge. This is a fundamental mistake that undermines KM initiatives.

## 3. Codification principles

Not all knowledge can be effectively codified. Their guidance:

- "At most, technology should take up one-third of all resources geared towards knowledge management."
- The other two-thirds belong to culture, roles, responsibilities, strategy, economics, and the knowledge content itself.

Four managerial questions for codification:
1. What business goals will the codified knowledge serve?
2. What forms does that knowledge currently take in the organisation?
3. Is this knowledge useful and appropriate to codify at all?
4. What medium fits both the knowledge and its intended distribution?

## 4. The knowledge-market metaphor

Davenport & Prusak treat internal knowledge flow as a *market* with givers, receivers, and brokers. Markets clear only when:

- people know where valuable knowledge lives,
- there is an incentive to share it,
- transaction cost is low enough that exchange actually happens.

The barrier is rarely lack of knowledge — it is mis-pricing and friction. Much "unshared" knowledge is simply not economically worth sharing under the existing incentive structure.

## 5. Tacit knowledge transfer

> "Informal networks are the most effective means of spreading knowledge."

Tacit knowledge — expertise embedded in people's minds — transfers primarily through human interaction and networks, not through document repositories. An assumption that tacit expertise can be fully dumped into a database is, per D&P, categorically wrong. The implication for AI is strong: tacit operator knowledge (what a senior developer actually does when a build fails) resists capture and must be deliberately elicited, not passively harvested.

## 6. Value of experience

Experience itself is a load-bearing organisational asset:

- Firms hire experienced individuals specifically because their knowledge is embedded in professional judgement.
- Microsoft (D&P's 1998 example) has a market value far exceeding its physical assets precisely because valuable knowledge resides in its workforce.
- Experience is not quickly replicated through training; it is accumulated over time and leaves the organisation when its bearer leaves.

## 7. Cultural requirements

- Hire people with "a predisposition toward intellectual curiosity."
- Foster cultures where knowledge sharing is valued.
- But **do not** try to retrofit culture to support a KM initiative — "changing the culture for the purposes of knowledge management would be like the tail wagging the dog."

## 8. Implications for an AI agent's experience base

1. **"Framed experience" is the unit of capture.** A raw session log is *data*, not experience. The experience base must store interpretation: what it meant, why it happened, what rule it implies. This maps directly to Kolb's AC stage and to Argyris & Schön's insistence on theory-in-use.

2. **Resist the database fallacy.** D&P's central warning applies with force to AI: a markdown folder of session notes is an *information system*, not a knowledge base. Without interpretation, classification, retrieval heuristics, and a mechanism for consulting the right entry at the right moment, it becomes inert.

3. **Budget culture and process, not just storage.** D&P's 1/3 rule — at most one third of effort on technology — warns against believing that having the experience-base scaffold *is* the solution. The harder work is the procedural habit of writing entries, reviewing them, promoting them into standards, and pruning stale ones.

4. **Tacit-rich moments need deliberate elicitation.** Entries about judgement calls ("I overruled the obvious choice because of X") carry the highest tacit value and the greatest capture risk. The schema should make these explicit and not let them evaporate as "we just did the usual."

5. **Treat the experience base as a market.** An entry no one can find, or that is too costly to understand, is an entry that does not exist. Index, summarise, and reduce friction for downstream consumption.

## Verbatim anchors

- Knowledge is "a fluid mix of framed experience, values, contextual information, and expert insight that provides a framework for evaluating and incorporating new experiences and information."
- "At most, technology should take up one-third of all resources geared towards knowledge management."
- "Informal networks are the most effective means of spreading knowledge."
- "Changing the culture for the purposes of knowledge management would be like the tail wagging the dog."
