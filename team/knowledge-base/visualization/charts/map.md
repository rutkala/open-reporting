# Maps (Choropleth and Symbol)

Maps visualize geographic data — showing spatial patterns, regional comparisons, and location-based metrics.

---

## When to Use

| Scenario | Best Variant |
|----------|-------------|
| Show values by region | Choropleth (colored regions) |
| Show magnitude at points | Symbol/circle map |
| Both value and location | Combined |
| Show flows between locations | Flow/arc map |

---

## Choropleth Map

Regions colored by value (e.g., unemployment rate by state).

### Best For

- Regional metrics (country, state, province)
- Normalized rates (per capita, percentage)
- Comparison across geographic areas

### Design Rules

- **Use normalized data:** Avoid raw counts (population, not total cases)
- **Consistent intervals:** Use quantile, equal interval, or natural breaks
- **Clear legend:** Show color scale with values
- **Include labels:** Label notable regions

### Color

- **Sequential:** Single hue light→dark for low→high
- **Diverging:** Two colors for diverging (e.g., +/– from zero)
- **Colorblind-safe:** Test with simulators

---

## Symbol/Proportional Circle Map

Circles sized by value at location.

### Best For

- Raw totals (total sales, population)
- Point locations (stores, cities)
- Magnitude comparison

### Design Rules

- **Size by area, not radius:** Area = value
- **Limit size range:** Max 10-15x min to avoid dominance
- **Transparent fill:** 50% if overlapping
- **Include value labels:** On largest circles

---

## Combined Choropleth + Symbols

Show both rate and total.

- Choropleth for rate (color)
- Overlay symbols for total (size)

---

## Common Mistakes

| Mistake | Problem | Solution |
|---------|---------|----------|
| Raw counts on choropleth | Misleading (bigger = more, not worse) | Use rates/per capita |
| Too many classes | Hard to distinguish | Limit to 5-7 classes |
| Rainbow colors | No logical order | Use sequential palette |
| Missing data | Gaps unclear | Mark as "no data" |
| Overly detailed geography | Clutter | Use higher level (country vs county) |

---

## Accessibility

- Don't rely on color alone
- Include labels for values
- Provide table alternative
- Test with colorblind simulators

---

## Data Considerations

- **Geographic boundaries:** Need shapefiles or built-in geocoding
- **Aggregation level:** Country, state, county — choose appropriate
- **Normalize:** Rates vs. raw values
- **Missing data:** Handle explicitly

---

## Sources

- Playfair Data — Map tutorials
- EU Data Visualisation Guide — Chart types
- Material Design — Data visualization
- Urban Institute styleguide — Map conventions