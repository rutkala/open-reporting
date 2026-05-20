# KPI Card

## When to use
Display a single key metric as a callout value — optionally with a comparison (target,
prior period, benchmark) and trend arrow. Always placed at the top of a section before
charts. Use `kpi_standard` for primary KPIs, `kpi_compact` for secondary/dense rows.
**Not:** for showing trends over time (use Line); for showing distributions (use Histogram).

## Field bindings
| Slot | Required | Accept |
|------|----------|--------|
| VALUE | Yes | single aggregated scalar — `_scalars["metric_key"]` |
| LABEL | Yes | metric display name — from `m.MEASURES["key"].label` |
| UNIT | Yes | tick suffix — from `m.MEASURES["key"].plotly_ticksuffix` |
| REFERENCE VALUE | No | comparison scalar (target, prior year, EU avg) |
| REFERENCE LABEL | No | label for the reference ("Cel", "Rok poprz.", "UE-27") |
| TREND | No | trend string e.g. `"▲ +0.8"` or `"▼ -1.2"` |
| TREND COLOR | No | `POSITIVE` (green), `NEGATIVE` (red), `SUBTEXT` (neutral) |

## Import
```python
from complex_dashboard.assets.components.kpi_card import kpi_row, kpi_standard, kpi_compact
from complex_dashboard.assets.theme import POSITIVE, NEGATIVE, SUBTEXT
```

## Template — standard row (primary KPIs)
```python
# VALUE:     _scalars["TODO_metric"] — pre-aggregated scalar from data_loaders
# LABEL:     m.MEASURES["TODO"].label
# UNIT:      m.MEASURES["TODO"].plotly_ticksuffix
# REFERENCE: comparison scalar + label (optional)
# TREND:     direction string + colour (optional)

kpi_row([
    kpi_standard(
        label=m.MEASURES["TODO_MEASURE_1"].label,
        value=m.MEASURES["TODO_MEASURE_1"].kpi_value(_scalars["TODO_MEASURE_1"]),
        unit=m.MEASURES["TODO_MEASURE_1"].plotly_ticksuffix,
        reference_value=m.MEASURES["TODO_MEASURE_1"].kpi_value(TODO_TARGET),
        reference_label="TODO: Cel / Rok poprz. / UE-27",
        trend="▲ +0.8",         # TODO: replace with actual delta
        trend_color=POSITIVE,   # TODO: POSITIVE / NEGATIVE / SUBTEXT
    ),
    kpi_standard(
        label=m.MEASURES["TODO_MEASURE_2"].label,
        value=m.MEASURES["TODO_MEASURE_2"].kpi_value(_scalars["TODO_MEASURE_2"]),
        unit=m.MEASURES["TODO_MEASURE_2"].plotly_ticksuffix,
    ),
    kpi_standard(
        label=m.MEASURES["TODO_MEASURE_3"].label,
        value=m.MEASURES["TODO_MEASURE_3"].kpi_value(_scalars["TODO_MEASURE_3"]),
        unit=m.MEASURES["TODO_MEASURE_3"].plotly_ticksuffix,
        trend="▼ -1.2",
        trend_color=NEGATIVE,
    ),
])
```

## Template — compact row (secondary KPIs / dense layout)
```python
kpi_row([
    kpi_compact(
        label=m.MEASURES["TODO_1"].label,
        value=m.MEASURES["TODO_1"].kpi_value(_scalars["TODO_1"]),
        unit=m.MEASURES["TODO_1"].plotly_ticksuffix,
    ),
    kpi_compact(
        label=m.MEASURES["TODO_2"].label,
        value=m.MEASURES["TODO_2"].kpi_value(_scalars["TODO_2"]),
        unit=m.MEASURES["TODO_2"].plotly_ticksuffix,
        trend="▲ +0.3", trend_color=POSITIVE,
    ),
    kpi_compact(
        label=m.MEASURES["TODO_3"].label,
        value=m.MEASURES["TODO_3"].kpi_value(_scalars["TODO_3"]),
        unit=m.MEASURES["TODO_3"].plotly_ticksuffix,
    ),
], min_width="140px", gap="12px")
```

## Rules
- 3–5 cards per `kpi_row` (Cowan 4±1 — never more than 5)
- Use `kpi_standard` for top-level KPIs; `kpi_compact` only in secondary rows
- `trend_color`: `POSITIVE` for good direction, `NEGATIVE` for bad — never for decoration
- Always provide `reference_value` + `reference_label` on primary KPIs
- KPI row always comes before charts in a section
