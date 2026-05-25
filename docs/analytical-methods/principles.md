# Analytical Thinking Framework

Agent reference for moving from raw data to insight to narrative.
Read at the start of `/plan` when designing any analytical output (dashboard, article, social card).

**Sources:** UK Government Analysis Function ("Writing About Statistics", "Communicating Quality, Uncertainty and Change"), UNECE "Making Data Meaningful", Online Journalism Blog (Paul Bradshaw), IZA World of Labor, Eurostat Statistics Explained, GIJN data journalism training materials, IRE/Journalist's Resource, Royal Society Open Science.

---

## 1. The Five Analytical Moves

Every data story is built from one or more of these five moves. Identify which move you are making before writing a single sentence — different moves have different validity requirements and different failure modes.

| Move | Question answered | Typical output |
|------|------------------|----------------|
| **Describe** | What is the current state? | Distribution, central tendency, dispersion |
| **Compare** | How does this measure up against something else? | Cross-section, demographic, sectoral contrast |
| **Change** | Has this gotten better, worse, or stayed the same? | Trend, YoY, period-over-period |
| **Relate** | Is there a relationship between X and Y? | Correlation, co-movement, explanatory hypothesis |
| **Rank** | Where does this sit relative to all other cases? | League table, position, spread |

---

### 1.1 Describe

Characterise a dataset as it currently exists: distribution, central tendency, dispersion, shape. A snapshot without comparison.

**Use the median, not the mean, for skewed distributions** — wages, income, time-series with outliers. In Polish wage data (GUS structural wage surveys), the median is approximately 75–80% of the mean. Reporting only the mean overstates typical conditions.

**Always report dispersion alongside the centre.** Two regions can have identical median wages with entirely different wage distributions. A central value without variance hides inequality.

**Failure modes:**
- **Mean/median confusion** — the most common error in wage and income reporting.
- **Ignoring dispersion** — central tendency without variance is a half-answer.
- **Population scope error** — ZUS registration data and BAEL survey data cover different populations. Describe one as if it were the other and the finding is invalid.
- **Ecological fallacy** — inferring individual behaviour from group-level aggregate figures. A region's high average wage does not characterise its individuals.

---

### 1.2 Compare

Place a figure alongside another to establish relative magnitude. Comparisons can be cross-sectional (country A vs country B), demographic (men vs women), or sectoral.

**Validity requirement: the compared units must be equivalent.** This is the most dangerous move because invalid comparisons are easy to make and hard to detect at a glance.

**Failure modes:**
- **Non-comparable definitions** — Poland's registered unemployment (GUS/PUP data) is systematically higher than LFS/BAEL unemployment because benefit access incentivises registration. These two series are not directly comparable.
- **Non-equivalent time points** — comparing Poland's employment rate in 2004 (structural low, 51%) to today without acknowledging the transformation makes policy effects look larger than they are.
- **Cherry-picked reference group** — choose the comparator based on what is methodologically appropriate, not what makes the subject look best or worst. V4 is the right frame for Poland's structural position; EU27 is the right frame for convergence progress.
- **Scope mismatch** — gross wages vs net wages, employer cost vs take-home pay. Always flag when the comparison crosses a scope boundary.
- **Selection bias** — comparing groups that differ not just on the variable of interest but on the selection mechanism. Comparing employed workers' wages to all workers' wages is not a clean comparison.

---

### 1.3 Change (Over Time)

Measure the difference between a value at two or more points in time. Absolute change (level difference) and relative change (percentage) serve different purposes and must not be confused.

**Percentage point vs percent change — the single most common journalist error:**

| Situation | Correct framing |
|-----------|----------------|
| Unemployment rises from 3% to 6% | Rose **3 percentage points** (pp) OR **doubled** / rose 100% |
| GDP grows from 500bn to 550bn PLN | Rose **10%** |
| Never | "Rose 3 percent" when the original figure is already a percent |

Use "percentage points" when the original value is itself a percentage. Use "percent" when measuring proportional change in any number.

**Failure modes:**
- **Base effect distortion** — an equal absolute change produces different percentage changes depending on the base. A 50-point rise from 100 = 50%; the same 50-point rise from 150 = 33%. Post-COVID recovery percentages are systematically inflated by the depressed base.
- **Base year cherry-picking** — starting a time series at a trough (to show growth) or peak (to show decline) is a framing manipulation. Apply the same calendar consistently.
- **CAGR across structural breaks** — CAGR assumes constant compounding throughout the period. It blends pre-break and post-break regimes into a single misleading number. Do not use CAGR across the 2008–09 crisis, the 2020 COVID contraction, or the 2004 accession year. Report pre-break and post-break trends separately, then note the cumulative change since the anchor point.
- **Seasonal confounding** — month-on-month changes in employment, construction, and retail carry strong seasonal components. Always compare year-on-year or use seasonally adjusted series. Never compare a seasonally adjusted figure to a non-adjusted one.
- **Stock vs flow confusion** — employment level is a stock (snapshot); job creation is a flow (accumulation over a period). Averaging a flow variable over periods where the denominator changes is invalid.

---

### 1.4 Relate

Identify and describe a statistical relationship between two variables. The correlation / explanatory move. Answers "why" questions at the hypothesis level — without necessarily establishing causation.

**No correlation is evidence of causation.** This is not a stylistic preference — it is a logical requirement. Every analysis that uses the word "driven by", "caused by", or "because" must be supported by mechanism evidence, not correlation alone.

**Failure modes:**
- **Spurious correlation** — a third variable (confound) drives both. In Polish regional data, GDP per capita and educational attainment are both driven by urbanisation. A naive bivariate analysis overstates the education-income relationship.
- **Simpson's paradox (aggregation direction reversal)** — a trend that holds within every subgroup can reverse at the aggregate level if subgroup sizes are unevenly distributed. Example: overall average wages may rise even if wages fall in every sector, if employment is shifting toward higher-wage sectors (compositional effect). Always decompose aggregate changes into within-group and between-group (compositional) components before concluding about direction.
- **Ecological fallacy** — see §1.1. Regional-level relationships do not necessarily hold at the individual level.
- **Range restriction** — if the comparison is only among top-performers (e.g. only employed people's wages), correlation patterns within that group do not generalise to the full population.

---

### 1.5 Rank

Order observations from highest to lowest on a dimension. Positional information is the output: who leads, who lags, and by how much.

Distinguish two separate story types that both involve ranking:
- **Ranking angle** — "Which entity sits at the top/bottom of this ordered list?" Specific, concrete, often surprising. The more reliable story peg.
- **Variation angle** — "How much do entities differ from each other?" About the spread, not the winner. Only works "when fairness is expected or assumed" — less reliable as a standalone story.

**Failure modes:**
- **Ranking on absolute values without size normalisation** — ranking countries by absolute number of unemployed without adjusting for labour force size is invalid. Use rates or per capita figures, with the caveat below.
- **Per capita fallacy** — per capita figures are only valid if the numerator grows proportionally with population. Small countries are systematically over- or underrated because the proportionality assumption rarely holds. For cross-country size comparisons, treat per capita rankings with caution and prefer PPS-adjusted or regression-residual approaches.
- **Treating ordinal positions as measured distances** — country ranked 2nd is not necessarily "close" to country ranked 1st. Always check the actual values, not just the positions.
- **Ignoring margin of error in rankings** — for survey data, many adjacent positions in a ranking are statistically indistinguishable. Poland's unemployment rate difference from the EU average is often within sampling error.

---

## 2. The Insight Hierarchy

Every finding should be structured in four layers. Lead with the most important; do not bury the finding in methodology.

### Layer 1: Headline Finding

One clear declarative statement. Specific, concrete, everyday language. Contains the "so what."

**Must answer:** What changed, by how much, and is it unusual?

**Not:** "Unemployment data released" (label)
**Yes:** "Poland's unemployment rate falls to its lowest level since records began" (insight)

Rules:
- Never begin with methodology, definitions, or data source.
- If the headline requires a caveat to be honest, include the caveat in the headline, not in a footnote.
- Avoid numbers in the first sentence where the words are clearer ("more than doubled" rather than "rose 105.3%").

---

### Layer 2: Evidence

The numerical support for the headline. Quantified finding, with source, magnitude (absolute and relative change), direction, and time period.

Rules:
- Report both absolute and relative change where both are meaningful.
- Include the reference period and reference point explicitly ("compared to Q3 2023", "relative to the EU27 average of 6.1%").
- Begin each evidence paragraph with a theme sentence, then support it with the number — not the reverse.
- Only report what is genuinely new. Do not update numbers into the narrative of a previous period.

---

### Layer 3: Context

The interpretive frame. Answers: is this a trend, an anomaly, or noise? How does this compare to historical benchmarks, policy targets, or peer countries?

**Types of context for Polish public data:**
- Long-run trend (where is this in a 10–20 year arc from 2004 baseline?)
- Policy target reference (EU Fiscal Compact 3% deficit rule, 60% debt-to-GDP, 75% employment rate EU 2030 target)
- Peer comparison (V4, EU27, OECD — see §4)
- Historical inflection point (2004 accession, 2008–09 crisis, 2020 COVID, 2022 Ukrainian refugee wave)

**Rule:** Never report a latest value in isolation. A number without context is not an insight — it is a data point.

---

### Layer 4: Caveats and Limitations

Flags about data quality, definitional scope, uncertainty, and alternative explanations.

**Three types of caveat — ranked by materiality:**

1. **Definitional** — the indicator is defined differently across sources and the difference would change the conclusion. These belong near the headline.
2. **Quality** — sampling error, revision risk, coverage gaps. These belong in the evidence section.
3. **Interpretive** — the finding is consistent with multiple explanations. These belong after the context.

**Rule:** Material caveats (that would reverse the conclusion) are presented early. Minor methodological footnotes belong at the end or in a separate note. Do not use caveats to hedge every sentence — it dilutes the message without improving accuracy.

---

## 3. When Is an Indicator Interesting?

Apply these tests in sequence. An indicator must pass at least one to be worth highlighting.

### Test 1: Is the change statistically real (vs sampling noise)?

For survey-based indicators (BAEL/LFS unemployment, wage surveys), check whether the change exceeds the stated confidence interval. For Poland's LFS, the standard error on the quarterly unemployment rate is approximately ±0.3–0.5 percentage points. Changes below 0.5 pp between adjacent quarters are not reliably distinguishable from noise.

**Rule:** If the change is within the confidence interval, do not present it as a finding. Report it as "unchanged" or "broadly stable."

### Test 2: Is the change practically significant (large enough to matter)?

A finding can be statistically significant but trivially small in practical terms, especially with large administrative datasets. Apply domain-specific thresholds:

| Domain | Threshold for practical significance |
|--------|-------------------------------------|
| Unemployment / employment rate | ≥ 1 percentage point |
| Wage growth | ≥ 1 pp above or below inflation |
| Budget deficit | Crossing 1% of GDP increments |
| Debt-to-GDP | Approaching a named threshold (50%, 55%, 60%) |
| YoY GDP growth | Deviation > 1 pp from EU average or trailing 5-year trend |

### Test 3: Does it deviate from expectation?

Compare the latest value to:
- The same-period value one year prior (removes seasonality)
- The trailing 5-year average for that period
- The explicit policy target, if one exists

A value inside the expected range is not newsworthy even if it is the latest reading. A value outside the range by more than one standard deviation of recent history is.

### Test 4: Does it cross a named threshold?

Named thresholds carry inherent significance regardless of magnitude:

| Threshold | Domain | Significance |
|-----------|--------|-------------|
| Unemployment below 5% | Labour | EU conventional "full employment" benchmark |
| Employment rate above 75% | Labour | EU 2030 target (European Pillar of Social Rights) |
| Deficit above 3% of GDP | Fiscal | EU Excessive Deficit Procedure trigger |
| Debt at 50% / 55% of GDP | Fiscal | Polish constitutional rule thresholds |
| Debt at 60% of GDP | Fiscal | EU Maastricht limit |
| Real wages below CPI | Wages | Real purchasing power decline |

### Test 5: Is the rate of change more interesting than the level?

A level may be unremarkable; the rate of change may be extreme — or vice versa.

**Example:** Poland's employment rate (78.4% in 2024) is above the EU average (75.8%), so the level is not a gap-to-close story. But the improvement since 2004 (+26 pp) is one of the strongest in the EU — the rate of change is the finding.

**Example:** Poland's debt-to-GDP level (55%) is below the EU average, but the rate of increase since 2020 (+10 pp) is unusually fast — the acceleration is the finding.

Always examine both level and change. Report whichever is the more significant departure from expectation.

---

## 4. Polish Public Data Context

### 4.1 Standard Peer Groups

| Peer group | Use for |
|------------|---------|
| **V4** (Czech Republic, Slovakia, Hungary, Poland) | Structural comparisons: employment structure, labour market institutions, temporary employment, wage levels (PPS), fiscal trajectories. Natural first-order peer — shared communist legacy, simultaneous EU accession 2004, similar starting conditions. |
| **EU27 average** | Convergence narratives — how far Poland has come from its 2004 position. Compliance checks against Maastricht, European Pillar of Social Rights targets. |
| **OECD** | Structural comparisons of labour regulation, collective bargaining coverage, social protection, productivity measurement. |
| **CEE10 / CEE region** | Post-communist transition patterns, when the story is broader than EU-specific outcomes. |

**Default rule:** Lead with V4 for structural comparisons, EU27 for convergence and compliance.

### 4.2 Historical Benchmarks That Matter

| Anchor | What it benchmarks |
|--------|-------------------|
| **2004 — EU accession** | The critical baseline. Unemployment ~19%, employment rate ~51.7%, GDP per capita ~50% of EU average, wages ~4x below EU15. All "transformation" narratives anchor here. |
| **2008–09 — Financial crisis** | Poland was the only EU member to avoid a GDP contraction in 2009 ("green island"). Unemployment peaked at 10.6% in 2013 (lagged). Use for resilience comparisons. |
| **2014–2020 — Ukrainian labour immigration wave** | Fundamental alteration of labour supply. Partially explains wage growth moderation despite tight labour market pre-2017. Any wage dynamics analysis in this period must account for it. |
| **2017 — Pension reform reversal** | Retirement age reduced to 60/65 (women/men). Structurally reduced older-worker labour supply. Confounding factor in LFPR and employment rate trends post-2017. |
| **2020 — COVID** | Poland had one of the EU's mildest recessions (-2.7% vs EU average -5.6%). Anti-Crisis Shield wage subsidy protected formal employment. Do not compare Poland's "recovery" rate to EU peers without noting the denominator is different. |
| **~2021-present — Structural full employment** | Unemployment below 3% — historically unprecedented. Analytical questions shift from job creation to labour shortage, wage inflation, and productivity. |

### 4.3 Questions Polish Analysts Typically Ask

**Labour market:**
- Is employment growth extensive (more people working) or intensive (existing workers working more hours)?
- What explains the persistent gender employment gap relative to V4 peers?
- What is the effect of minimum wage increases on the lower wage deciles?
- Why does temporary employment remain the second-highest share in the EU despite reform attempts?
- How do regional labour markets differ? (Mazowieckie vs Świętokrzyskie / Podkarpacie)
- What is the role of civil-law contracts (zlecenie, o dzieło) in concealing true labour market precarity?
- How does labour's share of GDP compare to EU27? (Poland: ~39% vs EU: ~47.5%)

**Public finance:**
- Is the deficit structural (cyclically adjusted) or cyclical?
- Where is Poland relative to its own constitutional debt rules (50% and 55% of GDP thresholds)?
- What is driving the acceleration in debt-to-GDP? (defence spending, social transfers, debt service costs)
- Is Poland at risk of an EU Excessive Deficit Procedure?
- What share of public investment is EU-financed vs nationally financed? (Standard distinction in Polish Ministry of Finance analysis)

**Wages and productivity:**
- Is real wage growth outpacing productivity?
- What is the labour compensation gap relative to EU27? (Below in absolute terms, converging in PPS terms)
- What is the education wage premium?

---

## 5. Aggregation and Ratio Rules

### 5.1 Percent vs Percentage Point (mandatory)

Already covered in §1.3. Restated here as a hard rule:

> When the original value is itself a percentage, use **percentage points** for the change. Never say "rose X percent" when the original is already a percent.

### 5.2 Base Effect

An equal absolute change produces a different percentage change depending on the base. Post-recession recovery percentages are systematically inflated by the depressed base year. When bases differ structurally, use absolute change as the primary comparator and note the base effect explicitly.

### 5.3 Index Comparability

Index series are only comparable if they share the same base year. Before comparing two indexed series, verify the base year. If different, rebase to a common year before comparing. Note: rebasing does not change the underlying data — it only changes the reference point.

### 5.4 Per Capita Normalisation

Valid only if the numerator grows proportionally with population — a condition that rarely holds exactly. Small countries are systematically over- or underrated in per capita rankings. Use per capita for: income levels (GDP per capita in PPS), health spending, doctor-to-population ratios. Use cautiously for: absolute scientific output, market size, diplomatic capacity. Flag the assumption explicitly when it is not clearly met.

### 5.5 Simpson's Paradox

An aggregate trend can run in the opposite direction from every sub-group trend if sub-group sizes are unevenly distributed. Before reporting any aggregate change, decompose it into within-group and compositional (between-group) components.

**Mandatory check for Polish wage data:** Rising average wages in a period of structural employment shift should be decomposed into (a) wage growth within sectors and (b) compositional effect of employment moving toward higher-wage sectors.

### 5.6 CAGR

Appropriate only for smooth trajectories without structural breaks. Do not apply CAGR across the 2008–09 crisis, the 2020 COVID contraction, or the 2004 EU accession. Across these periods: report pre-break trend, post-break trend, and cumulative change from the anchor year.

### 5.7 Definition Consistency Across Time

Before constructing a long time series for Poland, check for definitional breaks:

| Break | Series affected |
|-------|----------------|
| 2012 | Wage survey coverage threshold changed from 5+ to 10+ employees |
| 2010 | GDP series affected by ESA 2010 revision |
| 2020 | Employment data affected by Anti-Crisis Shield reporting changes |
| Ongoing | Registered unemployment (GUS/PUP) vs LFS unemployment (BAEL) — not comparable |

When the series crosses a definitional break, either use the break-adjusted series (if available from GUS/Eurostat) or flag the break explicitly. Do not imply continuity across a break.

---

## 6. Worked Example — Labour Market Analysis

**Situation:** Poland's LFS unemployment rate for Q4 2024 is released at 2.8%.

**Step 1 — Which move?** *Change* (latest vs previous period) + *Compare* (vs EU average, vs V4 peers).

**Step 2 — Is it interesting?**
- Statistical significance: Q3 2024 was 2.9%. Change = 0.1 pp. Within LFS sampling error (~±0.4 pp). **Not statistically distinguishable from Q3 — report as "broadly stable."**
- Practical significance: 2.8% is below the 5% EU "full employment" benchmark — crossed several years ago, not new.
- Named threshold: No threshold crossed.
- Rate of change: The level (2.8%) is at a structural floor — the level is the finding, not the quarter-on-quarter change.
- Deviation from expectation: Below EU27 average (6.0% in Q4 2024). This gap is the story.

**Step 3 — Hierarchy:**
- **Headline:** Poland's unemployment rate (2.8%) is less than half the EU average (6.0%), continuing its position as one of the tightest labour markets in the bloc.
- **Evidence:** LFS Q4 2024, seasonally adjusted. Broadly unchanged from Q3 (2.9%, within sampling error). EU27 average: 6.0% (Eurostat, Q4 2024).
- **Context:** Poland entered the EU in 2004 with ~19% unemployment. The transformation to near-full employment represents a 16-percentage-point structural decline. Since ~2021, unemployment has been at or below 3% — a historically unprecedented sustained level.
- **Caveats:** LFS unemployment excludes persons not actively seeking work. Structural labour shortage (unfilled vacancies above 100,000) coexists with this rate. NEET rate and long-term inactivity are better indicators of remaining labour market slack.

**Step 4 — Aggregation check:**
- Is this the right aggregation? LFS quarterly rate is the correct indicator for labour market status. ✓
- Is the comparison valid? Comparing to EU27 is appropriate for convergence analysis. Use PPS for wage comparisons, not nominal. ✓
- Definitional consistency? LFS definition applied consistently across Poland and EU27 (ILO harmonised). ✓
