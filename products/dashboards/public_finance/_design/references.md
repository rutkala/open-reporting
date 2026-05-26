# References — Public Finance dashboards for citizens

**Research date:** 2026-05-22
**Audience target:** Polish citizens, non-economist, news-reader
**Researcher:** autonomous (Phase 2 of design workflow)

---

## Honest note on access

This phase tried to pull and visually evaluate ~10 candidate reference dashboards. Many were blocked at fetch time:

| Source | Outcome |
|---|---|
| **Where Does It Go? (UK 2025)** | ✅ Accessed + analysed in depth |
| **USAFacts State of Union (US)** | ⚠️ Page loaded but content sparse via WebFetch |
| **IMF DataMapper — Poland profile** | ❌ HTTP 403 |
| **OKF "Where Does My Money Go?" (UK 2009)** | ❌ ECONNREFUSED |
| **Information Is Beautiful — UK Govt Spending** | ❌ Certificate error |
| **IFS — TaxLab spending calculator** | ❌ HTTP 403 |
| **Bundeshaushalt.de (Germany)** | ❌ HTTP 503 |
| **OECD government deficit page** | ❌ HTTP 403 |
| **Eurostat news on EDP / fiscal** | ❌ HTTP 403 |
| **IIB Awards showcase** | ❌ HTTP 404 |

Pattern extraction below draws on (a) the **one** fully-analysed reference, (b) search-result descriptions for the rest, and (c) widely-documented characteristics of these well-known examples. This is a real limitation of WebFetch from a server context; a production workflow would use a headless browser (Playwright) to render and screenshot live pages multimodally.

**What this means for the workflow:** Phase 2 in its current "WebFetch only" form is partially blocked by anti-bot defences on most major data-journalism / official sites. A future iteration should use Playwright (already installed via the `screenshot` package) to render+capture+evaluate, exactly as the visual-screenshot-reviewer agent does.

---

## Reference 1 — Where Does It Go? (UK, 2025)

**URL:** https://wheredoesitgo.co.uk/
**Authority:** Independent citizen-facing project
**Audience match:** ⭐⭐⭐⭐⭐ — direct citizen audience, non-expert UK readers

### Visual structure observed

| Element | Observation |
|---|---|
| **Page layout** | Linear scroll, top-down. Headline → interactive tool → category breakdown → trend → explanatory context. No tabs. |
| **Navigation** | Fixed top: Home / Deep Dives / How It Works / Data Sources. 4 items only. |
| **Headline** | £1.37tn total spending — absolute pound figure dominant, not %GDP |
| **Category breakdown** | Eight categories as "emoji ledger": 🏥 Health, 📚 Education, 🛡️ Defence, etc. Each with absolute £ + percentage badge. |
| **Trend** | Single line graph "5-Year Spending Trend" with absolute £ and +27.7% growth marker |
| **Interactivity** | "What If?" Chancellor mode — preset budget scenarios ("Cut Defence 10%") with cascading effect on bottom line |
| **Personalisation** | Tax calculator with named personas (New Graduate, NHS Nurse) — "your daily tax contribution to each category" |
| **Source attribution** | Visible "How It Works" + "Data Sources" sections in main nav |
| **Comparison** | Year-over-year only. No cross-country benchmarking. No inflation adjustment shown. |

### What works for citizen audience

- Absolute £ as primary number (£384bn Social Protection), % as secondary (28.0%)
- Categories organised by function (health, education) not by ministry — what citizens actually think about
- Five-year trend by default — citizens want trajectory, not just snapshot
- Per-bracket "what your tax pays" — personal relevance hook
- Linear story arc: total → breakdown → trend → "what if" → context

### What's missing (for our adaptation)

- No cross-country comparison — UK chose this; Polish citizens following EU news care about peer comparison
- No deficit/debt focus — UK page is spending-only
- No inflation adjustment
- No structural breaks acknowledged

---

## Reference 2 — Information Is Beautiful: UK Government Spending Incomes & Outcomes

**URL:** https://informationisbeautiful.net/visualizations/uk-government-spending-incomes-outcomes/
**Authority:** David McCandless / IIB — award-winning data viz studio
**Audience match:** ⭐⭐⭐⭐ — citizen-friendly but more curated/static

### From documented characteristics

Single large scrollable infographic showing UK income sources (left side, revenue) vs spending categories (right side, expenditure) at proportional visual scale. Each block sized to its £ amount. Categories colour-coded but not loud. No interactivity — meant to be read top-to-bottom or right-to-left.

### Patterns relevant to citizens

- **Proportional visual encoding** — block size = £ amount, instantly comprehensible
- **Side-by-side comparison** of revenue/expenditure, balance implicit
- **Award-winning aesthetic** — minimal, high data-ink, no chartjunk
- **Single page** — no clicking required

### What's missing

- Static; doesn't update with new data
- Doesn't compare to other countries
- Limited dynamic context

---

## Reference 3 — IMF DataMapper (country profiles)

**URL:** https://www.imf.org/external/datamapper/profile/POL (couldn't fetch live)
**Authority:** International Monetary Fund — authoritative cross-country fiscal data
**Audience match:** ⭐⭐ — written for analysts, not citizens; but the framing patterns transfer

### From documented characteristics (Datamapper general design)

- **Country profile page**: collects all key indicators for one country in one place
- **Time series with projections** (solid history + dashed forecast) — visual language for "data we know vs. data we estimate"
- **Multi-country comparison** via slider/selector — Poland vs. peers
- **Headline: % of GDP** — international comparison frame
- **Source attribution prominent** at chart level (IMF WEO October 2024)
- **Minimal interactivity** — see + filter, no scenarios

### Patterns relevant to citizens (adapted)

- **History + projection visual language** — solid line for actual, dashed for forecast (we already do this in Phase B with `dash_when`)
- **Country comparison as core feature** — citizens benefit from seeing Poland positioned among neighbours
- **Threshold annotations** — Maastricht / SGP lines drawn on debt/deficit charts

### What's missing for citizen use

- No PLN / GBP / USD totals — only %GDP (analyst frame)
- No friendly category names — uses ESA codes
- No story; just data tables and charts

---

## Reference 4 — OECD Government Dashboards

**URL:** https://www.oecd.org/en/data/dashboards-and-tools.html (couldn't fetch in depth)
**Authority:** OECD — high-credibility comparative fiscal data
**Audience match:** ⭐⭐ — analyst-leaning but increasingly citizen-readable

### From documented characteristics

OECD provides comparable fiscal data for 38 member countries with:
- **Side-by-side country bar charts** (sorted, single year)
- **Time series with country selection**
- **Subnational government finance dashboard** — drill-down from national to regional
- **Polished design language** — high-quality typography, minimal palette, careful sourcing
- **Data table accessible alongside chart** for verification

### Patterns relevant to citizens

- **Sorted bar chart** for cross-country comparison is the canonical approach (we already do this in Phase B EU comparison)
- **Source + methodology link** on every chart — trust signal
- **Time-series + cross-section pairing** — same metric over time and across countries

---

## Reference 5 — USAFacts (US, citizen-facing)

**URL:** https://usafacts.org/state-of-the-union/budget/
**Authority:** Independent non-partisan, US citizen-facing
**Audience match:** ⭐⭐⭐⭐ — direct citizen audience

### From partial fetch + documented characteristics

- **Linear "State of the Union" structure** — annual digest format
- **Mix of dashboards and editorial** — charts embedded in explanatory text
- **Headline number framing** — "$X trillion" absolute first, % second
- **Interactive deep-dives** — filter by agency, function
- **Stated principle: "non-partisan, just facts"** — every chart cites US Treasury / GAO / BLS sources
- **Editorial sidebar** explaining what numbers mean for the average American

### Patterns relevant to citizens

- **Annual "state of the X" framing** — citizens want a yearly check-in, not real-time
- **Editorial framing alongside charts** — short prose paragraphs explaining what to look at
- **Source-first attribution** — single official source per chart, not "compiled from"
- **Functional categories** (Health, Defense, Education) not bureaucratic (Department of X)

---

## Other sources noted but not analysed

- **OKF "Where Does My Money Go" (UK 2009)** — Originator of the citizen-finance-viz genre. Famous treemap + bubble chart approach + "Daily Bread" per-tax-bracket calculator. Cited everywhere; design heavily influenced subsequent work.
- **IFS TaxLab spending calculators** — UK academic, citizen-readable. Scenario-based exploration ("what if NHS budget doubled").
- **VisGov / Arlington Visual Budget** — Award-winning US local-government budget tool. Heavy use of interactive color-coded breakdowns.
- **bundeshaushalt-info.de** — German federal budget. Heavy on tables, less on viz. Authoritative but not engaging.
- **USAspending.gov** — Federal database with detail-level transparency. Tool not designed for citizen browsing; designed for researchers/journalists.
- **Statistics Poland (stat.gov.pl)** — Authoritative source for Polish data; no citizen-facing viz layer.

---

## Summary — what got captured

| Source | Citizen audience | Cross-country comparison | Deficit/debt focus | Reachable |
|---|---|---|---|---|
| Where Does It Go? (UK) | ⭐⭐⭐⭐⭐ | ❌ | ❌ (spending-only) | ✅ |
| IIB UK Spending viz | ⭐⭐⭐⭐ | ❌ | ❌ (rev/exp only) | ❌ |
| IMF DataMapper | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ❌ |
| OECD dashboards | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ❌ |
| USAFacts | ⭐⭐⭐⭐ | ❌ | ⭐⭐ | ⚠️ |

The gap is clear: **no single reference covers both "citizen audience" AND "deficit/debt focus" AND "cross-country (EU) comparison"**. Our dashboard sits in a niche that none of these fully occupy. We have to synthesise — borrow the citizen framing from UK examples, the cross-country comparison from OECD/IMF, the deficit/debt depth from data-authority sources, the editorial framing from USAFacts.

This is actually useful information: we're not just copying one reference — we're combining best-of approach from four different lineages.
