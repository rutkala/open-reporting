---
name: knowledge-base
description: >
  Knowledge base artifact. Defines what a knowledge base is — a structured collection of
  resources, research syntheses, patterns, and reference material on a specific topic.
  Use when any work requires a knowledge foundation — for a product, skill, artifact, or
  technical area. Provide the topic and output path; this skill defines the structure and
  quality criteria.
  Triggers when: "build a knowledge base for X", "research and document X", "create a reference
  for X", "we need a KB on X before we start".
user-invocable: true
argument-hint: "<topic> at <output path>"
---

# Knowledge Base

A knowledge base is a structured collection of resources, research syntheses, patterns,
and reference material about a specific topic. It is the foundation for any artifact,
product, or skill built in that area — design decisions, standards, and quality rules
all derive from it.

---

## Source

The source of knowledge base is all possible content from internet about the topic provided in input

---

## Input

| What | Provided by |
|------|------------|
| Topic | Caller — what the knowledge base covers (e.g. "Plotly Dash", "dbt MetricFlow", "Polish labour market statistics") |
| Output path | Caller — where to save it (e.g. `team/knowledge-base/visualization/`, `.claude/skills/dashboard/references/`) |

<HARD-GATE>
Both topic and output path must be provided before any research begins. If either is
missing, stop and ask the caller. Do NOT infer the output path from context — a knowledge
base saved in the wrong location is harder to find than no knowledge base at all.
</HARD-GATE>

---

## Output

| Deliverable | Location | Purpose |
|-------------|----------|---------|
| Raw files directory | `{output_path}/raw/` | Source documents, scraped pages, downloaded references — unprocessed |
| Summary file | `{output_path}/summary.md` | Synthesised knowledge in the 7-section structure below |

Consumed by: any skill, artifact, or product that works in this topic area

---

## Structure of Summary file

Every knowledge base must contain all 7 sections:

**1. Overview**
What this topic is, its scope, key concepts, and why it matters for this project.
2–4 paragraphs. No assumed knowledge — write as if the reader is intelligent but new to this topic.

**2. Authoritative sources**
Official documentation, academic papers, statistical publications, reference implementations.
For each source: name, URL, what it covers, and why it is authoritative.
Prefer primary sources over summaries. Check dates — prefer 2023+ unless foundational.

**3. Key patterns and conventions**
How practitioners approach this topic. Established patterns, naming conventions, structural
decisions that are standard in the field. Not our opinions — what the field agrees on.

**4. Component / API reference**
Concrete inventory of what exists: functions, classes, configuration options, endpoints,
data structures, chart types, etc. Include signatures, parameters, and usage notes.
Verify against the current version — do not rely on memory.

**5. Examples**
Representative real-world examples or code snippets demonstrating key patterns.
Each example must be concrete and runnable, not pseudocode.

**6. Decisions and trade-offs**
Known choices in this topic area, their implications, and what we have decided (with rationale).
Format: Decision → Options considered → Choice made → Why.

**7. Gaps and open questions**
What is uncertain, not yet researched, or needs validation before building.
Be honest — do not invent knowledge to fill holes. Flag gaps explicitly so they can be addressed.

---

## Quality criteria

- Every factual claim cites a source from the Authoritative sources section
- Component/API reference verified against current version of the library/tool
- Gaps section is present and honest — no invented knowledge
- Output path confirmed with caller before any research begins
- No placeholders or TBDs — every section is complete or explicitly flagged as a gap
