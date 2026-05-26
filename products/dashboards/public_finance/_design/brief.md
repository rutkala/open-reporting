# Brief — Public Finance dashboard for Polish citizens

**Audience:** Polish citizens who follow news but are not economists.
**Source data:** Eurostat ESA 2010 (annual, through 2024), IMF WEO (projections through 2029), Polish Ministry of Finance DBW (PLN totals).
**Position in product:** flagship public-facing dashboard on `portal.open-reporting.dev/public_finance/`.

---

## Who the audience actually is

Not analysts. Not economists. Not journalists writing on the topic.

A typical visitor:
- Reads news — has heard "deficit", "dług publiczny", "kryteria z Maastricht", "EDP" — but doesn't know exactly what they mean
- Pays taxes — wants to know where the money goes
- Has opinions about pensions, healthcare, defence — wants to see if their intuitions match the data
- Trusts data but not blindly — wants the source visible
- Will spend 1–3 minutes here, not 20
- Will not click through to a methodology PDF
- Reads Polish

**What they want from this dashboard:**
1. A clear sense of "is the state in good or bad shape financially?"
2. Concrete numbers they can relate to (PLN, not just % PKB)
3. Comparison to neighbours (are we in line, or an outlier?)
4. Some sense of where things are heading (better or worse?)
5. To leave the page with something they can remember and repeat

---

## Five questions the dashboard must answer at a glance

For a citizen visitor, every page maps to one of these. If a chart doesn't answer one of these, it doesn't belong.

| # | Question (citizen voice) | Headline answer (2024 data) |
|---|---|---|
| 1 | **Czy państwo wydaje więcej niż zbiera?** | Tak. W 2024 wydatki przekroczyły dochody o ~236 mld zł (6,5% PKB). |
| 2 | **Na co idą moje podatki?** | Największa pozycja: ochrona socjalna (17% PKB — emerytury, renty, zasiłki). Potem gospodarka, zdrowie, edukacja. |
| 3 | **Jak duży mamy dług publiczny?** | ~2 013 mld zł, czyli 55% PKB — jeszcze poniżej unijnego progu 60%, ale rośnie. |
| 4 | **Jak wypadamy na tle innych krajów UE?** | 2. najwyższy deficyt w UE w 2024 (po Rumunii). Większy niż Francja, Słowacja, Węgry. |
| 5 | **Czy idzie ku lepszemu, czy gorszemu?** | Według prognoz MFW deficyt powoli się zmniejszy (do ~4% PKB w 2029), ale dług dalej rośnie. |

---

## The story the dashboard tells

The headline that emerges from the data, in plain Polish:

> **Polska wydaje znacząco więcej niż zbiera — i jest pod tym względem drugim najbardziej zadłużonym co roku krajem UE. Dług publiczny rośnie szybko, ale wciąż mieści się w unijnym progu. MFW oczekuje stopniowej, ale wolnej poprawy.**

Three sub-stories:

1. **Strukturalna nierównowaga** — deficyt 5–7% PKB to nie wypadek (jak COVID 2020), to stała sytuacja od 2022 r.
2. **Stopniowy wzrost obciążenia odsetkami** — koszty obsługi długu (2,2% PKB w 2024) zbliżyły się już do wydatków na obronę (2,1%). Każdy procent długu kosztuje coraz więcej.
3. **Co czeka nas dalej** — prognozy MFW pokazują stopniowe domykanie deficytu, ale dług publiczny w 2029 r. może przekroczyć próg 60% Maastricht.

The dashboard's job: surface this story with data, without telling the visitor what to think.

---

## KPIs (citizen-friendly framing)

Standard public-finance KPIs translated for citizen audience. Each gets a Polish label, a unit, a benchmark.

| Standard name | Citizen-friendly label | Unit shown | Benchmark visible |
|---|---|---|---|
| Fiscal balance | **Saldo finansów państwa** ("ile państwo zarobiło/straciło") | % PKB + mld zł | -3% PKB (próg SGP) |
| Public debt (gross) | **Dług publiczny** | % PKB + mld zł + zł per capita | 60% PKB (Maastricht) |
| Revenue (govt) | **Dochody państwa** ("ile państwo zbiera") | mld zł + % PKB | EU-27 średnia (~46%) |
| Expenditure (govt) | **Wydatki państwa** ("ile państwo wydaje") | mld zł + % PKB | EU-27 średnia (~50%) |
| Interest expenditure | **Koszty obsługi długu** ("ile płacimy za odsetki") | % PKB + mld zł | compared to defence (2.1%) |
| COFOG breakdown | **Na co idą wydatki** | % PKB per function | none — share matters |
| EU comparison | **Ranking UE-27** | sorted % PKB | -3% line, EU avg |
| IMF projection | **Prognozy MFW** | % PKB to 2029 | -3% + 60% thresholds |

**Critical citizen-framing rule:** every absolute number in % PKB must be paired with a PLN amount visible somewhere on the page. % PKB is meaningless to non-economists; mld zł is. PKB itself can be a separate "co to PKB?" sidebar.

---

## Benchmarks and thresholds (must be visible)

Citizens have heard these terms in news — the dashboard's job is to show *where Poland stands relative to them*:

| Threshold | Value | What it means | Visual treatment |
|---|---|---|---|
| **Próg SGP (deficit)** | −3% PKB | Pakt Stabilności i Wzrostu — przekroczenie uruchamia procedurę EDP | Red dashed reference line on every deficit chart |
| **Próg Maastricht (debt)** | 60% PKB | Limit z traktatu z Maastricht | Red dashed reference line on every debt chart |
| **EU-27 średnia** | varies | Median/mean of EU member states for the metric | Optional secondary line in comparisons |
| **EDP status** | currently in EDP | Excessive Deficit Procedure — Poland is under it as of 2024 | Badge / banner near deficit KPI |

---

## Structural breaks the dashboard must acknowledge

Plain notes citizens can understand — don't hide methodology issues:

- **2020 COVID shock** — deficit jumped to ~7% from <2% the year before; one-off, but partly converted to permanent spending
- **2022 war in Ukraine** — refugee costs + sharp defence increase (defence went from ~1.4% PKB pre-war to >2% from 2023)
- **2024 EDP launched** — EU formally opened Excessive Deficit Procedure against Poland; this is the "alert" status, not a fine
- **Pre-2004 data** — not directly comparable (EU accession changed methodology)

These belong in tooltips or a "kontekst" sidebar — never in a chart annotation that competes with the data.

---

## Tone, register, language

- **Formal Polish but plain.** "Pan/Pani" register if addressing the reader, but mostly third-person impersonal.
- **No jargon without translation.** "Saldo fiskalne" → at first use, "saldo finansów publicznych (różnica między dochodami a wydatkami)". After first use, just "saldo".
- **Numbers in Polish format.** Space thousand separator (`1 569`), comma decimal (`6,5%`), NBSP between number and unit.
- **Polish diacritics, always.** ą, ć, ę, ł, ń, ó, ś, ź, ż. Never "Srednia" — always "Średnia". Never "Polnoc" — always "Północ".
- **Avoid acronyms without expansion at first use.** EDP, SGP, ESA, COFOG, MFW, NBP — every one expanded the first time it appears.
- **No machine-translation feel.** Sentence structure should read naturally to a Polish reader.
- **No condescension.** "Citizen" doesn't mean "dumb". Don't explain what GDP is — they know. Do explain what "structural balance" is — most don't.

---

## What this dashboard is NOT

Things citizens don't need and the dashboard shouldn't try to deliver:

- **Quarterly granularity.** Citizens think in years.
- **Net vs gross debt distinction.** Show gross. The distinction matters for analysts, not citizens.
- **Structural vs headline balance.** Show headline. Mention structural in a tooltip if at all.
- **By-source comparison (Eurostat vs IMF vs DBW).** Pick one authoritative source per chart, attribute it, move on. The PHASE B "Porównanie źródeł" tab was an analyst feature, drop it.
- **NUTS2 regional breakdown.** Not yet — interesting but not a citizen's first question.
- **Methodology deep-dives.** Link out to Eurostat for the curious; don't reproduce.

---

## Trust signals required on every page

- **Source citation on every chart.** Not in a tiny footer — visible. Format: `Źródło: Eurostat (ESA 2010), 2024.`
- **Last-updated date in dashboard header.** When the warehouse last refreshed this data.
- **Project attribution in footer.** "Otwarte Raporty · Polska · 2026 · [link do metodyki]"
- **EDP status visible.** Currently under EDP — show it. Not as alarm, as fact.

---

## Assumptions (to confirm at Gate 1)

1. Primary visitor: Polish citizen, news-reader, non-economist.
2. Visit length: 1–3 minutes (not deep exploration).
3. Page count: 4–5 pages, each answering ONE of the five citizen questions.
4. Update cadence: annual (data refreshes once a year when Eurostat publishes).
5. Mobile important but not primary — desktop-first acceptable.
6. No interactive filters needed (year selector etc.) for v1 — static-ish per-page reading.

---

## Open design questions (to resolve in Phase 3-4)

These will be decided after reference research and brainstorm:

- **Page order** — overview-first vs story-arc-first vs hero-chart-first?
- **PLN vs % PKB primacy** — which number is bigger on KPI cards?
- **EDP / Maastricht badge** — how prominent? Banner? Subtle?
- **Historical depth** — show full 1995–2024, or focus on last decade?
- **COFOG presentation** — stacked column over time, or horizontal bar at latest year, or both?
- **EU comparison framing** — ranked all 27, or focus on neighbours (V4) + EU average?
- **Glossary handling** — sidebar, tooltips, or dedicated page?
- **Story narration** — pure data, or each page with a 1-sentence interpretive headline?
