# What to consider when choosing colors for data visualization (Datawrapper Academy) — annotation

## What this source teaches

This is the most practically rigorous color selection guide in the reference library. It presents 12 structured rules, each with a "NOT IDEAL / BETTER" paired visual example, covering the full decision space from categorical palettes to sequential gradients to diverging scales. The author (Lisa Charlotte Muth, Datawrapper's primary color writer) treats color as a semantic encoding layer, not a styling layer — every rule is framed around what the reader will infer, not what looks attractive.

## Key patterns documented

- **Seven-color maximum for categorical palettes** — More than seven distinct hues forces readers to consult the legend repeatedly, destroying at-a-glance comprehension. This is a hard constraint: if your data has more than seven categories, restructure the chart, not the palette.

- **Grey as the primary design tool** — The article positions grey as the most important color in data visualization, more important than any accent hue. Grey absorbs non-essential information (context series, reference data, unselected states) so that accent colors can do their signaling work without competition. `![](images/when-to-use-colors.png)`

- **Light = low, dark = high convention** — Sequential gradients should always flow from light (low value) to dark (high value). This is described as the most intuitive convention for readers globally. Violating it (dark = low) will cause systematic misreading.

- **Gradient type must match data type** — Sequential gradients for continuous magnitude data; diverging gradients for deviation-from-baseline data; distinct hues for categorical data. Using sequential shades of blue for categories implies a false ranking.

- **Diverging gradients for deviation** — When the data question is "above or below baseline?", a diverging palette (two contrasting hues meeting at a neutral light grey centre) is the correct tool. The centre should be light grey, not white — white reads as "zero" on maps but "background" everywhere else. `![](images/diverging-color-gradients.png)`

- **Lightness-driven gradients, not hue-driven** — Rainbow/spectrum gradients (high variation in hue, little variation in lightness) confuse readers because perceptual steps are uneven. A single-hue gradient from white to dark blue is more accurately decoded. `![](images/lightness-gradients.png)`

- **Color blindness testing as a mandatory step** — The article shows (with a vivid paired hexbin map) that a red/green palette collapses to near-uniform brown under both deuteranopia and protanopia — the two most common forms of color blindness, affecting ~8% of males. The "BETTER" alternative uses orange/teal, which remains distinguishable under both simulated conditions. `![](images/color-blind-check.png)`

- **Contrast ratio thresholds** — At least 2.5:1 for large text, 4:1 for small text. These are WCAG-derived thresholds applied in a data visualization context.

- **Intuitive colors respect cultural associations** — Party colors, natural colors (forest=green, water=blue), and learned signals (red=stop) should be honoured where they exist. Violating them adds a cognitive layer that costs the reader attention.

## Notable visual examples

**Lightness gradients** (`images/lightness-gradients.png`) — Side-by-side US county choropleth maps. Left ("NOT IDEAL"): a rainbow/heatmap palette with high hue variation, uniform lightness across the entire scale. Right ("BETTER"): a single-hue light-blue-to-dark-blue palette with lightness doing the encoding work. The NOT IDEAL map reads as visually chaotic — counties that are adjacent but close in value appear as different colors; the BETTER map allows spatial pattern reading with a single glance. The paired legend strips at the bottom make the structural difference between the two approaches unmistakable.

**Diverging color gradients** (`images/diverging-color-gradients.png`) — Same county-level US map, same two-panel format. Left: a sequential amber-to-dark-red palette used to show deviation data (which should have a neutral midpoint). Right: a diverging teal-to-neutral-to-rust palette with a clear midpoint. The NOT IDEAL version cannot communicate "above average" vs. "below average" — there is no visual centre. The BETTER version makes the above/below structure immediately legible from the midpoint grey outward.

**Color blindness simulation** (`images/color-blind-check.png`) — A 3×2 grid of hexbin US maps. Left column: red/green categorical palette under normal vision, deuteranopia, and protanopia — all three rows in the left column appear nearly identical brown/olive because both red and green collapse under these conditions. Right column: orange/teal palette — distinctly different across all three vision conditions. This is the most persuasive single visual argument for avoiding red/green categorical pairs.

## Relevance to public-finance dashboards

The diverging gradient rule is directly applicable to regional fiscal data (e.g. voivodeship deficit/surplus per capita where the colour question is "above or below the national average?"). The grey-as-primary-colour principle aligns with the Nordic design approach in the repo's visualization standards — historical series should default to grey, with the current year in the accent colour. The seven-colour maximum constrains any "expenditure by ministry" breakdown: if there are more than seven categories, the chart type should change (e.g. to a ranked bar) rather than extending the palette. The colorblind simulation images provide the clearest case for the repo's existing rule against red/green palette use.
