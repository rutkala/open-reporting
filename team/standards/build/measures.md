# Measures Standard

Rules for formatting numbers, units, and measures across all dashboards.

---

## Number Formatting

### Decimals

| Measure type | Decimal places | Example |
|-------------|----------------|---------|
| Whole numbers (counts, years) | 0 | `1 234` |
| Percentages | 1 | `56,7%` |
| Currency (large values) | 1 | `1 234,5 mln zł` |
| Currency (small values) | 2 | `123,45 zł` |
| Ratios / indices | 2 | `1,23` |
| Rates per 1000 | 1 | `12,3‰` |

### Thousand Separator

- Use **space** as thousand separator: `1 234 567`
- Use **comma** as decimal separator: `1 234,56`
- No separator for 4-digit numbers: `1234`
- Separator for 5+ digits: `12 345`

### Large Number Abbreviations

| Value range | Format | Example |
|-------------|--------|---------|
| < 1 000 | full number | `890` |
| 1 000 – 999 999 | thousands | `12,3 tys.` |
| 1 000 000 – 999 999 999 | millions | `1 234,5 mln` |
| ≥ 1 000 000 000 | billions | `1,2 mld` |

---

## Units of Measure

### Placement

- **KPI cards**: unit next to value, smaller font, muted color
  - Example: `1 234` `mln zł`
- **Chart axis**: unit in axis title, not on each tick
  - Example: `Wartość (mln zł)`
- **Table columns**: unit in column header
  - Example: `PKB (mld zł)`

### Standard Unit Names (Polish)

| Unit | Abbreviation | Usage |
|------|-------------|-------|
| złoty | `zł` | currency |
| tysiąc | `tys.` | 10³ |
| milion | `mln` | 10⁶ |
| miliard | `mld` | 10⁹ |
| procent | `%` | percentage |
| promil | `‰` | per mille |
| punkt procentowy | `pp` | percentage point change |
| osoba | `os.` | headcount |
| rok | `rok` | year reference |
| udział | `udział` | share/participation |

---

## Semantic Formatting

### Trends

| Direction | Symbol | Color |
|-----------|--------|-------|
| Increase (positive) | `▲` | POSITIVE |
| Decrease (negative) | `▼` | NEGATIVE |
| No change | `—` | SUBTEXT |

### Ranges

- Use en-dash: `2019–2024`
- Use "do" for text: `od 2019 do 2024`

---

## Implementation

### KPI Card

```python
kpi_card(
    label="Saldo fiskalne",
    value="-123,4",
    unit="mln zł",
    trend="▲ +5,2 pp",
    trend_color=POSITIVE,
)
```

### Chart Axis

```python
fig.update_layout(
    yaxis_title="Wartość (mln zł)",
    xaxis_title="Rok",
)
```

### Table Column

```python
dash_table.DataTable(
    columns=[
        {"name": "Rok", "id": "year"},
        {"name": "PKB (mld zł)", "id": "gdp"},
    ],
)
```
