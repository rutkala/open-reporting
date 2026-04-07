# Visualization Review Rules — Diff-based

**Derived from:** `team/knowledge-base/visualization/` *(partially)* + `team/knowledge-base/ux-perception/` *(KB not yet built — rules to be deepened when ux-perception KB is complete)*
**Used by:** `.claude/agents/visualization-reviewer.md`
**Does NOT cover:** rendered visual quality (see `evaluation/visualization-image.md`), statistical correctness (see `evaluation/analytical-review.md`), code quality (see `evaluation/code-review.md`)

Rules applied by the `visualization-reviewer` agent on every PR diff.
Scoped to what is verifiable from chart function calls in changed code — not from rendered output.

KB source: `team/knowledge-base/visualization/principles.md` and `team/knowledge-base/visualization/charts/`

---

## Scope

This agent reviews changes in:
- `products/dashboards/` — domain dashboards (Labour, Finance, Explorer, etc.)
- `products/visuals/components/` — chart component library

It does NOT flag:
- `products/dashboards/template/` — developer reference scaffold, not user-facing
- Files outside the above paths

---

## HIGH — Communicates Incorrectly

A single HIGH finding should be fixed before merge. These produce charts that actively mislead.

### Colour semantics — trend direction vs. colour
- **`trend_color=POSITIVE` on a downward trend** — if `trend=` string contains `▼` or `-`, `trend_color` must be `NEGATIVE` (or omitted). Using `POSITIVE` (green) for a falling value tells the wrong story.
- **`trend_color=NEGATIVE` on an upward trend** — if `trend=` string contains `▲` or `+`, `trend_color` must be `POSITIVE` (or omitted). Exception: if the measure is a cost or deficit where up is bad — note the ambiguity rather than blocking.

### KPI card — reference without label
- **`reference_value=` present but no `reference_label=`** — a number without context ("80.0") is meaningless. Every reference value needs a label ("Target", "EU avg", "Prior year"). Flag if `reference_value` is non-empty and `reference_label` is absent or empty string.

### Too many series
- **More than 5 series in a single chart** — flag any chart call with a `series=[...]` or `bar_series=[...]` list containing more than 5 items. KB rule: 3-4 is recommended, 5 is the hard limit before visual clutter makes the chart unreadable.

### Missing `y_measure` on domain dashboard chart calls
- **New chart calls in `products/dashboards/` (excluding template) without `y_measure`** — all chart components that accept `y_measure` should receive it in domain dashboards. Without it, the y-axis has no title and no unit suffix, leaving the user without context for what the numbers represent. (Note: `pct_stacked_*` variants are exempt — their axes are always %.)

---

## MEDIUM — Suboptimal but Not Misleading

Fix before merge where practical. Note in PR if not fixed.

### Missing subtitle on domain chart calls
- **New chart calls without `subtitle=`** — subtitle provides analytical context ("2018–2024 average", "EU-27 comparison", "Constant 2015 prices"). Not required in the component library; required on domain dashboard charts.

### `pie_chart` with more than 6 categories
- **`labels=` list with >6 literal items in the diff** — KB rule: pie/donut with >6 slices is unreadable. Only flag if the label list is visible in the diff (not a variable reference).

### Waterfall variant mismatch
- **`waterfall_contribution` where the first and last items are a base and result** — this is the pattern for `waterfall_variance`. Contribution waterfall shows components summing to a total; variance waterfall shows a bridge from base to result. Flag if `base_label` or `final_label` params suggest a bridge pattern on a contribution call, or vice versa.

---

## LOW — Best Practice Not Followed

Log in review output. Does not block merge.

- **`show_labels=True` not used on single-series bar chart with ≤8 categories** — direct labelling removes the need for the user to read the axis. Recommended per KB "direct labeling" rule.
- **`reference=` missing on a line chart in a domain dashboard** — KB: "a number alone means nothing." Trend charts benefit from a reference line (prior period, target, EU average). Flag as a suggestion, not a requirement.
- **Combo chart (`line_clustered_column`, etc.) without a comment explaining why both series share the same scale** — combo charts on a shared axis are only valid when scales are compatible. A brief comment in the code helps reviewers verify this.

---

## What this agent cannot check

Be explicit about these in the review output — do not invent findings for things that require rendering:

- **Chart type correctness** — whether a bar chart is the right choice vs. a line chart requires knowing the analytical question and data structure. This cannot be determined from a function call alone.
- **Axis truncation** — Plotly's `rangemode` handles this; not visible in chart call parameters.
- **Rendered readability** — contrast ratios, label overlap, legend positioning, colour appearance.
- **5-second test** — requires a human to look at the rendered dashboard.
- **Data-to-ink ratio** — not assessable from code.
- **Layout and F-pattern** — requires seeing the full dashboard layout.

---

## References

- `team/knowledge-base/visualization/principles.md` — IBCS SUCCESS framework, colour rules, chart selection
- `team/knowledge-base/visualization/charts/bar.md` — bar/column chart rules
- `team/knowledge-base/visualization/charts/line.md` — line chart rules
