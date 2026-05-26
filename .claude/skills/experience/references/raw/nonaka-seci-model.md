# Nonaka & Takeuchi — SECI Model of Knowledge Conversion

**Source:** https://en.wikipedia.org/wiki/SECI_model_of_knowledge_dimensions
**Retrieved:** 2026-04-19
**Citations:**
- Nonaka, Ikujiro. 1990. *Chishiki sōzō no keiei*. Tokyo: Nihon Keizai Shimbunsha.
- Nonaka, Ikujiro & Takeuchi, Hirotaka. 1995. *The Knowledge-Creating Company*. Oxford University Press.

## The four modes

| From ↓ \ To → | Tacit | Explicit |
|---|---|---|
| **Tacit** | **Socialisation** — sharing knowledge through observation, imitation, practice; apprenticeship, mentoring. Requires physical or mental proximity. | **Externalisation** — knowledge is crystallised and made shareable. Individuals articulate insights through concepts, images, written documents. |
| **Explicit** | **Internalisation** — absorbing explicit knowledge through learning-by-doing; procedures and manuals become personal understanding. Continuous reflection. | **Combination** — merging documented knowledge; reports, databases, prototypes integrated to form new explicit knowledge. |

## The knowledge spiral

Knowledge creation does not cycle through once — it spirals upward continuously.
Tacit and explicit knowledge perpetually interact to generate innovation.

## Ba (shared context)

Nonaka & Konno later introduced *Ba* — Japanese for "place". The shared context
that enables knowledge creation: physical spaces (offices), virtual spaces
(email, shared drives), and mental spaces (shared ideas). Ba is the environment
in which knowledge is exchanged and created.

## Relevance to the skills framework

- **Externalisation** is the critical move for AI: tacit practitioner knowledge
  must be externalised into explicit form before a model can consume it. Our
  `experience/` folder *is* the externalisation output — crystallised rules,
  templates, antipatterns.
- **Combination** is what happens inside `knowledge/summary.md` and inside
  `SKILL.md`: merging multiple explicit sources into new structured explicit
  knowledge.
- **Internalisation** happens in the model's behaviour — when a model reads the
  skill and starts applying it effectively in context. This is the closest we
  get to "tacit knowledge" on the AI side.
- **Socialisation** is not available to an AI model across sessions in any
  traditional sense; the substitute is externalising human practitioner tacit
  knowledge and feeding it to the model as explicit artefacts.
