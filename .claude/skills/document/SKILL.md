---
name: document
description: >
  Generic documentation process. Produces any artifact by running brainstorm → collect →
  analyze → save. Always paired with an artifact skill that defines the output structure.
  Invoked by /develop as Step 1, or standalone when producing a knowledge base, requirements
  document, domain brief, or any other artifact from scratch.
  Triggers when: "document X", "write the requirements", "build a knowledge base for X",
  "research and document X", or when /develop reaches Step 1.
user-invocable: true
argument-hint: "<artifact type> for <topic>"
---

# Document

Produces any artifact by running a four-step process: brainstorm → collect → analyze → save.

The artifact skill (e.g. `knowledge-base`, `requirements`, `domain-input`) defines what the
output looks like. This skill defines how to get there.

---

## Input

| What | Provided by |
|------|------------|
| Artifact type | Caller — which artifact to produce (e.g. `knowledge-base`, `requirements`) |
| Topic / context | Caller — what the artifact covers and any constraints |

<HARD-GATE>
Both artifact type and topic must be provided before starting. If either is missing, stop
and ask. Load the artifact skill first — it defines the output structure, quality criteria,
and any artifact-specific gates that apply during the write step.
</HARD-GATE>

---

## Output

Defined entirely by the artifact skill. This process skill produces no output of its own —
it drives the steps that produce the artifact.

---

## Steps

### 1. Brainstorm
Invoke `/brainstorm` to surface angles, source types, and open questions before collecting anything.

- What aspects of this topic matter most for the intended use?
- What types of sources exist (official docs, academic papers, community patterns, examples)?
- What gaps or uncertainties need to be resolved?

Output: a scoped list of questions and source directions to guide collection.

### 2. Collect
Gather raw material based on the brainstorm output. Collection has two parts — do both:

**Web research (always required for any topic with external sources):**
- Search official documentation, authoritative sites, academic sources, community resources
- Use web search tools to find current, primary sources — do not rely on training knowledge alone
- For each page fetched: write the full page content as a markdown file to `raw/` — e.g. `raw/dash_callbacks.md`, `raw/ibcs_chart_rules.md`. Write the fetched content itself, not a summary of it.

**Internal sources (when the topic relates to this codebase):**
- Read relevant project files, existing reference documents, configuration, code examples
- For each file read: write a copy or verbatim excerpt to `raw/` — e.g. `raw/semantic_py.md`, `raw/template_app_py.md`

Do not filter or synthesise at this stage — save the source material first, draw no conclusions yet.

### 3. Analyze
Invoke `/analyze` to assess collected material before writing.

- Maps coverage against the artifact structure — which sections are well-supported, which are thin
- Flags source quality issues and contradictions
- Identifies gaps: minor ones go into the artifact's Gaps section; major ones trigger another `/collect` pass

### 4. Save
Invoke `/save` to synthesise collected material into the artifact and write it to disk.

- Follows the artifact skill's structure exactly
- Cites sources throughout — every factual claim traces back to collected material
- Respects any artifact-specific gates defined in the artifact skill (e.g. PO approval, reviewer agent)
