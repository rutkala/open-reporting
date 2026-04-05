# Bar and Column Charts

The bar chart is the most fundamental and versatile chart type for comparing categorical data. Invented by William Playfair in 1786, it remains the best option for comparing discrete categories.

---

## When to Use

| Scenario | Best Variant |
|----------|-------------|
| Compare values across categories | Vertical or horizontal bar |
| Rank categories by value | Horizontal bar (sorted) |
| Show composition of total | Stacked bar |
| Compare multiple metrics per category | Grouped bar |
| Show positive/negative values | Diverging bar |
| Compare to target | Bar with reference line |

---

## Anatomy

A bar chart consists of:
- **Axis** — One categorical dimension (x or y), one value axis
- **Bars** — One bar per category, length/height encodes value
- **Labels** — Category labels, value labels (optional but recommended)
- **Gridlines** — Light horizontal lines for value axis (optional)

---

## Design Rules

### Orientation

- **Vertical bar (column):** Default. Use when category labels are short (1-2 words)
- **Horizontal bar:** Use when category labels are long, or when ranking (sorting is easier to read left-to-right)
- **Sort bars in descending order** unless there's a natural order (chronological, alphabetical)

### Sizing

- **Bar width:** Thick enough to be visible, with small gaps between bars
- **Minimum value:** If values are very small, consider alternative or use log scale
- **Zero baseline:** Bar charts must start at zero — never truncate the axis

### Labels

- **Direct labeling:** Place value labels directly on bars when possible
- **Readable font:** 12-14px minimum, contrasting color
- **Format numbers:** Use appropriate units (K, M, B) and decimal places

### Color

- **Single color:** Use one color for all bars unless encoding a second dimension
- **Avoid gradients:** Solid colors work better than gradients within bars
- **IBCS convention:** Dark grey for primary data, light grey for comparison

---

## Variants

### Grouped Bar Chart

Compare multiple measures or categories side-by-side.

**Best for:**
- Comparing same metric across different dimensions
- Showing actual vs. target

**Rules:**
- Limit to 3-4 groups per category
- Use consistent colors across groups
- Include legend or direct labels

### Stacked Bar Chart

Show part-to-whole while also showing totals.

**Best for:**
- Show total AND composition
- Compare composition across categories

**Rules:**
- Limit stacks to 4-5 segments
- Use consistent color order across all stacks
- Consider 100% stacked for composition-only comparison

### Diverging Bar Chart

Show positive and negative values from a central zero line.

**Best for:**
- Sentiment analysis (positive/negative)
- Budget variance (over/under)
- Before/after comparison

**Rules:**
- Align bars to center or zero
- Use semantic colors (green/red or blue/orange)
- Include clear zero line

### Horizontal Bar Chart (Ranking)

Show ranks with natural left-to-right reading.

**Best for:**
- Top N analysis
- Leaderboards
- Categories with long names

**Rules:**
- Always sort descending (largest at top)
- Include value labels
- Consider limiting to top 10-15

---

## Common Mistakes

| Mistake | Problem | Solution |
|---------|---------|----------|
| Truncated axis | Misleading proportions | Start at zero |
| Too many bars | Clutter, hard to read | Aggregate or filter to top N |
| Wrong orientation | Hard to read labels | Use horizontal for long labels |
| 3D effects | Distorted perception | Always use 2D |
| No sorting | Hard to compare | Sort by value descending |
| Double encoding | Cognitive load | Color OR position, not both |

---

## IBCS Conventions

- Use solid fill for actual values
- Use outlined/filled for planned/budget values
- Dark grey = current period
- Light grey = previous period
- Reference lines for targets/benchmarks

---

## Accessibility

- Minimum contrast 4.5:1 for labels
- Don't rely on color alone — include value labels
- Provide data table alternative
- Consider screen reader compatibility

---

## Sources

- Playfair Data — "5 Ways to Make a Bar Chart in Tableau"
- Playfair Data — "3 Ways to Make Beautiful Bar Charts"
- **Wall Street Journal — "Pie Chart Design"** (PDF: `graphics-styleguide/img/Pie Chart Design from WSJ.pdf`)
- EU Data Visualisation Guide — "Vertical versus horizontal bars"
- IBCS Standards — Bar chart conventions