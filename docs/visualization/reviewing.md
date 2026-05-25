# Visualization Review Rules — Image-based

**Derived from:** `docs/ux-perception/principles.md` ✓ + `docs/visualization/principles.md` ✓ (KBs complete — pre-attentive, Gestalt, WCAG, cognitive load)
**Used by:** `.claude/agents/visual-screenshot-reviewer.md`
**Does NOT cover:** code-level chart configuration (see `evaluation/visualization-image.md`), statistical correctness (see `evaluation/analytical-review.md`)

Agent reference for image-based dashboard review. Apply only these rules when evaluating a screenshot.
Complement to `visualization-diff.md` (code-based) — covers what cannot be checked from code.

---

## HIGH — Communicates Incorrectly (BLOCK)

These findings mean the dashboard is actively misleading a user. Must be fixed before merge.

- **Semantic colour mismatch visible** — a KPI delta or chart bar uses red for a positive value or green for a negative value. Look for coloured arrows, delta numbers, or coloured bars where the colour contradicts the direction.
- **Broken or blank render** — any chart area that is empty, white, shows an error message, shows a Plotly placeholder ("No data"), or fails to render. A blank KPI card value. A chart title with no chart beneath it.
- **Text unreadable — contrast failure** — any label, axis tick, title, or value where the text colour is too close to the background to read at normal screen brightness. Applies to light grey text on white background, or dark text on dark backgrounds.
- **Critical text truncated** — a chart title, axis label, KPI label, or legend entry that is cut off mid-word by the container boundary, making it meaningless or misleading.

---

## MEDIUM — Suboptimal (CONDITIONAL)

These findings degrade communication without actively misleading. Flag but do not block.

- **Layout does not follow F-pattern** — the most important metric or finding is not in the top-left quadrant of the visible viewport. If a headline KPI is buried below the fold or in the bottom-right, the layout priority is wrong.
- **Too many competing elements in one view** — more than 6 distinct chart or KPI areas visible in a single viewport without clear visual grouping or hierarchy. The eye has no obvious starting point.
- **Chart type looks wrong for the data** — a pie chart with clearly more than 6 slices; a line chart with a single data point; a bar chart with bars so narrow they are indistinguishable; a scatter with all points in a single cluster with no spread.
- **Colour palette inconsistency** — different colours used for the same concept across two charts on the same page (e.g., Poland shown as blue in one chart and orange in another).
- **Legend present but not needed** — a legend describing a single series. Or no legend present for a multi-series chart where series are not labelled on the chart.
- **Axis labels missing or generic** — a visible axis (not a KPI card) that has no label, or a label that reads "value", "y", or "index" instead of the actual measure name and unit.

---

## LOW — Best Practice (SUGGESTION)

Minor issues that do not meaningfully affect communication.

- **Subtitle absent on a chart** — a chart has a title but no subtitle explaining what is shown (period, geography, source). Not blocking if the title is self-explanatory.
- **Source attribution missing** — no footer or caption attributing the data source on a page with data.
- **Inconsistent decimal formatting** — some KPI values show 1 decimal, others show 0 or 2 decimals on the same page, without a clear reason based on magnitude.
- **Gridlines dominate** — gridlines are darker or more prominent than the data marks they support.

---

## Cannot evaluate from a screenshot

Always include this section in the output so the reviewer knows the limits of image analysis:

- Whether SQL aggregation is statistically correct
- Whether the correct data source is being queried
- Whether the data shown is current (vs stale cache)
- Accessibility for screen readers
- Performance / load time
- Behaviour of interactive filters and callbacks
- Mobile responsiveness (screenshot is desktop-only at 1440×900)
