# Design Spec — Public Finance dashboard for Polish citizens

**Phase 4 output. Direction:** Hybrid F + question-headers from E.
**Page 1:** dense scoreboard summary.
**Pages 2-5:** question-as-header chapters (citizen voice, descriptive subtitle, focused content).

Build phase implements this spec exactly. Self-critique compares output to this spec.

---

## Global elements

### Dashboard metadata

```yaml
domain:   public_finance
port:     8057
title:    "Finanse publiczne Polski"
subtitle: "Stan budżetu państwa — dla obywateli"   # ⚠️ NEW FIELD — see eng req 1
```

### Sidebar navigation (5 anchors)

| # | Anchor | Sidebar label |
|---|---|---|
| 1 | `przeglad` | Przegląd |
| 2 | `wydatki` | Na co idą wydatki? |
| 3 | `dlug` | Dług publiczny |
| 4 | `ue` | Polska w UE |
| 5 | `prognozy` | Co czeka nas dalej? |

### Footer

```
Źródła: Eurostat (ESA 2010) · MFW WEO · Polskie Ministerstwo Finansów (DBW)
Ostatnia aktualizacja danych: <YYYY-MM-DD>
Otwarte Raporty 2026 · open-reporting.dev
```

### Visual language (inherited from theme, no overrides)

- Background: BG_PAGE (#F7F8FA) page, BG_SURFACE (#FFFFFF) cards
- Series colours: COLORWAY (azure/slate/teal — already enforced)
- Threshold lines: NEGATIVE (#C0503A), dashed, with annotation
- Polish labels everywhere; no English leak
- Number format: space thousand separator, comma decimal, NBSP + unit

---

## Engineering requests (framework extensions needed)

To deliver this design at full quality, dbr needs three framework extensions. The build phase can either:
(a) wait for these to land (escalate to Opus session) before building, or
(b) ship a v1 with workarounds noted.

**My recommendation for these:** ship v1 with workarounds; log requests for v2.

| # | Request | What | v1 workaround |
|---|---|---|---|
| **E1** | `card.subtitle` field on card visual | Render a secondary smaller line below the primary value — e.g. "−6,5 % PKB" primary, "= −236 mld zł" subtitle | Use a single value per card (PLN for revenue/expenditure where DBW provides, % PKB for ratios where Eurostat is the source). Accept that citizens see only one number per card. |
| **E2** | `page.subtitle` field on page.yml | Render descriptive Polish answer below the page title | Bake the answer into the page title itself — longer titles OK. |
| **E3** | `text` / `markdown` visual type | Inline prose between charts for editorial framing, source notes, glossary tooltips | Use chart titles + footer attribution; editorial framing limited to page titles. |

Engineering requests live as TODOs at end of this spec — explicit for the Opus session that picks them up.

---

## Page 1 — Polska 2024 w skrócie (scoreboard)

**Anchor:** `przeglad`
**Title:** `Polska 2024 w skrócie`
**Pattern citations:** P1 (PLN+%PKB pairing), P2 (linear page), P5 (thresholds visible), P7 (EU comparison highlighted), USAFacts annual digest framing.

### Row layout

```
┌────────────────────────────────────────────────────────────────┐
│ Row 1 — KPI strip (4 cards, 25% each)                          │
│   ┌─────────┬─────────┬─────────┬─────────┐                   │
│   │ Saldo   │ Dług    │ UE rank │ Odsetki │                   │
│   └─────────┴─────────┴─────────┴─────────┘                   │
├────────────────────────────────────────────────────────────────┤
│ Row 2 — Trends (2 charts, 50% each)                            │
│   ┌─────────────────────┬─────────────────────┐               │
│   │ Saldo 2015–2024     │ Dług 2015–2024      │               │
│   │ + −3% SGP threshold │ + 60% Maastricht    │               │
│   └─────────────────────┴─────────────────────┘               │
├────────────────────────────────────────────────────────────────┤
│ Row 3 — EU comparison (1 chart, 100%)                          │
│   ┌──────────────────────────────────────────────┐            │
│   │ Polska na tle UE-27: saldo fiskalne 2024     │            │
│   │ Sorted horizontal bar, Polska highlighted    │            │
│   └──────────────────────────────────────────────┘            │
└────────────────────────────────────────────────────────────────┘
```

### Visual specs

#### V1.1 — Card: Saldo finansów publicznych

```yaml
type: card
encoding:
  value: { metric: fiscal_balance }
filter:
  geo: PL
options:
  threshold:
    rule: sgp_deficit
```

- Metric: `fiscal_balance` (existing — % PKB, with `sgp_deficit` threshold at -3)
- Display: `-6,5 % PKB` with badge `✗ Próg SGP` (red — fail threshold)
- **Workaround note (E1):** Polish citizens see only % PKB; PLN amount appears in chart axes.
- Source label (already in metric meta): `Eurostat ESA 2010, sektor rządowy`

#### V1.2 — Card: Dług publiczny

```yaml
type: card
encoding:
  value: { metric: public_debt }
filter:
  geo: PL
options:
  threshold:
    rule: maastricht_debt
```

- Metric: `public_debt` (existing — % PKB, with `maastricht_debt` threshold at 60)
- Display: `55,1 % PKB` with badge `✓ Maastricht` (green — passes threshold)
- Source: `Kryterium z Maastricht: 60% PKB`

#### V1.3 — Card: Pozycja w UE-27

**Workaround required**: dbr has no "computed metric" for "rank of Poland". Options:
- (a) Pre-compute rank in fact_finance_overview and expose as a new metric `eu_rank_deficit` — adds dbt work
- (b) Use a static card with hardcoded "2/27" text — requires E1 framework support for text-only cards
- (c) Skip this KPI on page 1; rely on the EU bar chart below to communicate position

**v1 decision:** Skip the rank card; the EU comparison chart immediately below does the work. Replace this slot with **Wydatki państwa** card instead:

```yaml
type: card
encoding:
  value: { metric: total_expenditure }
filter:
  geo: PL
```

- Metric: `total_expenditure` (existing — % PKB)
- Display: `49,4 % PKB`
- Note: For DBW absolute PLN we have `govt_revenue` (mld zł) but `total_expenditure` is in % PKB. Pairing not possible without metric definition extension. Acceptable for v1.

#### V1.4 — Card: Koszty obsługi długu

```yaml
type: card
encoding:
  value: { metric: interest_expenditure }
filter:
  geo: PL
```

- Metric: `interest_expenditure` (existing — % PKB)
- Display: `2,2 % PKB`
- **Editorial framing (NOT shown on card — flagged for E2 page subtitle support):** "Prawie tyle co obrona narodowa (2,1% PKB)"

#### V1.5 — Line: Saldo fiskalne 2015–2024

```yaml
type: line
encoding:
  x: { dimension: date_key__cal_year }
  y: { metric: fiscal_balance }
filter:
  geo: PL
  date_key__cal_year: [2015,2016,2017,2018,2019,2020,2021,2022,2023,2024]   # last decade default
options:
  reference_lines:
    - { value: -3, label: "Próg SGP", color: negative }
    - { value:  0, label: "Równowaga", color: subtext }
```

- Pattern P10: last decade default; full history available via interaction
- ⚠️ **Filter limitation:** dbr currently filters on dimension values; can dbr filter `date_key__cal_year` by list? — confirm in build phase. If not, drop filter and accept full history.

#### V1.6 — Line: Dług publiczny 2015–2024

```yaml
type: line
encoding:
  x: { dimension: date_key__cal_year }
  y: { metric: public_debt }
filter:
  geo: PL
options:
  reference_lines:
    - { value: 60, label: "Próg Maastricht (60% PKB)", color: negative }
```

#### V1.7 — Bar: Polska na tle UE-27 (saldo 2024)

```yaml
type: bar
encoding:
  x: { metric: fiscal_balance }
  y: { dimension: geo__country_name_pl }
filter:
  geo: [AT, BE, BG, CY, CZ, DE, DK, EE, EL, ES, FI, FR, HR, HU, IE, IT, LT, LU, LV, MT, NL, PL, PT, RO, SE, SI, SK]
  date_key__cal_year: 2024
options:
  sort: value-asc
  highlight:
    value: Polska
    color: azure_1
    other: slate_3
  reference_lines:
    - { value: -3, label: "Próg SGP", color: negative }
```

- This is the existing Phase A EU bar visual — reuse as-is

---

## Page 2 — Na co idą wydatki państwa?

**Anchor:** `wydatki`
**Title:** `Na co idą wydatki państwa?`
**Subtitle (flagged E2):** `Największa pozycja: ochrona socjalna (16,9 % PKB). Razem z gospodarką, zdrowiem i edukacją — 35 % PKB.`
**Pattern citations:** P3 (categories by function), P10 (recent trend), R6 (no quarterly), Where Does It Go? emoji-ledger inspiration.

### Row layout

```
┌────────────────────────────────────────────────────────────────┐
│ Row 1 — COFOG ranked horizontal bar 2024 (100%)                │
│   Sorted descending. 10 categories with Polish labels.         │
├────────────────────────────────────────────────────────────────┤
│ Row 2 — Top categories trend 2015–2024 (100%)                  │
│   Multi-line: top 4 categories only (Ochrona, Gospodarka,      │
│   Zdrowie, Edukacja). Smaller categories elided.               │
└────────────────────────────────────────────────────────────────┘
```

### Visual specs

#### V2.1 — Bar: COFOG breakdown 2024

```yaml
type: bar
encoding:
  x: { metric: cofog_expenditure }
  y: { dimension: cofog_function__cofog_label_pl }
filter:
  geo: PL
  date_key__cal_year: 2024
options:
  sort: value-desc
```

- Reuses existing `cofog_expenditure` metric and `dim_cofog`
- Sort descending so largest category sits at top — strongest pre-attentive signal

#### V2.2 — Line: Top 4 COFOG categories 2015–2024

```yaml
type: line
encoding:
  x: { dimension: date_key__cal_year }
  y: { metric: cofog_expenditure }
  color: { dimension: cofog_function__cofog_label_pl }
filter:
  geo: PL
  cofog_function__cofog_label_pl: [Ochrona socjalna, Gospodarka, Zdrowie, Edukacja]
```

- ⚠️ Confirm in build: can we filter by `cofog_function__cofog_label_pl` value list? If not, use `cofog_function` numeric list (1, 4, 7, 9).
- 4 series stays within Cowan 4±1 working memory; smaller categories skipped because they'd compress the visual.

---

## Page 3 — Jak duży mamy dług publiczny?

**Anchor:** `dlug`
**Title:** `Jak duży mamy dług publiczny?`
**Subtitle (flagged E2):** `Polska 2024: 55,1 % PKB. To poniżej unijnego progu 60 %, ale rośnie szybko. Koszty obsługi długu (2,2 % PKB) zbliżyły się do wydatków na obronę.`
**Pattern citations:** P5 (Maastricht threshold), P6 (history + projection visual language).

### Row layout

```
┌────────────────────────────────────────────────────────────────┐
│ Row 1 — Dług publiczny trend 2015–2024 (100%)                  │
│   Line + 60% Maastricht reference                              │
├────────────────────────────────────────────────────────────────┤
│ Row 2 — Koszty obsługi długu trend (100%)                      │
│   Line of interest_expenditure 2015–2024                       │
│   Annotation: defence comparison                               │
└────────────────────────────────────────────────────────────────┘
```

### Visual specs

#### V3.1 — Line: Dług publiczny 2015–2024

```yaml
type: line
encoding:
  x: { dimension: date_key__cal_year }
  y: { metric: public_debt }
filter:
  geo: PL
options:
  reference_lines:
    - { value: 60, label: "Próg Maastricht (60% PKB)", color: negative }
```

- Same as V1.6 but standalone full-width
- Consider adding markers on key years (COVID 2020, war 2022) — would need dbr `annotations` option (does not exist; flag as future)

#### V3.2 — Line: Koszty obsługi długu 2015–2024

```yaml
type: line
encoding:
  x: { dimension: date_key__cal_year }
  y:
    metric:
      - interest_expenditure
filter:
  geo: PL
```

- Multi-metric path would include defence (cofog_02) for comparison — but defence is in COFOG semantic model, not the revenue_expenditure one. Cross-semantic-model metric query may not work.
- ⚠️ **Build verification needed:** can dbr's line visual query metrics from different semantic models in one chart? Most likely NO. v1 workaround: single metric (interest), defence comparison in subtitle (E2) or as a static annotation.

---

## Page 4 — Polska na tle UE-27

**Anchor:** `ue`
**Title:** `Polska na tle UE-27`
**Subtitle (flagged E2):** `2. największy deficyt w UE w 2024 — gorzej tylko Rumunia. Dług publiczny rośnie w tempie szybszym niż średnia unijna.`
**Pattern citations:** P7 (sorted ranked bar), OECD comparison pattern, P5 (thresholds).

### Row layout

```
┌────────────────────────────────────────────────────────────────┐
│ Row 1 — EU-27 deficit ranked 2024 (100%)                       │
│   Sorted horizontal bar, Polska highlighted, -3% threshold     │
├────────────────────────────────────────────────────────────────┤
│ Row 2 — EU-27 debt ranked 2024 (100%)                          │
│   Sorted horizontal bar, Polska highlighted, 60% threshold     │
└────────────────────────────────────────────────────────────────┘
```

### Visual specs

#### V4.1 — Bar: Deficyt UE-27 2024 (sorted, Polska highlighted)

```yaml
type: bar
encoding:
  x: { metric: fiscal_balance }
  y: { dimension: geo__country_name_pl }
filter:
  geo: [AT, BE, BG, CY, CZ, DE, DK, EE, EL, ES, FI, FR, HR, HU, IE, IT, LT, LU, LV, MT, NL, PL, PT, RO, SE, SI, SK]
  date_key__cal_year: 2024
options:
  sort: value-asc
  highlight:
    value: Polska
    color: azure_1
    other: slate_3
  reference_lines:
    - { value: -3, label: "Próg SGP", color: negative }
```

- Same as V1.7. Reused intentionally — page 4 amplifies the EU comparison; same visual at larger size reinforces.
- Note: this duplicates V1.7. Acceptable because page 1 is overview and page 4 is the dedicated EU page.

#### V4.2 — Bar: Dług publiczny UE-27 2024 (sorted)

```yaml
type: bar
encoding:
  x: { metric: public_debt }
  y: { dimension: geo__country_name_pl }
filter:
  geo: [<same EU-27 list>]
  date_key__cal_year: 2024
options:
  sort: value-desc
  highlight:
    value: Polska
    color: azure_1
    other: slate_3
  reference_lines:
    - { value: 60, label: "Próg Maastricht", color: negative }
```

- `value-desc` (largest debt first) — most-indebted countries at top
- Polish citizens see Greece, Italy, France above Poland; Poland is mid-pack on debt (unlike deficit where Poland is near worst)

---

## Page 5 — Co czeka nas dalej?

**Anchor:** `prognozy`
**Title:** `Co czeka nas dalej?`
**Subtitle (flagged E2):** `Prognozy MFW: stopniowa poprawa deficytu do ok. 4 % PKB w 2029. Dług publiczny dalej rośnie — może przekroczyć próg 60 % PKB w najbliższych latach.`
**Pattern citations:** P6 (history solid + projection dashed), IMF Datamapper-style projection viz.

### Row layout

```
┌────────────────────────────────────────────────────────────────┐
│ Row 1 — Saldo fiskalne: historia + prognoza MFW (100%)         │
│   Line, dash_when imf__is_projection                           │
├────────────────────────────────────────────────────────────────┤
│ Row 2 — Dług publiczny: historia + prognoza MFW (100%)         │
│   Line, dash_when imf__is_projection                           │
└────────────────────────────────────────────────────────────────┘
```

### Visual specs

#### V5.1 — Line: Saldo fiskalne historia + prognoza

```yaml
type: line
encoding:
  x: { dimension: date_key__cal_year }
  y: { metric: fiscal_balance_weo }
filter:
  geo: PL
options:
  dash_when:
    dimension: imf__is_projection
    value: true
  reference_lines:
    - { value: -3, label: "Próg SGP", color: negative }
    - { value:  0, label: "Równowaga", color: subtext }
```

- Reuses Phase B `fiscal_balance_weo` metric and `dash_when` mechanism
- Single metric for clarity (drop `primary_balance_weo` from page 5 of phase B — citizens don't distinguish; keep it simple)

#### V5.2 — Line: Dług publiczny historia + prognoza

```yaml
type: line
encoding:
  x: { dimension: date_key__cal_year }
  y: { metric: gross_debt_weo }
filter:
  geo: PL
options:
  dash_when:
    dimension: imf__is_projection
    value: true
  reference_lines:
    - { value: 60, label: "Próg Maastricht", color: negative }
```

- Single metric (drop `net_debt_weo` from phase B — citizens don't need the gross/net distinction; brief explicitly excluded)

---

## Summary — visual count

| Page | Visuals | dbr type breakdown |
|---|---|---|
| 1 — Przegląd | 7 (4 cards + 3 charts) | card×4, line×2, bar×1 |
| 2 — Wydatki | 2 (1 bar + 1 multi-line) | bar×1, line×1 |
| 3 — Dług | 2 (lines) | line×2 |
| 4 — UE | 2 (bars) | bar×2 |
| 5 — Prognozy | 2 (lines with dash_when) | line×2 |
| **Total** | **15** | card×4, line×7, bar×4 |

Page 1 carries 7 visuals (the scoreboard density of option F); pages 2-5 have 2 each (focused chapters from option C).

---

## Metric inventory check

Metrics referenced by this design, and whether they exist:

| Metric | Status | Notes |
|---|---|---|
| `fiscal_balance` | ✅ exists | finance_overview.yml |
| `public_debt` | ✅ exists | finance_overview.yml |
| `govt_revenue` | ✅ exists | finance_overview.yml |
| `total_expenditure` | ✅ exists | finance_revenue_expenditure.yml |
| `interest_expenditure` | ✅ exists | finance_revenue_expenditure.yml |
| `cofog_expenditure` | ✅ exists | finance_cofog.yml |
| `fiscal_balance_weo` | ✅ exists | finance_imf.yml |
| `gross_debt_weo` | ✅ exists | finance_imf.yml |

All metrics needed are already in the semantic layer. **No new metrics required.** This is intentional — design honoured the existing data model.

---

## Filters needed

EU-27 country code list (used twice — V1.7, V4.1, V4.2):
```
[AT, BE, BG, CY, CZ, DE, DK, EE, EL, ES, FI, FR, HR, HU, IE, IT, LT, LU, LV, MT, NL, PL, PT, RO, SE, SI, SK]
```

Year filter for last-decade view (used in some V1.5, V1.6, V2.2, V3.1, V3.2 if `date_key__cal_year` list filter works):
```
[2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]
```

⚠️ Build phase must verify whether `filter: date_key__cal_year: [list]` works as expected with semantic-layer dimension filters. If not, drop the year filter and accept full-history default (1995-2024 for Eurostat metrics, 1995-2029 for IMF).

---

## Polish copy reference

Every user-facing string in one place — for Polish quality review before build.

### Page titles
- Przegląd / Polska 2024 w skrócie
- Na co idą wydatki państwa?
- Jak duży mamy dług publiczny?
- Polska na tle UE-27
- Co czeka nas dalej?

### Page subtitles (E2 — to add when supported)
- *Page 1:* `Stan budżetu państwa w 2024 r. — najważniejsze liczby`
- *Page 2:* `Największa pozycja: ochrona socjalna (16,9 % PKB). Razem z gospodarką, zdrowiem i edukacją — 35 % PKB.`
- *Page 3:* `Polska 2024: 55,1 % PKB. To poniżej unijnego progu 60 %, ale rośnie szybko. Koszty obsługi długu (2,2 % PKB) zbliżyły się do wydatków na obronę.`
- *Page 4:* `2. największy deficyt w UE w 2024 — gorzej tylko Rumunia. Dług publiczny rośnie w tempie szybszym niż średnia unijna.`
- *Page 5:* `Prognozy MFW: stopniowa poprawa deficytu do ok. 4 % PKB w 2029. Dług publiczny dalej rośnie — może przekroczyć próg 60 % PKB w najbliższych latach.`

### KPI card labels (read from metric.label in semantic models)
- Saldo finansów publicznych
- Dług publiczny
- Wydatki ogółem
- Koszty obsługi długu

### Reference line labels (per design)
- Próg SGP (-3% PKB)
- Próg Maastricht (60% PKB)
- Równowaga

### Threshold rule meta (existing in metric YAMLs)
- `sgp_deficit`: -3.0
- `maastricht_debt`: 60.0

---

## What's deliberately OUT (per brief and brainstorm)

Already excluded — flagged here to prevent scope creep in build:

- Quarterly granularity (R6)
- Net debt distinction (brief explicit)
- Structural balance (brief explicit)
- By-source comparison page (brief explicit)
- NUTS2 regional breakdown (brief explicit)
- "What if" scenario controls (R1)
- Per-taxpayer calculator (R2)
- Treemap visuals (P11 — deferred, requires new dbr visual)
- Year selector / dropdown (brief: "no interactive filters needed for v1")
- Mobile-first responsive nav (brief: "desktop-first acceptable")

---

## Self-critique items to track (Phase 6 checklist)

When the build is complete and screenshotted, the critique loop must check:

1. ✅ Every chart shows source (chart-level attribution visible)
2. ✅ Polish diacritics correct everywhere (ą ć ę ł ń ó ś ź ż)
3. ✅ Number format: space thousand separator, comma decimal
4. ✅ Threshold lines render with Polish labels on saldo (−3%) and dług (60%) charts
5. ✅ Polska highlighted in azure_1, others in slate_3 on EU bars
6. ✅ Top COFOG category (Ochrona socjalna) is clearly the largest visual bar
7. ✅ Saldo card shows red `✗ Próg SGP` badge (threshold fail)
8. ✅ Dług card shows green `✓ Maastricht` badge (threshold pass — currently)
9. ✅ Pages render in declared order; sidebar matches
10. ✅ History solid + projection dashed visible on page 5 charts
11. ✅ Footer present with sources and update date
12. ✅ No "No data" placeholder anywhere
13. ✅ Width capped at 1440px on wide monitors

---

## Engineering requests log

Three framework extensions surfaced by this design. v1 build proceeds with workarounds; flag for Opus session to address:

### E1 — `card.subtitle` field
Card visual needs an optional `subtitle` field rendering a secondary value/text below the primary value. Use case: pair `% PKB` with `mld zł` on every KPI card. Currently every card shows only one number; citizens see either the ratio or the absolute, not both.

Schema:
```yaml
type: card
encoding:
  value:    { metric: fiscal_balance }
  subtitle: { metric: fiscal_balance_pln_mn }   # NEW — secondary value
```

### E2 — `page.subtitle` field
page.yml needs a `subtitle` field for the descriptive Polish answer below the page title. Citizen audience benefits from "answer-first" pattern (Where Does It Go?, USAFacts). Currently only title is supported.

Schema:
```yaml
title:    "Na co idą wydatki państwa?"
subtitle: "Największa pozycja: ochrona socjalna (16,9 % PKB)."
```

### E3 — `text` / `markdown` visual type
A text-block visual that renders inline prose between charts. Use case: editorial framing, source notes, glossary tooltips. Currently dbr renders only data visuals — no way to put editorial copy in the canvas.

Schema:
```yaml
type: text
content: |
  Polska ma drugi największy deficyt w UE...
  [arbitrary Polish markdown]
```

---

## v1 build plan with workarounds (Phase 5)

Given E1-E3 are not yet built, v1 will:

- Show one number per KPI card (% PKB for ratios, mld zł for absolute revenue/expenditure where available)
- Embed descriptive subtitle text into page titles where critical (long titles OK), or accept they're missing for v1
- Skip inline editorial framing; rely on page titles + chart titles for context

After v1 is shipped at this reduced quality, Opus session can implement E1-E3 and a v1.1 polish pass adds the missing editorial layer.

---

**Build phase reads this spec and executes. No design decisions during build. If something is unclear, build pauses and asks.**
