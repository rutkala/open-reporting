# Scatter and Bubble Charts

Scatter plots show the relationship between two continuous variables. Bubble charts add a third dimension through size encoding.

---

## When to Use

| Scenario | Best Variant |
|----------|-------------|
| Show correlation | Scatter plot |
| Add third dimension | Bubble chart (size = third variable) |
| Identify outliers | Scatter with highlighting |
| Compare categories | Colored scatter or bubble |

---

## Anatomy

A scatter plot consists of:
- **X-axis** — Continuous variable
- **Y-axis** — Continuous variable  
- **Points** — Each observation as a mark
- **Size** — Optional, for third variable (bubble)
- **Color** — Optional, for categorical encoding

---

## Design Rules

### Point Properties

- **Size:** Large enough to see (10-20px), not overlapping
- **Opacity:** 60-80% if overlapping points
- **Shape:** Use different shapes for categories if helpful
- **Color:** Use semantic colors or category palette

### Axes

- **Start at zero:** Not required for scatter (unlike bar)
- **Label clearly:** Include units and variable names
- **Consider ranges:** Don't let outliers compress the view

### Overlap

- **Transparency:** Use if many overlapping points
- **Jitter:** Add slight random offset for discrete data
- **Aggregation:** Consider hexbin for very large datasets

---

## Variants

### Basic Scatter

Two continuous variables.

**Best for:**
- Correlation analysis
- Finding patterns
- Identifying outliers

**Rules:**
- Include trend line if relationship exists
- Label interesting points
- Consider density contours for large data

### Bubble Chart

Add size for third variable.

**Best for:**
- Three variables (X, Y, Size)
- Showing magnitude along with relationship

**Rules:**
- Size encoding should be proportional (not area)
- Limit size range (max 3-4x min)
- Label largest/smallest bubbles

### Colored Scatter

Add color for category.

**Best for:**
- Show different groups
- Compare relationships across categories

**Rules:**
- Use colorblind-safe palette
- Limit to 4-5 categories
- Include legend or direct labels

---

## Common Mistakes

| Mistake | Problem | Solution |
|---------|---------|----------|
| Too many points | Overlapping, no pattern visible | Sample, aggregate, or use density |
| Axes not labeled | Unclear what variables are | Label with units |
| No trend line | Can't see relationship | Add regression line |
| Scale too wide | Points compressed | Consider log scale or focus |
| Size not proportional | Misleading | Use area, not radius |

---

## Correlation Interpretation

Scatter plots reveal relationship types:

| Pattern | Interpretation |
|---------|---------------|
| ↑ Positive | As X increases, Y increases |
| ↓ Negative | As X increases, Y decreases |
| ○ No pattern | No relationship |
| ⬡ Curved | Non-linear relationship |
| ⬛ Clustered | Groupings in data |

---

## Accessibility

- Don't rely on color alone
- Include labels for key points
- Provide data table alternative
- Ensure sufficient contrast

---

## Sources

- Playfair Data — Scatter plot tutorials
- EU Data Visualisation Guide — Chart types
- IBCS Standards — Correlation visualization