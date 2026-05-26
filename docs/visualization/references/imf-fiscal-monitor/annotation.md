# IMF Fiscal Monitor — annotation

## Access status

This source was fully inaccessible during Wave 2 capture (Akamai CDN blocking at the IP network level). This annotation cannot be grounded in captured images.

## What this source would teach (from prior knowledge — weaker rating)

The IMF Fiscal Monitor is the world's leading technical publication on government fiscal policy. Its chart conventions are studied and replicated by national finance ministries and central banks. Key design patterns documented in the Fiscal Monitor series:

- **Fan charts for fiscal projections** — The Fiscal Monitor consistently uses fan charts (shaded confidence bands around a central projection line) for deficit/GDP trajectories. The standard encoding: solid line for history, dashed line for baseline projection, dark shaded band for 50th percentile uncertainty, light shaded band for 90th percentile. The fan chart is the canonical tool for communicating that fiscal projections are uncertain without abandoning the projection entirely.
- **Cross-country scatter plots for debt sustainability analysis** — Typical axes: current debt level (x) vs. required fiscal adjustment (y). Countries are labelled directly on the scatter, clustered by income group (AE = Advanced Economy, EM = Emerging Market, LIC = Low Income Country) using shape or colour encoding. The -3%/60% SGP thresholds appear as reference lines.
- **Waterfall for fiscal decomposition** — The Fiscal Monitor regularly decomposes changes in the fiscal balance into components: primary expenditure, revenue, interest payments, cyclical component, one-off measures. The waterfall encoding maps each component as a step, with the closing bar showing the total deficit change. This is the chart type most directly applicable to budget execution analysis in the public_finance dashboard.
- **Small multiples of country groups** — When comparing Advanced Economies vs Emerging Markets vs Low Income Countries across a shared metric, the Fiscal Monitor uses a 1×3 or 2×3 grid of identical line charts with the same y-axis scale, allowing direct visual comparison of group trajectories. This small-multiples approach is cleaner than overlaying all groups in a single chart.
- **Heat map of fiscal vulnerability** — Some issues include a heat map where rows are countries and columns are fiscal risk indicators, with a red (high risk) → white → green (low risk) colour gradient. This provides a multi-indicator summary at a glance.

## Relevance to public-finance dashboards

The fan chart and waterfall decomposition are the two IMF patterns most applicable to the public_finance dashboard. Poland's fiscal trajectory could be shown as a fan chart (history + MF/EC forecast + uncertainty). Budget execution could be shown as a waterfall (revenue components + expenditure components → fiscal balance). The IMF's cross-country scatter plots (debt vs required adjustment) would contextualise Poland's fiscal position relative to EU peers more powerfully than a simple ranking bar chart.

## Wave 3 recommendation

Download the October 2024 Fiscal Monitor PDF locally (the URL is known, the block is IP-level), then use `Read` with the `pages` parameter to process 5 pages at a time. Target pages: Executive Summary figures (pages 1-5), Chapter 1 figures (pages 10-30). The Read tool handles PDFs natively and supports page ranges up to 20 pages per call.
