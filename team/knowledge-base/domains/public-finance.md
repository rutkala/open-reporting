# Domain Brief: Public Finance

## What this domain is

Public finance tracks government revenue, expenditure, borrowing, and debt to assess fiscal sustainability and policy effectiveness. For Poland, it's particularly relevant due to EU membership obligations under the Stability and Growth Pact (SGP), ongoing EDP (Excessive Deficit Procedure) monitoring, and post-pandemic debt trajectory concerns.

**Polish context:**
- Member of EU since 2004, subject to SGP fiscal rules
- Currently under EDP due to deficit exceeding 3% threshold
- Public debt grew significantly post-2020 (COVID, refugees, reconstruction fund)
- Key institutions: Ministry of Finance (MF), NBP, Eurostat, IMF

---

## Key practitioners and their questions

**Primary users of public finance data:**
- **Economists at MF/NBP** — Policy design, debt sustainability analysis, EU compliance
- **EU/Eurostat analysts** — EDP notifications, Maastricht criteria assessment
- **IMF watchers** — Article IV missions, WEO projections
- **Journalists/analysts** — Budget news, deficit/debt trajectory stories
- **Investors/credit rating agencies** — Poland's fiscal credibility

**Questions they ask:**
1. Is the budget in deficit or surplus? How does it compare to 3% SGP threshold?
2. What's the debt trajectory? Is it sustainable (debt-to-GDP ratio)?
3. What's the structural balance (cyclically-adjusted)?
4. How does Poland compare to EU peers (V4, Eurozone)?
5. What drives the deficit (recurrent vs capital)?
6. Interest burden — how much of budget goes to debt service?

---

## Standard KPIs

| KPI | Definition | Unit | Standard breakdown |
|-----|-----------|------|-------------------|
| **Fiscal balance (deficit/surplus)** | Revenue - Expenditure | % GDP | Annual, quarterly |
| **Primary balance** | Fiscal balance excluding interest | % GDP | Annual |
| **Structural balance** | Cyclically-adjusted, excludes one-off items | % GDP | Annual |
| **Public debt (gross)** | Total government liabilities | % GDP | Annual, quarterly |
| **Public debt (net)** | Gross debt minus liquid assets | % GDP | Annual |
| **Interest expenditure** | Debt servicing costs | % GDP | Annual |
| **Revenue** | Total government receipts | % GDP | By type (taxes, contributions, other) |
| **Expenditure** | Total government spending | % GDP | By COFOG function |
| **Primary expenditure** | Expenditure excluding interest | % GDP | Annual |
| **Deficit-debt adjustment** | Gap between deficit change and debt change | % GDP | Quarterly |

**Polish-specific benchmarks:**
- SGP deficit threshold: 3% GDP
- SGP debt threshold: 60% GDP
- Poland's historical range: -1% to -8% GDP (deficit), 30%-60% GDP (debt)

---

## Standard analytical angles

### 1. Headline: Deficit status
- Current fiscal balance vs. 3% SGP threshold
- Trajectory: improving or deteriorating?
- Context: COVID shock recovery, war refugee costs, EU funds absorption

### 2. Debt sustainability
- Debt-to-GDP ratio: current level vs. 60% Maastricht threshold
- Trajectory: accelerating or stabilizing?
- Primary balance: is policy setting sustainable long-term?

### 3. Composition breakdown
- Revenue: taxes (income, VAT, excise) vs. contributions vs. other
- Expenditure: current (wages, social transfers) vs. capital (investment)
- COFOG: functional breakdown — where is money spent?

### 4. EU/International comparison
- Poland vs. V4 (CZ, SK, HU), Eurozone average, EU average
- Position: is Poland an outlier or in line?
- Ranking: where does Poland stand among EU-27?

### 5. Projections
- IMF WEO forecasts: where is deficit/debt heading?
- Policy assumptions: what if no change in fiscal stance?

---

## Visualization conventions

**From Eurostat, IMF, and national statistical offices:**

1. **Deficit-debt chart** (canonical)
   - Dual-axis: deficit (% GDP) as bars, debt (% GDP) as line
   - Time series: annual or quarterly
   - Reference line at 3% (deficit) and 60% (debt)

2. **Revenue vs. expenditure** (canonical)
   - Grouped bars: revenue | expenditure over time
   - Balance (gap) shown as line or difference indicator

3. **Debt trajectory**
   - Line chart: debt-to-GDP over time
   - Shaded areas for Maastricht thresholds

4. **COFOG breakdown**
   - Stacked bar: functional expenditure composition
   - Horizontal bar for comparison across years

5. **EU comparison**
   - Bar chart: Poland vs. EU average vs. Eurozone
   - Maybe ranked: Poland's position among EU-27

6. **Waterfall** (less common but effective)
   - Revenue to expenditure to balance breakdown

---

## Data dimensions available in warehouse

### From curated.mart_finance:

**Core metrics (already available):**
- `pub.fiscal_balance_gdp` — Fiscal balance (% GDP), Eurostat
- `pub.fiscal_balance_imf` — Fiscal balance (% GDP), IMF WEO
- `pub.primary_balance_imf` — Primary balance, IMF
- `pub.structural_balance_imf` — Structural balance, IMF
- `pub.public_debt_gdp` — Gross debt (% GDP), Eurostat
- `pub.public_debt_total` — Debt (mln PLN), DBW
- `pub.gross_debt_imf`, `pub.net_debt_imf` — IMF debt
- `pub.expenditure_gdp`, `pub.revenue_gdp` — Totals (% GDP)
- `pub.interest_expenditure_gdp` — Interest (% GDP)
- `pub.govt_investment_gdp` — Investment (% GDP)

**COFOG (10 functions):**
- `pub.cofog_01_gdp` through `pub.cofog_10_gdp`

**Revenue breakdown:**
- `pub.taxes_income_gdp`, `pub.taxes_prod_imports_gdp`
- `pub.social_contributions_gdp`

**Sources:**
- Eurostat (annual GFS)
- IMF WEO (projections)
- DBW (Polish Ministry of Finance, monthly)

---

## Analytical Questions → Chart Type Mapping

For each standard analytical question in public finance, map to the appropriate chart type from visualization-guide section 6.

| Analytical Question | Analysis Type | Best Chart | Why |
|---------------------|---------------|------------|-----|
| **1. Deficit status** — How does current balance compare to SGP? | Deviation from benchmark | Column chart with reference line | Column height shows value, reference line shows 3% threshold |
| **1. Deficit trajectory** — How has deficit changed over time? | Trend analysis | Column chart | Clear at each time point, shows negative values clearly |
| **1. Revenue vs Expenditure + Balance** — How do all three relate? | Multi-metric financial | **Stacked subplots** (top: balance, bottom: grouped bars) | Different scales require separate panels, shared x-axis aligns time |
| **2. Debt sustainability** — Is debt ratio rising/falling? | Trend analysis | Line chart with threshold band | Line shows trajectory, shaded area shows 60% Maastricht threshold |
| **2. Debt vs. deficit** — How do they relate over time? | Relationship analysis | Stacked subplots (not dual-axis) | Avoid dual-axis confusion, use aligned panels |

### Revenue vs Expenditure vs Balance — Best Practice

For the core fiscal metrics, the recommended layout:

```
[Balance/Deficit columns]   ← Top panel: shows trajectory, SGP threshold
[Revenue | Expenditure]     ← Bottom panel: grouped bars, comparison
           ↓
       shared x-axis (years)
```

**Why this works:**
- Balance (top): Column chart — shows deficit trajectory, reference at -3%
- Revenue/Expenditure (bottom): Grouped bars — compares two values
- Different scales → separate panels (not dual-axis)
- Shared x-axis → easy to cross-reference between panels
- Visual alignment → you see "gap grew" in top panel and "spending up" in bottom

---

## Chart Selection Decision Tree

When designing a public finance chart, ask:

1. **What am I answering?** (Select analytical type)
   - "How has X changed?" → Trend → Line chart
   - "How does X compare to benchmark?" → Deviation → Column + reference line
   - "What are the parts of X?" → Composition → Donut/Stacked bar
   - "How does X rank?" → Ranking → Sorted horizontal bar
   - "How do X and Y relate?" → Relationship → Scatter or dual-axis line

2. **How many categories/time points?**
   - 1-5 time points → Column chart
   - 5+ time points → Line chart
   - 5-10 categories → Horizontal bar
   - 10+ categories → Treemap

3. **Are there thresholds/benchmarks?**
   - Yes → Add reference line (3% SGP, 60% Maastricht)
   - Threshold is range → Add shaded area

4. **Is there domain-specific convention?**
   - Yes → Follow it (e.g., Eurostat deficit-debt chart)
   - No → Apply general chart selection rules

---

## Gap analysis

**KPIs standard but not yet available:**
1. **Quarterly data** — Only annual currently; quarterly essential for timely analysis
2. **Net lending/borrowing** — Detailed GFS transaction data
3. **Primary expenditure** — Expenditure minus interest (could compute)
4. **Deficit-debt adjustment** — Stock-flow adjustment components
5. **Cyclically-adjusted balance** — Requires output gap calculation

**Enhancement opportunities:**
- Add quarterly Eurostat GFS for more timely updates
- Add sub-annual data for expenditure (monthly from DBW)

---

## Sources consulted

- Eurostat Government Finance Statistics: https://ec.europa.eu/eurostat/web/government-finance-statistics
- Eurostat News: Deficit-Debt Relation (Jan 2026): https://ec.europa.eu/eurostat/web/products-eurostat-news/w/ddn-20260122-1
- IMF Poland Article IV Mission (Nov 2025): https://www.imf.org/en/news/articles/2025/11/24/cs-poland-staff-concluding-statement-of-the-2025-article-iv-mission
- EU SGP information: https://ec.europa.eu/eurostat/web/government-finance-statistics/excessive-deficit-procedure
- NBP Financial Stability Report (Dec 2025): https://nbp.pl/wp-content/uploads/2025/12/Raport-o-stabilnosci-systemu-finansowego.-Grudzien-2025-r._EN.pdf
- Ministry of Finance Poland: https://www.gov.pl/finance