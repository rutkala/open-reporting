# Patterns extracted from references — for the design phase

Synthesis of design patterns from Phase 2 reference research. Each pattern is annotated with where it came from and whether to ADOPT, ADAPT, or REJECT for our Polish-citizen public-finance dashboard.

---

## Patterns to ADOPT directly

### P1 — Absolute currency primary, %GDP secondary
**From:** Where Does It Go? (UK), USAFacts
**Why:** Citizens don't natively read %GDP. £1.37tn is real; 41% GDP is abstract. Every KPI shows both, but PLN is the larger / more prominent number.
**Our implementation:** KPI cards lead with `1 806 mld zł`, show `49.4% PKB` as sub-line. Charts axis-label both.

### P2 — Linear story-arc page structure (no complex tabs)
**From:** Where Does It Go?, USAFacts annual digest
**Why:** Citizens scroll; they don't navigate. Top-down: total → breakdown → comparison → trend → projection.
**Our implementation:** Page order = story order. No "Explorer" tab. Sidebar nav is for orientation, not deep navigation.

### P3 — Categories by function, not by institution
**From:** Where Does It Go?, USAFacts
**Why:** Citizens think "zdrowie / edukacja / obrona" not "Ministry X / Voivodeship Y".
**Our implementation:** COFOG functional categories with Polish labels (Ochrona socjalna, Zdrowie, Edukacja, Obrona, …) — already done.

### P4 — Source visible on every chart
**From:** All authoritative references
**Why:** Trust signal. Polish citizens need to verify; mistrust of official data is real.
**Our implementation:** Every chart footer: `Źródło: Eurostat (ESA 2010), 2024.` Visible, not micro-print.

### P5 — Threshold reference lines on bench-marked metrics
**From:** IMF DataMapper, OECD, our Phase B work
**Why:** Maastricht 60%, SGP −3% are referenced in every news article — visitors need to see where Poland sits relative.
**Our implementation:** Dashed red reference line at −3% on every deficit chart, 60% on every debt chart. With Polish annotation: `Próg SGP (-3% PKB)`, `Próg Maastricht (60% PKB)`.

### P6 — History + projection visual language
**From:** IMF DataMapper, our Phase B dash_when
**Why:** Citizens want trajectory: where we've been, where we're heading. Solid line = past, dashed = forecast.
**Our implementation:** Already built — `options.dash_when` on line visuals. Use on both deficit and debt projection charts.

### P7 — Cross-country comparison as ranked bar (sorted)
**From:** OECD bar charts, our Phase A EU comparison
**Why:** "Where does Poland sit?" answered immediately by position in sorted list. Highlight Poland.
**Our implementation:** Already built — Phase A horizontal bar with Polska in `azure_1`, others in `slate_3`. Sort ascending by value.

---

## Patterns to ADAPT (modify for our context)

### P8 — Personal-relevance hook ("what your tax pays")
**From:** Where Does It Go? Chancellor Mode / tax-bracket calculator
**Why interesting:** Powerful citizen engagement device.
**Why ADAPT (not adopt):** Polish tax system is complicated (PIT, składki, VAT, akcyza). A calculator could be added later but adds significant complexity. v1 substitute: show `per capita` figures alongside totals where they're meaningful (debt per capita = ~53 000 zł, deficit per capita = ~6 200 zł in 2024).

### P9 — "Interpretive headline" per chart
**From:** USAFacts editorial framing
**Why interesting:** A 1-sentence interpretive headline turns "data" into "answer to citizen question".
**Why ADAPT:** Editorialising risks bias. Keep headlines descriptive but pointed:
- ❌ "Government spending is out of control" (opinion)
- ❌ "Government spending grew" (vague)
- ✅ "Wydatki państwa rosną szybciej niż dochody od 2022 r." (descriptive but informative)

### P10 — Five-year default historical window
**From:** Where Does It Go?
**Why interesting:** Citizens don't need 30-year history at first glance.
**Why ADAPT:** Our data goes 1995–2024. For citizens, default visible window should be ~last decade (2014–2024 or 2015–present) so trend is visible without overwhelming. Full history available but not shown by default.

### P11 — Award-winning proportional visual (block/area sized to £)
**From:** Information Is Beautiful UK Spending
**Why interesting:** Visceral comprehension of scale.
**Why ADAPT:** A flowing infographic isn't dbr-native. The same intuition can be served with stacked-bar % of expenditure, or with bar widths scaled by value. v1: use existing column/bar visuals well; consider treemap as a future dbr visual type if budget breakdown story warrants it.

---

## Patterns to REJECT

### R1 — "What if" / scenario simulation
**From:** Where Does It Go? Chancellor Mode
**Why reject:** Out of scope for v1. Requires modelling assumptions, would require user controls + recalculation logic. Defer to v2.

### R2 — Per-taxpayer / per-persona calculator
**From:** Where Does It Go? "New Graduate", "NHS Nurse" personas
**Why reject:** Out of scope. Requires PIT calculation logic. Per capita is the v1 substitute (P8).

### R3 — Real-time / monthly data
**From:** USAspending.gov, some Treasury sites
**Why reject:** Citizens don't think monthly about state finances. Annual data is right. Polish Ministry of Finance DBW provides monthly but we use annual.

### R4 — Dense tabular drilldown
**From:** Eurostat, OECD raw data interfaces
**Why reject:** Tables overwhelm citizen audience. Link out to source for deep dives.

### R5 — Editorial opinion / political framing
**From:** Some advocacy-organisation sites (FOR, citizen-budget projects with policy stance)
**Why reject:** Open Reporting brand is "non-partisan facts". Stay descriptive, never prescriptive.

### R6 — Quarterly granularity
**From:** Some IMF and Eurostat dashboards
**Why reject:** Citizens think annually. Already in the brief.

---

## Composite design implications for OUR dashboard

Combining the above into a coherent design direction:

### Page sequence (proposed for brainstorm phase)

The citizen question → page mapping from the brief, refined by reference patterns:

```
Page 1 — Ile państwo zbiera i wydaje?
   Headlines: Dochody (mld zł), Wydatki (mld zł), Saldo (mld zł + % PKB)
   Trend: revenue vs expenditure 2015–2029 (history solid, projection dashed)
   Reference line: SGP −3% on saldo chart
   Editorial headline (descriptive)

Page 2 — Na co idą wydatki państwa?
   COFOG breakdown — sorted horizontal bar at latest year (not 10-stack)
   Headline: largest categories explicit (Ochrona socjalna, Gospodarka, Zdrowie...)
   Trend: top 4-5 categories over time (small multiples or focused line)
   Annotations: defence growth since 2022; healthcare aging

Page 3 — Jak duży mamy dług publiczny?
   Headlines: Dług total (mld zł), %PKB, per capita
   Trend: debt over time 2015–2029 (history solid, projection dashed)
   Reference line: Maastricht 60% PKB
   Interest cost as separate KPI ("ile płacimy odsetek")

Page 4 — Jak wypadamy w UE?
   EU-27 sorted bar — deficit + debt, two charts
   Polska highlighted
   EU-27 average line
   Reference threshold lines

Page 5 — Co czeka nas dalej?
   IMF projections — deficit and debt to 2029
   History + projection visual language (already built)
   Threshold annotations: when does debt cross 60%?
```

### Visual language summary

| Element | Choice |
|---|---|
| Primary number type | Absolute PLN (mld zł), with % PKB as secondary |
| Categorical colour | Nordic azure/slate/teal palette (already built) |
| Threshold colour | Red dashed reference line — sparingly, semantic only |
| Highlight (Polska in comparisons) | Azure_1 vs slate_3 (already built) |
| Trend window | Last decade by default; full history available |
| Story headlines per page | Descriptive Polish, never opinion |
| Source attribution | Visible per chart, format: `Źródło: <source>, <year>.` |
| Per-page anchor in sidebar | One per citizen question |

### Things to still decide in brainstorm/design phases

- Exact PLN vs %PKB layout on KPI cards
- Editorial headline wording (per page)
- Whether `per capita` is shown as headline or sidebar
- COFOG presentation: sorted bar at latest year vs over-time small multiples vs both
- Page 2 (COFOG) — single chart or KPI cards for top 5 + bar for full breakdown
- Header / global navigation
- Footer / source attribution
- Glossary handling
- EDP banner / badge prominence
