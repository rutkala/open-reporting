# Dashboard quality rubric

A concrete, observable rubric for what makes a data dashboard high-quality. Distilled from 8 vision-grounded reference sources (`docs/visualization/references/`) captured during Phase B.

## How to use this rubric

**At build time** — read this when composing any dashboard or chart. Each dimension is a question to ask while you work. The rubric is the floor, not the ceiling.

**At review time** — `visual-screenshot-reviewer` agent uses this as its checklist. Each pass criterion is observable from a rendered screenshot; each fail pattern is a callable defect.

**Each rubric item links to a captured reference image** that exemplifies the principle. When in doubt, look at the image, not just the text.

This rubric supersedes ad-hoc rules in `principles.md` and `building.md` for any dashboard-level judgment. Those files cover lower-level chart-type rules; this file covers dashboard quality as a whole.

---

## I. Information architecture

### 1. Hierarchical composition is explicit

**Thesis.** A dashboard is a composition of sections, each made of modules, each module made of data. The hierarchy should be readable from the visual layout alone.

**Pass.** Distinct, named sections separated by clear whitespace or rules. Each section has a single subject. Modules within a section visually group through proximity and consistent card styling.

**Fail.** Flat grid of unrelated charts. No visual indication of which modules belong together. Reader has to read every title to understand the structure.

**Reference.** [PencilAndPaper anatomy diagram](references/pencilandpaper-ux-patterns/images/Anatomy-v2.png) — the foundational mental model.

### 2. F/Z scan layout — most important top-left

**Thesis.** Reader attention decays as you scan right and down. The most global, most actionable, most-likely-asked numbers belong top-left. Detail and context belong bottom-right.

**Pass.** Top-left module answers "what's the headline?" in one glance. Filters and supplementary controls are in non-prime positions (top-right or sidebar). Bottom rows hold drill-down detail.

**Fail.** Title or logo in the prime top-left position. Critical KPIs buried below the fold. Most actionable number requires scrolling to find.

**Reference.** [PencilAndPaper F/Z scan diagram](references/pencilandpaper-ux-patterns/images/F-Z-Patterns.png).

### 3. Chart for pattern, table for precision (paired)

**Thesis.** A chart communicates a pattern; a table provides the reference number. When precise values matter alongside trend reading, provide both — co-located, not on separate tabs.

**Pass.** Chart shows the pattern at-a-glance. Table sits adjacent (typically below or right) holding precise period-by-period or country-by-country values. Summary rows in the table (EU totals, national averages) are visually anchored at the top.

**Fail.** Chart alone, no way to look up exact values. Table alone, no way to see the trend. Separate tabs forcing the reader to switch context.

**Reference.** [Eurostat public balance + debt table](references/eurostat-gus/images/public-balance-debt-table-2022-2025.png).

---

## II. Chart-level encoding

### 4. Chart type matches the data question

**Thesis.** Every data question maps to a small set of correct chart types. The choice is not aesthetic — it is semantic. The FT Visual Vocabulary names nine question categories (Deviation, Change over Time, Correlation, Distribution, Magnitude, Flow, Part-to-whole, Spatial, Ranking) each with named chart types.

**Pass.** Chart type chosen by asking "what question am I answering?" then picking from the matching category. Waterfall for budget flow. Diverging bar for deficit/surplus. Slope chart for "before vs after." Choropleth for spatial distribution.

**Fail.** Pie chart used for more than 3-4 categories. Donut chart for binary part-to-whole (use a KPI card with progress bar instead). Stacked bar where the eye can't compare non-baseline series. 3D anything.

**Reference.** [FT Visual Vocabulary poster](references/ft-visual-vocabulary/images/poster.png) — the canonical decision framework.

### 5. Reference lines are load-bearing, not decoration

**Thesis.** A chart with a benchmark (target, threshold, baseline, prior period) carries far more analytical content than a chart without. For fiscal data, the benchmark is the entire point of the comparison.

**Pass.** Threshold rendered as a bright contrasting horizontal/vertical line. The line is pre-attentively dominant — the reader sees it before the data series. Each bar/point becomes a pass/fail verdict against it.

**Fail.** No reference at all. Reference shown only as a faint grey gridline. Threshold mentioned in the chart subtitle but not drawn.

**Reference.** [Eurostat debt chart with 60% SGP line](references/eurostat-gus/images/gov-debt-2024-2025.png) — the red line dominates and turns each bar into a verdict.

### 6. Direct labelling over legends; annotations integrated

**Thesis.** Eye movement between a legend and the data series adds cognitive cost. Labels next to lines, value labels on bar ends, annotations on the chart surface — these eliminate the lookup tax. The Pudding and BBC both treat annotation as a first-class chart element.

**Pass.** Line endpoints labelled directly. Value labels on bar ends where the chart has room. Key data points carry inline callouts ("← COVID 2020 spike"). Legend used only when direct labelling would crowd the chart.

**Fail.** Standard legend top-right with cryptic series names (`Series 1`, `cat_a`). Critical context (units, source, "data revised in 2018") buried in a footnote. Annotations rendered as separate text boxes disconnected from the data.

**Reference.** [The Pudding birthday-effect](references/nyt-upshot/) image set; [BBC cookbook composite](references/bbc-r-cookbook/images/bbplot_example_plots.png).

### 7. Mandatory zero baseline for bar charts

**Thesis.** Bar length encodes value. Truncating the baseline distorts proportional reading. Bars must start at zero. (Line charts with narrow-range data may legitimately cut the y-axis with a labelled break — see point 11.)

**Pass.** Every bar chart starts at y=0. Bar length is proportional to value.

**Fail.** Bar chart with y-axis starting at 90% to "make differences visible" — exaggerates trivial differences and is a known deception pattern.

**Reference.** [BBC R cookbook composite](references/bbc-r-cookbook/images/bbplot_example_plots.png) — all bar examples baseline at zero.

---

## III. Colour as structure

### 8. Grey as primary, accent for signal

**Thesis.** Grey is the most important colour in data visualisation. It absorbs non-essential information (historical context series, unselected states, gridlines) so accent colours can do their semantic work without competition.

**Pass.** Context series (prior years, "all other countries", reference data) rendered in light or mid grey. Current year, selected item, or signal series carry the one accent colour. Backgrounds neutral. Gridlines subtle.

**Fail.** Every series gets a distinct vivid hue. Background tinted. Default palette ("Set1", "Tableau 10") applied to everything by reflex.

**Reference.** [Datawrapper when-to-use-colors](references/datawrapper-academy/images/when-to-use-colors.png).

### 9. Blue/orange polarity, not red/green

**Thesis.** Trend direction (up vs down, positive vs negative) is better encoded as blue/orange than red/green. Red/green carries unintended stoplight semantics (alarm framing for rising deficits) and fails for ~8% of male readers (deuteranopia/protanopia).

**Pass.** Positive trend → blue. Negative trend → orange. Or another colourblind-safe contrasting pair (teal/rust, purple/yellow).

**Fail.** Rising deficit shown in red, falling deficit in green. Stoplight palette applied indiscriminately.

**Reference.** [PencilAndPaper blue/orange convention](references/pencilandpaper-ux-patterns/images/Blues-Oranges.webp); [Datawrapper colorblind check](references/datawrapper-academy/images/color-blind-check.png).

### 10. Sequential = lightness; diverging = deviation from baseline

**Thesis.** Sequential gradients (low to high magnitude) must flow from light to dark within a single hue. Diverging gradients (above/below a baseline) use two contrasting hues meeting at a neutral light-grey centre. Rainbow/spectrum gradients confuse readers because perceptual steps are uneven.

**Pass.** Choropleth of fiscal magnitude uses single-hue light-to-dark. Choropleth of deviation from average uses diverging (teal/grey/rust) with the midpoint at the baseline. Categorical maps use distinct hues.

**Fail.** Rainbow choropleth ("heatmap" defaults in many tools). Sequential gradient where dark = low. Diverging gradient with white at the centre (white reads as "missing data" on maps).

**Reference.** [Datawrapper lightness-gradients](references/datawrapper-academy/images/lightness-gradients.png); [Datawrapper diverging-color-gradients](references/datawrapper-academy/images/diverging-color-gradients.png).

### 11. Accessibility — WCAG contrast, colorblind-safe, ≤7 categorical

**Thesis.** Three hard rules. Contrast ratio ≥4.5:1 for body text against background, ≥3:1 for large text and chart marks. All palettes pass colorblind simulation (deuteranopia + protanopia). Categorical palettes capped at 7 distinct hues — beyond that, restructure the chart, don't extend the palette.

**Pass.** Light theme (white or near-white background) by default — dark themes require extra contrast vigilance and almost never beat light themes for analytical reports. Colorblind simulation run before publishing. Categories >7 → switch to ranked bar or small multiples.

**Fail.** Dark-theme dashboard where fine text is unreadable. Red/green categorical palette ignored despite being the most common access failure. 12-category pie chart with hairline distinctions.

**Reference.** [Datawrapper colorblind check 3×2 grid](references/datawrapper-academy/images/color-blind-check.png) — the most persuasive single visual argument in the library.

---

## IV. Delta + change communication

### 12. Standardised delta taxonomy (icon-first / textual / inline)

**Thesis.** Change indicators (Δ vs prior period, vs target, vs benchmark) recur on every dashboard. Three canonical formats exist: **icon-first** (arrow + colour + value, compact, for KPI cards), **textual** (natural-language sentence, for narrative sections), **inline** (compact, embedded in table rows). Pick one per context; apply uniformly.

**Pass.** Every delta on the dashboard uses one of the three formats consistent with its context. Colour convention applied uniformly (per point 9, blue/orange).

**Fail.** Three different delta formats mixed within one dashboard. Bare numbers ("+2.1") with no semantic encoding.

**Reference.** [PencilAndPaper delta taxonomy](references/pencilandpaper-ux-patterns/images/Deltas-icons-colours.webp).

### 13. Dual-year grouped encoding > animated transitions

**Thesis.** For dashboards where year-over-year comparison is the analytical point, side-by-side grouped bars (prior year + current year per country/category) outperform animated transitions. Animation forces the reader to remember the prior state; side-by-side makes the comparison spatial and persistent.

**Pass.** Cross-country or cross-category comparisons use paired bars, two distinct fills (per point 8: prior = grey, current = accent). Comparison is visible without interaction.

**Fail.** Animated chart that auto-cycles through years. Slider that requires the user to manually flip between years to compare.

**Reference.** [Eurostat dual-year debt bar](references/eurostat-gus/images/gov-debt-2024-2025.png).

---

## V. Density + progressive disclosure

### 14. Whitespace > density; "eyeball attack" is a defect

**Thesis.** Information density beyond what the reader can absorb at a glance produces cognitive overload — what PencilAndPaper calls "data eyeball attack." The cure is whitespace, selective default display, and letting the reader toggle variables on/off.

**Pass.** Visible breathing room between modules. Default view shows the most-asked subset; less-asked variables hidden behind toggles or filters. Each module fits within Cowan's 4±1 chunks of working memory.

**Fail.** Dashboard packed with 20+ KPI cards and 10+ charts on one screen. Charts crammed against each other with no margin. Reader has to squint to read labels.

**Reference.** PencilAndPaper article text on "data eyeball attack" anti-pattern. (No counter-image in library — the absence of such a screenshot in our captures is informative; quality sources don't publish anti-patterns as positives.)

### 15. Two-level disclosure maximum

**Thesis.** Progressive disclosure is essential, but a chain of disclosure deeper than two levels (overview → drill → drill-into-drill) loses the reader. Cognitive research (NN/g) caps useful disclosure at two levels for non-expert users.

**Pass.** Landing screen shows headline KPIs + top-level breakdowns. One click opens a drill view with detail. Drill view has its own clear "back" affordance.

**Fail.** Modal opens another modal. Drill page opens another drill page. Reader gets lost in the hierarchy.

**Reference.** NN/g Progressive Disclosure principle. The GUS Socio-Economic Situation dashboard (annotation only — no captured image) is a positive example: KPI-card-only landing with drill on demand.

### 16. Trend visible without precise values; hover/tooltip for precision

**Thesis.** Reading a chart surface should communicate the trend immediately. Precise numeric values surface on hover or in a paired table (point 3). This prevents visual overload from value labels on every point while preserving depth.

**Pass.** Chart surface readable without numbers cluttering every data point. Tooltips on hover surface exact values. Sparkline conventions: shape + endpoint, no axis or labels.

**Fail.** Every data point labelled with a number, defeating the visual encoding. Or: chart with no way to retrieve exact values at all.

**Reference.** PencilAndPaper hover-tooltip pattern; [Eurostat trend chart](references/eurostat-gus/images/expenditure-revenue-trend-2015-2025.png).

---

## VI. Storytelling

### 17. Sequential zoom for narrative explanation

**Thesis.** When a chart needs to make a non-obvious analytical point, walk the reader through it: full view → highlighted detail → distributional context. Each step strips one degree of ambiguity. The Pudding's "Birthday Effect" piece is the canonical example.

**Pass.** A narrative section that needs explanation uses 2-3 chart steps in sequence, each annotated to draw attention to the next finding. Static charts when the data speaks for itself; sequential when it doesn't.

**Fail.** A single complex chart trying to do all the explanatory work alone. Multi-panel small multiples used decoratively rather than as a stepped argument.

**Reference.** [The Pudding birthday-effect images](references/nyt-upshot/).

---

## VII. Anti-patterns (always wrong)

### 18. The forbidden list

These are wrong by default; only deviate with a documented domain reason:

- **Gauges** for non-real-time KPIs. A semi-circular gauge consumes 10× the canvas of a KPI card for the same information density. Use a KPI card with a delta + threshold marker instead. [Power BI Manufacturing dashboard gauge — captured as negative pattern](references/power-bi-showcase/).
- **Rainbow / spectrum gradients** for sequential data. See point 10.
- **Red/green categorical palettes**. See points 9, 11.
- **Pie/donut for >3 categories**. Always a ranked bar instead.
- **3D charts of any kind**. Distortion exceeds informational gain.
- **Dark backgrounds** for analytical reports. Aesthetic appeal; readability cost. Reserve for monitoring / situational-awareness dashboards where it is genuinely standard (security operations, vehicle telemetry).
- **Data eyeball attack** — see point 14.

---

## VIII. Domain extensions — public finance

### 19. SGP threshold lines are mandatory anchors

**Thesis.** For Polish/EU public-finance dashboards, the SGP 3% deficit and 60% debt thresholds are not optional reference points — they are the entire analytical context. A deficit chart without the -3% line is incomplete.

**Pass.** Every deficit chart shows the -3% line in a contrasting colour. Every debt chart shows the 60% line. Cross-country comparisons sort by value (not alphabet) so the reader sees the league table immediately.

**Fail.** Deficit chart with no SGP reference. Country list in alphabetical order forcing the reader to do mental scanning.

**Reference.** [Eurostat debt chart with 60% line](references/eurostat-gus/images/gov-debt-2024-2025.png); [Eurostat balance chart with -3% line](references/eurostat-gus/images/public-balance-2024-2025.png).

### 20. Poland highlighted in cross-country comparisons

**Thesis.** This is a Polish public-data product. In any EU cross-section, the Poland bar/point should be visually distinguishable (highlight colour, bold label, or accent fill).

**Pass.** Poland renders in a distinct fill or with a callout label in any chart showing all 27 EU countries.

**Fail.** Poland rendered identically to every other country, with the reader required to scan for "PL" in axis labels.

**Reference.** Captured Eurostat charts include Poland in the dataset — see how the chart loses analytical value when one specific country isn't highlighted.

### 21. Structural breaks annotated; narrow-range y-axes acceptable

**Thesis.** Polish fiscal time series carry structural breaks (COVID 2020 expenditure spike; pre/post-EU-accession; ESA 2010 methodology changes). These must be annotated, not silently presented. For narrow-range indicators (tax revenue 12-15% of GDP, expenditure 44-54%), a labelled y-axis break is acceptable to make small movements legible — but always labelled, never silent.

**Pass.** COVID 2020 spike carries an inline annotation. Methodology change years marked with a vertical reference line + footnote. Y-axis breaks labelled explicitly ("// note: y-axis cut").

**Fail.** Time series with a sudden inflection and no explanation. Y-axis truncation without a label.

**Reference.** [Eurostat trend chart with visible COVID spike](references/eurostat-gus/images/expenditure-revenue-trend-2015-2025.png).

---

## Applying the rubric

A reviewer or builder uses the rubric like this:

1. **Layout check** — items 1, 2, 3. Open the screenshot full-size. Look only at structure for 5 seconds. Can you tell what the dashboard is about? Where the headline lives? How modules group?
2. **Encoding check** — items 4-7. For each chart, ask: is the type right? Is there a reference? Are labels direct? Bars baseline at zero?
3. **Colour check** — items 8-11. Does grey dominate? Is accent used sparingly? Run a colorblind simulation. Count categorical hues.
4. **Change check** — items 12, 13. Are deltas consistent? Are comparisons spatial?
5. **Density check** — items 14-16. Whitespace present? Disclosure deep but not endless?
6. **Storytelling check** — item 17. Where the data needs explanation, is the narrative built?
7. **Anti-pattern scan** — item 18. Any of the forbidden list present?
8. **Domain check** — items 19-21. For fiscal dashboards specifically, are SGP lines present? Is Poland highlighted? Are breaks annotated?

A "high-quality" dashboard passes all items in I-V plus VIII, has no item 18 violations, and uses item 17 where the data warrants narrative. Items 6 and 16 have soft trade-offs; document the choice in the dashboard's design notes.

---

## Provenance

Each rubric item is grounded in ≥1 captured reference image. The Phase B reference library (`docs/visualization/references/`) is the corpus. If you disagree with an item, look at the cited image first — disputes are easier to resolve with both parties looking at the same screenshot.

The rubric is intentionally finite (21 items). Resist adding more without first asking whether an existing item already covers the concern.
