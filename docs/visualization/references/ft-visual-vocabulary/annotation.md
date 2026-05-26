# FT Visual Vocabulary — annotation

## What this source teaches

The FT Visual Vocabulary is a decision framework, not a style guide. It organises chart types into nine semantic categories based on what relationship the data shows (Deviation, Correlation, Ranking, Distribution, Change over Time, Part-to-whole, Magnitude, Spatial, Flow), with each category carrying a design intent prescription. The central lesson is that chart selection should be driven by the communicative question, not by data availability or aesthetic preference.

## Key patterns documented

- **Nine semantic categories as chart-selection entry points** — The poster organises all chart types under nine top-level questions the reader is trying to answer. This taxonomy is the primary reference: before choosing a chart type, first identify which category your communication falls into. `![](images/poster.png)`

- **Deviation category — the fiscal analyst's home base** — Diverging bar, diverging stacked bar, spine chart, and surplus/deficit filled line all belong here. These are the canonical tools for showing budget surplus/deficit, variance from target, or performance against benchmark — all central to public finance dashboards.

- **Change over Time — line as the canonical choice** — Line charts are explicitly identified as "the standard way to show a changing time series." Area charts are flagged with "use with care." Fan charts are recommended specifically for showing uncertainty in projections. These rules are normative at the FT; they are derived from reader perception research.

- **Waterfall — named for budget flow** — Listed under both Part-to-whole and Flow. The FT description says: "Designed to show the sequencing of data through a flow process, typically budgets. Can include +/- components." This is the canonical chart for fiscal decomposition (revenue + expenditure → balance).

- **Part-to-whole distinction from Magnitude** — A subtle but important rule: if the reader's interest is solely in the size of components, use a Magnitude chart. Only use Part-to-whole (pie, stacked column, treemap) if the whole-unit relationship matters. Many dashboards misuse stacked bars when ranked bars would serve better.

- **Correlation causation warning** — Explicitly noted in the Correlation category header: "unless you tell them otherwise, many readers will assume the relationships you show them to be causal." This is a standard annotation caveat for any scatter or connected scatter plot used in public finance analysis.

- **Spatial — rate/ratio only for choropleth** — "Should always be rates rather than totals." This is the canonical rule against mapping raw counts geographically (which creates population-density artefacts rather than showing the phenomenon of interest).

- **Fan chart for projection uncertainty** — Explicitly recommended for showing that uncertainty grows further into the future. Directly applicable to fiscal projections, deficit forecasts, and SGP convergence paths.

- **Lollipop as an alternative to bar** — Listed under both Ranking and Magnitude. "Draws more attention to the data value than standard bar/column." Useful when labels need to be legible at the data point without chart-ink overhead.

## Notable visual examples

**The poster** (`images/poster.png`) — A dense A1-format reference sheet with a warm grey background. Nine category headers run horizontally across the top in distinct colours (pink/salmon for Deviation, green for Correlation, orange for Ranking, etc.). Each category contains 4–12 small chart thumbnails, each with a name and 1-2 sentence description. The visual density is high but deliberate — this is a reference document, not a teaching document. The colour-coded top strip gives the eye an immediate orientation system. The miniature chart thumbnails are spare but accurate enough to identify chart shapes by their structural silhouette.

## Relevance to public-finance dashboards

The Deviation and Flow categories are the primary chart selection pools for fiscal dashboards: surplus/deficit lines, waterfall for revenue/expenditure decomposition, and diverging bars for comparing budget outturn against plan. The Change over Time guidance (line = standard, area = use with care, fan = projections) should be treated as a normative constraint. The Part-to-whole vs. Magnitude distinction prevents the common mistake of using stacked bars for expenditure components when the question is actually about ranking ministries by spend.
