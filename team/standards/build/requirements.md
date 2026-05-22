# Requirements Standard

## Purpose

Every Linear issue must be well-defined before work starts. This standard defines:
1. What a well-formed issue looks like per type
2. How Claude validates requirements before proceeding
3. What questions to ask when information is missing

---

## Definition of Ready

An issue is ready to implement when it answers:
- **Why** — what business need or user need does this address?
- **What** — what is the expected output/deliverable?
- **Who** — who is the audience?
- **How to verify** — what does done look like? (acceptance criteria)
- **Constraints** — any known limitations, preferences, or boundaries?

If any of these are missing, Claude must ask before starting work.

---

## Issue Types

### Dashboard Issue

**Required fields:**
```
Title: [Domain] Short description of what the dashboard shows

Business question:
  What question should this dashboard answer for the user?
  (e.g. "How has the Polish unemployment rate changed by region over the last 10 years?")

Audience:
  Who will use this dashboard and what do they know?
  (e.g. "Polish citizens with no economics background")

Metrics / what to show:
  What data dimensions matter? (time range, geography, category)
  What specific indicators or metrics should be visible?

Data source hint (optional):
  Any known source, or leave blank for Claude to research

Visual preferences (optional):
  Any specific chart types, layout preferences, examples to follow

Acceptance criteria:
  - [ ] Specific, testable conditions that define done
  - [ ] (e.g. "Shows unemployment rate by voivodeship for 2010-2024")
  - [ ] (e.g. "Source attribution visible in footer")
  - [ ] (e.g. "All labels in Polish")
```

**Minimum to start:** Business question + audience + at least one acceptance criterion

---

### Ingestion / Data Pipeline Issue

**Required fields:**
```
Title: Ingest [Source Name] — [what data]

What data is needed:
  What specific dataset, variables, time range, geography?

Why it is needed:
  Which dashboard or product depends on this data?

Source:
  Known source URL or "research required"

Update frequency:
  How often should data be refreshed? (one-time, monthly, annual)

Acceptance criteria:
  - [ ] Data lands in raw.{source}_{entity}
  - [ ] Row count and date range match source
  - [ ] Validation passes (no nulls in required columns)
```

**Minimum to start:** What data + why it is needed + at least one acceptance criterion

---

### Article / Content Issue

**Required fields:**
```
Title: [Topic] — short description

Main message:
  What is the one key insight or story this article communicates?

Audience:
  Who will read this and what is their background?

Data angle:
  What data supports the story? Any specific findings to highlight?

Format:
  Article length (short/medium/long), any specific sections required?

Acceptance criteria:
  - [ ] Specific, testable conditions that define done
```

**Minimum to start:** Main message + audience + format

---

### Infrastructure / Technical Issue

**Required fields:**
```
Title: Short description of change

Problem or need:
  What is broken or missing? Why is this needed now?

Expected outcome:
  What should work after this is done?

Constraints:
  Any services that must stay running? Any downtime limits?

Acceptance criteria:
  - [ ] Specific, testable conditions
```

**Minimum to start:** Problem + expected outcome + acceptance criteria

---

## Requirements Validation — Claude's Responsibility

When `/kickoff` reads a Linear issue, before doing anything else:

1. **Identify the issue type** (dashboard / ingestion / article / infrastructure)
2. **Check required fields** against the template above
3. **For each missing field** — ask a specific question, not a generic one

Bad: *"Can you provide more details?"*
Good: *"What business question should this dashboard answer? For example: 'How has X changed over time?' or 'Which regions have the highest Y?'"*

4. **Do not proceed until minimum requirements are met**
5. **Summarise confirmed requirements** back to the user before moving to research

---

## Acceptance Criteria Rules

Good acceptance criteria are:
- **Specific** — "Shows unemployment rate by voivodeship" not "shows regional data"
- **Testable** — can be verified by looking at the output
- **Outcome-focused** — what the user sees, not how it is built
- **In plain language** — no technical jargon

Format: `- [ ] {who} can {do what} using {what}`

Examples:
- `- [ ] User can see unemployment rate for each voivodeship for years 2010–2024`
- `- [ ] Source (GUS BDL) is visible in the footer`
- `- [ ] Filtering by year updates all charts on the page`
- `- [ ] All chart labels and titles are in Polish`

---

## PR Review Checklist

Before approving any PR, the reviewer verifies:

```markdown
### All PRs
- [ ] No secrets committed (.env, API keys, passwords)
- [ ] English-only backend (names, variables, logs, SQL columns)
- [ ] Polish user-facing strings (labels, titles, tooltips)
- [ ] 100 char line length, 4-space indent
- [ ] logging.getLogger(__name__) — no print() in scripts

### Ingestion PRs (products/ingestion/)
- [ ] Parameterised queries — no string concatenation in SQL
- [ ] load_dotenv(override=True) + lazy _dsn() pattern
- [ ] Idempotent — safe to re-run without duplicating data
- [ ] Source documented in catalogue (catalogue.domain_detail_sources)

### Processing PRs (products/warehouse/)
- [ ] dbt model follows curated schema naming
- [ ] Data quality checks included
- [ ] Seeds use --full-refresh when schema changes

### Visualisation PRs (products/)
- [ ] Nordic theme imported from `complex_dashboard.assets.theme` — no hardcoded colours
- [ ] All chart labels in Polish
- [ ] Source attribution visible

### Acceptance criteria
- [ ] All acceptance criteria from the Linear issue are met
- [ ] RELEASE_NOTES.md updated under "Unreleased"
```

---

## User Story Format (optional)

For user-facing features, the standard format:

```
As a [type of user]
I want [to do something / see something]
So that [I achieve some goal / understand something]
```

Example:
```
As a Polish citizen with no economics background
I want to see how unemployment has changed in my region over the last decade
So that I can understand whether the local job market is improving
```

This is optional — use it when it helps clarify the audience and need. Not required for technical issues.
