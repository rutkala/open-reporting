# Line and Area Charts

Line charts are the standard choice for visualizing trends over time. Like bar charts, they were invented by William Playfair (1786) and remain one of the most effective chart types for continuous data.

---

## When to Use

| Scenario | Best Variant |
|----------|-------------|
| Show trend over time | Line chart |
| Compare multiple trends | Multi-line chart |
| Emphasize volume/magnitude | Area chart |
| Show part-to-whole over time | Stacked area |
| Show cumulative trend | 100% stacked area |

---

## Anatomy

A line chart consists of:
- **Time axis** — Continuous or discrete time periods (x-axis)
- **Value axis** — Numerical scale (y-axis)
- **Line** — Connects data points, encodes value through position
- **Points** — Optional markers at each data point
- **Area** — Optional fill below line (for area charts)

---

## Design Rules

### Line Properties

- **Line weight:** 2-3px minimum for visibility
- **Smoothing:** Avoid spline interpolation — straight lines are more accurate
- **Interpolation:** Connect points directly; don't interpolate missing values

### Multiple Lines

- **Limit:** 2-4 lines maximum per chart
- **Distinct colors:** Use colorblind-safe palette
- **Include markers:** Show data points, especially for irregular intervals
- **Direct labels:** Label lines directly instead of legend when possible

### Area Charts

- **Transparency:** Use 50-70% opacity if overlapping
- **Stacked:** For composition over time, use stacked area
- **0 baseline:** Area charts should start at zero

### Time Axis

- **Appropriate granularity:** Daily for short periods, monthly/quarterly for longer
- **Consistent intervals:** Don't skip periods — show gaps
- **Time-based:** Only use line charts for time-series data (not categorical)

---

## Variants

### Single Line

Show one metric over time.

**Best for:**
- Revenue trend
- Stock price history
- Temperature over day

**Rules:**
- Thick, clear line (2-3px)
- Include markers for clarity
- Show data labels at key points

### Multi-Line

Compare multiple metrics over same time period.

**Best for:**
- Comparing products
- Actual vs. target
- Multiple regions

**Rules:**
- Maximum 3-4 lines
- Distinct, colorblind-safe colors
- Direct labeling preferred over legend
- Consider small multiples for more series

### Area Chart

Emphasize magnitude and show volume.

**Best for:**
- Cumulative values
- Stock/flow over time
- Emphasizing magnitude

**Rules:**
- Start at zero
- Use transparency if overlapping
- Consider stacked for composition

### Stacked Area

Show part-to-whole while emphasizing total.

**Best for:**
- Revenue by product over time
- Population breakdown
- Market share trends

**Rules:**
- Consistent color order across charts
- Limit to 4-5 segments
- Most important segment at bottom

---

## Common Mistakes

| Mistake | Problem | Solution |
|---------|---------|----------|
| Line chart for categorical data | Implies false continuity | Use bar chart |
| Too many lines | Visual clutter | Limit to 3-4, use small multiples |
| Missing markers | Unclear where data points are | Add markers, especially for irregular data |
| Interpolated gaps | False data | Show gaps for missing data |
| 3D effects | Distorted perception | Always use 2D |
| Smoothing | Inaccurate representation | Use straight lines |

---

## IBCS Conventions

- Dark grey = current period
- Light grey = previous period
- Hatched pattern = forecast
- Dotted line = target/goal
- Reference lines for benchmarks

---

## Accessibility

- Don't rely on color alone — add labels
- Use pattern alternatives for colorblind users
- Ensure 4.5:1 contrast for labels
- Provide data table alternative

---

## Sources

- Playfair Data — "3 Ways to Make Lovely Line Graphs in Tableau"
- Playfair Data — "Cornerstone Module Part 2" (line vs bar)
- EU Data Visualisation Guide — "A deep dive into line charts"
- IBCS Standards — Line chart conventions