# Tables and Heatmap Tables

Tables present data in structured rows and columns. When enhanced with color, they become heatmap tables — combining the precision of tables with visual pattern recognition.

---

## When to Use

| Scenario | Best Variant |
|----------|-------------|
| Show exact values | Plain table |
| Show patterns across values | Heatmap table |
| Show trend alongside values | Table with sparklines |
| Rank items | Sorted table |
| Compare to target | Table with conditional formatting |

---

## Plain Tables

### Best For

- Exact values required
- Lookups and reference
- Precise comparison
- Accessible alternative to charts

### Design Rules

- **Header row:** Clear, bold, distinct background
- **Alignment:** Numbers right-aligned, text left-aligned
- **Alternating rows:** Zebra striping for readability (optional)
- **Borders:** Light, only where needed
- **Padding:** Adequate whitespace

### Formatting

- **Numbers:** Consistent decimal places
- **Thousands separator:** Use for large numbers
- **Units:** In header, not every cell
- **Null handling:** Show "—" or "N/A" clearly

---

## Heatmap Table

Add color encoding to table cells.

### Best For

- Pattern recognition across many values
- Finding highs and lows
- Showing distribution

### Color Encoding

- **Sequential:** Light→dark for low→high
- **Diverging:** Two colors for diverging values
- **Semantic:** Red/green for negative/positive

### Design Rules

- **Color intensity:** Vary by value magnitude
- **White text on dark:** For contrast
- **Include numbers:** Don't hide values behind color
- **Legend:** Show color scale

---

## Table with Sparklines

Embed mini-charts in table cells.

### Best For

- Show trend with current value
- Rank items with context
- Compact dashboard layouts

### Design Rules

- **Sparkline width:** 50-100px
- **Consistent scale:** Same y-axis across rows
- **Current value prominent:** Bold or highlighted
- **Max rows:** 10-15 to avoid clutter

---

## Conditional Formatting

Highlight based on values.

### Types

- **Data bars:** Bar within cell showing magnitude
- **Color scales:** Background color by value
- **Icon sets:** Traffic lights, arrows
- **Threshold-based:** Color if above/below target

### Design Rules

- **Don't over-format:** One method per column max
- **Clear rules:** Show thresholds
- **Consistent:** Same logic across similar columns

---

## Common Mistakes

| Mistake | Problem | Solution |
|---------|---------|----------|
| Too many columns | Horizontal scroll | Limit to 5-7 essential |
| Too many rows | Vertical scroll | Paginate or limit to top N |
| No alignment | Hard to compare | Right-align numbers |
| Color without numbers | Lose precision | Include values |
| 3D effects | Hard to read | Always flat |

---

## Accessibility

- Clear header row
- Adequate contrast
- Provide for screen readers
- Consider sortable columns

---

## IBCS Conventions

- **Consistent formatting** across similar columns
- **Units in header** not every cell
- **Negative values** with minus or parentheses
- **Nulls** clearly marked

---

## Sources

- Playfair Data — "3 Ways to Make Handsome Highlight Tables"
- Playfair Data — "Bullet graphs" (table variant)
- EU Data Visualisation Guide — Tables
- IBCS Standards — Table conventions