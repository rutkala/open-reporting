# Combo Charts and Subplots

Combo charts and subplots combine multiple chart types or metrics in a unified view. Used correctly, they enhance comparison; used incorrectly, they create confusion.

---

## When to Use

| Scenario | Best Solution |
|----------|---------------|
| Bar + Line on same scale | Combo chart |
| Metrics with different scales | Stacked subplots (panels) |
| Revenue + profit trend | Stacked subplots |
| Actual vs. target | Side-by-side or reference line |

---

## The Core Rule: Scale Compatibility

**Before combining charts, ask: Are the scales compatible?**

- **Same units?** (e.g., both in EUR)
- **Similar magnitude?** (within 2-3x range)
- **Same meaning?** (both are counts, not one count and one ratio)

If **yes** → Single chart (combo)
If **no** → Stacked subplots

---

## Combo Chart (Same Scale)

Combine bar + line when both metrics share a scale.

**Example:** Revenue (bars) + margin % (line) — NOT same scale
**Example:** Sales this year + Sales last year (both EUR) — SAME scale

### Design Rules

- Use **left axis** for bars, **right axis** for line (or shared axis)
- Ensure scales are truly compatible
- Label both axes clearly
- Use distinct mark types (bar vs. line)
- Limit to 2 series per type

---

## Stacked Subplots (Different Scales)

Use multiple stacked panels when scales differ.

### Decision Tree

1. **Are scales compatible?** → Single chart
2. **Are scales different?** → Stacked subplots
3. **Do they share time/category?** → Share x-axis for alignment
4. **Is there a primary metric?** → Put it on top

### Financial Pattern: Revenue / Expense / Balance

Classic fiscal dashboard pattern:

```
┌─────────────────────┐
│   Revenue (bars)    │  ← Primary: EUR, large values
├─────────────────────┤
│  Expenditure (bars) │  ← Same scale as revenue
├─────────────────────┤
│   Balance (line)    │  ← Can be negative, different scale
└─────────────────────┘
```

This is the **IBCS-recommended** pattern for P&L visualization.

### Design Rules

- **Shared x-axis** for time alignment
- **Clear axis labels** on each panel
- **Visual separation** between panels (white space or line)
- **Consistent width** across panels
- **Primary metric on top**

---

## What NOT to Do

| Invalid Combination | Why |
|---------------------|-----|
| Bar + line, different scales | Two axes confuse comparison |
| 5+ lines | Visual clutter |
| Stacked bar + line on same axis | Incompatible encodings |
| Pie + line | No spatial relationship |
| Dual-axis without relationship | Misleading correlation |

---

## Dual-Axis Warning

**Use only when:**
- Variables have **direct, meaningful relationship**
- Scale units are **the same** (or directly comparable)
- You're not trying to **manufacture a correlation**

**Never use dual-axis to:**
- Force comparison of unrelated metrics
- Make two different things look correlated
- Hide that scales are incompatible

---

## IBCS Conventions

- **Solid bar** = actual
- **Line overlay** = secondary metric (same scale)
- **Hatched bar** = forecast
- **Reference line** = target/budget
- **Red/green** = negative/positive deviation

---

## Accessibility

- Label each axis clearly
- Don't rely on color alone
- Ensure sufficient contrast between elements
- Consider providing separate charts as alternative

---

## Sources

- principles.md — "Chart Combination Rules" section
- IBCS Standards — Multi-panel charts
- Playfair Data — "Cornerstone Module Part 2" (combo charts)