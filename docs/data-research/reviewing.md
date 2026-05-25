# Data Research Review Rules

**Derived from:** `docs/data-research/principles.md` ✓ (KB complete — source discovery, DAMA quality dimensions, licence assessment, indicator prioritisation, structural break documentation, output format)
**Used by:** `.claude/agents/data-research-reviewer.md`
**Does NOT cover:** ingestion script correctness (see `evaluation/data-engineering-review.md`), analytical soundness of downstream models (see `evaluation/analytical-review.md`), editorial quality of content based on the data (see `evaluation/content-review.md`)

Rules applied by the `data-research-reviewer` agent on data source research summaries produced by the `data-researcher` agent. Research is reviewed before it becomes a design input for the ingestion pipeline. The goal is to catch source selection errors, quality assessment gaps, and licence ambiguities before they propagate into the warehouse.

---

## P1 — Blocks Acceptance

### Source authority

- **Tier 1 source available but not identified** — a known official statistical source (GUS, Eurostat, NBP, MF) publishes the required data but the research recommends a lower-tier source instead without justification. This silently degrades data quality for all downstream products.
- **Source authority unverifiable** — the recommended source is not an official statistical office, central bank, ministry, or recognised international organisation, and no methodology documentation is available. The research cannot proceed from an unverifiable source.

### Licence

- **Licence unclear or restrictive without escalation** — the source has no stated licence, or has a CC BY-NC (non-commercial) licence, and the research recommends ingestion without flagging the legal risk. Open Reporting is a data media company; commercial use ambiguity must be resolved before ingestion.

### Quality

- **RED quality flag on a critical dimension not escalated** — any of the six DAMA dimensions (accuracy, completeness, consistency, timeliness, uniqueness, validity) flagged as RED without escalation to the lead analyst. A RED flag means the data has critical integrity problems.

---

## P2 — Should Fix Before Use

### Quality assessment

- **Fewer than six DAMA dimensions assessed** — the research does not evaluate all six dimensions (accuracy, completeness, consistency, timeliness, uniqueness, validity) for each data series. Missing dimensions create blind spots.
- **Quality flags assigned without evidence** — a GREEN or YELLOW flag is assigned without describing what was checked to justify it. Flags must be evidence-based, not assumed.

### Structural breaks

- **Known structural break not documented** — a data series has a documented structural break (GUS BAEL 2021, ESA 2010, currency redenomination 1995, EU accession 2004) and the research does not mention it. This silently corrupts any longitudinal analysis.
- **Revision policy not documented** — the source revises its data (GUS preliminary → final, national accounts revisions) but the research does not note the revision policy or magnitude.

### Indicator prioritisation

- **Priority not assigned** — a data series is recommended without a priority classification (P1–P4). The data-engineer cannot plan ingestion order without prioritisation.
- **P1 indicator not justified** — a series is marked P1 (essential) but does not meet the criteria: official statistic, regular update, high audience relevance, benchmarkable.

### Licence

- **Attribution text not specified** — the licence requires attribution but the research does not provide the exact attribution string (e.g., "Źródło: GUS, Bank Danych Lokalnych"). The ingestion pipeline needs this for chart footers and metadata.

### Output format

- **Source tier not assigned** — the source does not have a tier classification (1–5). The tier determines trust level and downstream usage.
- **API endpoint or file URL not documented** — the access method is described but the specific endpoint or download URL is not provided. The data-engineer cannot build the ingestion script without this.

---

## P3 — Noted

- **No alternative sources compared** — the research recommends one source without comparing it to alternatives. A brief note on why this source was preferred over others would improve traceability.
- **Historical depth limited without comment** — the data series has a short history (< 3 years for annual data, < 2 years for monthly) and this is not noted as a limitation.
- **No granularity assessment** — the research does not specify the finest level of disaggregation (time, geography, demographic) available from the source.
- **Update frequency not verified against release calendar** — the stated update frequency is not cross-checked against the source's published release calendar.
- **No data sample provided** — the research does not include a small sample of the actual data (first 5 rows) to help the data-engineer understand the structure.

---

## What this standard does NOT cover

- Whether the data-engineer builds the ingestion script correctly — that is `data-engineer-reviewer`'s scope.
- Whether the data, once ingested, is used correctly in analysis — that is `analytical-validator`'s scope.
- Whether the indicator is the best choice for the domain — that is `business-analyst` and `domain-specialist`'s scope.
- The technical quality of the API or file format — that is the data-engineer's concern during implementation.
