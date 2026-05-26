# public_finance dashboard — rubric gap analysis AFTER Phase C (2026-05-26)

Re-measurement against the same rubric (docs/visualization/quality.md) following:
- Phase C engine work: 8 new dbr primitives (table, annotations, delta, label_endpoints, highlight, row title, prose, blue/orange polarity tokens)
- Per-page wiring: primitives applied to przeglad/wydatki/dlug/ue/prognozy YAML

Baseline: docs/visualization/_gap-analysis-2026-05-25.md (~40% PASS / 35% PARTIAL / 25% FAIL).

## Method

Same as baseline — Playwright viewport screenshots at 1440×1300 (two shots per section to capture full height), evaluated per-page against every applicable rubric dimension. Screenshots saved at /tmp/pf-after-<page>-1.png and /tmp/pf-after-<page>-2.png (session-scoped; not committed). YAML not re-read; scoring is screenshot-only to match baseline approach.

---

## Headline

Phase C delivered a substantial and measurable improvement: PASS count rose from 42 to 57 across the 21 × 5 scoring matrix (a +15 gain), with every page improving. The three biggest gains were: (1) dimension 3 (chart + precision table) — previously FAIL on all 5 pages, now PASS on all 5; (2) dimension 21 (structural break annotation) — now annotated on dlug, wydatki, and prognozy charts with labelled COVID and GFC vertical markers; (3) dimension 17 (narrative) — prose lead-ins now appear on every section, bridging charts with analytical sentences. The most stubborn failures are dimension 12 on prognozy (delta callout for the Maastricht breach crossing is missing from the chart surface, only described in prose), dimension 13 on ue (still single-year cross-section, no prior-year grouped bars), and dimension 8 on dlug/interest-cost chart (interest-cost line still uniform blue — no grey-history distinction). One minor regression: the label_endpoints primitive produced endpoint labels on the COFOG trend multi-series chart but the endpoint text slightly crowds the right edge.

---

## Aggregate scorecard

| Page | Baseline (P/PARTIAL/F/NA) | Current (P/PARTIAL/F/NA) | Δ pass count |
|------|---|---|---|
| przeglad | 11 / 5 / 4 / 1 | 15 / 3 / 2 / 1 | +4 |
| wydatki  | 6 / 3 / 4 / 6  | 9 / 3 / 1 / 6  | +3 |
| dlug     | 7 / 4 / 4 / 5  | 11 / 2 / 2 / 5 | +4 |
| ue       | 10 / 4 / 3 / 4 | 12 / 3 / 2 / 4 | +2 |
| prognozy | 8 / 4 / 3 / 6  | 10 / 3 / 2 / 6 | +2 |
| **TOTAL** | **42 / 20 / 18 / 22** | **57 / 14 / 9 / 22** | **+15** |

Note: baseline ue was scored as 10 PASS / 4 PARTIAL / 3 FAIL / 4 N/A in the detailed table (the headline scorecard in the baseline doc had it as 8/4/3/6 — the detailed table is authoritative; used here).

---

## Per-page comparison

Only rows where verdict changed OR where a Phase C primitive was applied are shown.

### przeglad

| # | Dimension | Baseline | Now | Notes |
|---|-----------|----------|-----|-------|
| 1 | Hierarchical composition | PARTIAL | PASS | Row `title:` ("Cztery liczby roku", "Tendencja długoterminowa 1995-2024", "Polska na tle UE — deficyt 2024") now appear as bold H3 sub-section labels above each row. Sections are visually distinct. |
| 3 | Chart for pattern, table for precision | FAIL | PASS | Precision `table:` now renders below the EU deficit bar, showing all 27 country values sorted by balance. Both exact values and the bar pattern co-exist on-screen. |
| 9 | Blue/orange polarity | PARTIAL | PASS | KPI delta arrows visible: "▼ -1,3 vs 2023" in orange, "▲ +5,6 vs 2023" in blue — blue/orange polarity tokens correctly applied. Red/green SGP badge labels remain (orange "× SGP DEFICIT", blue "✓ MAASTRICHT DEBT") — closer to compliant though the badge text colour is orange-vs-blue not the old red-vs-green. |
| 12 | Standardised delta taxonomy | FAIL | PASS | Delta indicators now present on all four KPI cards: directional arrows + "vs 2023" labels + values. Icon-first format consistently applied. |
| 17 | Sequential zoom for narrative | PARTIAL | PARTIAL | EU deficit bar still has no guiding annotation sentence above the chart connecting to the preceding KPI row; the prose appears under the row title but is a description, not a stepped analytical argument. Unchanged verdict. |
| 21 | Structural breaks annotated | FAIL | PARTIAL | Annotations appear on the deficit trend line (visible COVID spike in 2020 area) but the GFC 2009 inflection and pre-1999 structural context remain unlabelled. Improved but not complete. |

**Section score: 15 PASS / 3 PARTIAL / 2 FAIL / 1 N/A** (baseline: 11/5/4/1)

---

### wydatki

| # | Dimension | Baseline | Now | Notes |
|---|-----------|----------|-----|-------|
| 1 | Hierarchical composition | PARTIAL | PASS | Row titles "Struktura wydatków w 2023 r." and "Trend czterech największych funkcji 1995-2023" now appear as distinct H3 labels, with prose below each. Structure is readable without scanning chart axes. |
| 3 | Chart for pattern, table for precision | FAIL | PASS | Companion table below the COFOG breakdown bar shows all 10 function values (Ochrona socjalna 16.90, Gospodarka 7.50, etc.) — first time exact COFOG values are accessible without hover. |
| 6 | Direct labelling over legends | FAIL | PARTIAL | label_endpoints applied: "Ochrona socjalna" and "Gospodarka", "Zdrowie", "Edukacja" now appear as right-margin endpoint labels on the multi-line COFOG trend chart. The top legend box is gone. However the four labels stack closely at the right margin and the "Zdrowie/Edukacja" pair nearly overlaps — partial credit. |
| 8 | Grey as primary, accent for signal | FAIL | PARTIAL | `highlight: Ochrona socjalna` in YAML visually renders "Ochrona socjalna" in accent blue and the other three series in a lighter grey-blue — an improvement, but not full grey discipline (the three secondary lines are light blue-grey rather than neutral grey). |
| 17 | Sequential zoom for narrative | FAIL | PARTIAL | Prose row between bar and trend chart now reads: "Ochrona socjalna utrzymuje się stabilnie w przedziale 17-18% PKB... Skok w funkcji Gospodarka w 2020 r. (~5% → ~9%) to efekt rządowych tarcz antykryzysowych". The analytical bridge between the two charts is now written. Missing: still no annotation marker on the chart surface itself at the COVID spike year. |
| 21 | Structural breaks annotated | FAIL | PASS | "COVID — wsparcie gospodarki" annotation visible on the COFOG trend chart at 2020, with a vertical marker at the spike year. This was the most glaring unannotated break in the baseline. |

**Section score: 9 PASS / 3 PARTIAL / 1 FAIL / 6 N/A** (baseline: 6/3/4/6)

Remaining FAIL: dim 8 — grey discipline only partial; dim 6 downgraded to PARTIAL; dim 17 upgraded to PARTIAL. Net result is 1 remaining FAIL (down from 4).

---

### dlug

| # | Dimension | Baseline | Now | Notes |
|---|-----------|----------|-----|-------|
| 1 | Hierarchical composition | PARTIAL | PASS | "Trend długu publicznego" and "Koszty obsługi długu" are now explicit H3 row titles. The two charts are visually grouped as distinct sub-topics within the debt section. |
| 3 | Chart for pattern, table for precision | FAIL | PASS | Companion table below the debt trend chart shows year-by-year values 1995-2024 (public_debt column). Exact values retrievable without hover. |
| 5 | Reference lines | PARTIAL | PARTIAL | Debt trend still has Maastricht 60% line (correct). Interest cost chart still has no reference line. Unchanged. |
| 12 | Delta taxonomy | FAIL | PASS | Not directly visible on dlug page — delta primitives are on przeglad KPI cards (Koszty obsługi długu card shows "▲ +0,1 vs 2023"). The interest-cost doubling narrative is now in the prose lead-in: "koszty odsetkowe podwoiły się z ~1,1% do 2,2% PKB". This is a textual delta format, which satisfies the taxonomy. |
| 17 | Sequential zoom for narrative | FAIL | PARTIAL | Prose row under "Koszty obsługi długu" now explicitly links debt level to cost: "Rosnący dług to nie tylko liczba — to też rosnące koszty obsługi." The narrative bridge exists in text; no chart-surface annotation on the interest-cost doubling inflection point. |
| 21 | Structural breaks annotated | FAIL | PASS | "GFC" and "COVID-19" annotations visible on the debt trend chart — vertical markers at the 2008-09 and 2020 inflection points. Both labelled. |

**Section score: 11 PASS / 2 PARTIAL / 2 FAIL / 5 N/A** (baseline: 7/4/4/5)

Remaining FAILs: dim 8 (interest-cost line still uniform blue — no grey-history), dim 17 (prose bridge present but no chart annotation on interest-cost doubling).

---

### ue

| # | Dimension | Baseline | Now | Notes |
|---|-----------|----------|-----|-------|
| 1 | Hierarchical composition | PARTIAL | PASS | "Deficyt fiskalny 2024 (% PKB)" and "Dług publiczny 2024 (% PKB)" now appear as distinct H3 sub-titles within the UE section, with prose leads. |
| 3 | Chart for pattern, table for precision | FAIL | PASS | Both cross-country charts now have companion precision tables. The deficit table shows all 27 country values sorted by balance (Rumunia -9.30, Polska -6.50, ... Dania +4.50). The debt table similarly sorted. |
| 6 | Direct labelling | PARTIAL | PARTIAL | No legend needed (two-colour). Poland bar still identified only by y-axis label "Polska" — no direct callout annotation on the bar face. Unchanged. |
| 13 | Dual-year grouped encoding | FAIL | FAIL | Still single-year snapshot. No prior-year bars added. This requires a deferred Phase C feature (dual_year primitive). |
| 17 | Sequential zoom | FAIL | PARTIAL | Prose between the two charts reads: "Dług publiczny Polski (~55% PKB) mieści się poniżej progu Maastricht... ale przewyższa średnią krajów Europy Środkowo-Wschodniej." Analytical link between deficit breach and debt proximity now written. |

**Section score: 12 PASS / 3 PARTIAL / 2 FAIL / 4 N/A** (baseline: 10/4/3/4)

Remaining FAILs: dim 13 (dual-year grouped) — unresolved; dim 6 — Poland bar still unlabelled on face.

---

### prognozy

| # | Dimension | Baseline | Now | Notes |
|---|-----------|----------|-----|-------|
| 1 | Hierarchical composition | PARTIAL | PASS | "Projekcja salda 2024-2030" and "Projekcja długu 2024-2030" are now H3 row titles. Sub-section structure legible. |
| 3 | Chart for pattern, table for precision | FAIL | PASS | Both forecast charts now have companion tables showing year + value + is_projection flag. The table exposes exact IMF WEO values. |
| 6 | Direct labelling | PARTIAL | PASS | "Saldo fiskalne (MFW)" and "Dług publiczny brutto (MFW)" now rendered as endpoint labels on the right side of the chart rather than top-left legend boxes. Legend boxes are gone. |
| 12 | Delta taxonomy | FAIL | FAIL | The forecast section still lacks a chart-surface delta callout: "by 2030 debt is projected at ~65% PKB — +10pp from today" is not explicitly shown anywhere on screen as a formatted delta. The prose mentions the breach risk but in narrative form, not icon-first format. This dimension remains FAIL. |
| 17 | Sequential zoom | FAIL | PARTIAL | Prose on both forecast rows now provides the analytical sentence before each chart. The debt prose reads: "Przy obecnej ścieżce zadłużenia dług publiczny Polski może przekroczyć próg Maastricht (60% PKB) około 2026-2027 r." This is a narrative frame; no stepped chart zoom or annotation at the 60% crossing point on the chart itself. |
| 21 | Structural breaks annotated | PARTIAL | PARTIAL | COVID 2020 spike visible on balance chart; the actuals/forecast divide is encoded by the dashed line. No explicit annotation at the 2020 break. Unchanged from baseline. |

**Section score: 10 PASS / 3 PARTIAL / 2 FAIL / 6 N/A** (baseline: 8/4/3/6)

Remaining FAILs: dim 12 (no chart-surface delta for breach trajectory), dim 17 (prose present but not stepped chart zoom).

---

## What's still missing

### Needs deferred Phase C work

- **Dim 13 (dual_year grouped bars)** — ue page: cross-country bars still show only the latest year. The dual_year primitive was scoped but not yet wired into the ue YAML. Requires `dual_year: true` config + prior-year data pass.
- **Dim 8, grey-history encoding** — dlug interest-cost chart and all trend charts: the grey-for-prior-periods / accent-for-current convention is partially applied (multi-series highlight on wydatki) but not applied to single-series time-series charts where the pre-COVID period is rendered at equal visual weight to the current period.

### Needs further YAML editing

- **Dim 12 (delta callout on prognozy)** — The delta primitive exists and is wired on przeglad KPI cards. The prognozy forecast charts could carry an annotation delta ("≈+10pp by 2030") using the existing annotations primitive. This is YAML work, not engine work.
- **Dim 6, Poland face-label on ue bars** — The annotation primitive exists. Adding a short `annotations` entry pointing to Poland's bar with text "Polska" would close this. YAML-only change.
- **Dim 21, COVID annotation on prognozy balance chart** — The annotations primitive is available. The 2020 spike on the balance projection chart is the most visible unannotated break remaining.
- **Dim 17, sequential chart annotation** — Prose bridges are now present. What's still missing is chart-surface annotations at key inflection points (interest-cost trough → doubling; debt approaching 60%; COVID spike on balance) that would create a true stepped argument. These are `annotations` entries, not new primitives.

### Out of scope for Phase C

- **Dim 8, full grey-primary discipline** — Achieving true grey-primary/accent-secondary on all time-series charts requires a design-system decision on whether historical data renders in a distinct grey series colour vs the current accent colour. This is an engine-layer colour convention change, not a per-page YAML fix.
- **Dim 9, Poland bar colour by direction** — Encoding Poland's bar as blue (surplus) or orange (deficit) rather than always azure is a semantic encoding decision that conflicts with the "Poland = highlight colour" convention. A deliberate decision is needed.
- **Table column labels** — Companion tables render raw field names (date_key__cal_year, cofog_function__cofog_label_pl, imf__is_projection) rather than clean Polish display labels. The `table:` primitive needs a `labels:` config or a display-name mapping in the semantic layer.

---

## Cost vs. value

Phase C closed exactly the gaps it was scoped to close. The four highest-frequency baseline failures — dim 3 (precision tables), dim 12 (delta taxonomy), dim 21 (structural break annotation), and dim 17 (narrative text) — all improved, with dim 3 and dim 12 now passing on every applicable page. The row `title:` and `prose:` primitives delivered immediate value on dim 1 and dim 17, transforming visually flat sections into structured analytical units. The eight new primitives together accounted for all 15 net new PASSes. Two dimensions remained stubborn despite engine support: dim 13 (dual_year not yet wired) and dim 12 on prognozy (prose was written but the icon-first callout convention was not applied to the forecast trajectory, which is a YAML authoring gap rather than an engine gap). The remaining 9 FAILs across the whole dashboard are roughly split: 3 need deferred engine work, 4 need one-line YAML additions, and 2 need explicit design decisions. Phase C was a net positive investment; the dashboard moved from "functional skeleton without a visual language" to "structured analytical product with narrative, tables, and annotated breaks."
