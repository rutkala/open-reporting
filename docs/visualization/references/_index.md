# Visualization references — index

Wave 1 captured 2026-05-25. All five sources processed.
Wave 2 captured 2026-05-25. 3 of 5 sources yielded images; 2 dropped (network-blocked). See per-source `source.md` files.

**Rubric distilled** from these sources at [`docs/visualization/quality.md`](../quality.md) — 21 dimensions, each grounded in ≥1 captured reference image. Use the rubric for build + review judgments; come back to the source folders here when you need to look at a specific reference.

## Wave 1

| Source | What it teaches | Type | Images |
|--------|----------------|------|--------|
| [Dashboard Design UX Patterns (PencilAndPaper)](pencilandpaper-ux-patterns/) | Full UX journey through a dashboard: anatomy, layout priority (F/Z scan), colour conventions (blue/orange polarity), delta taxonomy (icon-first / textual / inline), progressive disclosure via hover | UX pattern analysis | 8 captured, 0 skipped |
| [FT Visual Vocabulary](ft-visual-vocabulary/) | Canonical chart-type decision framework: 9 semantic categories (Deviation, Change over Time, Part-to-whole, Magnitude, Flow, etc.) each with named chart types and when-to-use rules; Waterfall explicitly named for budget flow | Reference poster | 1 captured, 0 skipped |
| [BBC News R Graphics Cookbook](bbc-r-cookbook/) | Opinionated house-style enforcement via `bbc_style()`: mandatory zero baseline, colour minimalism (one accent + grey), y-axis-only gridlines, direct line labelling, left-aligned titles | Code cookbook | 1 captured, 0 skipped |
| [What to consider when choosing colors for data visualization (Datawrapper Academy)](datawrapper-academy/) | 12 structured colour rules with NOT IDEAL / BETTER paired examples: grey as primary tool, seven-colour categorical maximum, diverging gradients for deviation data, lightness-driven gradients, colour blindness simulation | Design principles article | 4 captured, 0 skipped |
| [NNG — Progressive Disclosure + Information Scent](nng-dashboards/) | Cognitive science foundation for dashboard density decisions: two-level disclosure maximum, initial-screen split based on task frequency, information scent as the mechanism that determines whether users notice KPI labels and charts | Foundational UX research (paired articles) | 1 captured, 0 skipped |

## Wave 2

| Source | What it teaches | Type | Images | Strength |
|--------|----------------|------|--------|----------|
| [Eurostat — Government Finance Statistics](eurostat-gus/) | Official EU fiscal chart templates: SGP threshold reference line as primary anchor, diverging deficit bar, grouped debt bar, cross-section sorted by average, dual-line expenditure/revenue trend, three-series tax decomposition. Most directly applicable source in the library to public_finance dashboard. | Official statistics article | 6 captured, 0 skipped | Strong — vision-grounded |
| [Power BI Community — Data Stories Gallery](power-bi-showcase/) | Practitioner Power BI patterns: dark-theme conventions, scenario simulator layout (sliders → KPI cards → actual vs simulated chart), geographic map as anchor, waterfall for cost decomposition, KPI row as mandatory first element. Also negative patterns: gauge waste, contrast failures in dark themes. | Community gallery | 4 captured, 0 skipped | Strong — vision-grounded |
| [The Pudding — "Birthday Effect" (NYT Upshot substitute)](nyt-upshot/) | Sequential chart zoom as explanatory mechanism, histogram for statistical credibility, std dev bands as colour encoding, hand-drawn aesthetic as approachability signal, strict two-colour discipline, annotation as first-class element co-located with data. | Data journalism narrative | 4 captured, 0 skipped | Strong — vision-grounded |
| [Tableau Public — Viz of the Day](tableau-public/) | DROPPED — Cloudflare blocks all access (WebFetch + Playwright). Text-only annotation from prior knowledge: bump charts, slope charts, custom palettes, scrollytelling with embedded views, small multiples. Wave 3 recommendation in article-text.md. | Gallery | 0 captured | Weak — text-only, prior knowledge |
| [IMF Fiscal Monitor](imf-fiscal-monitor/) | DROPPED — Akamai blocks all access at IP level. Text-only annotation from prior knowledge: fan charts for projections, scatter for debt sustainability, waterfall for fiscal decomposition, small multiples by country group. Wave 3 recommendation: local PDF download + Read tool. | PDF report | 0 captured | Weak — text-only, prior knowledge |
