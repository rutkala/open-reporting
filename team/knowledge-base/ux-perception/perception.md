# Visual Perception and UX for Data Visualisation

**Agent reference for designing and evaluating rendered dashboards.**
Read at the start of `/plan` when designing any dashboard layout, chart, or visual component.
Read in full by the `visual-design-reviewer` agent before evaluating any screenshot.

**Sources:** Colin Ware, *Information Visualization: Perception for Design* (4th ed., Elsevier 2021); Anne Treisman & Garry Gelade, "A Feature-Integration Theory of Attention," *Cognitive Psychology* 12(1) 1980; Nelson Cowan, "The Magical Number 4 in Short-Term Memory," *Behavioral and Brain Sciences* 24(1) 2001; George Miller, "The Magical Number Seven, Plus or Minus Two," *Psychological Review* 63(2) 1956; John Sweller, "Cognitive Load During Problem Solving," *Cognitive Science* 12(2) 1988; Jakob Nielsen & Kara Pernice, *Eyetracking Web Usability* (New Riders, 2010); Nielsen Norman Group, "F-Shaped Pattern for Reading Web Content" (2006/2017 update); Cynthia Brewer, ColorBrewer (colorbrewer2.org); W3C, *Web Content Accessibility Guidelines 2.2* (2023); Stephen Few, *Information Dashboard Design* (O'Reilly, 2006) and *Show Me the Numbers* (Analytics Press, 2004); Alberto Cairo, *The Functional Art* (New Riders, 2012) and *The Truthful Art* (New Riders, 2016); Ewald Hering, opponent-process colour theory (1892), formalised in LGN pathway research (De Valois & De Valois, 1993).

---

## 1. Pre-Attentive Attributes

### 1.1 What Pre-Attentive Processing Is

Treisman's Feature Integration Theory (1980) established a two-stage model of visual processing. In **Stage 1 (pre-attentive)**, the visual system in parallel registers a fixed set of low-level features across the entire visual field in under 200–250ms — before focal attention is deployed. In **Stage 2 (focused attention)**, the brain binds individual features into objects, which is serial and slow.

The implication for data visualisation: any encoding that exploits a pre-attentive attribute is processed instantaneously across the entire display. An encoding that does not (e.g. label text, numerical values) requires the viewer to serially scan each element. The difference in comprehension time is an order of magnitude.

A pre-attentive attribute can be detected in a "pop-out search" — a single target item that differs from all distractors along that dimension is found in constant time regardless of how many distractors are present. This is the operational definition: if search time does not increase with set size, the attribute is pre-attentive.

### 1.2 The Complete Attribute Set

Colin Ware (4th ed.) organises pre-attentive attributes into four perceptual channels:

**Colour channel:**
| Attribute | Encoding power | Best used for |
|-----------|---------------|---------------|
| Hue (colour category) | Strong — categorical | Series identity, data category, alert status |
| Luminance/intensity (light–dark) | Strong — ordered | Sequential magnitude encoding |
| Saturation | Moderate — ordered | Secondary emphasis, muted vs active |

**Form channel:**
| Attribute | Encoding power | Best used for |
|-----------|---------------|---------------|
| 2D position (x, y) | Strongest of all attributes | Any quantitative value — the primary channel |
| Length | Strong — quantitative | Bar chart magnitude |
| Orientation | Strong — categorical / directional | Arrows, slope, signal vs noise |
| Size (area) | Moderate — quantitative | Magnitude (use with caution — perceptual compression) |
| Shape | Moderate — categorical | Data series markers, small multiples |
| Curvature | Moderate | Line type distinction |
| Enclosure (containment) | Moderate — grouping | Panel borders, card backgrounds |
| Added marks (fill, hash) | Weak | Texture-based grouping |
| Numerosity | Weak | Point density, cluster presence |

**Motion channel (dynamic only):**
| Attribute | Encoding power | Best used for |
|-----------|---------------|---------------|
| Flicker / blink | Extremely strong | Alerts (use sparingly — high irritation) |
| Motion direction / velocity | Strong | Animated transitions, live-updating values |

**Position note:** Ware consistently identifies 2D position as the most accurate quantitative encoding. Cleveland & McGill's 1984 ranking — position > length > angle > area > volume > colour density > colour hue — remains the empirical benchmark. Avoid encoding quantitative magnitude in angle (pie charts), area (bubble charts), or colour hue alone when position or length is available.

### 1.3 Implications for Chart Design

- **One pre-attentive attribute per encoding purpose.** Using two attributes simultaneously (e.g. both colour and size to encode the same variable) creates redundant coding, which can aid the colour-blind but risks visual confusion if they encode different variables.
- **Categorical hue breaks down above 8–10 distinct categories.** The visual system cannot reliably distinguish more than 8–10 hues in a chart legend. Above this limit, hue encoding fails and requires the viewer to match legend to element with focused attention — losing the pre-attentive advantage entirely.
- **Size encoding (bubble/area) underestimates magnitude.** Psychophysically, perceived area grows as the 0.7 power of actual area (Stevens' Power Law). Viewers systematically underestimate differences encoded in area. Correct or label explicitly when using bubble charts.
- **Orientation is excellent for direction, poor for magnitude.** Slope in line charts encodes rate of change pre-attentively — this is why line charts are superior to bar charts for trend communication. However, axis scaling determines perceived slope; a truncated y-axis distorts pre-attentive slope perception and misleads before the viewer reads any values.

---

## 2. Gestalt Principles

The Gestalt laws, developed by Wertheimer, Köhler, and Koffka (Berlin school, 1910s–1920s), describe how the visual system groups individual elements into perceived wholes. They operate pre-attentively — grouping is automatic, not deliberate.

### 2.1 The Seven Core Laws

**Law of Proximity:** Elements that are spatially close are perceived as belonging together. Distance implies relationship.

*Dashboard application:* A chart title placed 20px above the chart is perceived as belonging to it. A title placed equidistant between two charts is ambiguous — the viewer cannot determine which chart it labels. Filters and controls should be placed adjacent to the charts they affect, not in a distant header strip.

**Law of Similarity:** Elements that share visual attributes (colour, shape, size, orientation) are perceived as a group, regardless of position.

*Dashboard application:* If Poland is always blue across all charts on a dashboard, the viewer builds a colour-concept association that allows instant lookup. Break that association (Poland as orange in one chart, blue in another) and the viewer must re-read the legend each time — destroying the pre-attentive benefit.

**Law of Continuity (Good Continuation):** The eye follows the smoothest path. Elements aligned along a line or curve are perceived as related.

*Dashboard application:* Aligning chart components to an invisible grid creates reading paths. Charts that are vertically aligned can be compared as a column. Deliberately misaligning a chart breaks the reading flow and isolates it perceptually — useful for calling it out as a standalone finding.

**Law of Closure:** The eye completes incomplete shapes, treating a partial boundary as enclosure.

*Dashboard application:* A row of KPI cards does not need a visible border box around each card if the whitespace gap between cards is consistent — the viewer perceives the enclosed groups. Adding unnecessary border boxes creates visual noise without adding grouping information.

**Law of Figure/Ground:** The visual system divides the field into a figure (foreground object of attention) and ground (background). Figure is perceived as having shape; ground is perceived as shapeless and receding.

*Dashboard application:* Data marks must be the figure; gridlines, axes, and backgrounds must be the ground. When gridlines are darker or more saturated than the data, the relationship inverts — the viewer perceives the grid as the figure and data as overlaid noise. This is the perceptual basis for Tufte's data-ink ratio principle.

**Law of Common Fate:** Elements that move together, or change together, are perceived as a group.

*Dashboard application:* Interactive filter callbacks that simultaneously update all charts in a view signal that those charts share a data context. This is one of the strongest grouping signals in dynamic dashboards. If only some charts respond to a filter, the non-responding charts are perceptually grouped as a separate, independent set.

**Law of Prägnanz (Good Form / Simplicity):** The visual system resolves ambiguous scenes into the simplest, most stable interpretation. Complexity that does not add information is resolved away.

*Dashboard application:* This is the perceptual basis for minimalism in chart design. Chart elements that do not encode data — 3D bevels, gradient fills, decorative borders, background images — are not perceived as neutral; they are resolved as noise that competes with the signal. The viewer's perceptual system must spend resources determining that the decoration is not information. This is the cognitive cost of chartjunk.

### 2.2 Legend Placement Rule

Gestalt proximity + similarity combined: place legends immediately adjacent to the data they describe. Right-side legends are conventional but require the viewer to look away from the chart area for every category lookup. Direct labelling (labels on the data series itself) eliminates the lookup entirely and should be the default for charts with 6 or fewer series.

---

## 3. Cognitive Load Theory

### 3.1 Sweller's Three Types

John Sweller (1988, extended 1994) proposed that human working memory has a fixed capacity, and that total cognitive load is the sum of three components:

**Intrinsic load** — the irreducible complexity of the information itself. A dashboard showing seven economic indicators has higher intrinsic load than one showing three. Cannot be reduced without reducing the information content.

**Extraneous load** — load caused by the *presentation format*, not by the information. Chartjunk, poor layout, inconsistent colour, missing labels, 3D effects, overloaded axes — all increase extraneous load. This load competes with intrinsic load and consumes the same fixed-capacity working memory. Extraneous load is entirely within the designer's control.

**Germane load** — the cognitive effort directed at understanding and building a mental schema. This is the "useful" load. When extraneous load is reduced, the freed capacity is available for germane load — the viewer actually understands more.

**The key design implication:** Every element of a dashboard that does not encode information generates extraneous load. The goal is to drive extraneous load as close to zero as possible, freeing working memory capacity for the actual analytical task.

### 3.2 What Increases Extraneous Load (Chartjunk Taxonomy)

Derived from Tufte (1983), Few (2006), and cognitive load research:

| Element | Load mechanism |
|---------|---------------|
| 3D bars, 3D pies | Depth cue creates false spatial encoding; viewer must mentally project back to 2D to read values. Distorts perception of magnitude. |
| Gradient fills on bars | Luminance gradient is a pre-attentive attribute — the eye reads it as a data signal that isn't there |
| Drop shadows | Creates figure/ground ambiguity; the shadow is a second figure competing with the bar |
| Decorative gridlines (bold or numerous) | Grid becomes the figure; data becomes ground (figure/ground inversion) |
| Background images or textures | Compete with data for figure/ground resolution |
| Overloaded legend (10+ categories) | Forces serial lookup for every data interpretation; destroys pre-attentive hue encoding |
| Unnecessary dual axes | Requires viewer to maintain two quantitative scales simultaneously in working memory |
| Pie chart with 7+ slices | Angle encoding (weak) combined with many small values; viewer cannot distinguish or rank |
| Redundant data labels on bar charts | Provides numeric precision the chart already implies, at the cost of visual clutter |
| Ticker animations on KPI cards | Motion is the strongest pre-attentive attribute; attracts attention disproportionately to KPI importance |

### 3.3 Miller's Law and the 7±2 Series Limit

George Miller (1956) established that short-term memory holds approximately 7±2 chunks. While often cited as a design rule for chart series limits, the more precise constraint comes from Cowan (2001): **visual working memory capacity is approximately 4±1 chunks**, not seven. This is the binding constraint for simultaneous visual comparison:

- A viewer comparing four coloured series on a line chart must hold four colour-concept associations in visual working memory simultaneously. This is at the capacity limit.
- Five or more series on a single line chart reliably exceeds visual working memory. The viewer loses track of which line is which and must repeatedly consult the legend — the comparison task fails.
- **Hard rule derived from Cowan:** Maximum 4 series on a line chart intended for comparison. Maximum 6 for a stacked bar (where relative comparison is easier because the eye uses position, not memory). Maximum 8 distinct hues in a categorical palette before the encoding degrades.

The 7±2 figure applies to **chunked** information (e.g. a viewer who knows the chart context well may chunk "GDP growth" as a single concept). For an unfamiliar viewer, the limit is lower. Design for Cowan's 4, not Miller's 7.

---

## 4. Eye-Tracking Patterns and Dashboard Layout

### 4.1 The F-Pattern

Nielsen and Pernice (2006, replicated 2017) conducted large-scale eye-tracking studies on text-heavy web pages. The dominant pattern: **two horizontal sweeps** across the top of the content, followed by a **vertical scan down the left edge**. The result is an F-shaped fixation heatmap.

Critically, the 2017 follow-up study identified multiple sub-patterns depending on content type:
- **F-pattern** — dominant for text-heavy, undifferentiated pages
- **Layer-cake pattern** — horizontal scans across headings, skipping body text — common for structured dashboards with clear section headers
- **Spotted pattern** — selective fixation on specific known elements (numbers, highlighted values) — dominant for expert users who know the dashboard layout
- **Commitment pattern** — thorough reading of every element — rare, only for highly motivated users

**Dashboard implication:** First-time viewers use the F-pattern or layer-cake pattern. Returning expert users use the spotted pattern. Design primarily for the spotted pattern (experienced users) while ensuring the F-pattern starting zone (top-left) carries the most important content.

### 4.2 Z-Pattern and the Gutenberg Diagram

The **Z-pattern** applies to content with low information density (landing pages, marketing layouts): the eye scans horizontally across the top, diagonally down-left to bottom-left, and horizontally across the bottom.

The **Gutenberg diagram** (Edmond Arnold, 1950s, later formalised as a design principle) divides the display into four zones based on reading gravity — the tendency to read top-to-bottom, left-to-right in Western typography:

| Zone | Location | Attention weight |
|------|----------|-----------------|
| Primary optical area | Top-left | Highest — first fixation point |
| Strong fallow area | Top-right | Second — catches during initial horizontal sweep |
| Weak fallow area | Bottom-left | Low — skipped in fast scanning |
| Terminal area | Bottom-right | Moderate — final resting point, best for CTAs |

**Dashboard application of the Gutenberg diagram:**
- Top-left: the single most important KPI or headline finding
- Top-right: the second-priority KPI or a context number
- Bottom-left: supplementary detail, footnotes, source attribution
- Bottom-right: navigation, export buttons, date filter

### 4.3 Above the Fold

"Above the fold" — content visible without scrolling in the initial viewport — receives 80% of total viewing time on information pages (Nielsen Norman Group research). For a 1440×900 desktop viewport, approximately the top 700px of visible content accounts for the vast majority of user attention.

**Dashboard implication:**
- All headline KPIs must be visible without scrolling
- The primary chart (the analytical core of the dashboard) must be at least partially visible above the fold
- Do not place the only chart on a dashboard below a large header band that consumes the first 400px

### 4.4 Foveal vs Peripheral Vision

The fovea (central 2° of visual field) provides high-acuity colour vision and resolves fine detail. The periphery processes motion, large shapes, luminance contrast, and orientation pre-attentively but cannot resolve text or fine marks.

**Dashboard implication:** A viewer with foveal focus on a KPI card cannot read axis labels on a chart at the edge of the screen — but they *will* notice a bold anomaly highlight or a colour change at the periphery. This is the perceptual basis for the "call-out" pattern: use peripheral-compatible cues (colour, contrast, size) to draw attention before detail is needed.

---

## 5. Colour Perception

### 5.1 The Opponent-Process Model

The visual system does not simply pass raw RGB values to the brain. After cone signals (L, M, S cones) are generated in the retina, the lateral geniculate nucleus (LGN) recodes them into **three opponent channels**:

| Channel | Encoding | What fails |
|---------|---------|-----------|
| L–M (red–green) | Differences between long and medium wavelength cones | Protanopia and deuteranopia (red-green colour blindness) |
| S–(L+M) (blue–yellow) | Short wavelength vs sum of long+medium | Tritanopia (rare, 0.01%) |
| Luminance (L+M) | Achromatic brightness | Not affected by colour blindness |

The opponent-process architecture explains why red and green are maximally confusable for the 8% of European males with red-green deficiency: both hues are processed in the same channel, and when that channel is degraded, they become identical in appearance. Red-green is not a contrast problem (the luminance channel is intact); it is a categorical identification problem. A red bar and a green bar of equal luminance are indistinguishable to a deuteranoope.

### 5.2 Colour Blindness Rates

| Type | Mechanism | Prevalence (males) | Prevalence (females) |
|------|-----------|-------------------|---------------------|
| Deuteranomaly (weak green) | M-cone shifted | 5% | 0.4% |
| Protanomaly (weak red) | L-cone shifted | 1% | 0.1% |
| Deuteranopia (no green) | M-cone absent | 1% | 0.01% |
| Protanopia (no red) | L-cone absent | 1% | 0.01% |
| **Total red-green** | | **~8%** | **~0.5%** |
| Tritanopia (no blue) | S-cone absent | 0.01% | 0.01% |

**Design implication:** On a dashboard showing Polish economic data, if 100 users view it, approximately 8 of the male users and 1 of the female users cannot distinguish red from green. A semantic colour convention of red=bad, green=good — without any luminance or shape redundancy — is unreadable to roughly 4–5% of all users.

### 5.3 Safe Colour Practices

- **Never rely on red vs green alone** to encode a positive/negative distinction. Always add a second redundant channel: an arrow symbol (▲/▼), a ± sign, or luminance contrast. This is the "redundant coding" principle.
- **Use luminance as the primary differentiator,** not hue. The luminance channel is intact in all colour-blind conditions. A dark navy vs light yellow is distinguishable by everyone. Red vs green of equal luminance is not.
- **Okabe-Ito palette** (Masataka Okabe & Kei Ito, 2002) and **ColorBrewer** palettes are validated as colour-blind safe. For categorical data, use these before constructing custom palettes.
- **Avoid using the full spectral rainbow** (ROYGBIV) for sequential data. Rainbow palettes create artificial perceptual boundaries at wavelength transitions (cyan, yellow) that do not correspond to data boundaries. Use perceptually uniform sequential palettes (viridis, cividis, or ColorBrewer sequential).

### 5.4 Palette Selection Rules (Brewer / ColorBrewer)

| Data type | Palette type | Example |
|-----------|-------------|---------|
| Ordered, one direction (0 → high) | Sequential | Light-to-dark single hue, or YlGnBu |
| Ordered, two directions from a critical midpoint | Diverging | RdBu, RdYlGn (but check colour-blind safety) |
| Nominal / categorical | Qualitative | Set2, Okabe-Ito |

**Selection rules:**
- Use diverging palettes only when a meaningful midpoint exists in the data (zero, target, mean). Do not apply a diverging palette to data that has no meaningful midpoint — it implies a structure that is not there.
- For sequential data with a natural zero, use palettes that start at near-white (low intensity signals zero or absence) and end at full saturation.
- Do not use more than 8–10 distinct hues in a categorical palette. Beyond 10, hue discrimination fails.

### 5.5 WCAG 2.2 Contrast Requirements

W3C WCAG 2.2 (2023) specifies minimum contrast ratios for accessibility (Level AA):

| Element | Minimum contrast ratio |
|---------|----------------------|
| Normal text (< 18pt or < 14pt bold) | 4.5:1 |
| Large text (≥ 18pt or ≥ 14pt bold) | 3:1 |
| UI components, graphical objects, chart elements required for understanding | 3:1 |
| Decorative elements, logotypes | No requirement |

**Practical thresholds:**
- White background (#FFFFFF): text must be ≤ #767676 (mid-grey) to meet 4.5:1
- Light grey text (#AAAAAA) on white: ratio ≈ 2.3:1 — **fails** WCAG AA — do not use for axis labels, legends, or data values
- The common "muted grey" label (#999999 on #FFFFFF) achieves only 2.85:1 — fails for normal text, passes only for large titles

**Chart-specific note:** Axis tick labels, legend text, and value annotations are "required to understand content" and thus require at minimum 3:1 (as graphical objects), and practically 4.5:1 because they are typically rendered at small sizes (10–12px).

---

## 6. Working Memory Limits

### 6.1 The 4±1 Constraint

Cowan (2001) reviewed evidence from multiple experimental paradigms and concluded that the fundamental limit of visual working memory is approximately **4 independent chunks**, not Miller's 7±2. The 7-item figure conflates chunked information (where the brain compresses familiar patterns) with atomic items.

For data visualisation, the relevant constraint is the number of **simultaneously held visual associations** — the number of legend items a viewer can track at once while interpreting a chart. This is approximately 4.

### 6.2 Applied Limits by Chart Element

| Element | Recommended maximum | Basis |
|---------|-------------------|-------|
| Line chart series | 4 | Cowan's 4-chunk visual WM limit |
| Grouped bar chart groups | 5–6 | Position encoding reduces WM demand |
| Legend items without direct labels | 4 | Beyond this, serial lookup is required |
| KPI cards in one row | 5–6 | Gestalt row grouping helps, but beyond 6 the row is not scannable pre-attentively |
| Simultaneous filters | 3–4 | Each active filter occupies a working memory slot |
| Dashboard panels in one viewport | 6–7 | Beyond this, the eye has no natural entry point (see §4.1) |
| Pie/donut slices | 5–6 | Angle encoding; beyond 6, slices are not rankable |

### 6.3 The Chunking Exception

Expert users who have worked with the same dashboard repeatedly develop schemas (mental chunks) that allow them to process familiar configurations more efficiently. A senior analyst reading a familiar fiscal dashboard is not constrained by 4 items in the same way a first-time viewer is. Design for first-time viewers in the layout and primary encoding; expert users will adapt.

---

## 7. Change Blindness and Attention

### 7.1 What Change Blindness Is

Change blindness (Rensink et al., 1997; Simons & Levin, 1998) is the failure to detect a change in a visual scene when that change is not accompanied by a local visual transient (a sudden onset, motion, or luminance flash at the location of change). In the classic mudsplash paradigm, scattered high-contrast distractors appearing simultaneously with a change prevent detection of that change even when the change is objectively large.

**The fundamental finding:** detection of change requires focal attention at the location of change. Without either a bottom-up attentional capture cue (motion, high contrast, sudden onset) or a top-down intention to look at that location, changes can be large and completely missed.

### 7.2 Implications for Dashboard Design

- **Changes in data values between states will be missed** unless the dashboard actively signals them. A KPI value that updates from 3.2% to 2.8% between page loads will not be noticed unless the change is highlighted (colour, delta indicator, animation on load).
- **Comparison across separate charts requires active attentional effort.** The viewer cannot pre-attentively compare a value in the top-left chart to a value in the bottom-right chart. Design to reduce the spatial distance between related values that need comparison.
- **Inattentional blindness** (Simons & Chabris, 1999) is related: viewers focused on a specific chart or metric will fail to notice an unexpected anomaly elsewhere on the page, even if it is visually prominent. Critical alerts require proactive placement in the viewer's expected focal zone (top-left, above fold).

### 7.3 What Draws the Eye: Attentional Capture

Bottom-up attentional capture — automatic, pre-attentive — is driven by:
1. **Sudden onset / motion** — anything that was not there before, or that moves. The strongest attentional cue.
2. **High luminance contrast** — a dark mark on a light background, or vice versa. A bold number draws the eye relative to regular-weight numbers.
3. **Chromatic salience** — a single red or orange element among grey or blue elements will capture attention even in peripheral vision. This is the basis for semantic highlight colours (red for an alert KPI).
4. **Size anomaly** — a mark or number significantly larger than surrounding elements.
5. **Shape singleton** — a different shape (e.g., a diamond marker among circles) among otherwise homogeneous elements.

**Dashboard design rules derived from attentional capture:**
- Use attentional capture cues intentionally and sparingly. Every high-contrast or colour-salient element sends a signal: "look here first." If everything uses high contrast, nothing is highlighted — the signal cancels itself out.
- Semantic colour: reserve red for genuinely negative or alert states. Use it in at most 1–2 places per dashboard. If 8 KPIs are all red, the viewer habituates and stops treating red as an alert.
- Trend arrows (▲/▼) exploit the shape singleton effect. A ▲ in a KPI card captures attention and communicates direction pre-attentively, before the viewer reads the numeric value. Use them consistently.

---

## 8. Applied Rules for Dashboard Screenshot Review

These rules are derived directly from the perception science above. Each cites the principle it enforces. Format: `RULE [SEVERITY] — condition → why it fails perceptually`.

### HIGH — Communicates Incorrectly (BLOCK)

**RULE H1** — A positive delta (value improved vs prior period) is shown in red, OR a negative delta is shown in green → Violates semantic colour convention built on attentional capture and change blindness signalling. The viewer's pre-attentive system reads red as alert/danger; showing a positive value in red generates a false alarm that cannot be overridden by reading the text. (Sources: §7.3 attentional capture; §5 colour semantics.)

**RULE H2** — Any chart area is blank, shows a Plotly placeholder, renders an error message, or displays no data when data is expected → The viewer cannot distinguish intentional absence from a broken render. A blank figure area is perceived as a failed graphic — the viewer's information need goes unmet. (Source: general rendering integrity; §3.2 extraneous load.)

**RULE H3** — The y-axis of a bar or column chart does not start at zero → Truncated baseline distorts the pre-attentive length encoding. Bar length is the data signal (§1.2); a bar chart with a truncated axis encodes a different ratio than the data. Viewers perceive a 3:1 visual ratio when the data ratio is 1.05:1. Acceptable only for line charts showing trends (where slope, not absolute length, is the encoding). (Sources: §1.3 pre-attentive length encoding; Cleveland & McGill 1984.)

**RULE H4** — Two or more charts on the same page use different colours to represent the same named entity (e.g., Poland is blue in chart A and orange in chart B) → Violates the Law of Similarity (§2.1). The viewer builds a colour-concept association from the first chart; the second chart breaks it, forcing serial legend lookups and creating false categorical distinctions.

**RULE H5** — Text is rendered in a colour that fails WCAG 2.2 AA contrast (< 4.5:1 for small text, < 3:1 for large text or graphical marks) → Fails contrast threshold; users with low vision, users in bright ambient light, and users on low-quality displays cannot read it. Axis tick labels at #999999 on #FFFFFF achieve only 2.85:1 — **fails**. (Source: §5.5 WCAG 2.2.)

**RULE H6** — A critical label, chart title, axis label, or KPI value is truncated mid-word by the container boundary → Truncation converts a meaningful label into an ambiguous or meaningless fragment. The closure law (§2.1) does not apply to text truncation — the viewer cannot complete the missing word. The information is simply absent.

**RULE H7** — A 3D chart type (3D bar, 3D pie, 3D area) is used → 3D depth encoding creates perceptual distortion in position and length estimation (§3.2). Bars at the back of a 3D cluster appear shorter than identical-value bars at the front. The visual system interprets depth cues as real spatial information, creating systematic errors in magnitude reading. No data type requires 3D. (Sources: §3.2 chartjunk; §1.2 position encoding.)

**RULE H8** — Red and green are the sole differentiators between two data series or states, with no luminance difference or shape redundancy → Unreadable for the ~8% of European male users with red-green colour blindness (§5.2). The opponent L–M channel that differentiates red and green is absent; the two colours appear identical. (Source: §5.1–5.3.)

### MEDIUM — Suboptimal (FLAG, DO NOT BLOCK)

**RULE M1** — The most important KPI or headline chart is not located in the top-left quadrant of the visible viewport → Violates the Gutenberg primary optical area and F-pattern starting zone (§4.2–4.3). The viewer's first fixation is top-left; placing the key metric anywhere else requires active redirection of attention that many viewers will not perform.

**RULE M2** — More than 4 series are present on a single line chart → Exceeds Cowan's 4-chunk visual working memory limit (§6.1). The viewer cannot simultaneously hold 5 colour-series associations while tracking lines across the chart. At 5+ series, viewers begin confusing lines and must serial-scan the legend after each comparison. (Source: §6.2.)

**RULE M3** — A pie or donut chart has more than 6 slices → Angle and area are among the weakest quantitative encodings (Cleveland & McGill; §1.2). Beyond 6 slices, the viewer cannot rank them perceptually — they appear approximately equal. Any ranking task requires reading numeric labels, defeating the purpose of a chart over a table.

**RULE M4** — More than 7 distinct chart or KPI panels are visible in a single viewport without clear visual grouping → Exceeds the pre-attentive grouping capacity for unstructured layouts (§6.2). The eye has no natural entry point; the viewer scans randomly and misses elements. Gestalt enclosure or spacing must group elements into 3–4 clusters at maximum.

**RULE M5** — Gridlines are darker, bolder, or more visually prominent than the data marks they support → Figure/ground inversion (§2.1, Law of Figure/Ground). The grid becomes the figure; data becomes ground. The viewer must mentally suppress the dominant visual element to read the data. Gridlines should be at minimum 50% lower luminance contrast than the data marks.

**RULE M6** — A legend is present for a single-series chart → Extraneous load with zero information value (§3.2). A single-series legend requires the viewer to process a label that is already in the title or axis. Remove it. (Source: §3.1 extraneous load.)

**RULE M7** — A multi-series chart has a right-side legend with 5+ entries and no direct labels on the data series → Forces serial lookup for each comparison (§2.2, §6.2). For every series identification, the viewer must: locate the legend, match the colour, return to the chart, locate the series. Direct labelling eliminates three of these four steps. (Source: §2.2 legend placement.)

**RULE M8** — Axis labels read "value", "y", "index", or are absent on a visible axis → The axis encodes nothing without a label. The viewer cannot determine units, scale, or what is being measured. This is an intrinsic information deficit, not merely cosmetic. (Source: general; §1.2 position is the primary quantitative channel — the axis label is the key to reading that channel.)

**RULE M9** — KPI delta colours are used but no ▲/▼ or ± symbol accompanies them → Colour alone fails colour-blind users (§5.2–5.3). The symbol provides redundant encoding that makes the direction legible in all colour vision modes. (Source: §5.3 redundant coding principle.)

**RULE M10** — A sequential colour palette (single hue progression) is used for categorical data, or a categorical palette is used for ordered data → Palette type mismatch. Sequential palettes imply order (§5.4); applying them to nominal categories implies a ranking or ordering in the data that does not exist. Categorical palettes imply equivalence; applying them to ordered data (e.g. a year range) makes ordering unreadable. (Source: §5.4 palette selection rules.)

**RULE M11** — A diverging palette is applied to data without a meaningful midpoint → Implies a critical threshold at the palette midpoint (usually a neutral light colour) where none exists. Viewers will interpret the midpoint as meaningful (e.g. the mean, zero, a policy target) even if it is arbitrary. (Source: §5.4 palette selection rules.)

**RULE M12** — The most important visual element (headline chart, primary KPI) is below the visible fold on a standard 1440×900 viewport → Receives a fraction of total viewing time. NNGroup research: 80% of viewing time above the fold. Placing the primary finding below it means most viewers never see it. (Source: §4.3.)

**RULE M13** — A rainbow (ROYGBIV) sequential palette is used for ordered or continuous data → Creates perceptual false boundaries at wavelength transitions. Viewers see discrete bands (green-to-yellow transition, cyan band) that correspond to wavelength physics, not data values. The palette is also not perceptually uniform — equal steps in data are not perceived as equal steps in colour. Use viridis or a single-hue sequential palette. (Source: §5.3.)

**RULE M14** — Border boxes are drawn around every individual chart panel with equal visual weight as the data marks → Violates figure/ground (§2.1) and increases extraneous load (§3.2). Enclosure should be used to group related panels; heavy borders on every individual panel create visual noise without structural information. Use whitespace for containment where possible (Law of Closure, §2.1).

### LOW — Best Practice (SUGGEST)

**RULE L1** — A chart has a title but no subtitle stating the period, geography, and unit → The viewer must infer context. Subtitle is not required if the title is fully self-explanatory (includes period and unit), but most chart titles are not. Missing context forces working memory to hold assumptions rather than data. (Source: §3.1 germane load.)

**RULE L2** — No data source attribution is visible on a page with data → Violates Cairo's truthfulness principle. Source attribution is the minimum provenance signal. (Source: §8 truthfulness; Cairo, *The Truthful Art*.)

**RULE L3** — KPI cards on the same dashboard show inconsistent decimal precision (some 1 dp, some 0 dp, some 2 dp) without a principled reason → Creates apparent precision differences that imply different data quality or measurement approaches. The viewer will interpret inconsistency as meaningful. (Source: §3.2 extraneous load — inconsistency generates resolution effort.)

**RULE L4** — Value annotations are placed directly on top of bars or chart elements, reducing legibility → Added marks (§1.2 form attributes) compete with the mark they annotate. Labels should be placed above bars or outside chart elements, with sufficient contrast. If the bar is too short to receive a top label, use a callout line.

**RULE L5** — A chart uses more than 3 typeface weights or sizes without a clear typographic hierarchy → Typographic noise. More than 3 distinct type treatments (title / label / annotation) generates visual hierarchy uncertainty — the viewer cannot determine which text level is most important. (Source: §3.2 extraneous load.)

**RULE L6** — No visual grouping (Gestalt enclosure or whitespace) separates thematically distinct sections of the dashboard → Viewer cannot determine which panels belong together (§2.1, proximity and enclosure). The absence of grouping implies all panels are equally related, which is rarely true.

**RULE L7** — Trend arrows (▲/▼) are present but are the same colour as the base KPI value → The arrow is a shape singleton that draws attention (§7.3), but if it is the same colour as the base value, the directional signal is weakened. Arrows should carry the semantic colour (green/red, or with redundant symbol) to maximise the pre-attentive signal.

---

## 9. Summary Reference Table

Quick lookup for design decisions:

| Decision | Principle | Rule |
|----------|-----------|------|
| How many line series? | Cowan 4-chunk WM | Max 4 |
| How many pie slices? | Angle encoding weakness | Max 6 |
| Where to put headline KPI? | Gutenberg primary area | Top-left |
| Red=bad, green=good? | Opponent process; colour-blind | + symbol or luminance redundancy required |
| Dark label on grey background? | WCAG 2.2 | Must achieve ≥ 4.5:1 |
| 3D chart acceptable? | Figure/ground; extraneous load | Never |
| How many distinct hues? | Pre-attentive hue limit | Max 8–10 |
| Legend or direct labels? | Gestalt proximity; WM limit | Direct labels up to 6 series |
| Sequential palette for categories? | Brewer palette rules | Never |
| What makes a finding visible? | Attentional capture | Colour singleton, size anomaly, motion |

---

*This KB provides the scientific grounding for `team/standards/evaluation/visualization-image.md` and `team/standards/build/visualisation.md`. When those standards are updated, trace each rule to the section(s) above that justify it.*

---

Here is the complete file content. Key things to note about what was produced:

**Structure matches the existing KB format** — agent-reference header, sourced, sectioned with numbered headings and tables.

**Research basis:**
- Treisman's Feature Integration Theory grounds the pre-attentive attribute list and the pop-out search criterion
- Ware's four-channel taxonomy (colour, form, position, motion) with the Cleveland & McGill accuracy ranking
- Sweller's three-load types with a concrete chartjunk taxonomy showing the *mechanism* of each element's cost
- Cowan (2001) is used — not Miller — for the 4-chunk visual WM limit; Miller's 7 is explicitly corrected
- Opponent-process neuroscience (LGN channels) explains *why* red-green is the colour blindness failure mode, not just stating the statistic
- Nielsen Norman F-pattern updated to include the 2017 follow-up distinguishing spotted/layer-cake/commitment patterns
- Gutenberg diagram four zones with directional dashboard placement guidance
- WCAG 2.2 ratios with actual hex values showing what fails in practice (#999999 on white = 2.85:1)

**27 numbered evaluation rules** (8 HIGH, 14 MEDIUM, 7 LOW) each citing the specific section that justifies them — directly usable by the `visual-design-reviewer` agent and compatible with the existing severity schema in `visualization-image.md`.