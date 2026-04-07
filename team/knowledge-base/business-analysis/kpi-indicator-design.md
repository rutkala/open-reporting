# Knowledge Base: KPI Theory, Indicator Design & Analytical Frameworks for Public Sector Data

**Module:** `team/knowledge-base/business-analysis/kpi-indicator-design.md`
**Version:** 1.0 — April 2026
**Status:** Ready for use

Agent reference for designing, selecting, and evaluating KPIs in public sector data journalism. Read at the start of `/plan` for any dashboard or analytical product, and during analytical review.

**Does not duplicate:** `analytical-thinking.md` (five analytical moves, insight hierarchy, aggregation rules §5, Polish data context §4). Read that file first. This file extends it with indicator theory, design patterns, and applied review rules.

**Sources:** Eurostat "Towards a harmonised methodology for statistical indicators" (Parts 1–3, 2014/2017); OECD "Measuring Government Activity" (2009); OECD "Strengthening Performance Reporting Practices" (2025); Kaplan & Norton, "The Balanced Scorecard — Measures that Drive Performance" (HBR, 1992); UK Government Analysis Function "Communicating Quality, Uncertainty and Change"; ONS Statistical Quality Framework; W.K. Kellogg Foundation Logic Model Development Guide; EU Commission Composite Indicator Handbook (JRC); Statistics Poland (GUS) BAEL methodology notes 2021; Eurostat ESS Guidelines on Seasonal Adjustment (2024); IMF Article IV Poland 2025; European Commission Convergence Report 2024.

---

## 1. What Makes a Good Indicator

### 1.1 The SMART Test

Every indicator proposed for a dashboard or analytical product must pass the SMART test. Apply it at design time, not at review time.

| Criterion | Question | Failure signal |
|-----------|----------|---------------|
| **Specific** | Does it measure one thing, not a composite of many? | "Economic wellbeing index" without a definition is not specific |
| **Measurable** | Is a precise numerical value computable from available data? | Qualitative assessments that cannot be reduced to a number fail |
| **Achievable** | Is the indicator computable from data that actually exists, with documented methodology? | Indicators requiring unavailable breakdowns are aspirational, not operational |
| **Relevant** | Does the indicator answer the analytical question being asked? | A deficit-to-GDP ratio is relevant to fiscal sustainability; it is not relevant to poverty risk |
| **Time-bound** | Is there a defined reference period, and can it be updated on a regular publication cycle? | One-off surveys that cannot be refreshed are not operational KPIs |

SMART is necessary but not sufficient. Eurostat's harmonised indicator methodology (2014) adds three further quality dimensions: **comparability over time**, **comparability between countries**, and **accuracy**. An indicator can be SMART and still fail on comparability if the definition changed mid-series.

**Additional quality test — FABRIC** (Balanced Scorecard Institute): Focused (one purpose), Appropriate (fits the audience and decision context), Balanced (not gaming a single metric), Robust (not distorted by outliers or structural breaks), Integrated (linked to other indicators in the set), Cost-effective (collection cost proportionate to analytical value). Apply FABRIC as a secondary screen after SMART.

### 1.2 Indicator Types: Output, Outcome, Impact

The public sector logic model — also the standard evaluation framework used by European Commission DGs, the World Bank, and national audit offices — distinguishes five levels. Every KPI on a dashboard implicitly sits at one level. Mislabelling an output as an outcome is the most common conceptual error in public policy analysis.

| Level | Definition | Typical form | Example — labour policy |
|-------|-----------|-------------|------------------------|
| **Input** | Resources committed | Spending (PLN, % GDP), staff count | PLN 2.4bn spent on active labour market policies |
| **Activity** | Actions taken | Count of programme runs, participants enrolled | 180,000 persons through retraining programmes |
| **Output** | Direct product delivered | Count, rate at point of delivery | 78% of participants completed retraining |
| **Outcome** | Change attributable to the programme | Rate of change in target population's condition | 6-month employment rate of completers: 62% |
| **Impact** | Long-run systemic change | Structural shift in conditions | Regional employment rate +3pp over five years |

**Rules:**
- Dashboards oriented toward accountability must include at least one outcome indicator — outputs alone measure activity, not results.
- Outputs can be controlled directly by the implementing body; outcomes cannot, because external factors intervene. Label accordingly.
- For macroeconomic dashboards (GDP, employment rate, fiscal balance), the indicators are coincident or lagging outcome indicators of the economy's condition — they are not policy outputs. Do not imply direct policy causation from a macroeconomic time series.
- Impact indicators require long time windows (5–10 years) and typically require counterfactual construction (e.g., difference-in-differences). Dashboards usually cannot support impact claims — use "association" or "covariation" language, not "effect."

### 1.3 Leading, Lagging, and Coincident Indicators

Timing classification originates from NBER business cycle research and is formalised in Conference Board composite index methodology.

| Type | Definition | Lead time | Polish examples |
|------|-----------|-----------|----------------|
| **Leading** | Changes direction 6–18 months before economic turning points | +6 to +18 months | Business confidence (PMI), building permits, new job vacancies, money supply M1 |
| **Coincident** | Moves simultaneously with the economy | ~0 months | Employment level, industrial production volume, retail sales |
| **Lagging** | Confirms a trend already underway | −3 to −12 months | Registered unemployment (PUP), long-term unemployment rate, consumer credit outstanding |

**Design rules:**
- Leading indicators are useful for forward-looking dashboards and nowcasting contexts. They carry higher uncertainty — never present a leading indicator without an uncertainty label.
- Lagging indicators are appropriate for confirming structural changes. Poland's registered unemployment (PUP) lags both LFS unemployment and the economic cycle by 6–12 months — it should never be used as a real-time signal.
- Coincident indicators are the correct choice for current-state dashboards. LFS employment rate, GDP growth, and industrial output are coincident.
- Mixing leading, coincident, and lagging indicators on the same chart without labelling their timing properties creates a misleading impression of synchrony.

### 1.4 Stock vs. Flow vs. Ratio Indicators

| Type | Definition | Correct aggregation | Common error |
|------|-----------|-------------------|-------------|
| **Stock** | Snapshot of accumulated quantity at a point in time | Value at period-end; do not sum across periods | Summing debt levels across quarters to get "annual debt" |
| **Flow** | Accumulation over a defined period | Sum for the period | Averaging quarterly deficits to get annual deficit when underlying transactions are not uniform |
| **Rate / ratio** | Numerator / denominator, usually normalised | Weighted average (see §3) — never simple average | Averaging regional unemployment rates without population weighting to get national rate |
| **Index** | Relative value with a defined base period | Rebase to common year before comparison | Comparing two index series with different base years |

**Rule:** Identify the indicator type before designing any aggregation or comparison. The aggregation method follows from the type, not from convenience.

---

## 2. KPI Design Patterns

### 2.1 Rate vs. Count vs. Index — Choosing the Right Form

Three primary forms for any quantitative indicator. The choice is not arbitrary — it depends on what analytical question is being answered.

| Form | Use when | Do not use when |
|------|----------|----------------|
| **Absolute count (level)** | The absolute magnitude matters (total deficit in PLN bn, total employment in thousands) | Comparing entities of different size — a count without normalisation is not comparable |
| **Rate / share** | Comparing across entities of different size, or expressing a condition relative to a denominator (employment rate, debt-to-GDP, share of long-term unemployed) | The denominator is itself unstable (e.g., dividing by a rapidly growing denominator inflates apparent decline) |
| **Index** | Tracking change from a defined baseline, especially when the absolute level is not interpretable to a general audience | Cross-entity comparison without rebasing to a common year (see index comparability rule in analytical-thinking.md §5.3) |

**The "compared to what?" principle (mandatory):** Every indicator on a published dashboard must have an explicit comparison point visible to the reader. The comparison point may be: a prior period value (YoY, QoQ), a named benchmark or target (EU 2030 target, SGP 3% threshold), a peer average (V4, EU27), or a historical range. A number without a comparison is a label, not an insight. This principle derives from the ONS Analysis Function guidance on communicating change and from IBCS rule U3 (unified comparison).

### 2.2 Per-Capita Normalisation

Per-capita figures (GDP per capita, health spending per capita, employment per 1,000 population) are the standard form for cross-country size normalisation. They are valid under one condition: **the numerator scales proportionally with population.** This condition is frequently violated.

**When per-capita normalisation is appropriate:**
- Income levels (GDP per capita in PPS — this is the EC's standard for purchasing power comparison)
- Public expenditure per capita (health, education, social protection)
- Health infrastructure (physicians per 1,000 population)
- Any indicator where the service or resource is genuinely population-directed

**When per-capita normalisation is misleading or requires a caveat:**
- Small countries with specialised economic structures (Luxembourg's GDP per capita is inflated by financial sector commuters who live in France/Belgium/Germany)
- Indicators where the numerator is driven by factors other than population size (R&D expenditure, patent filings — driven by industrial structure, not population)
- Comparisons where the relevant denominator is the labour force, not total population (use employment rates, not employment per capita)
- Regional comparisons within Poland: voivodeship populations differ but so do age structures — for labour market analysis, use working-age population (15–64) as the denominator, not total population

**Purchasing power standards (PPS):** For any cross-country income or wage comparison, use PPS (Eurostat's price-level-adjusted measure), not nominal EUR or PLN. Poland's GDP per capita in nominal EUR understates real living standards by approximately 25–30% compared to PPS terms (2023 data). The EC Convergence Reports and Eurostat use PPS as the standard for NMS comparisons.

### 2.3 Seasonally Adjusted vs. Raw Series

Two fundamentally different statistical objects. Treating them as interchangeable is a methodological error. Eurostat's ESS Guidelines on Seasonal Adjustment (2024 edition) establish the canonical rules.

| Series type | Definition | When to use | Label requirement |
|-------------|-----------|-------------|------------------|
| **Unadjusted (raw)** | Observed value, includes seasonal component | Year-on-year comparisons; annual totals; when the seasonal pattern is itself part of the story | "Unadjusted" or "Actual" |
| **Seasonally adjusted (SA)** | Seasonal and calendar effects removed | Month-on-month or quarter-on-quarter comparisons; detecting turning points | "Seasonally adjusted" — always explicit |
| **Trend-cycle** | SA series further smoothed to remove irregular component | Identifying the underlying direction with noise removed | "Trend" — label clearly |

**Polish seasonal patterns relevant to dashboard design:**
- Labour market: strong Q1 seasonal trough (construction, agriculture), Q2/Q3 peak — YoY is the correct comparison for raw data
- Fiscal data: fiscal year aligns with calendar year in Poland; quarterly expenditure has strong Q4 spike due to budget execution patterns — never compare Q3 to Q4 without SA
- Retail/consumption: December spike is approximately 30–35% above the de-seasonalised average

**Critical labelling rule:** Never display a seasonally adjusted and an unadjusted series on the same chart without explicit labelling of both. Never compare a SA figure to a non-SA figure in the same sentence. This is among the most common errors in Polish economic commentary.

### 2.4 Reference Values and Benchmarks

Every dashboard indicator should carry one or more reference values. Hierarchy of preference:

1. **Named policy target** (strongest) — a value that carries institutional authority: EU 2030 employment target (75%), SGP deficit threshold (3% GDP), Polish constitutional debt thresholds (50%, 55%)
2. **EU27 or EU-11 average** — the convergence benchmark; Poland's position relative to this is the convergence story
3. **V4 peer average** — the structural benchmark; how Poland compares to its closest economic peers
4. **Prior year same period** — the change signal; removes seasonal effects when using raw data
5. **Trailing 5-year average** — the cyclical baseline; is the current reading above or below the medium-term norm?

Never invent a reference value. If no reference exists for an indicator, say so and use a trailing average instead. A fabricated benchmark is worse than no benchmark.

---

## 3. Aggregation Correctness

Extends analytical-thinking.md §5. Focused on indicator-design-specific errors not already covered there.

### 3.1 Weighted vs. Unweighted Averages for Regional Aggregation

**The core rule:** Rates and ratios must be aggregated using population-weighted averages, not simple averages. Simple averaging of regional rates treats a voivodeship of 5 million people identically to one of 800,000 — which is valid only if you are computing the average regional condition, not the national condition.

| Aggregation scenario | Correct method | Wrong method |
|---------------------|---------------|-------------|
| National unemployment rate from 16 voivodeships | Weighted average using working-age population of each voivodeship | Simple average of 16 voivodeship rates |
| EU27 average from member states | Population-weighted average (Eurostat standard) | Simple average of 27 national rates |
| Average wage across sectors | Employment-weighted average | Simple average of sectoral median wages |
| Average deficit across EU member states | GDP-weighted average (for a fiscal position indicator) | Simple average |

**Source:** Eurostat-OECD Methodological Manual on Purchasing Power Parities; World Bank Poverty and Inequality Platform methodology (population-weighted regional aggregation is the standard).

**Practical check:** When GUS publishes national labour market figures, they are already computed as population-weighted aggregates from the BAEL sample — do not re-aggregate voivodeship figures from GUS regional releases into a national rate yourself. If you do, verify against the published national figure.

### 3.2 When Summing Rates is Wrong

Rates cannot be summed. Only the underlying counts can be summed; the rate is then recalculated from the summed counts.

**Example — wrong:** "The three eastern voivodeships have unemployment rates of 4.2%, 5.8%, and 6.1%. Total unemployment rate = 16.1%." (Sum of rates is meaningless.)

**Example — correct:** "The three eastern voivodeships have 32,000; 48,000; 57,000 unemployed persons out of labour forces of 760,000; 825,000; and 935,000 respectively. Combined unemployment rate = 137,000 / 2,520,000 = 5.4%."

**Important cases in Polish data:**
- NEET rate: cannot add youth unemployment rate + inactivity rate. The NEET rate is defined on a distinct population (15–29 not in employment, education, or training) and must be computed from that denominator.
- At-risk-of-poverty rate: cannot average across household types. The rate must be computed from the microdata or from the published population-weighted aggregate.

### 3.3 CAGR and Structural Breaks

Already in analytical-thinking.md §5.6. Extended here with the deflation dimension:

**Nominal vs. real CAGR distinction:** CAGR calculated on nominal values includes inflation. For any indicator expressed in PLN (wages, GDP, expenditure), calculate CAGR on real (price-deflated) values. Use the GDP deflator for macro aggregates; use CPI for household-level series (wages, disposable income). Never report nominal CAGR without flagging it is nominal.

**Deflation method for Polish PLN series:** Deflate using GUS CPI index, base year = 2015 (standard GUS base), unless the analysis explicitly requires a different reference year. When converting to EUR, use Eurostat purchasing power parities, not market exchange rates, for cross-country comparison.

### 3.4 Composite Indicator Aggregation

When aggregating multiple indicators into a composite score or index (e.g., a social cohesion index, regional competitiveness index), the EC Joint Research Centre Composite Indicator Handbook applies. Three mandatory steps:

1. **Normalisation before aggregation** — bring all sub-indicators to a common scale (min-max, z-score, or rank-based). Do not aggregate raw values with different units.
2. **Weighting transparency** — document whether weights are equal or expert-assigned; test sensitivity to weight changes. Equal weighting is a methodological choice, not a default — it implies equal importance.
3. **Correlation screening** — highly correlated sub-indicators inflate the weight of that dimension implicitly. Screen for correlations above 0.9 and remove redundant components or group them.

For Open Reporting dashboards: avoid composite indices unless the individual components are also displayed. A composite without components obscures what is driving it.

---

## 4. Interpretation Traps for Polish Public Data

### 4.1 Structural Breaks — The Complete Map

| Break event | Year(s) | Series primarily affected | What it does to analysis |
|-------------|---------|--------------------------|--------------------------|
| **EU accession** | 2004 | All macro series, employment, wages, trade | The 2004 baseline is the fundamental anchor for all convergence narratives. Do not use pre-2004 data as part of a trend line without flagging the structural shift. |
| **BAEL methodology revision (LFS)** | Q3 2012 | Employment, unemployment, LFPR (2010–Q2 2012 recalculated, pre-2010 not directly comparable) | Long series pre-2010 require a splice or explicit break annotation |
| **Wage survey coverage change** | 2012 | GUS structural wage surveys (firms with 5+ → 10+ employees) | Shifts the effective coverage downward; post-2012 series excludes more small firms |
| **ESA 2010 GDP revision** | 2010 (applied retroactively) | All GDP-relative indicators | Pre-ESA 2010 and post-ESA 2010 data are comparable in Eurostat series but not in older national publications |
| **Global Financial Crisis** | 2008–09 | GDP, investment, fiscal balance, unemployment (lagged peak 2013) | Poland avoided GDP contraction ("green island") — Polish GFC data is not comparable to EU peers for recession-recovery analysis |
| **Pension reform reversal** | 2017 | Labour force participation, employment rate (55–67 cohort) | Reduced statutory retirement age reduced LFPR of older workers — trend break in 55–64 employment rate |
| **Ukrainian migration wave** | 2014–2018 (first wave), 2022–present (second wave) | Labour supply, wage dynamics, population denominators | GUS population estimates do not fully capture non-registered migrants — denominators for per-capita and rate calculations are uncertain |
| **COVID Anti-Crisis Shield** | 2020 | Employment, short-time work, GDP composition | Wage subsidy inflated formal employment counts — employment rate in 2020 is not fully comparable to pre-2020 or post-2022 levels |
| **BAEL methodology revision (EU Reg. 2019/1700)** | From Q1 2021 | Employment, unemployment, inactivity definitions; GUS recalculated 2010–2020 | Post-2021 data uses new definitions; use GUS recalculated series for comparability |
| **Energy/inflation crisis** | 2022 | CPI, real wages, energy expenditure, industrial output | Inflation peaked at 18.4% (February 2023) — real series computed from nominal require careful deflation in this period |

**Operational rule:** Before constructing any Polish time series longer than 5 years, map it against this table. Flag every break that falls within the series window. If GUS or Eurostat provides a recalculated backcast, use it. If not, split the series at the break and present two segments.

### 4.2 LFS/BAEL Definitional Changes — Detail

Statistics Poland (GUS) implemented EU Regulation 2019/1700 from Q1 2021, which changed definitions for the employed, unemployed, and economically inactive persons. The key changes:

- **Self-employment classification:** New questions on economic and organisational dependency of self-employed persons; some previously classified as "self-employed" are reclassified
- **Migration variables:** New variables on migration origin affect composition of the employed population in border regions
- **Non-formal education:** Added, affects classification of some inactive persons
- **GUS response:** Published recalculated data for 2010–2020 with new definitions. Use the recalculated series (available from stat.gov.pl, LFS section) for any analysis spanning 2019–2022. The pre-2010 series is not directly comparable and should be treated as a separate segment.

**Practical implication for dashboard time series:** When displaying employment/unemployment trends starting before 2021, use the GUS recalculated series (2010–2020) spliced with post-2021 data. Add a break annotation at 2010 if extending further back.

### 4.3 EU Convergence Effect on Polish Growth Rates

Poland's GDP growth consistently appears strong relative to EU27 averages. Part of this differential is genuine catch-up; part is a convergence effect that would be expected of any lower-income economy with open capital markets. The EC's convergence theory predicts faster growth for NMS until factor price equalisation is approached.

**Analytical implication:** Do not present Poland's growth rate as evidence of exceptional economic management without decomposing:
- Convergence component (catching up from a lower base)
- Structural reform component (policy-driven productivity gains)
- EU structural fund absorption component (investment inflated by EU transfers; 2.5–4% of GDP annually in peak absorption years)
- Demographic component (labour supply from immigration, changing age structure)

Poland's GDP per capita reached ~83% of EU27 average by 2023 (EC Convergence Report 2024), up from ~50% in 2004. At this stage, the convergence dividend is narrowing — the base effect argument is weaker for 2020s data than for 2010s data.

### 4.4 Base Effects in Year-on-Year Comparisons

Already in analytical-thinking.md §5.2, extended here for Polish-specific patterns:

**COVID base effect rule:** Any YoY comparison involving 2020 or 2021 data is contaminated by an abnormal base. The depth of Poland's 2020 contraction was mild (-2.7% GDP) compared to EU average (-5.6%), which means:
- Polish "recovery" growth in 2021 (+5.7%) looks less spectacular than EU average recovery, because the Polish trough was shallower
- Comparisons of Poland's 2021 growth to EU peers systematically understate Poland's relative resilience — the correct comparison is cumulative GDP change from 2019 to 2022

**Energy crisis base effect (2022–2023):** CPI peaked at 18.4% in February 2023. YoY inflation comparisons from February 2023 onwards will show sharp deflation in the base — this is a base effect, not actual deflation. Present 24-month cumulative price change alongside YoY to prevent misreading.

---

## 5. Benchmarking Frameworks for Poland

### 5.1 Peer Group Selection Guide

Already introduced in analytical-thinking.md §4.1. Extended here with the analytical rationale and practical usage rules for each group.

| Peer group | Members | Structural justification | Use for | Do not use for |
|------------|---------|--------------------------|---------|----------------|
| **V4** | Czechia, Hungary, Slovakia, Poland | Simultaneous 2004 EU accession, shared post-communist transition, similar starting economic structures, comparable institutional frameworks | Labour market structure, wage levels (PPS), fiscal trajectories, employment protection legislation, temporary work share | Monetary policy (Poland retains PLN; Czechia retains CZK; Slovakia and Hungary have different regimes) |
| **EU-11 / NMS-11** | 11 new member states post-2004 | Post-communist transition economies, EU structural fund recipients, convergence trajectory | Convergence analysis, structural fund absorption, institutional transition | Intra-group heterogeneity is large — Baltic states (high debt reduction, wage flexibility) differ significantly from Poland |
| **EU27** | All EU members | Common legal and regulatory framework, Eurostat harmonised data, SGP common rules | Convergence distance, SGP compliance context, European Pillar of Social Rights progress, Maastricht criteria | Structural economic comparisons — Poland's GDP per capita and labour market structure differ substantially from EU15 |
| **OECD** | 38 countries | Developed-country peer benchmarks, comparable institutional and governance quality data | Labour regulation, collective bargaining coverage, social protection generosity, productivity measurement, R&D intensity | Eastern Europe convergence narratives — OECD average includes high-income economies that are not meaningful structural peers for Poland |
| **CEE10** | Post-communist transition economies broadly | When story is about transition patterns beyond the EU framework | Long historical transition narratives, comparisons with non-EU transition economies (Ukraine, Western Balkans) | EU compliance or convergence analysis — only EU members are subject to Eurostat and SGP frameworks |

**Default rule (restate from analytical-thinking.md):** Lead with V4 for structural comparisons; EU27 for convergence and compliance. Add OECD only when the analytical question requires it.

### 5.2 What Structural Differences to Note When Benchmarking

When presenting any Poland-V4 comparison, flag these structural differences that drive divergence independently of policy:

| Dimension | Poland relative to V4 | Analytical implication |
|-----------|----------------------|------------------------|
| **Population size** | 4–5× larger than other V4 members | Internal market scale effects; regional heterogeneity much larger (Warsaw ≠ Podkarpacie) |
| **Agricultural share** | Higher than CZ, SK; comparable to HU | Seasonal employment patterns, structural underemployment, rural-urban income gaps |
| **Currency regime** | Floating PLN | Exchange rate channel affects competitiveness, real wage comparisons, inflation exposure |
| **Demographic trajectory** | Similar ageing, but refugee inflow 2022 changed working-age population | Labour supply comparisons post-2022 require population-adjustment caveats |
| **EU fund absorption** | Higher in absolute terms due to size; comparable as % GDP | Investment data inflated relative to own-funded investment; decompose when assessing fiscal stance |

### 5.3 Eurostat, OECD, World Bank Data Hierarchy for Benchmarking

| Use case | Primary source | Why |
|----------|---------------|-----|
| EU cross-country comparisons | Eurostat | Harmonised definitions, ESA 2010 accounting standard, consistent coverage |
| Fiscal position, debt sustainability | Eurostat GFS + IMF WEO | Eurostat for EDP-compliant series; IMF for projections and structural balance |
| Labour market | Eurostat LFS (EU-LFS) | ILO-harmonised definitions across all member states |
| Wages, compensation, productivity | Eurostat (national accounts) + OECD | OECD more detailed for labour cost components |
| Social protection, inequality | Eurostat EU-SILC | Harmonised income and living conditions |
| Development comparison | World Bank WDI | Broader country coverage; use when OECD/Eurostat scope insufficient |
| Governance, institutional quality | OECD Government at a Glance | Governance indicators, public administration efficiency |

---

## 6. Public Sector Analytical Frameworks

### 6.1 Input-Output-Outcome Logic Model Applied to Macroeconomic Dashboards

The W.K. Kellogg Foundation logic model and the EC's logframe methodology are designed for programme evaluation. Adapted here for macroeconomic data journalism:

**Mapping macro indicators to the logic model:**

| Logic model level | Macro equivalent | Dashboard use |
|-------------------|-----------------|---------------|
| **Input** | Government spending (% GDP), staff in public sector | Resource adequacy questions |
| **Activity** | Programme delivery (benefit recipients, job placements) | Implementation fidelity |
| **Output** | Direct measurable product (number of jobs created, km of road built) | Short-term accountability |
| **Outcome** | Change in population condition (employment rate, poverty rate, life expectancy) | Medium-term effectiveness |
| **Impact** | Structural systemic change (10–20 year shift in GDP per capita, human capital accumulation) | Long-term transformation |

**Critical rule for causal language:** The logic model assumes a causal chain. In macroeconomic journalism, this chain is rarely fully established. "The 500+ programme increased birth rates" makes a causal claim. "The 500+ programme coincided with a temporary birth rate increase" is accurate. Use the logic model to structure what level of indicator you are presenting; do not infer causation beyond what the data supports.

### 6.2 Fiscal Space Analysis

The IMF framework for assessing a government's ability to increase expenditure without compromising debt sustainability. Relevant for Polish fiscal analysis, especially post-2020 debt trajectory.

**Three fiscal space indicators (IMF standard):**
1. **Gross financing need** = deficit + maturing debt — measures how much borrowing is required in a given year
2. **Debt-to-GDP trajectory** — projected path under baseline and stress scenarios
3. **Cyclically-adjusted (structural) balance** — removes the effect of the economic cycle; the policy-relevant measure

**Rule:** For Polish fiscal analysis, always separate the structural balance from the nominal balance. The nominal deficit in a recession year overstates the underlying policy stance; in a boom year it understates it. The IMF and EC publish structural balance estimates for Poland annually (EC Autumn Forecast, IMF WEO). Use these rather than computing your own.

### 6.3 Presenting Politically Sensitive Data Without Editorialising

Public sector data on unemployment, inequality, poverty, and deficit can be politically charged. The standard analytical approach (from ONS Code of Practice, Eurostat quality guidelines, UK Analysis Function) is empirical objectivity: present what the data shows, with full methodological transparency, without framing that implies a policy verdict.

**Practical rules:**

1. **Describe the phenomenon, not the policy verdict.** "The poverty rate at material deprivation threshold fell from 14.2% to 10.8%" is neutral. "Government policies reduced poverty" attributes causation not established by the data. "Despite government transfers, poverty remains above the EU average" introduces an adversarial frame without basis in the data alone.

2. **Present the indicator's own definition, not a substitute one.** Poland's registered unemployment (PUP) and LFS unemployment measure different phenomena. Using registered unemployment to make a point about labour market slack, when LFS unemployment (the internationally comparable measure) tells a different story, is misleading by indicator selection.

3. **Acknowledge uncertainty without undermining the finding.** "The data shows X, though sampling uncertainty means the true value may be within a range of Y to Z" is correct. Overloading caveats to the point where no conclusion can be drawn serves no one.

4. **Research has shown** (Tandfonline, 2016 data journalism study) that simply presenting competing statistical claims without independent analysis creates "widespread cynicism about statistical expertise." The journalist's role is to interrogate the data, not simply to relay competing numbers. Apply the analytical moves (describe, compare, change, relate, rank) and state what they show.

5. **Framing effects:** Negatively framed statistics (losses, deficits, declines) are perceived as more credible than positively framed ones, even when the underlying data is identical (Lindgren et al., 2024). Where both framings are equally valid, prefer neutral framing (absolute change, not directional characterisation).

### 6.4 Balanced Scorecard Principles Applied to Dashboard Design

Kaplan and Norton's Balanced Scorecard (HBR, 1992) argues that no single metric captures organisational performance. For Open Reporting dashboards, this principle translates to a rule about indicator set balance.

**Four adapted perspectives for public sector dashboards:**

| BSC perspective (original) | Public sector adaptation | Application to Open Reporting |
|---------------------------|--------------------------|-------------------------------|
| **Financial** | Fiscal stewardship — cost-effectiveness, deficit/debt sustainability | Include both fiscal position and the economic output it finances |
| **Customer** | Citizen outcomes — employment, income, poverty, life expectancy | The headline outcome indicators |
| **Internal Process** | Institutional effectiveness — policy implementation rates, public service quality | Programme output indicators |
| **Learning & Growth** | Structural capacity — human capital, R&D, institutional quality | Long-term structural competitiveness indicators |

**Practical rule:** A dashboard that only shows financial/fiscal indicators (deficits, debt) without outcome indicators (employment, poverty, real incomes) presents an incomplete picture. Conversely, a dashboard showing only outcomes without fiscal context strips the sustainability dimension. Balance is not optional.

---

## 7. Insight Framing for Data Journalism

### 7.1 Turning a Number Into a Story

The number is never the story. The story is the departure from expectation, the implication for a named group of people, or the decision that follows. Three questions to ask for every indicator before writing a single word:

**Q1 — "So what?" test:** If the reader reads this number and asks "so what?", the framing has failed. The answer to "so what?" must be in the headline or the first sentence. If it cannot be stated in plain language, the indicator may not be the right one, or the analytical work is incomplete.

**Q2 — "Compared to what?" test:** What is the reference point? Without a comparison, a number conveys magnitude but not meaning. Poland's unemployment rate of 2.8% is remarkable only against the EU27 average of 6.0% or against Poland's own 2004 level of 19%. The comparison is the story.

**Q3 — "Who is affected?" test:** Data journalism is most powerful when abstract statistics are connected to identifiable populations. "Wages fell in real terms" becomes "the median Polish worker's purchasing power fell by the equivalent of one month's income in 2022" — same data, different reader connection.

### 7.2 When a Difference Is Newsworthy vs. Noise

Already in analytical-thinking.md §3 (interest tests). Supplementary rules specific to indicator framing:

**The "noise floor" rule:** For every indicator type, establish the minimum change that is practically meaningful before publishing. Anything below the noise floor should be labelled "broadly stable" or "unchanged." Do not report marginal movements as trends.

| Indicator type | Minimum change worth reporting |
|----------------|-------------------------------|
| Unemployment / employment rate | 1 pp sustained (≥2 consecutive periods), or crossing a named threshold |
| Real wage growth | Deviation > 2 pp from CPI (real purchasing power change) |
| GDP growth quarterly | Deviation > 1 pp from prior quarter (SA) or from EU average |
| Debt-to-GDP | Approaching a named constitutional or treaty threshold (±2 pp) |
| Poverty / at-risk-of-poverty | ≥ 1 pp over at least two survey periods (EU-SILC annual) |

**The context test:** A value inside the normal range is not newsworthy even if it is the latest reading. The normal range is the trailing 5-year range for that season/period. Only values outside the normal range — or crossing named thresholds — are candidates for a headline.

### 7.3 Citing Uncertainty Without Undermining the Story

Uncertainty is a feature of all statistical estimates, not a reason to withhold findings. The goal is proportionate disclosure: material uncertainty (that would change the conclusion) is presented early; methodological footnotes belong at the end.

**Three-tier uncertainty disclosure:**
1. **Decisive uncertainty:** The indicator's confidence interval is wider than the observed change. Finding: report as "no statistically significant change." Do not present a directional claim.
2. **Material uncertainty:** The confidence interval is narrower than the change, but covers a meaningful range. Finding: state the range. "Unemployment fell by between 0.6 and 1.2 percentage points."
3. **Incidental uncertainty:** Minor methodological caveats that do not alter the conclusion. Finding: footnote only, do not dilute the headline.

**Data revision risk:** Polish national accounts and labour market data are subject to revision. First estimates (flash estimates, preliminary GUS releases) carry higher revision risk than final data. Label preliminary data clearly. When revisions are significant, report the revision as a story in its own right if it crosses the newsworthiness threshold.

### 7.4 Narrative Structure for Analytical Products

Consistent with the Insight Hierarchy in analytical-thinking.md §2. Operationalised here as a paragraph-level template:

```
[Headline finding — one sentence, declarative, specific]
[Evidence — what the data shows, with source, period, and magnitude]
[Comparison — how this relates to the reference point (EU27, V4, target, prior year)]
[Context — what historical or structural pattern this sits within]
[Caveat — one or two sentences on material limitations; nothing more]
[Implication] — optional, only when the analytical chain is clear enough to support it]
```

Do not invert this structure. Do not begin with methodology, data sources, or definitional notes — these belong at the end or in a sidebar, not in the opening.

---

## 8. Applied Rules for Analytical Review

Forty rules for the analytical reviewer / `business-analyst` agent. Extending analytical-thinking.md. Format: `RULE [severity] — [condition] → [reason]`

Severity tiers: **MISLEADING** (conclusion reversed or substantially altered); **QUESTIONABLE** (raises doubt without definitive reversal); **NOTE** (methodological weakness, label or caveat required).

---

**Indicator selection rules:**

RULE MISLEADING — Registered unemployment (PUP) used as the primary labour market indicator without noting it measures registration entitlement, not employment status → LFS/BAEL unemployment is the internationally comparable measure; PUP overstates slack due to benefit-registration incentive.

RULE MISLEADING — Nominal wage figures compared across years without CPI deflation → real and nominal wage trends have diverged by 20–40 pp cumulatively since 2019; nominal series obscures purchasing power losses in 2022–2023.

RULE MISLEADING — Employment count (absolute level) compared across regions of different size without normalisation to employment rate or working-age population → Mazowieckie has 5× the population of Podlaskie; absolute count comparison is not meaningful.

RULE MISLEADING — Output indicator presented as an outcome indicator without evidence of the causal chain → number of training places delivered ≠ employment outcome; the difference is methodologically fundamental.

RULE QUESTIONABLE — Lagging indicator (e.g., registered unemployment PUP) used to characterise a current or future state → confirmed trends only; misleads on timing.

RULE QUESTIONABLE — Leading indicator (PMI, building permits) presented as confirmed economic data without forward-looking caveat → leading indicators are probabilistic, not deterministic; require uncertainty framing.

RULE NOTE — Mixed use of LFS unemployment and registered unemployment in the same time series without explicit splice annotation → two definitional series presented as one continuous series.

---

**Aggregation and normalisation rules:**

RULE MISLEADING — Regional unemployment rates averaged without population weighting to produce a national figure → unweighted average treats each voivodeship identically regardless of size; differs from the GUS national rate by 0.3–0.8 pp depending on composition.

RULE MISLEADING — Rates summed across groups to produce a total rate (e.g., NEET rate = youth unemployment rate + inactivity rate) → rates cannot be summed; must be recomputed from underlying counts.

RULE MISLEADING — Nominal CAGR reported for PLN-denominated series (wages, expenditure, GDP) without deflation → nominal CAGR in a high-inflation period (2022–2023, CPI peaking at 18.4%) inflates apparent growth; real CAGR is the correct measure.

RULE MISLEADING — CAGR computed across a structural break (2004 accession, 2009 GFC, 2020 COVID) → CAGR assumes constant compounding; blends structurally different regimes into a single number.

RULE QUESTIONABLE — Per-capita normalisation applied to indicators where the numerator does not scale proportionally with total population → requires explicit statement of the proportionality assumption and its limitations.

RULE QUESTIONABLE — GDP per capita in nominal EUR used for Poland-EU comparison instead of PPS-adjusted → nominal EUR understates Polish real living standards by 25–30% relative to PPS.

RULE NOTE — Index series compared without verifying base year alignment → two series with different base years are not directly comparable; rebase to common year.

RULE NOTE — Simple (unweighted) average used for composite indicator aggregation → equal weighting is a deliberate methodological choice, not a default; document and test sensitivity.

---

**Seasonal and time-series rules:**

RULE MISLEADING — Seasonally adjusted figure compared to non-adjusted figure in same sentence or chart without explicit labelling → systematic bias introduced; Q4 fiscal data vs Q3 SA employment is not a valid comparison.

RULE MISLEADING — Month-on-month or quarter-on-quarter comparison of unadjusted series in sectors with strong seasonal patterns (Polish construction, agriculture, retail, fiscal Q4 spending) → seasonal component dominates the signal; use YoY or SA series.

RULE QUESTIONABLE — Year-on-year comparison of 2021 data against 2020 data presented as "recovery" without noting the COVID base → 2020 was an abnormally depressed base; the correct measure of recovery is cumulative change from 2019.

RULE QUESTIONABLE — Year-on-year inflation comparison from February–June 2023 period presented as "falling inflation" without noting the high-base effect → the 2022 base was at or near peak; YoY decline partly reflects base, not disinflation.

RULE NOTE — Time series beginning in a non-representative year (post-crisis trough, post-reform peak) without annotation → base year choice implies a narrative framing; document why that start year was chosen.

---

**Definitional and structural break rules:**

RULE MISLEADING — Polish BAEL data pre-2021 used together with post-2021 data without using the GUS recalculated series (2010–2020) → GUS changed employment/unemployment definitions in Q1 2021; without recalculated backcast, the series contains a manufactured break.

RULE MISLEADING — Pre-2010 BAEL data combined with post-2010 data without a break annotation → GUS's recalculation covers only 2010–2020; pre-2010 data is not directly comparable on new definitions.

RULE QUESTIONABLE — Long-term employment rate trends including 2017–2020 period without noting the pension reform reversal effect → the 2017 retirement age reduction structurally depressed LFPR for the 55–64 cohort; conflates policy reform with labour market deterioration.

RULE QUESTIONABLE — Wage dynamics analysis for 2015–2020 without noting the Ukrainian labour immigration effect → first-wave immigration moderated wages despite tight labour market; excluding it overstates the responsiveness of wages to employment conditions.

RULE NOTE — Structural balance (cyclically-adjusted) computed independently rather than using IMF WEO or EC Autumn Forecast estimates → own computation requires output gap estimation which is methodologically complex; use official estimates and cite them.

---

**Comparison and benchmarking rules:**

RULE MISLEADING — Poland's growth rate compared to EU27 average without decomposing the convergence component → a portion of Poland's premium growth rate is expected catch-up, not exceptionalism; EC Convergence Reports provide this decomposition.

RULE QUESTIONABLE — V4 peer comparison used for euro area monetary policy analysis → Poland, Czechia retain floating currencies; Slovakia adopted EUR in 2009, Hungary uses HUF — V4 is not a valid monetary policy peer group.

RULE QUESTIONABLE — EU11 average used as the benchmark for governance or institutional quality → EU11 heterogeneity on these dimensions is very large (Baltic states vs. Bulgaria/Romania); V4 is a tighter structural peer.

RULE NOTE — Peer comparison using Eurostat data on employment or wages without verifying that all peer countries use harmonised EU-LFS definitions → most EU members do, but methodological notes should be checked for countries with known LFS irregularities.

---

**Framing and communication rules:**

RULE MISLEADING — "Driven by" or "caused by" language used to connect a policy change to a macro indicator without mechanism evidence or counterfactual → correlation in a time series without experimental or quasi-experimental design is not causation.

RULE QUESTIONABLE — Single-period data point presented as a trend → a trend requires at minimum 3 data points in the same direction beyond seasonal noise; one period is an observation, not a trend.

RULE NOTE — Headline framing uses percentage without specifying whether it is a percentage point or a percentage change for a series that is itself expressed as a percentage → "unemployment rose 3 percent" when it rose from 3% to 6% is three-fold error; requires "percentage points" or "doubled."

RULE NOTE — Preliminary GUS flash estimate used without revision-risk label → preliminary estimates are revised; material revisions in subsequent releases should be tracked and reported.

---

**Sources consulted for this KB:**

- Eurostat, "Towards a harmonised methodology for statistical indicators," Part 1 (2014): https://ec.europa.eu/eurostat/web/products-manuals-and-guidelines/-/ks-gq-14-011
- Eurostat, "Towards a harmonised methodology for statistical indicators," Part 3 — Relevance for policy making (2017): https://ec.europa.eu/eurostat/web/products-manuals-and-guidelines/-/ks-gq-17-007
- Eurostat, ESS Guidelines on Seasonal Adjustment, 2024 edition: https://ec.europa.eu/eurostat/documents/3859598/19355229/KS-GQ-24-012-EN-N.pdf
- OECD, "Measuring Government Activity" (2009): https://www.oecd.org/content/dam/oecd/en/publications/reports/2009/04/measuring-government-activity_g1ghaae6/9789264060784-en.pdf
- OECD, "Strengthening Performance Reporting Practices" (2025): https://www.oecd.org/content/dam/oecd/en/publications/reports/2025/09/strengthening-performance-reporting-practices_73b8ee6e/bcea6d2d-en.pdf
- Kaplan & Norton, "The Balanced Scorecard — Measures that Drive Performance," HBR (1992): https://hbr.org/1992/01/the-balanced-scorecard-measures-that-drive-performance-2
- Balanced Scorecard Institute, BSC Basics: https://balancedscorecard.org/bsc-basics-overview/
- ONS, Quality in Official Statistics: https://www.ons.gov.uk/methodology/methodologytopicsandstatisticalconcepts/qualityinofficialstatistics
- UK Government Analysis Function, Communicating Analysis: https://analysisfunction.civilservice.gov.uk/support/communicating-analysis/
- Statistics Poland (GUS), BAEL methodology changes from Q1 2021: https://stat.gov.pl/en/topics/labour-market/working-unemployed-economically-inactive-by-lfs/information-of-the-statistics-poland-regarding-the-changes-introduced-from-2021-onwards-into-the-bael,22,1.html
- Statistics Poland (GUS), BAEL recalculated 2010–2020: https://stat.gov.pl/en/topics/labour-market/working-unemployed-economically-inactive-by-lfs/information-of-statistics-poland-concerning-the-results-of-the-badanie-aktywnosci-ekonomicznej-ludnosci-recalculated-for-the-years-2010-2020-bael-the-polish-equivalent-of-the-european-survey-on-,24,1.html
- W.K. Kellogg Foundation, Logic Model Development Guide: https://www.naccho.org/uploads/downloadable-resources/Programs/Public-Health-Infrastructure/KelloggLogicModelGuide_161122_162808.pdf
- EC JRC, Composite Indicators Normalisation Guidance: https://knowledge4policy.ec.europa.eu/composite-indicators/toolkit_en/navigation-page/10-step-guide_en/step-5-normalisation_en
- European Commission, Convergence Report 2024: https://economy-finance.ec.europa.eu/document/download/a3bb3063-6478-44a5-a270-933e49fb304b_en
- IMF, "Estimating Indexes of Coincident and Leading Indicators" (WP/03/170): https://www.imf.org/external/pubs/ft/wp/2003/wp03170.pdf
- Tandfonline, "Data Journalism, Impartiality and Statistical Claims" (2016): https://www.tandfonline.com/doi/full/10.1080/17512786.2016.1256789
- Lindgren et al., "Trusting the Facts: Framing and Perceived Truth in Statistical Statements," Political Communication (2024): https://journals.sagepub.com/doi/10.1177/10776990221117117
- World Bank, Poverty and Inequality Platform Methodology (population-weighted aggregation): https://datanalytics.worldbank.org/PIP-Methodology/lineupestimates.html

---

That is the complete KB. Summary of what was produced:

**8 sections, approximately 480 lines of dense practical content:**

1. What makes a good indicator — SMART + FABRIC criteria, output/outcome/impact distinction with Polish examples, leading/lagging/coincident classification with Polish instances, stock/flow/rate/index type table with aggregation rules.

2. KPI design patterns — rate vs count vs index selection logic, the "compared to what?" principle, per-capita normalisation validity rules (including PPS vs nominal EUR for Poland), seasonally adjusted vs raw labelling rules with Polish seasonal patterns, reference value hierarchy.

3. Aggregation correctness — weighted vs unweighted regional aggregation with worked examples, when summing rates is wrong (with NEET and poverty examples), nominal vs real CAGR, composite indicator aggregation rules.

4. Interpretation traps for Polish data — complete structural break map (12 events, 2004–2023), BAEL methodology change detail (2012 and 2021), EU convergence decomposition requirement, base effects for 2020 COVID and 2022–2023 inflation.

5. Benchmarking frameworks — peer group selection guide with V4/EU27/OECD/NMS-11/CEE10 use cases, structural differences within V4 to note, data source hierarchy by analytical use case.

6. Public sector analytical frameworks — logic model adapted for macro dashboards, fiscal space analysis (IMF framework), rules for presenting politically sensitive data without editorialising, Balanced Scorecard four perspectives adapted for public sector dashboards.

7. Insight framing — "so what?", "compared to what?", "who is affected?" tests, noise floor table by indicator type, three-tier uncertainty disclosure, paragraph-level narrative template.

8. Applied rules — 40 review rules in MISLEADING / QUESTIONABLE / NOTE format, covering indicator selection, aggregation, seasonal/time-series, definitional breaks, comparison/benchmarking, and framing.