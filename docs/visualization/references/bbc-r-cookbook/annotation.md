# BBC Visual and Data Journalism cookbook for R graphics — annotation

## What this source teaches

The BBC cookbook is primarily a reproducible-code reference, not a design essay — but its design philosophy is communicated implicitly through the house style the `bbc_style()` function enforces. The central lesson is that a strongly opinionated theme function, applied consistently, produces publication-ready output faster than ad-hoc styling. The underlying design principles (minimal ink, zero baseline, sparse colour, direct annotation) are learned by reading the output, not from a stated manifesto.

## Key patterns documented

- **Opinionated theme function as the design contract** — `bbc_style()` encodes all typography, grid, axis, and spacing decisions in one call. This is the BBC's way of ensuring visual consistency across many chart-makers. The function takes no arguments — if you disagree with the defaults, you override them after calling it. `![](images/bbplot_example_plots.png)`

- **Zero baseline as a mandatory anchor** — Every chart in the cookbook adds `geom_hline(yintercept = 0, size = 1, colour="#333333")`. This is a normative rule, not optional styling. It establishes the visual boundary between positive and negative, prevents the truncated-axis illusion, and signals professional discipline.

- **Colour minimalism: one or two accent colours, rest in grey** — The primary accent is `#1380A1` (BBC blue). A secondary gold `#FAAB18` is used for contrast series. All other data, labels, and structure elements use grey. This is the standard approach for news graphics where reader comprehension, not aesthetic richness, is the goal.

- **Direct labelling over legend reliance** — Multiple line chart examples annotate lines with their category names at the line endpoints, eliminating the eye-travel required to match legend colours to lines. Where a legend is needed, the cookbook documents how to reposition, remove title, or rearrange it to minimise clutter.

- **Y-axis-only gridlines as default** — The BBC style omits x-axis gridlines by default. This is deliberate: vertical gridlines add visual noise in time-series and bar charts where the category axis is nominal. Horizontal gridlines support value reading on the quantitative axis.

- **Small multiples with fixed scales** — The cookbook explicitly states: "It's always best to use the same y-axis scale across small multiples, to avoid misleading." Free scales are documented as a technique but framed as a deviation from the safe default.

- **Annotation as narrative device** — The example plots show text annotations placed directly on the chart area to highlight specific data points, events, or comparisons. This is the BBC editorial approach: the chart tells a story, not just displays data.

- **Left-aligned titles as a typographic standard** — `finalise_plot()` enforces left-aligned titles. This is consistent with BBC editorial style and with research showing left-aligned text is faster to read in LTR languages.

## Notable visual examples

**bbplot_example_plots.png** (`images/bbplot_example_plots.png`) — A six-panel composite showing the range of BBC chart types in production. Top row: two political bar charts (blue/red palette, sorted bars, vote-share x-axis) and a scatter/bubble chart on climate vulnerability. Bottom row: a dot plot with labelled categories, a scatter plot with highlighted series in contrasting colour, and a multi-category dot/line chart. Observations: every chart uses the same sparse gridline treatment (horizontal only), the same font weight hierarchy (bold headline, medium subtitle, light labels), and the same colour sparseness principle — one or two colours stand out, everything else is grey. The charts read at density appropriate for a news website (wider than tall, no decorative elements, data-ink ratio is high).

## Relevance to public-finance dashboards

The zero-baseline rule is directly applicable: fiscal charts showing deficit/surplus or budget outturn should always anchor at zero, and the `#333333` baseline stroke is visible enough to read without dominating. The colour minimalism principle — one accent colour for the series of interest, grey for everything else — maps well to single-indicator fiscal KPI charts where the current year should stand out from historical context. The y-axis-only gridline default is the correct choice for time-series charts (the standard form in public finance), where vertical gridlines add noise without aiding value reading.
