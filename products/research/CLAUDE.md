# Research — Agent Instructions

**Extends:** root `CLAUDE.md` — collaboration model, safety guardrails, git workflow, and language rules all apply here. This file adds research-specific context on top.

## Purpose
Academic-grade economic and statistical research using Polish public data. Work is grounded in
established theory — models are applied from the library, not invented ad hoc.

## Guiding Principle
**Theory first, data second.** Before running any analysis, identify the relevant model from
`library/`, confirm its assumptions hold for the available data, then apply it. Cite the source.

## Directory Layout

```
research/
├── library/                   — knowledge base of theories, models, equations
│   ├── economic_theory/
│   │   ├── microeconomics/    — consumer theory, production, market structures
│   │   └── macroeconomics/    — growth, business cycle, monetary, open economy
│   ├── econometrics/          — regression, time series, panel data methods
│   └── statistics/            — probability, inference, hypothesis testing
├── references/                — bibliography index with summaries
├── notebooks/                 — Jupyter notebooks for analysis
└── models/                    — reusable Python implementations
```

## Library File Format

Each library entry follows this template:

```
# Model Name
**Area:** micro / macro / econometrics / statistics
**Source:** Author, Title (Year), Chapter X
**Tags:** [tag1, tag2]

## Core Idea
One paragraph — what the model explains and when to use it.

## Key Equations
LaTeX-formatted equations with variable definitions.

## Assumptions
Numbered list of assumptions with notes on testability.

## Data Requirements
What variables are needed and which catalogue sources provide them.

## Limitations
Known weaknesses, common violations, remedies.

## Related Models
Links to related library entries.
```

## Research Workflow

1. **Define the question** — what economic phenomenon are we studying?
2. **Find the theory** — read the relevant library entry, check assumptions
3. **Identify data** — map required variables to `catalogue.sources`
4. **Pull data** — query DuckDB warehouse or call source APIs
5. **Apply model** — implement in a notebook using `models/` where available
6. **Interpret results** — in terms of the original theory, with caveats
7. **Document** — update the notebook with findings and references

## Data Access

```python
# Direct warehouse queries (filters, time series)
from dbr.semantic import query

# Example: pull GDP growth series
df = query("SELECT period, value FROM curated.mac_gdp_growth WHERE geo = 'PL'")
```

## Language Note
- Code, comments, library entries: **English**
- Published research output (articles, charts): **Polish**
