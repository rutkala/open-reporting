# NNG — Progressive Disclosure + Information Scent — annotation

## What this source teaches

These two NNG articles together form the cognitive science foundation for dashboard usability. Progressive disclosure answers the question "what should I show on the initial screen vs. behind a click?" — the single most consequential design decision in a data dashboard. Information scent answers the question "will the user even notice and engage with what I've designed?" — a prerequisite that designers often overlook. Neither article is dashboard-specific, but both are directly applicable and cited across all dashboard usability literature including the PencilAndPaper source in this library.

## Key patterns documented

- **Progressive disclosure as the governing principle for dashboard density** — Show only what most users need most of the time on the initial view. Filters, drill-downs, and detail views are secondary. The very fact that something appears on the dashboard tells users it is important — so every KPI card and chart that appears by default is an implicit claim about priority. If the dashboard displays 20 metrics, no single one reads as important.

- **Two-level maximum** — Designs that go beyond two disclosure levels typically have low usability. Applied to dashboards: overview (level 1) → detail/drill-down (level 2). A third level (e.g. a modal within a drawer within a dashboard) is a strong indicator of over-complexity.

- **The split decision: what goes on the initial screen** — Determined by task frequency and task criticality, not by data availability. Tools: task analysis, field studies, frequency-of-use statistics. Data availability is never a valid reason to show something — "we have it so why not show it" is the anti-pattern named in the PencilAndPaper article.

- **Information scent for chart and KPI label design** — Chart titles, axis labels, and KPI card labels function as "link labels" in information-scent terms. They must tell the user, before reading the data, what question this chart answers. Ambiguous labels ("Revenue") have weak scent; precise labels ("Monthly revenue vs. prior year target") have strong scent. This has direct implications for how axis titles and KPI card headers should be written.

- **Prior knowledge dependency** — Users with domain expertise (e.g. fiscal analysts who know what "SGP ceiling" means) have richer scent from shorter labels than general-audience users. Dashboard design must decide which audience's prior knowledge to calibrate for — and either choose the smaller audience with more informative short labels, or invest in tooltips to build scent for less experienced users.

- **Staged vs. progressive disclosure in filter design** — A dashboard with a global filter sidebar (affects all charts) uses staged disclosure; per-chart filter dropdowns use progressive disclosure. The NNG framework predicts that per-chart filters are better when charts are used independently and global filters are better when users need to compare across charts under the same conditions.

- **Tooltips as the correct second-level disclosure mechanism** — Hover tooltips are the canonical implementation of progressive disclosure in data visualization: the chart surface communicates the trend (level 1), precise values appear on hover (level 2). This confirms the PencilAndPaper recommendation from first principles.

## Notable visual examples

**Information Scent diagram** (`images/information-scent-diagram.png`) — A clean three-panel explanatory diagram on white background. Left panel (orange): browser window icon labelled "SOURCE — The webpage." Centre panel (orange/grey): a list of links with one highlighted and a cursor pointing at it, labelled "REPRESENTATION — Link to webpage and surrounding context." Right panel (purple): a brain icon with an arrow pointing back to the representation, labelled "INFO SCENT — User's perception of the link plus prior knowledge." The three-plane perspective (source → representation → perceived value) captures the cognitive gap between what a designer builds and what a user experiences. Applied to dashboards: a KPI card is the source; its title, number, and surrounding layout are the representation; whether the user stops to read it depends on the estimated value, not the actual value.

## Relevance to public-finance dashboards

Progressive disclosure maps directly onto the public_finance dashboard structure: the top section should show the three or four fiscal indicators that define the current situation (primary balance, deficit/GDP, public debt/GDP, interest-to-revenue ratio). Everything else — breakdowns by ministry, trend decomposition, regional comparisons — belongs to a detail level accessible via click-through or filter expansion. Information scent applies to every KPI label: "Deficyt sektora general government" has stronger scent than "Deficyt" for the target audience of fiscal analysts; the tooltip can carry the formal ESA 2010 definition for users who need it.
