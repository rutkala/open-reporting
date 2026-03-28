# Playbook: Dashboard

## Overview

This playbook defines the complete process for building a dashboard — from a Linear task to a published page. Follow every phase in order. Do not skip phases or gates.

```
/kickoff → Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5 → /document
```

---

## Phase 0: Kickoff

**Skill:** `/kickoff <OR-XXX>`

1. Read the Linear issue
2. Assess feasibility:
   - Is the required data likely available? (check `docs/DATA_SOURCES.md`)
   - Does this depend on anything not yet built?
   - Is this one dashboard or multiple?
3. Present plain-language summary to user
4. **Gate: user confirms understanding and approves proceeding**
5. Update Linear → In Progress

---

## Phase 1: Data Source Evaluation

**Skill:** `/research`

**Standard:** `docs/DATA_SOURCES.md` — source hierarchy (Level 1 → Level 4)

Steps:
1. Identify what data is needed (metrics, dimensions, time range, geography)
2. Search for sources following the hierarchy — start at Level 1
3. For each candidate source evaluate:
   - Is it official? (Level 1-3 only, no commercial providers)
   - Is an API available, or file download only?
   - What variables are available? Time range? Geographic granularity?
   - Rate limits, authentication requirements?
   - Data freshness — how often is it updated?
4. Present findings:
   - Recommended source with reasoning
   - Variables available and what they cover
   - Any gaps — data not available or incomplete
   - Proposed ingestion method (API or file)

**Gate: user approves data source before any code is written**

---

## Phase 2: Ingestion

**Skills:** `/plan` → implement → `/review`

**Standard:** `.claude/standards/ingestion.md`

Steps:
1. `/plan` — design the ingestion script:
   - Source URL, authentication, pagination
   - Update method (upsert / incremental / full load)
   - Raw schema: `raw.{source}_{entity}`
   - Present plan in plain language — what data will land, how often, how much
2. **Gate: user approves plan**
3. Implement ingestion script in `ingestion/{source}_ingest.py`
4. Run script, verify data lands in `raw.` schema
5. `/review` — check against ingestion.md checklist
6. **Gate: user approves ingestion output**
   - Show: row count, date range, sample rows in plain language
   - Flag any gaps or unexpected values

---

## Phase 3: Processing

**Skills:** `/plan` → implement → `/review`

**Standard:** `.claude/standards/processing.md`

Steps:
1. `/plan` — design the processing script:
   - Input: `raw.{source}_{entity}`
   - Output: `curated.{domain}_{metric}`
   - Define required vs optional columns
   - Define validity rules (ranges, allowed values)
   - Define natural key for deduplication
   - Present plan — what the curated table will contain and how it differs from raw
2. **Gate: user approves plan**
3. Implement processing script in `processing/{source}_process.py`
4. Apply all 6 quality categories (encoding → completeness → types → validity → consistency → deduplication)
5. Run script, verify data in `curated.` schema
6. `/review` — check against processing.md checklist
7. **Gate: user approves curated data**
   - Show: row count, date range, quality issues found, sample values in plain language

---

## Phase 4: Visualisation

**Skills:** `/plan` → implement → `/review`

**Standard:** `.claude/standards/visualisation.md`

Steps:
1. `/plan` — design the dashboard:
   - What story does this dashboard tell? (one sentence)
   - What metrics are shown and how (chart types, groupings)
   - Page structure: which topic groups, which charts in each group
   - Filters available to the user
   - Present as a written description — no code, no wireframe needed
2. **Gate: user approves dashboard design**
3. Implement dashboard in `products/dashboards/{domain}/app.py`:
   - Use `nordic` Plotly template (registered in `products/visuals/lib/theme.py`)
   - Plotly figures use transparent backgrounds (`paper_bgcolor="rgba(0,0,0,0)"`)
   - Each chart in a white card with shadow (defined in HTML template)
   - Charts grouped by topic with section headings
   - All user-facing text in Polish
   - Required elements: title, subtitle, source attribution, last updated date
4. Generate dashboard HTML → `nginx/html/{domain}/{name}.html`
5. `/review` — check against visualisation.md checklist
6. **Gate: user reviews the rendered dashboard**
   - Present: what was built, what story it tells, any design decisions made
   - User opens the HTML file to review visually

---

## Phase 5: Publish

**Skills:** `/commit` → `/document`

Steps:
1. `/commit` — commit all changes (ingestion script, processing script, dashboard, HTML output)
2. Update session memory
3. Update Linear → Done, add completion comment
4. `/document` — update relevant docs:
   - `docs/DATA_SOURCES.md` — add any new source details discovered
   - `docs/ARCHITECTURE.md` — if new folders or schemas were created
5. Verify dashboard is live: `curl -I https://portal.open-reporting.dev/{path}`

---

## Quick Reference

| Phase | Input | Output | Standard |
|-------|-------|--------|----------|
| 0: Kickoff | Linear issue | Confirmed scope | — |
| 1: Data Source | Issue requirements | Approved source | DATA_SOURCES.md |
| 2: Ingestion | Source API/file | `raw.` table | ingestion.md |
| 3: Processing | `raw.` table | `curated.` table | processing.md |
| 4: Visualisation | `curated.` table | Dashboard HTML | visualisation.md |
| 5: Publish | All outputs | Live dashboard | — |

---

## Rules

- **Never skip a gate** — every gate exists to catch problems before they compound
- **Never query `raw.` from dashboards** — always query `curated.`
- **Never use a Level 4 source** without explicit user approval
- **Never publish without user reviewing the rendered dashboard**
- **One dashboard per Linear issue** — if scope grows, create a new issue
