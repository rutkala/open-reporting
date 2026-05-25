# Documentation

Single source of truth for the Open Reporting project. **Humans and AI read the same files** — there is no separate "knowledge base" vs "standards" split.

## How this folder is organised

```
docs/
├── README.md          ← you are here
├── ARCHITECTURE.md    ← repo layout, two-plane contract, AI delegation
├── PROJECT.md         ← vision, product lines, principles
├── ROADMAP.md         ← pointer to Linear roadmap
├── RELEASE_NOTES.md   ← what shipped
├── CONTRIBUTING.md    ← contribution + Git workflow
├── DATA_MODEL.md      ← warehouse schema overview
├── DATA_SOURCES.md    ← data sources, APIs, naming
├── DOMAINS.md         ← domain taxonomy
├── session-memory.md  ← cross-session continuity (auto-injected by hook)
├── lessons-learned.md ← post-issue retrospectives
├── languages.json     ← language config
├── archive/           ← superseded docs (SITUATION.md, MVP.md, refactor-plan.md, …)
└── <topic>/           ← one folder per discipline (see below)
```

Each `<topic>/` folder contains up to three kinds of file, only those that apply:

| File | Purpose |
|------|---------|
| `principles.md` | What good X is — theory, frameworks, authoritative sources. The reference reading. |
| `building.md` (or named: `ingestion.md`, `measures.md`, …) | Rules when building X — patterns, conventions, do / don't. |
| `reviewing.md` (or `<x>-review.md`) | Checklist when reviewing X — for PR reviewers and review agents. |

Some topics also hold sub-areas (`charts/`, `_external/`).

## Topic folders

| Topic | What's in it | Read when |
|-------|-------------|-----------|
| [`visualization/`](visualization/) | `principles.md`, `ui-principles.md`, `building.md`, `reviewing.md`, `quality.md`, `charts/`, `references/` | Designing or reviewing any chart, dashboard, or layout. `quality.md` is the rubric; `references/` is the multimodal example library |
| [`ux-perception/`](ux-perception/) | `principles.md` | Designing any layout or colour scheme (Pre-attentive, Gestalt, WCAG, Cowan 4±1) |
| [`data-engineering/`](data-engineering/) | `principles.md`, `ingestion.md`, `processing.md`, `storage.md`, `measures.md`, `reviewing.md`, `measures-review.md` | Writing or reviewing any ETL script, dbt model, semantic measure, or DB DDL |
| [`data-architecture/`](data-architecture/) | `principles.md`, `reviewing.md` | Any schema design, new mart, dimensional model decision |
| [`business-analysis/`](business-analysis/) | `principles.md`, `reviewing.md` | Designing any KPI, measure, indicator, or analytical brief |
| [`analytical-methods/`](analytical-methods/) | `principles.md`, `reviewing.md` | Structuring any analysis or insight |
| [`content/`](content/) | `principles.md`, `reviewing.md` | Writing or reviewing blog / social / editorial content |
| [`platform-ops/`](platform-ops/) | `principles.md`, `reviewing.md` | Infrastructure, deployment, ops changes |
| [`research-methods/`](research-methods/) | `principles.md`, `reviewing.md` | Quantitative research, econometric models, notebooks |
| [`data-research/`](data-research/) | `principles.md`, `reviewing.md` | Evaluating a new data source for ingestion |
| [`public-finance/`](public-finance/) | `principles.md` | Any public-finance work — fiscal KPIs, SGP rules, canonical patterns |
| [`process/`](process/) | `requirements.md`, `code-review.md`, `model-delegation.md` | Cross-cutting: Linear issue templates, code review rules, model-tiering policy |
| [`sources/`](sources/) | `SUMMARY.md` | Authoritative data-source catalogue |

## Loading guidance (for AI agents)

Do not auto-load everything. Read on demand:
- Building a chart? → `docs/visualization/principles.md` + `docs/visualization/building.md` + `docs/visualization/quality.md` (rubric) + the relevant `docs/visualization/charts/<type>.md`
- Reviewing a dashboard? → `docs/visualization/quality.md` (the rubric) + cited reference images under `docs/visualization/references/`
- Writing a dbt model? → `docs/data-engineering/principles.md` + the specific build file (`ingestion.md` / `processing.md` / `storage.md` / `measures.md`)
- Reviewing a PR? → the corresponding `<topic>/reviewing.md`
- Designing a KPI? → `docs/business-analysis/principles.md` + the relevant domain folder (e.g. `docs/public-finance/principles.md`)
- Starting any analysis? → `docs/analytical-methods/principles.md`

When in doubt, start at [`ARCHITECTURE.md`](ARCHITECTURE.md) for the big picture, then drill into the relevant topic folder.
