> **ARCHIVED 2026-05-22** — describes a prior state of the project. Current architecture: [`../ARCHITECTURE.md`](../ARCHITECTURE.md).

# OR-142 — Chart Template Evaluation Findings
<!-- date: 2026-04-08 -->

Two-pass review: code audit (visualization-reviewer) + screenshot audit (visual-screenshot-reviewer) against `docs/visualization-diff.md` and `docs/visualization/reviewing.md`.

**Overall verdict: CONDITIONAL** — no blocking HIGH findings, but several MEDIUM issues to fix in OR-143.

---

## Combined Findings

### MEDIUM (fix in OR-143)

| # | Source | Component | Finding | Rule |
|---|--------|-----------|---------|------|
| M1 | Code | `combo_chart.py` — `combo_subplots` | `diverging=True` on `"type": "line"` panel applies `POSITIVE` colour unconditionally — line is always green regardless of whether values cross zero | Colour semantics — trend direction |
| M2 | Screenshot | Template | Axis labels (measure name / unit) absent on Clustered column, Stacked column, 100% Stacked, Clustered+Stacked, Combo chart sections | Axis labels required |
| M3 | Screenshot | Template | Clustered area chart — all series collapse into a near-flat band, 90% of plot area empty. Likely sample data issue; confirms the component needs better default sample data | Chart legibility / series spread |
| M4 | Screenshot | Template | Line chart — two series nearly flat and overlapping across full x-axis. Same root cause as M3 | Chart legibility / series spread |

> **M3 / M4 note:** The collapse is a sample data problem in `template/data.py`, not a component bug. Fix is to update sample data to show meaningful spread across all chart types.

> **KPI delta colour:** Screenshot reviewer flagged green delta (▲ +0.8) alongside a value (47.4) below a target (50.0). This is a sample data framing issue, not a component bug — the component correctly takes `trend_color` from the caller. No fix needed in the component; update sample data so the demo is internally consistent.

---

### LOW (fix in OR-143 or follow-up)

| # | Source | Component | Finding | Rule |
|---|--------|-----------|---------|------|
| L1 | Code | `line_chart.py` — `stacked_area` | `line.width=1.5` — below the 2px KB minimum | Line width minimum 2px |
| L2 | Code | `combo_chart.py` — `line_clustered_column`, `line_stacked_column`, `line_pct_stacked_column` | No inline comment confirming both series share the same scale | Combo shared-scale comment |
| L3 | Code | `kpi_card.py` | No guard or docstring warning against passing `reference_value` without `reference_label` | KPI reference requires label |
| L4 | Code | `map_chart.py` | Hardcoded colour strings (`"#EEF3F7"`, `"#FFFFFF"`) not imported from `theme.py` | Theme system consistency |
| L5 | Screenshot | Template | No source attribution visible anywhere on page | Source attribution required |
| L6 | Screenshot | Template | Subtitle absent from most charts (only KPI card has one) | Subtitle convention |
| L7 | Screenshot | Template | Inconsistent decimal formatting across KPI card, table, waterfall | Number formatting consistency |

> **L5–L7 note:** Template is a developer reference scaffold, not a user-facing product. L5 source attribution is N/A for the scaffold. L6/L7 are valid sample data and default improvements for OR-143.

---

## What was NOT reviewed

- `datalist` and `funnel` chart types (screenshot not captured — covered by code review)
- Sidebar nav item truncation (too small in screenshots)
- `bar_chart.py` docstring nudge for `show_labels=True` on ≤8 categories (LOW, no rule violation)

---

## Fix scope for OR-143

**In `products/visuals/components/`:**
- `combo_chart.py`: Fix `diverging=True` line panel colour logic (M1)
- `line_chart.py`: Change `stacked_area` line width from 1.5 → 2 (L1)
- `combo_chart.py`: Add inline shared-scale comment to 3 combo variants (L2)
- `map_chart.py`: Import `#EEF3F7` and `#FFFFFF` from `theme.py` or define as module constants (L4)

**In `products/dashboards/template/data.py`:**
- Update sample data to show meaningful spread in area/line chart examples (M3/M4)
- Fix KPI sample so delta direction is consistent with target gap (KPI note)
- Add subtitles to chart samples (L6)
- Standardise decimal places across components (L7)

**In `products/dashboards/template/app.py`:**
- Add y-axis labels to clustered column, stacked column, and combo chart examples (M2)
