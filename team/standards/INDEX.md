# Standards — Index

Standards are derived from the knowledge base and distilled into actionable rules.
See `team/PLATFORM.md §8` for the full standards map and derivation chain.

**Two categories:**
- `build/` — how we build (developer-facing, tells practitioners what to do)
- `evaluation/` — how we review (agent-facing, tells evaluator agents what to check)

---

## Build Standards

| Standard | File | Derived from KB | Applies to |
|----------|------|----------------|------------|
| Data ingestion | [build/ingestion.md](build/ingestion.md) | `knowledge-base/data-engineering/` *(not yet traced)* | ETL scripts in `platform/ingestion/` |
| Data processing | [build/processing.md](build/processing.md) | `knowledge-base/data-engineering/` *(not yet traced)* | dbt models in `platform/processing/` |
| Data storage | [build/storage.md](build/storage.md) | `knowledge-base/data-architecture/` *(not yet traced)* | All DB schema work |
| Visualisation design | [build/visualisation.md](build/visualisation.md) | `knowledge-base/visualization/` + `knowledge-base/ux-perception/` *(not yet traced)* | Dashboard and component development |
| Measures | [build/measures.md](build/measures.md) | `knowledge-base/business-analysis/` *(not yet traced)* | Semantic model definitions |
| Linear requirements | [build/requirements.md](build/requirements.md) | Workflow convention (not KB-derived) | All Linear issues |

---

## Evaluation Standards

| Standard | File | Derived from | Agent | Phase |
|----------|------|-------------|-------|-------|
| Code review | [evaluation/code-review.md](evaluation/code-review.md) | `knowledge-base/data-engineering/` *(not yet traced)* | `code-reviewer` | PR |
| Visualization — diff | [evaluation/visualization-diff.md](evaluation/visualization-diff.md) | `knowledge-base/visualization/` + `ux-perception/` *(not yet traced)* | `visualization-reviewer` | PR |
| Visualization — image | [evaluation/visualization-image.md](evaluation/visualization-image.md) | `knowledge-base/ux-perception/` *(not yet traced)* | `visual-screenshot-reviewer` | PR |
| Analytical review | *(embedded in agent — extraction planned)* | `knowledge-base/analytical-methods/` | `analytical-validator` | Plan + PR |
| Architecture review | *(embedded in agent — extraction planned)* | `knowledge-base/data-architecture/` | `architecture-critic` | Plan |
| Feasibility criteria | *(planned)* | All KB | `feasibility-panel` | Pre-sprint |
| Cost estimation | *(planned)* | `team/lessons-learned.md` | `cost-estimator` | Feasibility |
| Domain review | *(planned)* | `knowledge-base/domains/{domain}/` | `domain-specialist` | Plan + PR |

---

## Derivation traceability

All evaluation standards should open with:
```
Derived from: team/knowledge-base/{path}
Used by: .claude/agents/{agent}.md
Does NOT cover: {explicit scope boundary}
```

Standards marked "not yet traced" were written before the KB existed. They should be audited and updated when the corresponding KB is built.
