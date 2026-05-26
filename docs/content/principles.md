# Knowledge Base: Editorial Standards & Data Journalism Writing

**Module:** `docs/content/principles.md`
**Version:** 1.0 — April 2026
**Status:** Ready for use

Agent reference for writing and reviewing editorial content — blog articles, social media cards, and data journalism copy — for Open Reporting. Read at the start of any content production task, and during editorial review.

**Does not duplicate:** `analytical-thinking.md` (analytical moves, insight hierarchy, aggregation rules). Read that file first when the content is analytical in nature. This file extends it with writing craft, fact-checking, and editorial quality rules.

**Sources:** Paul Bradshaw, "The Inverted Pyramid of Data Journalism" (Online Journalism Blog, 2011/2024); Data Journalism Handbook (2012/2022); NN/g "Inverted Pyramid: Writing for Comprehension" (2018); Purdue OWL "The Inverted Pyramid Structure"; River "How to Fact-Check and Verify Sources" (2026); CUNY Journalism "Fact-Checking & Verification"; LexisNexis "How to Fact Check Like a Pro"; Polish Press Law Act (Ustawa Prawo Prasowe, Dz.U. 1984 nr 5 poz. 24, consolidated text); IPI Media Capture Monitoring Report: Poland (2025); Society of Professional Journalists Code of Ethics; Reuters Handbook of Journalism.

---

## 1. The Inverted Pyramid of Data Journalism

### 1.1 The Six Stages

Paul Bradshaw's Inverted Pyramid of Data Journalism defines six stages that every data journalism product passes through. The model has been translated into multiple languages and taught worldwide. For Open Reporting, the most relevant stages are **Conceive**, **Context**, **Question**, and **Communicate** — the others (Compile, Clean) are handled by the data platform, not the editorial layer.

| Stage | What it means | Open Reporting application |
|-------|--------------|---------------------------|
| **Conceive** | Idea generation — what story does the data tell? | Before writing any article or social card, identify the analytical angle (from the domain brief) |
| **Compile** | Gathering data from sources | Already handled by ingestion layer; editorial assumes data exists |
| **Clean** | Preparing data for analysis | Already handled by processing layer |
| **Context** | Putting numbers into meaningful comparison | Every article must provide benchmarks: EU average, prior year, peer group |
| **Question** | Analytical interrogation at every stage | Every claim must be answerable from the data; every chart must answer a question |
| **Communicate** | Visualise, narrate, humanise, personalise, utilise | The dashboard, article, or social card itself |

### 1.2 Communicate: Five Modes

| Mode | Definition | When to use |
|------|-----------|-------------|
| **Visualise** | Charts, graphs, maps, tables | Default for dashboard content; quantitative comparisons |
| **Narrate** | Written prose — headline, lead, body, conclusion | Blog articles, social captions, explanatory text |
| **Humanise** | Connecting numbers to people's lived experience | When the data has direct impact on citizens' daily life |
| **Personalise** | Interactive tools that let users find their own position | Explorers, calculators, "where do you fit" features |
| **Utilise** | Making the data actionable — what should the reader do? | Policy recommendations, voting guidance, financial decisions |

**Rule:** Every editorial product must use at least two modes. A chart alone is visualise-only — add narration (what the chart shows) and humanisation (what it means for the reader).

---

## 2. Writing Structure

### 2.1 The Inverted Pyramid for News Writing

The inverted pyramid structure — originating in telegraph-era journalism and validated by NN/g usability research — remains the gold standard for news writing. The principle: start with the most important information, then add supporting detail, then background.

**Structure for data journalism articles:**

1. **Lead (1–2 sentences)** — The single most important finding. Must contain the key number, the direction of change, and the time period. Example: "Liczba bezrobotnych w Polsce spadła do 1,1 mln w 2024 r. — najniższy poziom od 20 lat."
2. **Nut graph (1–2 sentences)** — Why this matters now. Context, comparison, or significance.
3. **Supporting evidence (2–4 paragraphs)** — Data points, charts, quotes from sources, breakdowns by dimension.
4. **Background** — Historical context, methodology notes, prior trends.
5. **What to watch** — Forward-looking: what data release or event comes next.

**Rules:**
- The lead must be self-contained — a reader who stops after the lead should still know the main finding.
- Every paragraph after the lead must add new information, not repeat.
- Charts reference: describe what the chart shows in the text before or after it, never assume the chart speaks for itself.
- Numbers: always provide the unit and the reference period. "1,1 mln" not "ponad milion"; "w 2024 r." not "ostatnio".

### 2.2 Precision vs. Simplicity

Data journalism walks a line between statistical precision and reader comprehension. The following rules govern that balance:

| Situation | Rule | Example |
|-----------|------|---------|
| **Headline** | Round to 1–2 significant digits; use direction words | "Bezrobocie spadło do 5,1%" not "Bezrobocie wyniosło 5,12%" |
| **Lead paragraph** | Round to 2 significant digits; include direction and period | "Wzrost o 3,2% r/r" not "Wzrost o 3,17%" |
| **Body text** | Use exact numbers from source; cite the source | "Według GUS, wynagrodzenie wzrosło z 7 234 zł do 7 467 zł" |
| **Chart labels** | Round for readability; exact values in tooltips or data tables | Axis: "7 000 zł"; tooltip: "7 234,56 zł" |
| **Percentages vs. percentage points** | Always use "pp" (punkty procentowe) for differences between rates | "Stopa bezrobocia spadła o 1,2 pp" not "o 1,2%" |

### 2.3 Headline Rules

- **Maximum 12 words** — shorter is better for scanning
- **Must contain the key finding** — not the topic, the finding. "Bezrobocie na najniższym poziomie od 20 lat" not "Dane o bezrobociu za 2024 r."
- **Active voice preferred** — "Firmy zwalniają" not "Zwolnienia są dokonywane przez firmy"
- **No questions in headlines** — headlines state findings, they do not pose questions
- **Polish diacritics required** — "Średnie wynagrodzenie" not "Srednie wynagrodzenie"

---

## 3. Source Attribution

### 3.1 Attribution Hierarchy

Every claim in editorial content must be attributable. The hierarchy of source authority:

| Level | Source type | Examples | When sufficient |
|-------|------------|----------|----------------|
| **Primary** | Official statistical publications | GUS BDL, Eurostat, NBP, MF, ZUS | Always sufficient for factual claims |
| **Secondary** | Reputable analysis of primary data | NBP reports, IMF Article IV, OECD Economic Surveys | Sufficient for interpretive claims |
| **Tertiary** | News media reporting on data | Press articles, TV news | Not sufficient alone — trace to primary |
| **Unverified** | Social media, blogs, press releases | Twitter, company PR, think tank briefs | Never sufficient alone; must be corroborated |

### 3.2 Attribution Format

- **In-text:** "Według danych GUS..." / "Eurostat podaje, że..." / "Jak wynika z raportu NBP..."
- **Chart footers:** "Źródło: GUS, Bank Danych Lokalnych, opracowanie własne"
- **Social cards:** "Źródło: GUS BDL" in small type at bottom
- **Blog articles:** Full source citation at end of article with URL and access date

**Rule:** Every chart, KPI card, and data claim must name its source. "Opracowanie własne" means Open Reporting's own calculation from named primary data — it is not a source substitute.

---

## 4. Fact-Checking & Verification

### 4.1 The Corroboration Standard

Adapted from investigative journalism practice for data journalism:

| Claim type | Verification requirement |
|-----------|-------------------------|
| **Official statistic** | Verify against the published source; note revision if different from prior release |
| **Calculated value** | Verify the calculation independently; document the formula |
| **Comparison claim** | Verify both values; confirm comparability (same definition, same period) |
| **Trend claim** | Verify at least three data points; confirm the trend is not an artefact of the chosen start/end |
| **Ranking claim** | Verify the ranking methodology; confirm the peer group is appropriate |
| **Causal claim** | Requires quoted expert source or experimental design; correlational data alone is insufficient |

### 4.2 Red Flags in Data Claims

- **Too-perfect numbers** — round numbers in official statistics are rare; verify
- **Cherry-picked time windows** — "X rose since 2020" when 2020 was a crisis trough; verify with longer context
- **Apples-to-oranges comparisons** — comparing GUS LFS unemployment with PUP registration counts; verify definitions match
- **Percentage change on percentage values** — "unemployment rose 15%" when it went from 5% to 5.75%; the correct framing is "rose 0,75 pp"
- **Missing denominator** — absolute numbers without population context; verify whether per-capita normalisation is needed

### 4.3 Verification Checklist

Before publishing any editorial content:

- [ ] Every number traced to its source
- [ ] Every calculation independently verified
- [ ] Every comparison uses compatible definitions
- [ ] Polish unit conventions: comma decimal, space thousand separator, "mln zł" / "mld zł", "pp" for percentage-point deltas
- [ ] Headline matches the data (not overstated, not understated)
- [ ] Source attribution visible on every chart and data claim
- [ ] No causal language unsupported by the data

---

## 5. Editorial Independence & Polish Press Law

### 5.1 Key Principles

The Polish Press Law Act (Prawo Prasowe, 1984) establishes:

- **Press freedom** — Article 1: the press enjoys freedom of speech and printing, realising citizens' right to information and influence on public affairs
- **Editorial independence** — Article 12: the press shapes public opinion and fulfils the task of social control and criticism
- **Accuracy obligation** — Article 11: the press is obliged to present facts truthfully
- **Right of reply** — Article 31–33: any person or entity has the right to demand publication of a correction if false information was published
- **Source protection** — Article 15: journalists have the right to protect the confidentiality of their sources

### 5.2 Implications for Open Reporting

- **Data is the source** — statistical data from GUS, Eurostat, NBP is the primary source; it must be cited accurately and without selective omission
- **Correction policy** — if an error is discovered, correct it promptly and transparently; explain what was wrong and what is correct
- **No sponsored content without disclosure** — any content produced in partnership with or funded by external entities must be clearly labelled
- **Balanced framing on politically sensitive topics** — fiscal deficit, public debt, immigration, unemployment, inflation: show both level and change, both nominal and real where applicable, both absolute and relative

### 5.3 Polish Language Standards

- **Formal register** — professional, formal Polish; no colloquialisms, no slang
- **Proper diacritics** — all Polish characters (ą, ć, ę, ł, ń, ó, ś, ź, ż) must be correct
- **Economic terminology** — use standard Polish economic terms: "stopa bezrobocia" (not "unemployment rate"), "wynagrodzenie" (not "płaca" in formal context), "produkt krajowy brutto" (not "PKB" on first mention)
- **Abbreviations** — define on first use: "Produkt Krajowy Brutto (PKB)", then "PKB" thereafter
- **Numbers** — Polish convention: comma as decimal separator (5,1%), space as thousand separator (1 234 567), non-breaking space between number and unit (5,1%)

---

## 6. Social Media Card Standards

### 6.1 Instagram Data Cards

- **Single finding per card** — one chart, one number, one message
- **Headline: maximum 8 words** — must be readable at thumbnail size
- **Number prominence** — the key number should be the largest text element
- **Source attribution** — visible, minimum 8pt equivalent, at bottom
- **Brand consistency** — Nordic colour palette, Open Reporting logo, consistent typography
- **Caption** — 1–3 sentences expanding the finding; include source URL and hashtags

### 6.2 Data Cards (Single-Stat)

- **One number** — the single most important statistic
- **Context line** — "najniższy poziom od 20 lat" / "wzrost o 3,2% r/r"
- **Source** — always visible
- **No chart needed** — the number is the visual

---

## 7. Blog Article Structure

### 7.1 Standard Article Template

```
Title: [Finding-focused headline, max 12 words]

Lead: [1–2 sentences: key number, direction, period]

Nut graph: [Why this matters now; context]

Section 1: [The data — what it shows, with chart]
Section 2: [The comparison — how it stacks up, with chart]
Section 3: [The context — why it happened, with chart or analysis]
Section 4: [What to watch — next data release, forward outlook]

Sources: [Full citations with URLs and access dates]
Methodology: [Brief note on calculation approach, if non-trivial]
```

### 7.2 Length Guidelines

| Type | Word count | Charts | Use case |
|------|-----------|--------|----------|
| **Short** | 300–500 | 1–2 | Single finding, quick update |
| **Medium** | 500–1000 | 2–4 | Standard analysis piece |
| **Long** | 1000–2000 | 4–6 | Deep dive, multi-dimensional analysis |

---

## 8. What Makes Good Data Journalism

### 8.1 Quality Dimensions

| Dimension | What it means | Failure signal |
|-----------|--------------|---------------|
| **Accuracy** | Every number correct, every calculation verified | Wrong figures, miscalculated percentages |
| **Clarity** | Reader understands the finding without economics training | Jargon, unexplained abbreviations, complex sentences |
| **Context** | Numbers compared to meaningful benchmarks | "X is 500" without saying whether that is high or low |
| **Balance** | Both sides of a politically charged story shown | Only one framing, only one peer group, only one time window |
| **Attribution** | Every claim traceable to a source | "Experts say" without naming who |
| **Relevance** | The finding matters to the reader's life or decisions | Interesting but irrelevant statistics |
| **Timeliness** | Published while the data is still new | Weeks-old data presented as breaking |

### 8.2 Common Errors to Avoid

- **Headline-data mismatch** — headline says "record high" but data shows second-highest
- **Missing inflation adjustment** — comparing nominal wages across years without real terms
- **Base rate neglect** — "X doubled" when it went from 1 to 2
- **Ecological fallacy** — inferring individual behaviour from aggregate data
- **Survivorship bias** — analyzing only entities that persist in the dataset
- **Seasonal confusion** — comparing Q4 to Q1 without seasonal adjustment note
- **Chart distortion** — truncated y-axis making small changes look dramatic
