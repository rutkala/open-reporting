---
name: basic_data_science_research
description: "Data science research product context. Loaded when producing analytical research — econometric models, statistical analysis, Jupyter notebooks. Defines what a research product is, its methodology standards, and output structure."
user-invocable: true
---

# Data Science Research

A research product is a reproducible analytical investigation — econometric modelling,
statistical analysis, or data exploration — produced as Jupyter notebooks with
documented methodology, code, and findings.

This skill defines WHAT a research product is. The process lives in `/composite_develop`.

---

## Technology stack

| Layer | Technology |
|-------|-----------|
| Analysis environment | Jupyter notebooks (`products/research/notebooks/`) |
| Language | Python (pandas, statsmodels, scipy, sklearn) |
| Models | `products/research/models/` |
| Data access | DuckDB via `products/visuals/lib/db.py` |
| References | `products/research/library/` |

---

## Input

| Artifact | Location | Produced by |
|----------|----------|-------------|
| Requirements document | `products/domain-briefs/{domain}/basic_requirements.md` | `/composite_document` |
| Domain brief | `products/domain-briefs/{domain}/domain-brief.md` | `/basic_research` (via `/composite_document`) |

---

## Output

| Deliverable | Location | Required |
|-------------|----------|---------|
| Analysis notebook | `products/research/notebooks/{slug}.ipynb` | Yes |
| Model implementation | `products/research/models/{model}.py` | If new model |
| Findings summary | `products/research/notebooks/{slug}_summary.md` | Yes |

---

## Methodology standards

- Every claim must be traceable to a test statistic or data query
- Assumptions must be stated and tested (normality, stationarity, etc.)
- Results must be reproducible: fixed random seeds, pinned library versions
- Distinguish: correlation vs causation — do not overstate causal claims
- Document data transformations — every filter and aggregation explained

---

## Quality gates

Before handing to `/composite_evaluate`:
- [ ] Notebook runs end-to-end without errors from fresh kernel
- [ ] All assumptions stated and tested
- [ ] Conclusions proportionate to evidence (no causal overreach)
- [ ] Data sources cited with versions or retrieval dates
- [ ] Findings summary is self-contained (readable without the notebook)

---

## Standards

- `docs/analytical-methods/reviewing.md`
- `docs/research-methods/reviewing.md` (if exists)
- `docs/analytical-methods/principles.md`
- `products/research/CLAUDE.md` (research-specific instructions)
