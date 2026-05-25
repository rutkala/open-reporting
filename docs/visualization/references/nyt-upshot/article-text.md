# The Pudding — "Birthday Effect" — Article Text

Source: https://pudding.cool/2025/04/birthday-effect
Author: Alvin Chang
Fetched: 2026-05-25

Note: NYT Upshot is network-blocked (ECONNREFUSED on nytimes.com). The Pudding is used as substitute — same design-journalism tradition, full access.

## Section Headings

- You will die someday
- The question
- But… (appears multiple times as narrative transitions)
- So what have we learned?
- Data and methods

## Summary

The article explores the "birthday effect" — the statistical phenomenon that people are more likely to die on their birthdays than on other days. Using Massachusetts death records 1990-2024 (1.9+ million records), the author demonstrates a 7.0% excess of birthday deaths after controlling for seasonal mortality patterns.

Key statistical concepts explained through progressive chart sequences:
- Z-scores and p-values (p ≈ 0.000001)
- Standard deviation bands on a distribution
- Seasonal mortality confounds

## Methodology

- Data: Massachusetts death records 1990-2024
- Method: Control for seasonal mortality by comparing each birthday against same calendar day across non-birthday years; compute z-score distribution
- Tool: Custom web scrollytelling (D3/canvas likely)

## Visualizations Used

1. **Full-year bar chart** — 365 bars, one per day-difference from birthday, all grey, x-axis from -182 to +182, y-axis ~50–180 deaths. Shows apparent uniform distribution.
2. **Zoomed bar chart with highlight** — Same chart zoomed to ±20 days, birthday bar highlighted red with annotation "183 birthday deaths", dashed average line at 156.
3. **Distribution/histogram of death counts** — Bell-curve histogram showing death count buckets (115–120 to 180–185), one bar coloured red ("8 days" in that tail range).
4. **Standard deviation histogram** — Same histogram with teal bars for "1+" std dev range and red bars for "2+" — illustrates statistical extremity of the birthday bar.
5. Monthly birth/death comparison (mentioned but not captured)
6. 365-day contingency grid (mentioned but not captured)

## Image Assets Captured

- assets/sketches/all-2000.webp — full year bar chart (grey, coarse view)
- assets/sketches/histogram.webp — death count distribution histogram
- assets/sketches/stddev.webp — std dev coloured histogram
- assets/sketches/enhance.webp — zoomed bar chart with birthday highlight
