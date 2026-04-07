# Playbook: Article

Covers sub-product #17 — Article (blog post / data journalism article).

## Recipe

### Sub-product #17 — Article

| Task | Competency | Builder | Evaluator | Standard |
|------|-----------|---------|-----------|----------|
| Domain brief (analytical framing, indicator selection, story angle) | Business Analysis | `business-analyst` | `brief-reviewer` | brief-review.md |
| Write (data journalism, Polish language, factual precision) | Content / Editorial | `content-writer` | `content-reviewer` | content-review.md |
| Visual embed (chart selection, integration) | Dashboard Development | `dashboard-dev` | `visualization-reviewer` | visualisation.md → visualization-diff.md |

---

## Phase 1 — Domain Brief

The `business-analyst` produces an analytical brief for the article topic:

1. **Identify the story angle** — what question does this article answer? What finding is newsworthy?
2. **Select indicators** — which metrics from the warehouse support the story? Use the domain KB for canonical indicators.
3. **Define benchmarks** — what comparisons give the numbers meaning? (EU average, prior year, peer group, policy threshold)
4. **Identify structural breaks** — are there methodology changes, EU accession effects, or definitional shifts that affect interpretation?
5. **Determine the audience** — who will read this and what is their economics background?

**Output:** An analytical brief documented in the Linear issue. Reviewed by `brief-reviewer` (SMART+FABRIC, aggregation rules, benchmarks, Polish structural breaks).

**Gate:** If `brief-reviewer` returns BLOCK, the brief is revised and re-reviewed. CONDITIONAL findings are noted but do not block proceeding.

---

## Phase 2 — Write

The `content-writer` produces the article following the editorial KB:

### 2.1 Structure

Follow the inverted pyramid structure (§2.1 of `content/editorial.md`):

1. **Lead (1–2 sentences)** — key number, direction of change, time period
2. **Nut graph (1–2 sentences)** — why this matters now; context
3. **Supporting evidence (2–4 paragraphs)** — data points, chart descriptions, breakdowns
4. **Background** — historical context, methodology notes
5. **What to watch** — next data release, forward outlook

### 2.2 Rules

- **Headline** (§2.3): max 12 words, active voice, contains the finding (not the topic), no questions, proper diacritics
- **Precision vs. simplicity** (§2.2): rounded in headline/lead, exact in body, rounded in chart labels
- **Source attribution** (§3): every claim attributed; "Źródło: ..." on every chart reference; full citations at end
- **Polish language** (§5.3): formal register, proper diacritics, standard economic terminology, Polish number conventions (comma decimal, space thousand separator)
- **Balanced framing** (§5.2): on politically sensitive topics, show both level and change, both nominal and real
- **No causal language** without expert source or experimental design (§4.1)
- **Fact-checking** (§4): every number traced to source, every calculation verified, every comparison uses compatible definitions

### 2.3 Length

| Type | Word count | Charts | Use case |
|------|-----------|--------|----------|
| Short | 300–500 | 1–2 | Single finding, quick update |
| Medium | 500–1000 | 2–4 | Standard analysis piece |
| Long | 1000–2000 | 4–6 | Deep dive, multi-dimensional analysis |

### 2.4 Output

The article is written as a Markdown file in `products/blog/articles/` (or Ghost CMS draft, depending on the publishing workflow). Include:
- Full Polish text with proper diacritics
- Chart references (descriptions of what each chart shows)
- Source attributions in the correct format
- A verification checklist (§4.3) as a comment at the end of the file

---

## Phase 3 — Content Review

The `content-reviewer` evaluates the article against `content-review.md`:

- **P1 findings** (blocks publication): factual errors, headline-data mismatch, causal claims unsupported, missing source attribution
- **P2 findings** (should fix): Polish language errors, missing benchmarks, cherry-picked time windows, headline too long
- **P3 findings** (noted): missing "what to watch", undefined abbreviations, no methodology note

**Gate:** If any P1 findings, the article returns to the content-writer for revision. P2 findings should be addressed before publication. P3 findings are noted but do not block.

---

## Phase 4 — Visual Embed

The `dashboard-dev` produces chart components for the article:

1. **Select chart types** — follow `visualization/charts/*.md` rules for each data pattern
2. **Build chart components** — import Nordic theme from `products/visuals/lib/theme.py`; no hardcoded colours
3. **All labels in Polish** — titles, axis labels, tooltips, footers
4. **Source attribution** — "Źródło: ..." on every chart footer
5. **Embed** — integrate charts into the article template (Ghost block or Markdown image reference)

Charts are reviewed by `visualization-reviewer` (diff) and `visual-screenshot-reviewer` (rendered output).

---

## Phase 5 — Publish

1. **Final review** — article + charts reviewed together; verify chart references match embedded charts
2. **Source check** — every data claim has a visible source attribution
3. **Polish proofread** — diacritics, grammar, terminology, number conventions
4. **Publish** — Ghost CMS draft → published, or Markdown file deployed to blog
5. **Social promotion** — create a social card (see `social.md` playbook) linking to the article

---

## Quality Gates

- [ ] Analytical brief reviewed and approved by `brief-reviewer`
- [ ] Article passes `content-reviewer` with no P1 findings
- [ ] Every number traced to its source
- [ ] Every chart has source attribution in footer
- [ ] Headline matches the data (not overstated, not understated)
- [ ] Polish diacritics correct throughout
- [ ] No causal language unsupported by the data
- [ ] Charts reviewed by `visualization-reviewer`
- [ ] Article previewed in browser before publishing
