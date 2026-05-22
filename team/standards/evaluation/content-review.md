# Content Review Rules

**Derived from:** `team/knowledge-base/content/editorial.md` ✓ (KB complete — inverted pyramid, fact-checking, source attribution, Polish press law, writing structure, social media standards)
**Used by:** `.claude/agents/content-reviewer.md`
**Does NOT cover:** analytical correctness of the underlying data (see `evaluation/analytical-review.md`), chart visual design (see `evaluation/visualization-image.md`), dashboard functionality (see `evaluation/code-review.md`)

Rules applied by the `content-reviewer` agent on editorial content produced by the `content-writer` agent. Content is reviewed before publication. The goal is to catch factual, framing, and language errors before they reach readers.

---

## P1 — Blocks Publication

### Factual accuracy

- **Number does not match source** — any statistic in the content that, when verified against the cited source, is incorrect. This includes wrong values, wrong units, wrong time periods, or wrong source attribution. Flag the specific number and the correct value.
- **Calculation error** — any derived value (percentage change, difference, ratio, average) that is mathematically incorrect when computed from the cited source data.
- **Headline-data mismatch** — the headline states a finding that the data does not support. Examples: headline says "record high" but data shows second-highest; headline says "spadek" (decline) but data shows increase; headline says "najwyższy od X lat" but the time window is wrong.

### Framing

- **Causal claim unsupported by the content's data** — language like "X powoduje Y", "X jest przyczyną Y", "X napędza Y" requires either a quoted expert source or an experimental/quasi-experimental design. Correlational data, time series co-movement, or cross-sectional comparison does not justify causal language. Flag as P1.
- **Unbalanced framing on a politically sensitive topic** — for politically sensitive indicators (deficit, debt, immigration, unemployment, inflation), the content must show both level and change, both nominal and real where applicable, both absolute and relative. Presenting only the framing that supports a single narrative is a P1.

### Source attribution

- **Data claim without any source** — any statistical claim (number, percentage, ranking, trend) that has no named source. "Według ekspertów" without naming which experts is a P1. "Dane pokazują" without naming which data is a P1.
- **"Opracowanie własne" without naming the underlying source** — "own calculation" is not a source; it is a method. The underlying primary data source must be named.

---

## P2 — Should Fix Before Publication

### Polish language

- **Missing or incorrect diacritics** — `Srednia` instead of `Średnia`, `bezrobocia` correct but `wynagrodzen` instead of `wynagrodzeń`. Polish labels must be correct Polish.
- **Wrong unit convention for Polish data** — using period as decimal separator (5.1%) instead of comma (5,1%); using no thousand separator for large numbers (1234567 instead of 1 234 567); using "%" for a percentage-point delta instead of "pp" or "punkty procentowe".
- **Informal register in formal content** — colloquialisms, slang, or casual phrasing in blog articles or official social cards. The register must be professional, formal Polish.
- **Economic terminology incorrect** — using non-standard terms where standard Polish economic terms exist. Examples: "płaca" in formal context where "wynagrodzenie" is standard; "PKB" on first mention without spelling out "Produkt Krajowy Brutto".

### Structure and clarity

- **Lead paragraph not self-contained** — a reader who stops after the lead should still know the main finding. If the lead requires reading further to understand what the article is about, it is P2.
- **Headline exceeds length limit** — blog headlines max 12 words; social card headlines max 8 words.
- **Headline states topic, not finding** — "Dane o bezrobociu za 2024 r." is a topic. "Bezrobocie na najniższym poziomie od 20 lat" is a finding.
- **Missing benchmark or context** — a number presented without any comparison (prior year, EU average, peer group). The reader cannot tell if the number is high or low.
- **Cherry-picked time window without note** — "X rose since 2020" when 2020 was a crisis trough, without noting the longer context.
- **Percentage change on a percentage value without pp clarification** — "bezrobocie wzrosło o 15%" when it went from 5% to 5.75%. The correct framing is "wzrosło o 0,75 pp". Note if the content uses "%" where "pp" is required.

### Source attribution

- **Source named but not specific enough** — "Według GUS" without specifying which publication (BDL, BAEL, communication). "According to Eurostat" without specifying the dataset code.
- **Missing chart footer source** — charts and data visuals must have "Źródło: ..." at the bottom.

---

## P3 — Noted

- **No "what to watch" section** — the content does not indicate what data release or event comes next. Note as an improvement opportunity.
- **Abbreviation not defined on first use** — "PKB" used without first spelling out "Produkt Krajowy Brutto (PKB)". Note as a clarity item.
- **No methodology note for non-trivial calculations** — if the content includes a derived metric (e.g., real wages adjusted for inflation), a brief methodology note would improve transparency.
- **Content does not cite which KB section grounds each recommendation** — note as traceability improvement.
- **Missing humanisation** — the content presents numbers but does not connect them to readers' lived experience. Note as an engagement improvement.

---

## What this standard does NOT cover

- Whether the underlying data in the warehouse is correct — that is the data pipeline's responsibility.
- Whether the chart renders correctly or uses the right colours — that is `visual-screenshot-reviewer`'s scope.
- Whether the SQL query that produced the number is correct — that is `analytical-validator`'s scope.
- Whether the indicator is the best KPI for the domain — that is `domain-specialist`'s scope.
- Subjective preferences for writing style beyond the rules listed above — matters of taste are not P1/P2/P3 findings.
