# Dashboard Design UX Patterns (PencilAndPaper) — annotation

## What this source teaches

This article maps the full user journey through a data dashboard — from navigation and orientation through filtering, drilling, and executing actions — and then zooms into chart-level patterns for colour, labels, deltas, and interaction. Its central thesis is that dashboard quality is determined as much by information architecture and progressive disclosure as by individual chart choices. It is practitioner-oriented (UX design consultancy writing for enterprise software teams) and is notably honest about the difficulty of the work.

## Key patterns documented

- **Hierarchical anatomy: dashboard → section → module → data** — The article makes the structural hierarchy explicit and illustrates it with a three-panel sketch diagram. This is the foundational mental model: a dashboard is a composition of sections, each made of modules, each module made of data elements. `![](images/Anatomy-v2.png)`

- **F/Z scan pattern for layout priority** — Top-left gets the most attention; importance should decrease as you scan right and down. The most global, most actionable numbers belong top-left. Illustrated with a sketch showing three numbered horizontal scan bands narrowing toward the bottom. `![](images/F-Z-Patterns.png)`

- **Consistent card layout** — Charts at every size share a structural grammar: title top-left, date picker top-right, legend bottom-centre. This reduces visual noise even when chart types vary. `![](images/Consistent-in-card-layout.png)`

- **Delta display taxonomy** — Three canonical formats are demonstrated: icon-first (directional arrow + colour + absolute value), textual (natural-language sentence), and inline (compact, embedded in a table row). All three use the same red/yellow/green semantic convention internally. `![](images/Deltas-icons-colours.webp)`

- **Blue/orange instead of red/green for trend polarity** — Encodes positive (blue) and negative (orange) without triggering stoplight semantics and without accessibility issues for deuteranopes. The illustration shows two small area charts, one rising in blue, one falling in orange. `![](images/Blues-Oranges.webp)`

- **Texture and line-style for accessibility** — Recommends adding hash patterns, dot grids, or dashed line variants rather than relying on colour alone to distinguish series. `![](images/Hashes-Textures.webp)`

- **Progressive disclosure via hover/tooltips** — Chart surface communicates trend; precise values appear only on hover. Prevents visual overload while preserving depth.

- **Comparisons and baselines as cognitive anchors** — Data without a reference point (average, target, prior period) is cognitively harder to interpret. Deltas and reference lines are the solution, not decoration.

- **Information density management** — "Data eyeball attack" is named as a specific anti-pattern. The prescription is whitespace, selective default display, and letting users toggle variables on/off via interactive legends.

- **Dashboard type taxonomy** — Five distinct types (Reporting, Monitoring, Exploration, Functional, Product Home) with different interaction contracts. Knowing which type you are building determines the correct defaults.

## Notable visual examples

**Anatomy diagram** (`images/Anatomy-v2.png`) — Hand-sketched in blue crayon on white. Three panels connected by red arrows show progressive zoom: full dashboard → section grid → individual module with numbers and a line chart. The sketch aesthetic is intentional — it signals "wireframe thinking," not final UI. The hierarchy is communicated through spatial containment and scale, not labelling alone. Effective because it collapses a complex composition rule into one glanceable diagram.

**F/Z scan pattern** (`images/F-Z-Patterns.png`) — Blue outline of a dashboard frame, three pink ellipses numbered 1-2-3, each spanning most of the width but narrowing slightly. Arrows show rightward scan with a diagonal drop between rows. The shrinking width of bands 2 and 3 visually reinforces the research finding: peripheral content at row-bottom is effectively invisible. Directly actionable for layout decisions.

**Deltas taxonomy** (`images/Deltas-icons-colours.webp`) — Light blue rounded card showing three columns (Icon-first, Textual, Inline) with real numbers and directional indicators. Icon-first is the most compact; textual is most readable but space-hungry; inline is designed for tables. The side-by-side comparison format makes the tradeoffs legible instantly. The colour coding is consistent: green up-arrow, yellow horizontal, red down-arrow — a semantic convention that should be applied uniformly across a dashboard.

## Relevance to public-finance dashboards

The delta taxonomy maps directly onto fiscal KPI cards: a deficit-as-percent-of-GDP card needs an icon-first delta (compact, scannable), while a narrative section comparing a budget outturn to the SGP 3% ceiling could use the textual form. The blue/orange colour convention is preferable to red/green for fiscal trend indicators because it avoids stoplight semantics (a rising deficit in red creates unnecessary alarm framing). The F-pattern layout principle means year-to-date totals and the most critical fiscal indicators belong in the top-left of the public_finance dashboard, with detailed breakdown charts lower on the page.
