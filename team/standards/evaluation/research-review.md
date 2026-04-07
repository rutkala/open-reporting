# Research Review Rules

**Derived from:** `team/knowledge-base/research-methods/methods.md` ✓ (KB complete — reproducible research, OLS/IV/DiD/synthetic control, standard errors, Polish data quirks, coefficient interpretation, common errors)
**Used by:** `.claude/agents/research-reviewer.md`
**Does NOT cover:** editorial quality of the prose (see `evaluation/content-review.md`), chart visual design (see `evaluation/visualization-diff.md`), dashboard functionality (see `evaluation/code-review.md`), general analytical framing (see `evaluation/analytical-review.md`)

Rules applied by the `research-reviewer` agent on quantitative research products produced by the `researcher` agent. Research is reviewed before publication. The goal is to catch econometric and methodological errors before they reach readers.

---

## P1 — Blocks Publication

### Model validity

- **Endogeneity ignored in a causal claim** — the research claims a causal effect ("X causes Y", "X reduces Y", "the effect of X on Y") using OLS on observational data without addressing reverse causality or omitted variable bias. Flag as P1. IV, DiD, or synthetic control is required for causal claims from observational data.
- **Wrong standard errors for the data structure** — non-robust SEs on cross-sectional data (heteroskedasticity is the norm), non-clustered SEs on panel/group-level data, non-HAC SEs on time series with autocorrelation. This invalidates all inference (p-values, confidence intervals, significance stars).
- **Spurious regression** — OLS on non-stationary time series without a cointegration test. Trend-stationary series produce significant coefficients even when no relationship exists.
- **Sample selection bias unaddressed** — analyzing only observed outcomes without addressing selection. Example: estimating wage equations only for employed individuals (ignoring that employment itself is selected).
- **Data leakage** — post-treatment variables used as controls in a causal model, or future information used to predict past outcomes. This produces biased estimates that appear precise.

### IV-specific

- **Weak instrument not reported** — first-stage F-statistic below 10 (Stock-Yogo threshold) and not disclosed. Weak instruments bias IV estimates toward OLS with misleadingly narrow confidence intervals.
- **Exclusion restriction not discussed** — IV results reported without any discussion of why the instrument should affect the outcome only through the treatment. This is the weakest link of IV and must be addressed.

### DiD-specific

- **Parallel trends not shown** — DiD results reported without a parallel trends plot or event-study design showing pre-treatment trends. Without this, the identifying assumption is unverified.
- **TWFE used for staggered adoption** — traditional two-way fixed effects estimator used when units receive treatment at different times, without acknowledging the bias from heterogeneous treatment effects.

---

## P2 — Should Fix Before Publication

### Robustness

- **Fewer than 4 robustness checks** — the research reports results from only one specification. Minimum: alternative controls, alternative functional forms, alternative sample, alternative standard errors.
- **Robustness checks run but not reported** — the researcher ran alternative specifications but only reported the one that worked. All robustness results must be reported, even if they weaken the main finding.

### Polish data

- **Structural break not acknowledged** — the analysis spans a known structural break (EU accession 2004, ESA 2010, BAEL 2021, COVID 2020, inflation 2022–23) without a break dummy, separate models, or explicit acknowledgement.
- **Administrative and survey series mixed** — registered unemployment compared with BAEL unemployment, or ZUS wages compared with GUS survey wages, without noting the definitional difference.
- **Data vintage not noted** — GUS data is subject to revision. The analysis does not state which vintage of the data was used.

### Inference

- **Multiple testing without correction** — 20+ coefficients tested and only the significant ones highlighted, without Bonferroni, Benjamini-Hochberg, or pre-registration note.
- **Cherry-picked time window** — the start/end date appears chosen to maximise significance (e.g., starting in 2020 for a post-COVID recovery story, or ending at a peak). No justification for the time window.
- **Confidence intervals not reported** — only p-values or significance stars reported. Confidence intervals provide more information about precision and should be included.

### Reproducibility

- **Data lineage incomplete** — the source is named but the specific dataset, version, or query is not documented.
- **Random seed not fixed** — bootstrapping, Monte Carlo, or random splits used without a documented seed.
- **Software versions not noted** — the notebook does not record Python version or key package versions.

---

## P3 — Noted

- **No power analysis** — small sample, no discussion of minimum detectable effect size.
- **No out-of-sample validation** — model fit reported only on training data.
- **Missing data not addressed** — listwise deletion used without checking whether missingness is random.
- **No discussion of limitations** — every model has limitations; acknowledging them is a strength, not a weakness.
- **Abbreviation not defined** — econometric acronyms (TWFE, HAC, LATE, SUTVA) used without definition on first use.
- **Functional form not tested** — linear model used for a relationship that may be non-linear, without a Ramsey RESET test or alternative specification.

---

## What this standard does NOT cover

- Whether the research question is interesting or important — that is a substantive judgment, not a methodological one.
- Whether the prose is well-written — that is `content-reviewer`'s scope.
- Whether the charts look good — that is `visualization-reviewer`'s scope.
- Whether the underlying data is correct — that is the data pipeline's responsibility.
- Whether the chosen method is the absolute best for the question (vs. another reasonable choice) — if the method is valid and assumptions are checked, the choice is the researcher's.
