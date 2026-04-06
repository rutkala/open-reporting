# Principles

A comprehensive knowledge base for building effective data visualizations and dashboards, grounded in international standards (IBCS, ISO) and established best practices.

---

## 1. Foundational Principles

### Clarity Over Complexity

Every element on a visualization must have a clear purpose. If a user asks "What am I looking at?", the design has failed. The best dashboards make complex data simple, not the other way around.

**Key practices:**
- Remove any element that does not serve a communication purpose
- Every chart, label, and decoration should earn its place
- When in doubt, remove it

### The 5-Second Test

Users should grasp key insights in under 5 seconds. Comprehensive detail matters less than fast comprehension for primary metrics.

**Application:**
- Show the dashboard to someone unfamiliar with it for 5 seconds, then hide it
- Ask: "What were the key metrics? What's the status?"
- If they cannot answer, simplify

### Data-to-Ink Ratio

Edward Tufte's principle states that a large share of pixels should be dedicated to presenting data itself, not extraneous decorative elements. "Chart junk" — unnecessary gridlines, borders, 3D effects, background shading — distracts from core insights.

**Application:**
- Remove chart borders, heavy gridlines, background colors
- Use thin, light gray gridlines only when necessary for context
- Avoid 3D effects, shadows, and unnecessary patterns

### Action Over Information

Data without action is noise. Effective visualizations guide users to decisions and next steps, not just present numbers. The goal is to help users make informed choices, not just consume data.

---

## 2. IBCS SUCCESS Framework

The International Business Communication Standards (IBCS) provide a rigorous framework for business reporting. The SUCCESS formula consists of seven areas that ensure consistent, effective communication.

### SAY — Convey a Message

Every visualization should communicate a clear message. Report titles must describe the content and include:

- **Topic** — What is being measured
- **Business unit** — For which area of the organization
- **Unit and scaling** — Currency (EUR, USD), units, scaling (e.g., tEUR for thousands)
- **Time frame and comparison** — Period covered (e.g., "2024"), comparison scenario (e.g., PY for previous year)

**Example:**
- Good: "Q3 2024 Sales — Europe — EUR millions — vs. PY"
- Poor: "Sales Data"

Avoid redundancy: If the page title says "Sales Report," individual chart titles should not repeat "Sales."

### UNIFY — Apply Consistent Notation

Use consistent notation throughout all reports and dashboards. This includes:

- **Terminology** — Use the same terms for the same concepts across all visualizations
- **Color coding** — Assign the same colors to the same data types (e.g., actuals always dark grey)
- **Symbols** — Use consistent symbols for the same elements (e.g., hatched patterns for forecasts)
- **Layout** — Apply the same structural patterns across all pages

### CONDENSE — Increase Information Density

Present more relevant information in less space without sacrificing clarity. Effective dashboards pack meaningful data densely while remaining scannable.

**Techniques:**
- Use sparklines for trend context in KPI cards
- Combine multiple metrics in a single chart (small multiples)
- Stack related charts vertically with shared axes
- Eliminate excessive whitespace between related elements

### CHECK — Ensure Visual Integrity

Verify that visualizations accurately represent the data. Common integrity issues:

- **Truncated axes** — Bar charts must start at zero to show proportional values correctly
- **Inconsistent scales** — When comparing multiple charts, use consistent scales
- **Misleading proportions** — Avoid 3D effects that distort size relationships
- **Cherry-picking time ranges** — Select time ranges that don't mislead about trends

### EXPRESS — Choose Proper Visualization

Select the chart type that best represents the data structure:

| Data Structure | Recommended Charts |
|----------------|--------------------|
| Trends over time | Line chart |
| Categorical comparison | Bar chart (horizontal for long labels) |
| Part-to-whole (few categories) | Donut chart |
| Part-to-whole (many categories) | Treemap |
| Progress vs. target | Progress bar, gauge |
| Correlation | Scatter plot |
| Distribution | Histogram |

Avoid pie charts with more than 6 slices — they become unreadable.

### SIMPLIFY — Avoid Clutter

Remove unnecessary elements that do not contribute to understanding:

- Remove redundant axis labels
- Eliminate decorative borders and backgrounds
- Use direct labeling instead of legends when possible
- Remove gridlines unless specifically needed for precise reading

### STRUCTURE — Organize Content

Apply logical hierarchy and consistent structure:

- Use a grid system (12 or 16 columns) for alignment
- Place most important metrics at top-left (F-pattern reading)
- Group related elements together
- Maintain consistent visual hierarchy throughout

---

## 3. IBCS Color Coding Rules

IBCS defines specific color conventions for business data:

| Data Type | Color | Notes |
|-----------|-------|-------|
| Current/actual | Dark grey | Primary data being reported |
| Previous period | Light grey | Comparison baseline |
| Forecast | Diagonally hatched | Projected future values |
| Budget/planned | White with black border | Target or planned values |
| Positive deviation | Green | Favorable variance |
| Negative deviation | Red | Unfavorable variance |
| Neutral deviation | Middle grey | When deviation is neither good nor bad (e.g., ±3%) |
| Highlighted items | Blue | Draw attention to specific data |

For category differentiation (not semantic), use a colorblind-safe palette of 4-6 distinct colors. Ensure all colors pass WCAG AA contrast standards (4.5:1 for text, 3:1 for UI components).

---

## 4. Perception and Cognitive Science

### Gestalt Principles

The Gestalt principles describe how humans perceive visual elements as organized patterns:

| Principle | Definition | Application |
|-----------|------------|-------------|
| **Proximity** | Things close together are perceived as a group | Group related metrics together; place filters close to the charts they affect |
| **Similarity** | Identical things (color, shape, size) are perceived as a group | Use consistent colors for categories across all charts |
| **Connectedness** | Objects linked by visual elements are perceived as a group | Use lines connecting points in line charts; apply row banding to tables |
| **Continuity** | Elements following a similar path are perceived as a group | Align elements to create visual flow; use consistent spacing |
| **Closure** | Things inside a boundary are perceived as a group | Use containers/cards to group related content |
| **Common Fate** | Elements moving in the same direction are perceived as a group | Use diverging bar charts for opposite metrics (profit/loss) |
| **Figure-ground** | One aspect perceived as figure, others as background | Emphasize data as figure; keep background minimal |
| **Pragnanz** | The brain prefers simple, orderly experiences | Keep designs clean and uncomplicated; remove complexity that doesn't add value |

### Preattentive Attributes

Preattentive processing allows the brain to detect certain visual properties in milliseconds, before conscious attention kicks in. Use these attributes to direct attention:

- **Color** — Most effective for immediate detection
- **Size** — Larger elements attract attention
- **Shape** — Distinct shapes stand out
- **Position** — Elements in unusual positions draw attention

**Application:**
- Use a distinct color to highlight a single data point
- Size encoding for magnitude (larger bubbles = larger values)
- Shape differentiation for categorical data (if tool supports)

### Reading Patterns

Eye-tracking studies show users scan dashboards in an F-pattern: top to bottom, left to right, with decreasing attention as they move down and right.

**Apply this principle:**
- **Top-left:** Most critical KPI or status indicator
- **Top-row:** Primary metrics (3-5 key numbers)
- **Middle section:** Trend charts and time-series data
- **Bottom section:** Detailed breakdowns and tables

---

## 5. Chart Type Selection

### For Trends Over Time

**Line chart** — Best for continuous time series. Use thick lines (2-3px minimum) for legibility. Limit to 2-3 lines per chart to avoid clutter. Include key event markers (product launches, campaigns).

### For Categorical Comparison

**Bar chart** — Best for comparing discrete categories. Sort by value (descending) unless order matters. Use horizontal bars for long category names. Include data labels for precise values.

**Avoid:** Using line charts for categorical data — users will incorrectly assume connectedness between categories.

### For Part-to-Whole

**Donut chart** — Best for 3-5 categories. Use for simple static breakdowns. Include data labels directly on slices.

**Treemap** — Best for many categories with hierarchical structure. Size represents proportion; color can encode a second dimension.

**Stacked bar (100%)** — Best for comparing compositions across multiple groups over time.

**Avoid:** Pie charts with more than 6 slices.

### For Progress and Targets

**Progress bar** — Best for linear progress (0-100%). Use for project completion, quota attainment.

**Gauge/meter** — Best for performance within a range. Use for server utilization, customer satisfaction scores. Include color-coded zones (green/yellow/red).

### For Correlation/Relationship

**Scatter plot** — Best for showing relationship between two continuous variables. Use for correlation analysis, outlier detection.

### For Distribution

**Histogram** — Best for frequency distribution of continuous data.

**Box plot** — Best for showing distribution summary (median, quartiles, outliers) across categories.

---

## 6. Analysis Scenarios and Chart Selection

This section maps analytical questions to chart types. The key principle: **the chart must make the relationship or comparison visually obvious**.

### 6.1 Comparison Analysis

**Question:** "How do values compare across categories or time?"

| Scenario | Best Chart | Why |
|----------|------------|-----|
| Compare values across 2-5 categories at one point in time | Grouped bar chart (vertical) | Easy to compare heights |
| Compare values across 5+ categories at one point in time | Horizontal bar chart | Labels readable, easy to rank |
| Compare one category across multiple time periods | Line chart | Shows trend, connected |
| Compare multiple categories across multiple time periods | Multi-line chart | Show relative trajectories |
| Compare values to a target/benchmark | Bar with reference line | Target is immediately visible |

### 6.2 Composition Analysis

**Question:** "What are the parts that make up the whole?"

| Scenario | Best Chart | Why |
|----------|------------|-----|
| Show simple breakdown (2-5 parts) | Donut chart | Parts visually distinct |
| Show breakdown with many parts | Treemap | Hierarchical, space-efficient |
| Show how composition changes over time | Stacked bar (100%) | Compare segments across time |
| Show contribution to total | Waterfall chart | Shows positive/negative contributions |
| Show absolute totals with composition | Stacked bar (absolute) | Both total and parts visible |

### 6.3 Relationship Analysis

**Question:** "How do two variables relate to each other?"

| Scenario | Best Chart | Why |
|----------|------------|-----|
| Show correlation between two continuous variables | Scatter plot | Each point = one observation |
| Show relationship over time | Dual-axis line chart | Two trends on same time scale |
| Show causal flow | Sankey diagram | Shows source to destination flow |

### 6.4 Financial/Budget Analysis

Specialized patterns for financial data (P&L, budgets, fiscal):

| Scenario | Best Chart | IBCS Convention |
|----------|------------|-----------------|
| Revenue vs Expenditure over time | Grouped bars | Dark grey (actuals), light grey (comparision) |
| Balance trajectory | Line or column chart | Show negative values clearly |
| Revenue → Expenditure → Balance flow | Waterfall | Shows contribution of each component |
| Variance from budget | Column with reference line | Red/green for deviation |
| Actual vs Plan | Side-by-side columns | Solid (actual), outlined (plan) |
| Forecast visualization | Hatched pattern | Distinguish from actuals |

**IBCS Key Principles for Financial Charts:**
- Use consistent visual notation: solid = actual, hatched = forecast, outlined = plan
- Red/Green for negative/positive deviations
- Always show zero clearly for balance/deficit
- Reference lines for thresholds (budget, SGP, targets)

**Caution:** Avoid dual-axis unless variables have a direct, meaningful relationship. Better to use two separate charts if no strong correlation exists.

### 6.5 Distribution Analysis

**Question:** "How is data spread or distributed?"

| Scenario | Best Chart | Why |
|----------|------------|-----|
| Show frequency of continuous data | Histogram | Reveals shape of distribution |
| Compare distributions across categories | Box plot | Shows median, quartiles, outliers |
| Show all individual values | Strip plot / jitter | Shows every data point |
| Show population by geography | Choropleth map | Geographic pattern |

### 6.6 Trend Analysis

**Question:** "How has something changed over time?"

| Scenario | Best Chart | Why |
|----------|------------|-----|
| Show continuous change over time | Line chart | Connected, shows trajectory |
| Show discrete changes at specific points | Column chart | Clear at each point |
| Show accelerating/decelerating trends | Area chart | Emphasizes volume under line |
| Show change between two time periods | Diverging bar | Shows gain/loss direction |

### 6.7 Deviation Analysis

**Question:** "How far from expected/target?"

| Scenario | Best Chart | Why |
|----------|------------|-----|
| Show deviation from zero (positive/negative) | Diverging bar | Direction immediately visible |
| Show deviation from target | Bar with reference line | Gap to target obvious |
| Show deviation over time | Line with reference line | Trend relative to benchmark |
| Show variance between periods | Waterfall | Shows step-by-step changes |

### 6.8 Ranking Analysis

**Question:** "Which is highest/lowest?"

| Scenario | Best Chart | Why |
|----------|------------|-----|
| Rank categories by single measure | Horizontal bar chart (sorted) | Natural reading order = ranking |
| Rank across multiple measures | Table with sparklines | Multiple metrics visible |
| Rank over time | Slope chart | Shows position change |

---

## 7. Chart Combination Rules

Multiple charts can be combined, but only when the relationships between them are visually and logically clear.

### Valid Combinations

| Combination | When Appropriate |
|-------------|------------------|
| Main chart + reference line | Benchmark/threshold clearly related to main data |
| Grouped bars + line overlay | Line shows secondary metric on same scale |
| Bar + sparkline in tooltip | Detail available on demand, not cluttering main view |
| Multiple small multiples | Same chart type, different categories (e.g., line for each region) |

### Invalid Combinations

| Combination | Why Not |
|-------------|---------|
| Bar + unrelated line on dual-axis | Different scales confuse comparison |
| Too many series (5+ lines) | Visual clutter, hard to distinguish |
| Stacked bars + line on same axis | Scales incompatible |
| Pie + line | No spatial relationship between them |

### Multi-Panel Charts (Subplots) — General Rule

**When to use:** You have multiple metrics that need to be shown together, but they have **different scales** (different ranges, different units).

**The rule:** Use **stacked subplots** with shared x-axis instead of dual-axis.

| Scenario | Solution | Why |
|----------|----------|-----|
| Two metrics, different scales | Two stacked panels | Each panel has own scale, aligned for comparison |
| Three metrics with different scales | Three stacked panels | Avoid mixing incompatible scales |
| Main metric + secondary metric | Panel above + panel below | Primary gets prominence, secondary supports |
| Multiple categories, same scale | Single panel with grouped bars | Can share axis when scales match |

**Decision tree:**
1. **Are scales compatible?** (same units, similar range) → Single panel
2. **Are scales different?** → Use stacked subplots
3. **Do they share time/category?** → Share x-axis for alignment
4. **Is there a primary metric?** → Put it on top

---

## 8. Dashboard Layout Patterns

### Before designing any visualization:
1. Research the domain — understand how experts in that field analyze data
2. Identify the analytical question — what is the user trying to answer?
3. Determine the analysis type — comparison, composition, trend, relationship, etc.
4. Apply chart selection rules — match analysis type to appropriate chart
5. Check scale compatibility — if different, use subplots not dual-axis
6. Validate against domain conventions — use domain-specific patterns if they exist

### Grid System

Professional dashboards use consistent grid systems — typically 12 or 16 columns. This creates visual rhythm and makes layout decisions systematic.

**Benefits:**
- Visual consistency across sections
- Easier responsive adaptation
- Professional, polished appearance
- Faster design iteration

### Dashboard Types

#### Executive Dashboard

**Purpose:** High-level overview for decision-makers

**Structure:**
- Row 1: 4-5 key metrics in prominent cards
- Row 2: 2-3 trend charts (revenue, users, conversions)
- Row 3: 2 comparison charts (products, regions, channels)
- Row 4: Detailed table (top opportunities or risks)

**Design emphasis:** Clarity, high-level trends, no clutter

#### Operational Dashboard

**Purpose:** Real-time monitoring and alerts

**Structure:**
- Top banner: Critical alerts and system status
- Left column: Real-time metrics with thresholds
- Center: Time-series charts (last hour, last day)
- Right column: Recent events log

**Design emphasis:** Immediate status recognition, prominent alerts

#### Analytical Dashboard

**Purpose:** Deep exploration for analysts

**Structure:**
- Top: Filter controls and date range selector
- Upper section: Summary metrics
- Middle section: Multiple detailed charts (4-6)
- Bottom section: Data tables with export options

**Design emphasis:** Flexibility, drill-down capability, data density

---

## 9. UX and Interaction Design

### User-Centered Design

Design with the audience in mind. Consider:

- Who is the target audience?
- What decisions will they make based on this data?
- What problems are they trying to solve?
- What is their level of expertise?

### Essential Interactions

- **Hover tooltips:** Show precise values without cluttering charts
- **Click-to-filter:** Click a chart element to filter entire dashboard
- **Drill-down:** Click a summary metric to see details
- **Date range picker:** Adjust time period

### Avoid

- Requiring interaction to see basic information
- Animations that delay information display
- Hover-dependent features without keyboard alternatives

### Loading and Empty States

**Loading states:**
- Show skeleton screens immediately
- Load above-the-fold content first
- Display stale data with "updating..." indicator

**Empty states:**
- Explain why it's empty ("No data for selected date range")
- Provide actionable next steps ("Adjust filters" or "Import data")

---

## 10. Accessibility

### Principles from ISO 9241-125

- Design for users with varying abilities
- Provide multiple ways to access information
- Do not rely on a single sensory channel

### WCAG AA Compliance

- **Text contrast:** 4.5:1 minimum for normal text, 3:1 for large text
- **UI components:** 3:1 minimum for graphical elements
- **Font size:** 14px minimum, 16px preferred

### Color

- Never rely on color alone to convey information
- Use patterns, textures, or shapes in addition to color
- Test with color blindness simulators

### Alternative Access

- Provide data tables as alternatives to charts
- Include descriptive alt-text for charts
- Ensure keyboard navigation for all interactive elements

---

## 11. Data Integrity and Ethics

### Always Start at Zero

Bar charts must start at zero to show proportional values correctly. Truncated axes mislead viewers about actual differences.

### Avoid 3D Effects

3D effects distort perception and add no informational value. Always use 2D visualizations.

### Dual-Axis Charts

Use with extreme caution. Only compare variables with a direct, meaningful relationship. Label each axis clearly to prevent misinterpretation.

### Provide Context

Always provide comparison context:
- vs. last period (e.g., "vs. Q3 2023")
- vs. target (e.g., "85% of goal")
- vs. same period last year

A number alone means nothing. "1,247 signups" is meaningless without context — is that good? Bad? Improving?

---

## 12. Testing and Iteration

### Visual Evaluation Checklist

Before finalizing any chart, evaluate it against these criteria:

1. **Simplicity test** — Can the key insight be described in one sentence?
2. **5-second test** — Can users grasp the main message in 5 seconds?
3. **Cognitive load** — Is there visual noise that distracts from the story?
4. **Relationship visibility** — Are the data relationships visually obvious?
5. **No-chart test** — If you covered the chart and described what it shows, would it match what the chart actually communicates?

### Common Evaluation Issues

| Issue | Symptom | Fix |
|-------|---------|-----|
| Too much data | 20+ bars/points cluster together | Show only recent years, or aggregate |
| Dual-axis confusion | Two different scales compete for attention | Use single scale, or separate charts |
| Buried insight | Key message requires explanation | Emphasize the insight, simplify around it |
| Unclear relationship | A and B shown separately without connection | Use visual linking (stacked, connected) |
| No context | Numbers shown without comparison | Add reference lines, benchmarks, previous period |

### Design Checklist

- [ ] Key insights graspable in under 5 seconds
- [ ] Most important metrics in top-left position
- [ ] No more than 7 primary metrics visible
- [ ] All metrics have comparison context
- [ ] Consistent grid alignment throughout
- [ ] Colorblind-safe palette used
- [ ] Charts have appropriate types for data
- [ ] No chart has more than 3-4 data series
- [ ] All text is 14px or larger
- [ ] Loading states implemented
- [ ] Empty states handled gracefully
- [ ] Responsive on mobile, tablet, desktop
- [ ] Keyboard navigable
- [ ] Last updated timestamps visible

### User Testing

Watch real users interact with your dashboard:

- "What's the most important thing on this screen?"
- "Is [specific metric] improving or declining?"
- "What action would you take based on this data?"
- "Find the top-performing [product/region/campaign]."

If users struggle or hesitate, redesign those elements.

### Iteration Cycle

1. Create low-fidelity prototype
2. Test with target users (5-8 people)
3. Gather qualitative and quantitative feedback
4. Refine design based on findings
5. Repeat until satisfactory

### Performance Budget

- Initial load: < 2 seconds
- Interaction response: < 100ms
- Maximum data points per chart: 1,000

---

## References

### Standards

- **IBCS** — International Business Communication Standards (ibcs.com)
- **ISO 24896** — Notation for business reporting (under development)
- **ISO 9241-125:2017** — Guidance on visual presentation of information
- **ISO 9241-112:2025** — Principles for the presentation of information

### Key Books

- Edward Tufte — "The Visual Display of Quantitative Information"
- Cole Nussbaumer Knaflic — "Storytelling with Data"
- Alberto Cairo — "The Functional Art"

### Tools

- ColorBrewer2.org — Colorblind-safe palettes
- WCAG Contrast Checker — Accessibility validation