# Tableau Public Viz of the Day — annotation

## Access status

This source was fully inaccessible during Wave 2 capture (Cloudflare blocking at CDN level, affecting both WebFetch and headless Playwright). This annotation cannot be grounded in captured images.

## What this source would teach (from prior knowledge — weaker rating)

Tableau Public is the largest open gallery of community-created data visualisations. The Viz of the Day programme features one selected viz daily, typically representing creative or technically sophisticated use of Tableau's feature set. Common patterns documented by the Tableau community and third-party curators:

- **Non-standard chart types via calculated fields** — Tableau practitioners routinely build bump charts, slope charts, radial bar charts, waffle charts, and hex tile maps using workarounds involving LOD expressions and transparent sheet stacking. These chart types are not available in the standard library but are achievable and frequently featured.
- **Strong use of custom colour palettes** — Tableau Public vizes typically define full custom colour palettes rather than using Tableau defaults. The most praised vizes are often monochromatic with a single vivid accent, similar to the BBC Cookbook pattern.
- **Scrollytelling with embedded Tableau views** — Some featured vizes use an HTML wrapper with scroll triggers that swap the embedded Tableau sheet — combining the interactivity of Tableau with the narrative pacing of a Pudding-style article.
- **Small multiples for cross-country comparison** — A preferred pattern for competitive/comparative data across many entities is a grid of small identical charts (one per country or team), allowing side-by-side comparison at the cost of detail per panel.

## Relevance to public-finance dashboards

Tableau Public's gallery is primarily useful as a chart-type inspiration source, not a design standards reference — community vizes often prioritise novelty over readability. For the public finance dashboard, the small multiples pattern and the bump/slope chart for ranking evolution (e.g., Poland's deficit rank among EU member states over time) are the most directly applicable patterns from the Tableau community aesthetic.

## Wave 3 recommendation

See `article-text.md` for the specific thumbnail URL pattern that may allow direct image fetch for 3-5 known vizes. Alternatively, capture from The Information Lab's "Data School" blog or the Tableau Ambassador portfolio pages, which link to specific Tableau Public embeds and often include static screenshot images accessible to regular fetchers.
