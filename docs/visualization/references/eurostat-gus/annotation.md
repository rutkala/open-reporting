# Eurostat Government Finance Statistics — annotation

## What this source teaches

Eurostat's Statistics Explained article on government finance statistics is the canonical public-finance chart template for EU institutional communication. Its charts are referenced in policy documents, academic papers, and national statistics publications across all 27 member states. The design is not fashionable — it is restrained, legible, and built for comparability across many countries and years. The design choices reflect decades of editorial convergence toward reproducibility and cross-country comparability rather than visual novelty.

## Key patterns documented

- **Grouped bar chart as the workhorse for cross-country comparison** — All cross-sectional fiscal charts use paired grouped bars (two years side by side per country, blue for the prior year, gold/olive for the current year). Countries are sorted by average value descending, placing the highest-debt or highest-deficit countries leftmost. EU and Euro area aggregates appear first as reference anchors. The colour pairing (dark blue + muted gold-olive) is consistent across all charts in the article — colour serves as a year legend, not a magnitude signal. `![](images/gov-debt-2024-2025.png)`

- **Threshold reference line as the most load-bearing element** — A horizontal red line at the SGP threshold (60% for debt, -3% for deficit) appears in both the debt and balance charts. This line is the entire point of the comparison — without it, the chart is just country rankings. With it, each bar becomes a pass/fail verdict. The line is drawn in bright red against the light grey gridlines, ensuring it pre-attentively dominates even at small sizes. This is a direct lesson: in fiscal dashboards, the benchmark line is not decoration; it is the primary analytical message. `![](images/public-balance-2024-2025.png)`

- **Diverging bar chart for deficit/surplus** — The public balance chart anchors bars at zero, with surpluses rising above and deficits descending below. The -3% threshold line crosses through the bars, cleanly separating compliant from non-compliant countries. Countries are sorted by their 2025 value, not by name — this sorting reveals which countries are improving (gold bar moving toward zero) vs deteriorating (gold bar moving away). The dual-year encoding makes the temporal comparison legible without requiring a separate time-series chart. `![](images/public-balance-2024-2025.png)`

- **Data table for precision alongside charts** — A full 27-country by 4-year table of both deficit and debt values accompanies the charts. Eurostat uses this as a parallel track: the chart communicates the pattern, the table provides the reference number. The table uses EU/Euro area rows in bold as summary anchors at the top, then alphabetical country order. This pattern — chart for pattern, table for value — is worth replicating on any dashboard where precise numbers matter alongside trend reading. `![](images/public-balance-debt-table-2022-2025.png)`

- **Annotated time series with event callout (COVID spike)** — The expenditure/revenue trend chart (2015-2025) shows a sharp spike in 2020 on both Euro area and EU expenditure lines, then a recovery. The y-axis is cut to the 44-54% range (not zero), with a note that "the y-axis is cut." The chart carries four series (EU expenditure, EU revenue, Euro area expenditure, Euro area revenue) encoded with line style + marker shape combinations rather than colour alone — solid vs dashed lines, square vs X markers. The COVID spike in 2020 is immediately legible without explicit annotation because the chart's visual grammar makes the deviation pre-attentive. `![](images/expenditure-revenue-trend-2015-2025.png)`

- **Cross-section bar chart sorted by average for comparison** — The government revenue and expenditure cross-section chart (all EU+EEA countries, 2025) sorts countries by the average of revenue and expenditure values descending. This sort order is not alphabetical and not by either variable alone — it minimises crossovers between the two bars, making the revenue-expenditure gap legible for every country without the bars interleaving visually. `![](images/gov-revenue-expenditure-cross-section-2025.png)`

- **Three-series line chart for tax category decomposition** — The taxes and social contributions time series uses three lines: production/import taxes (blue), income/wealth taxes (gold), net social contributions (red/pink). The y-axis range (12-15% of GDP) is deliberately narrow to make subtle changes legible. The COVID-year dip in income taxes and social contributions is visible without explicit annotation. `![](images/tax-social-contributions-2015-2025.png)`

## Notable visual examples

**Government debt grouped bar with 60% threshold** (`images/gov-debt-2024-2025.png`) — Greece and Italy stand dramatically above the 60% threshold at ~140-160% of GDP, making the red threshold line feel deeply meaningful rather than bureaucratic. The bars are densely packed across 27 countries, yet remain legible because the y-axis is well-scaled (0-180), bar widths are minimal, and country labels run diagonally. The threshold line cuts through the visual field at roughly half-height, dividing compliant countries (right cluster, below threshold) from non-compliant (left cluster, above threshold). Poland appears in the right cluster with debt around 55-60% — right at the threshold — which is directly relevant data for this project.

**Deficit/surplus diverging bar** (`images/public-balance-2024-2025.png`) — The zero baseline is clearly marked; the -3% line runs as a red horizontal across the negative territory. Romania appears as the deepest negative at approximately -8 to -9% for both years. The visual immediately communicates two things: how many countries breach the 3% rule (most do), and whether the breach is improving or worsening (2025 bar colour vs 2024 bar colour). This dual-year grouped format is more efficient than two separate year charts.

**Four-line expenditure/revenue trend** (`images/expenditure-revenue-trend-2015-2025.png`) — The COVID spike in 2020 is the dominant visual feature — Euro area total expenditure jumps from ~47% to ~53% of GDP in a single year, the largest single-year change in the entire series. The recovery back toward pre-COVID levels by 2022-2023 is clearly visible. Line style differentiation (solid vs dashed) distinguishes EU from Euro area cleanly even without colour difference.

## Relevance to public-finance dashboards

This source is the single most directly applicable reference in the Wave 2 library. Every chart type used here — diverging deficit bar, debt comparison bar with 60% threshold, revenue/expenditure dual-line, tax category decomposition — maps directly onto the charts planned for `products/dashboards/public_finance/`. Specific lessons:

1. The red threshold line at SGP limits must be the primary visual anchor in any deficit or debt chart — not an annotation option, but a structural requirement.
2. Sort countries by value, not alphabet, in cross-country comparisons — this makes outlier detection immediate.
3. The dual-year grouped bar is superior to animated year-over-year transitions for dashboards where the comparison is the point.
4. The GUS Socio-Economic Situation dashboard (ssgk.stat.gov.pl) uses a KPI-card-only layout with no charts on the landing screen — consistent with NNG's progressive disclosure finding that top-level dashboards should communicate high-level status, with drill-down available on demand.
