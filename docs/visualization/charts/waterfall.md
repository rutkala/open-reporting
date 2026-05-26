# Waterfall Charts

A waterfall chart (also called bridge, flying brick, or Mario chart) shows how a starting value becomes a final value through positive and negative contributions. It's ideal for explaining the components of change.

---

## When to Use

| Scenario | Example |
|----------|---------|
| Explain revenue change | Q1 → Q2 revenue (+new, -churn, +expansion) |
| Show P&L breakdown | Revenue - COGS - OpEx = Net Income |
| Variance analysis | Budget → Actual variance by category |
| Inventory flow | Opening + Purchases - Sales - Adjustments = Closing |

---

## Anatomy

A waterfall chart consists of:
- **Start bar** — Initial value
- **Step bars** — Individual contributions (floating)
  - Green/up = positive contribution
  - Red/down = negative contribution
- **Connector lines** — Show the running total
- **Total bar** — Final value (anchored to axis)

---

## Design Rules

### Structure

- **First bar:** Starting value (e.g., previous period)
- **Middle bars:** Each contribution as floating bar
- **Final bar:** Ending value (anchored to zero)
- **Connectors:** Thin lines connecting step to next start

### Color

- **Positive (increase):** Green or blue
- **Negative (decrease):** Red or orange
- **Totals:** Dark grey or neutral

### Sorting

- Sort by **magnitude** (largest absolute contribution first)
- Or sort by **logical flow** (chronological, categorical)

### Labels

- Include **value labels** on each bar
- Include **percentage** of total change (optional)
- Clear **axis labels** for start/end values

---

## Variants

### Composition Waterfall

Show how parts add up to whole.

**Best for:** Budget allocation, cost breakdown

### Contribution Waterfall

Show what drove the change.

**Best for:** Variance analysis, period-over-period explanation

### Bridge Chart

Connect two values with explanatory breakdown.

**Best for:** "How we got from A to B" stories

---

## Common Mistakes

| Mistake | Problem | Solution |
|---------|---------|----------|
| No connector lines | Hard to track running total | Add thin connector lines |
| Wrong color logic | Confusing positive/negative | Green = up, Red = down |
| Too many steps | Clutter | Group small items as "Other" |
| Starting at zero vs. floating | Inconsistent anchoring | Consistent approach |
| 3D effects | Distorted proportions | Always use 2D |

---

## IBCS Conventions

- **Green** = positive deviation (favorable)
- **Red** = negative deviation (unfavorable)
- **Dark grey** = totals/start/end
- Clear labeling of what each step represents

---

## Accessibility

- Don't rely on color alone — include labels
- Ensure sufficient contrast
- Provide data table alternative

---

## Sources

- Playfair Data — "Introducing Gap Charts in Tableau" (waterfall variant)
- IBCS Standards — Waterfall conventions
- EU Data Visualisation Guide — Chart types