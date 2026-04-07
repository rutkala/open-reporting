# Playbook: Research

Covers sub-product #18 — Research (econometric model, Jupyter notebook, quantitative analysis).

## Recipe

### Sub-product #18 — Research

| Task | Competency | Builder | Evaluator | Standard |
|------|-----------|---------|-----------|----------|
| Research question (hypothesis design, methodology selection, data feasibility) | Business Analysis | `business-analyst` | `brief-reviewer` | brief-review.md |
| Model (econometrics, statistical analysis, reproducible research, robustness checks) | Research | `researcher` | `research-reviewer` | research-review.md |
| Analytical review (model assumptions, aggregation, causal claims, interpretation) | Analytical Methods | — *(evaluator only)* | `analytical-validator` | analytical-review.md |

---

## Phase 1 — Research Question

The `business-analyst` frames the research question:

1. **Define the hypothesis** — what relationship or effect is being tested? Is this a causal or descriptive question?
2. **Select methodology** — which method is appropriate? (OLS for descriptive, IV/DiD/synthetic control for causal)
3. **Assess data feasibility** — does the warehouse contain the required indicators? What is the time range, granularity, and quality?
4. **Identify confounders** — what variables might bias the relationship? Are they available in the warehouse?
5. **Define the expected output** — notebook, model, report? What are the deliverable tables and figures?

**Output:** A research brief documented in the Linear issue. Reviewed by `brief-reviewer`.

**Gate:** If `brief-reviewer` returns BLOCK, the brief is revised and re-reviewed.

---

## Phase 2 — Model

The `researcher` builds the analysis following the research-methods KB:

### 2.1 Reproducibility Contract (§1 of `research-methods/methods.md`)

- **Data lineage** — every dataset named with source, version, access date, exact query
- **Code runs end-to-end** — fresh environment reproduces all outputs
- **Random seeds fixed** — documented seed for any stochastic process
- **Software versions pinned** — Python, statsmodels, linearmodels, numpy versions recorded
- **Notebook structure** — title → data → descriptive → methodology → results → robustness → interpretation → reproducibility note

### 2.2 Model-Specific Standards (§2)

**OLS:**
- Always report robust standard errors (HC3 for small samples)
- Check: linearity (Ramsey RESET), homoskedasticity (Breusch-Pagan), multicollinearity (VIF), autocorrelation (Durbin-Watson)
- Report R-squared, adjusted R-squared, and N

**IV:**
- Always report first-stage results and F-statistic
- F > 10 (Stock-Yogo threshold) required
- Discuss exclusion restriction honestly
- Report both OLS and IV estimates side by side
- Report LATE interpretation (not ATE)

**DiD:**
- Always show parallel trends plot (event-study design)
- Use modern estimators for staggered adoption (Callaway & Sant'Anna, Sun & Abraham) — not TWFE
- Cluster standard errors at the treatment level

**Synthetic Control:**
- Always show pre-treatment fit
- Run placebo tests
- Report donor weights

### 2.3 Robustness Checks (§1.3)

Minimum 4 checks:
1. **Alternative controls** — add/remove plausible confounders
2. **Alternative functional forms** — linear vs. log vs. quadratic
3. **Alternative sample** — exclude outliers, restrict subsample, extend time window
4. **Alternative standard errors** — robust, clustered, HAC

If a result disappears under any check, report this honestly.

### 2.4 Polish Data Quirks (§4)

- **Structural breaks** — EU accession 2004, ESA 2010, BAEL 2021, COVID 2020, inflation 2022–23. Use break dummies, separate models, or explicit acknowledgement.
- **Administrative vs. survey data** — never mix without noting definitional differences
- **Data revisions** — note the vintage; GUS revises; preliminary data may change

### 2.5 Interpretation (§5)

- **State units** — a coefficient without units is meaningless
- **Report confidence intervals**, not just p-values
- **Use cautious language** — "suggests", "is consistent with", "is associated with" — never "proves" or "causes" from observational data
- **Compare to benchmarks** — is the effect large or small relative to SD, policy threshold, prior literature?

### 2.6 Output

A Jupyter notebook in `products/research/notebooks/` with:
- All code cells with proper comments
- Diagnostic tests and their interpretation
- Robustness checks (minimum 4)
- Honest discussion of limitations
- Reproducibility note at the end

---

## Phase 3 — Research Review

The `research-reviewer` evaluates the notebook against `research-review.md`:

- **P1 findings** (blocks publication): endogeneity ignored in causal claim, wrong standard errors, spurious regression, sample selection bias, data leakage, weak instrument not reported, exclusion restriction not discussed, parallel trends not shown, TWFE used for staggered adoption
- **P2 findings** (should fix): fewer than 4 robustness checks, structural break not acknowledged, administrative/survey series mixed, multiple testing without correction, cherry-picked time window, confidence intervals not reported
- **P3 findings** (noted): no power analysis, no out-of-sample validation, missing data not addressed, no discussion of limitations

**Gate:** If any P1 findings, the research returns to the researcher for revision. P2 findings should be addressed before publication. P3 findings are noted but do not block.

---

## Phase 4 — Analytical Review

The `analytical-validator` performs an independent analytical review:

- Aggregation correctness — are aggregations (sum, mean, last) appropriate for the indicator type (flow, stock, rate)?
- Causal language — does the interpretation overclaim what the method supports?
- Chart labelling — are chart titles, axis labels, and units correct and in Polish?

This review runs in parallel with or after the research-reviewer. Both must pass (or have all P1 findings resolved) before the research is accepted.

---

## Phase 5 — Publish

1. **Final review** — notebook runs end-to-end from raw data to final tables/figures
2. **Reproducibility check** — a fresh environment can reproduce all outputs
3. **Editorial summary** — if the research findings are newsworthy, produce a blog article (see `article.md` playbook) or social card (see `social.md` playbook)
4. **Archive** — commit the notebook with all outputs; tag with research topic and date

---

## Quality Gates

- [ ] Research question clearly stated and methodology justified
- [ ] All model assumptions checked and reported
- [ ] Standard errors appropriate for data structure
- [ ] Robustness checks run (minimum 4) and results reported honestly
- [ ] Polish structural breaks acknowledged where relevant
- [ ] No causal language unsupported by the method
- [ ] Confidence intervals reported
- [ ] Data lineage documented
- [ ] Random seeds fixed (if applicable)
- [ ] Software versions noted
- [ ] Research-reviewer passes with no P1 findings
- [ ] Analytical-validator passes with no P1 findings
- [ ] Notebook runs end-to-end in a fresh environment
