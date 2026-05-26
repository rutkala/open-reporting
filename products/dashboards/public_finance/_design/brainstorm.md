# Brainstorm — 5 candidate dashboard structures

**Phase 3 of the design workflow. HARD-GATE: no convergence. User picks direction at Gate 3.**

All five options share the same 5 citizen-voice questions from the brief. They differ in **how the questions are sequenced, framed, and visualised at the page level**. Common elements (Nordic palette, Polish labels, threshold lines, source attribution) are not redrawn each time — those are the design system, not the structural choice.

---

## Common elements across all options

```
┌─────────────────────────────────────────────────────────────────┐
│ HEADER: Otwarte Raporty — Finanse publiczne          [Polska 🇵🇱] │
├──────────┬──────────────────────────────────────────────────────┤
│ Sidebar  │  Main content (5 pages, varies by option)            │
│ (5 nav   │                                                       │
│  links)  │                                                       │
├──────────┴──────────────────────────────────────────────────────┤
│ FOOTER: Źródła: Eurostat ESA 2010 · MFW WEO · MF DBW            │
│         Ostatnia aktualizacja: <date> · Otwarte Raporty 2026     │
└─────────────────────────────────────────────────────────────────┘
```

Sidebar always present, main canvas capped at 1440px (already enforced). Each option varies what fills the main canvas per page.

---

## Option A — "Scoreboard" (literal, scannable)

**Philosophy:** every page is a quick-scan dashboard. KPI strip on top, supporting chart(s) below. Citizen visits, scans, leaves with the headline numbers.

**Page sequence:** Same as brief — 5 questions in stated order.

### Layout: Page 1 — Ile państwo zbiera i wydaje?

```
┌──── Strona 1: Ile państwo zbiera i wydaje? ────────────────────┐
│                                                                  │
│ ┌─────────────┬─────────────┬─────────────┬─────────────┐      │
│ │ DOCHODY      │ WYDATKI     │ SALDO       │ % PKB       │      │
│ │ 1 570 mld zł │ 1 806 mld zł│ -236 mld zł │ -6,5% PKB   │      │
│ │ 43% PKB      │ 49,4% PKB   │             │ ✗ Próg SGP  │      │
│ └─────────────┴─────────────┴─────────────┴─────────────┘      │
│                                                                  │
│ ┌────────────────────────────────────────────────────────┐     │
│ │  Dochody i wydatki państwa 2015-2024 (mld zł)         │     │
│ │  [grouped column: revenue blue, expenditure slate]    │     │
│ └────────────────────────────────────────────────────────┘     │
│                                                                  │
│ ┌────────────────────────────────────────────────────────┐     │
│ │  Saldo finansów publicznych 2015-2024 (% PKB)         │     │
│ │  [column chart with −3% SGP threshold line]           │     │
│ └────────────────────────────────────────────────────────┘     │
│                                                                  │
│ Źródło: Eurostat ESA 2010 · Polskie Ministerstwo Finansów      │
└──────────────────────────────────────────────────────────────────┘
```

**Visual language:** KPI strip = 4 cards. Then 1-2 supporting charts. Same pattern every page.

**Pros:**
- Quick scanning — citizens get headline numbers fast
- Consistent rhythm across pages — learn once, navigate everywhere
- Matches USAFacts / Where Does It Go? approach
- Easiest to build; lowest risk

**Cons:**
- No narrative tension — feels like a database front-end
- Doesn't lean into the *story* the data tells
- Risk: citizens see numbers but don't synthesise them into understanding

---

## Option B — "Story arc" (narrative reordered)

**Philosophy:** pages flow as a story, not as a question list. Each page builds on the previous one's tension. Citizen reads top to bottom and ends with a coherent picture.

**Page sequence:** reordered for narrative flow:

```
Page 1 — Gdzie jesteśmy?               (snapshot: KPI summary + EU rank)
Page 2 — Jak doszło do tej sytuacji?   (trend story: deficit + debt growth 2015-2024)
Page 3 — Na co idą wydatki?            (composition — explains structural deficit)
Page 4 — Ile kosztuje nas dług?        (debt + interest cost)
Page 5 — Co czeka nas dalej?           (projections + threshold crossing)
```

### Layout: Page 1 — Gdzie jesteśmy? (snapshot + EU rank)

```
┌──── Strona 1: Gdzie jesteśmy? ────────────────────────────────┐
│                                                                  │
│ ┌─────────────────────────────────────────────────────────┐    │
│ │  Polska 2024 — finanse publiczne w skrócie              │    │
│ │                                                          │    │
│ │  Wydatki przekroczyły dochody o 236 mld zł (6,5% PKB).  │    │
│ │  To drugi największy deficyt w UE-27 — gorzej tylko     │    │
│ │  Rumunia (-9,3%).                                        │    │
│ └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│ ┌─────────────┬─────────────┬─────────────┬─────────────┐      │
│ │ DOCHODY      │ WYDATKI     │ SALDO       │ DŁUG PUBL.  │      │
│ │ 1 570 mld zł │ 1 806 mld zł│ −236 mld zł │ 2 013 mld zł │      │
│ │              │             │ −6,5% PKB   │ 55,1% PKB   │      │
│ └─────────────┴─────────────┴─────────────┴─────────────┘      │
│                                                                  │
│ ┌────────────────────────────────────────────────────────┐     │
│ │  Polska na tle UE-27: deficyt 2024                    │     │
│ │  [sorted horizontal bar, Polska highlighted, -3% ref] │     │
│ └────────────────────────────────────────────────────────┘     │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

**Visual language:** Each page opens with an editorial paragraph (descriptive, not opinion). Then KPI strip. Then 1-2 charts that elaborate. EU comparison appears on page 1 (set the stage) AND optionally on later pages.

**Pros:**
- Strongest narrative — citizens come away with a coherent picture
- Editorial paragraphs do the "interpretation" work (what UK Where Does It Go? skipped)
- Mirrors how data journalism actually works (FT, BBC, USAFacts annual digests)

**Cons:**
- Editorial copy is editorial responsibility — needs Polish review
- Less random-access — citizens dropping into page 3 lose context
- More to write/maintain — every page needs a story update annually

---

## Option C — "Hero per page" (radical focus)

**Philosophy:** each page has ONE chart that is the answer. No KPI strips, no supporting charts. Maximum focus per question.

**Page sequence:** same as brief, but each page is dramatically simpler.

### Layout: Page 3 — Jak duży mamy dług publiczny?

```
┌──── Strona 3: Jak duży mamy dług publiczny? ───────────────────┐
│                                                                  │
│  Polska ma dług publiczny ~2 013 mld zł (55,1% PKB) —           │
│  poniżej unijnego progu 60%, ale rośnie szybko.                 │
│                                                                  │
│ ┌────────────────────────────────────────────────────────┐     │
│ │                                                          │     │
│ │      Dług publiczny Polski 2015-2024 (% PKB)            │     │
│ │      [LARGE single line chart with 60% Maastricht line] │     │
│ │      [Annotation: "Maastricht 60% PKB" on right]        │     │
│ │      [Annotation: "55,1% PKB w 2024" on rightmost dot]  │     │
│ │                                                          │     │
│ └────────────────────────────────────────────────────────┘     │
│                                                                  │
│  Per capita: ~53 000 zł długu publicznego na obywatela.         │
│  Odsetki: 2,2% PKB rocznie (~80 mld zł) — prawie tyle co        │
│  obrona narodowa.                                                │
│                                                                  │
│  Źródło: Eurostat ESA 2010                                       │
└──────────────────────────────────────────────────────────────────┘
```

**Visual language:** Each page = 1 chart + framing text above + facts/context below. Hero chart takes ~60% of viewport.

**Pros:**
- Maximum cognitive ease — one thing per page
- Forces clarity — if it can't be answered in one chart, the page is wrong
- Beautiful on mobile

**Cons:**
- Some questions genuinely need multiple charts (EU comparison + ranking)
- Feels sparse for citizens who want more depth
- Risk: looks like an infographic, not a tool

---

## Option D — "Comparison-driven" (international frame)

**Philosophy:** lead with cross-country comparison on every page. Polish citizen is curious about EU peers — give them comparison as the primary lens. Domestic detail is secondary.

**Page sequence:** reordered to lead with EU comparison:

```
Page 1 — Polska na tle UE (overall ranking)
Page 2 — Deficyt: gdzie jesteśmy w rankingu?
Page 3 — Dług publiczny: gdzie jesteśmy w rankingu?
Page 4 — Wydatki: jak wydaje Polska vs średnia UE?
Page 5 — Prognozy: czy luka się domyka?
```

### Layout: Page 2 — Deficyt: gdzie jesteśmy w rankingu?

```
┌──── Strona 2: Deficyt — gdzie jesteśmy w rankingu? ────────────┐
│                                                                  │
│  Polska ma drugi największy deficyt w UE-27. Tylko Rumunia      │
│  ma większy.                                                     │
│                                                                  │
│ ┌────────────────────────────────────────────────────────┐     │
│ │  Saldo fiskalne — wszystkie kraje UE-27 (% PKB)        │     │
│ │  [sorted horizontal bar, Polska in azure, -3% line]    │     │
│ │  [27 country bars]                                      │     │
│ └────────────────────────────────────────────────────────┘     │
│                                                                  │
│ ┌────────────────────────────────────────────────────────┐     │
│ │  Polska vs średnia UE-27: trajektoria 2015-2024        │     │
│ │  [2-line chart: PL line + EU average line + −3% ref]   │     │
│ └────────────────────────────────────────────────────────┘     │
│                                                                  │
│  Polska średnia 2020-2024: -5,7% PKB                            │
│  UE-27 średnia 2020-2024: -3,8% PKB                             │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

**Visual language:** Every page has a sorted EU-27 bar (or its analogue). Polska always highlighted. Trend chart shows Polska vs EU average.

**Pros:**
- Strongest "how do we stack up?" answer — the citizen question #4 becomes pervasive
- Polish citizens follow EU news; this matches their frame
- EU comparison data already in warehouse — easy to render

**Cons:**
- Repetitive — five pages of "Poland in EU-27 sorted bar" gets monotonous
- De-emphasises domestic story (where the money goes within Poland)
- COFOG functional breakdown awkward to compare across countries (different categorisations)

---

## Option E — "Question-as-header" (editorial / engaging)

**Philosophy:** every page literally answers a Polish citizen question. Page title IS the question. Subtitle IS the descriptive answer. Charts are the evidence. Maximum engagement, minimum stiff "data dashboard" feel.

**Page sequence:** brief's 5 questions, each phrased conversationally:

```
Page 1 — Czy państwo wydaje więcej, niż zbiera?
   Subtitle: "Tak, od 2022 r. — w 2024 luka wyniosła 236 mld zł."

Page 2 — Na co idą moje podatki?
   Subtitle: "Największa pozycja: ochrona socjalna (17% PKB)."

Page 3 — Jak duży mamy dług publiczny?
   Subtitle: "Ok. 53 000 zł na obywatela. Rośnie, ale wciąż <60% PKB."

Page 4 — Jak wypadamy w UE?
   Subtitle: "Drugi największy deficyt w UE-27 (po Rumunii)."

Page 5 — Co czeka nas dalej?
   Subtitle: "MFW prognozuje powolną poprawę deficytu do 2029."
```

### Layout: Page 2 — Na co idą moje podatki?

```
┌──── Strona 2: Na co idą moje podatki? ─────────────────────────┐
│                                                                  │
│  Największa pozycja: ochrona socjalna (17% PKB).                │
│  Razem z gospodarką, zdrowiem i edukacją — ponad 60% wydatków.  │
│                                                                  │
│ ┌────────────────────────────────────────────────────────┐     │
│ │  Wydatki państwa wg funkcji 2024 (% PKB)               │     │
│ │  [sorted horizontal bar of 10 COFOG categories]        │     │
│ │  16,9 ███████████████ Ochrona socjalna                 │     │
│ │   7,5 ████████ Gospodarka                              │     │
│ │   5,7 ██████ Zdrowie                                   │     │
│ │   5,0 █████ Edukacja                                   │     │
│ │   ...                                                   │     │
│ └────────────────────────────────────────────────────────┘     │
│                                                                  │
│ ┌────────────────────────────────────────────────────────┐     │
│ │  Top 5 kategorii — trend 2015-2024                     │     │
│ │  [5-line chart, top categories only]                   │     │
│ └────────────────────────────────────────────────────────┘     │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

**Visual language:** Page title = literal Polish question. Subtitle = descriptive answer. 1-2 charts per page. Editorial framing built into page structure.

**Pros:**
- Most engaging — feels like a conversation, not a report
- Strong audience match — citizens think in questions, not in "metrics"
- Forces each page to answer its question clearly

**Cons:**
- Risks feeling chatty / not authoritative
- Questions need careful Polish phrasing (avoid sounding patronising)
- Subtitle is editorial — needs annual update

---

## Option F — "Hybrid" (scan + read = overview page + chapters)

**Philosophy:** combine scan-friendly (option A) and story-friendly (option B). Page 1 is a scoreboard summary; pages 2-5 are deeper story chapters. Citizen can scan page 1 in 60 seconds OR scroll through 2-5 for the full story.

**Page sequence:**

```
Page 1 — Polska 2024 w skrócie (4 KPI strip + 2 hero charts)
Page 2 — Dochody i wydatki (composition + revenue/expenditure trend)
Page 3 — Dług publiczny (debt trend + interest cost)
Page 4 — Polska w UE-27 (cross-country sorted bars)
Page 5 — Prognozy do 2029 (IMF projection with thresholds)
```

### Layout: Page 1 — Polska 2024 w skrócie

```
┌──── Strona 1: Polska 2024 w skrócie ──────────────────────────┐
│                                                                  │
│ ┌─────────────┬─────────────┬─────────────┬─────────────┐     │
│ │ SALDO        │ DŁUG PUBL.   │ WYDATKI/PKB  │ POZYCJA UE   │     │
│ │ −6,5% PKB    │ 55,1% PKB    │ 49,4% PKB    │ 2/27 (deficyt)│     │
│ │ −236 mld zł  │ 2 013 mld zł │ 1 806 mld zł │ pod Rumunią   │     │
│ │ ✗ Próg SGP   │ ✓ Maastricht │              │              │     │
│ └─────────────┴─────────────┴─────────────┴─────────────┘     │
│                                                                  │
│ ┌─────────────────────────────┬─────────────────────────────┐  │
│ │ Saldo fiskalne 2015-2024    │ Dług publiczny 2015-2024   │  │
│ │ [line + -3% threshold]      │ [line + 60% threshold]      │  │
│ └─────────────────────────────┴─────────────────────────────┘  │
│                                                                  │
│ ┌────────────────────────────────────────────────────────┐     │
│ │ Polska vs UE-27 (deficyt 2024)                         │     │
│ │ [sorted horizontal bar, Polska highlighted]            │     │
│ └────────────────────────────────────────────────────────┘     │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

**Visual language:** Page 1 = dense scoreboard summarising everything. Pages 2-5 = focused chapters with 2-3 charts each, no KPI strip (numbers are on page 1).

**Pros:**
- Serves both quick-scan and deep-read citizens
- Page 1 is the "shareable" page (link directly here for news context)
- Page 2-5 progressive deepening
- Matches "annual digest" framing of USAFacts

**Cons:**
- Page 1 is dense — risks cognitive overload (4 KPI + 3 charts)
- Some duplication: KPIs on page 1 also reflected in trends on pages 2-3

---

## Decision matrix — at a glance

| Option | Best for | Risk |
|---|---|---|
| **A — Scoreboard** | Quick lookup, consistent rhythm | Boring, no story |
| **B — Story arc** | Coherent narrative, journalism feel | Editorial maintenance, no random-access |
| **C — Hero per page** | Maximum clarity, mobile-perfect | Sparse, some questions need multiple charts |
| **D — Comparison-driven** | EU-curious citizens, ranking focus | Repetitive, de-emphasises domestic story |
| **E — Question-as-header** | Engaging, conversational | Risks chatty / not authoritative |
| **F — Hybrid (overview + chapters)** | Scan + read, shareability | Page 1 density, some duplication |

---

## What I'd resist at this gate

- Picking based on aesthetic preference alone — pick based on which match your **audience and your story**
- Hybrid-of-hybrid ("a bit of B and a bit of E") — kills coherence. Pick one main approach; allow one or two borrowings.
- Picking C because it sounds clean — some questions need 2 charts, period
- Picking D because comparison data is easiest to render — that's a building-driven shortcut, not a citizen-driven choice

---

## What happens next (Phase 4)

Once you pick an option (or a clearly-stated hybrid), Phase 4 converges into a specific design spec:
- Final page sequence and titles
- Each page: row layout + visual list + metric references
- Per-visual encoding choices (chart type, color, threshold lines)
- Polish copy for editorial elements (headlines, subtitles, source attributions)
- Glossary / tooltips strategy
- Mobile considerations

Phase 5 (build) implements exactly that spec. Phase 6 (critique) screenshots and iterates.
