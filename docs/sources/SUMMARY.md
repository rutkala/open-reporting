# Source Materials Summary

Extracted resources for building the visualization knowledge base. Cached in `visualization/docs/viz-kb-full/` from web crawling performed 2026-04-01.

---

## Extraction Script

**Location:** `docs/visualization/_external/documents_extraction.sh` *(moved from `docs/analytics/visualization/docs/` 2026-04-07)*

**URLs processed:**
```
1. https://data.europa.eu/apps/data-visualisation-guide/
2. https://ibcs.com
3. https://github.com/UrbanInstitute/graphics-styleguide
4. https://m2.material.io/design/communication/data-visualization.html
5. https://playfairdata.com
6. https://datavizstyleguide.com
7. https://scientificdiscovery.dev
8. https://hype4.academy/learn
```

---

## Extracted Content

### 1. playfairdata.com (618 files)

**Content:** Tableau tutorials, data visualization best practices, chart-specific guides
**Type:** HTML articles, video pages, PDF study guides
**Key articles:**
- "5 Ways to Make a Bar Chart in Tableau"
- "3 Ways to Make Lovely Line Graphs in Tableau"
- "Cornerstone Module Part 1 & 2" (fundamentals)
- "Bullet Graphs" tutorial
- "3 Storytelling with Color Tips"
- Study Guides (PDF): Visual Analytics Practitioner Exam, Advanced Analytics Exam

**Used for:** Chart-specific guidance, Tableau examples, practical implementation tips

### 2. data.europa.eu (20 files)

**Content:** EU Data Visualisation Guide — comprehensive guide to visualization principles
**Type:** Interactive web app (Svelte), HTML
**Sections:**
- Design principles (colour, typography)
- Data storytelling
- Pitfalls (statistics, chart types)
- Dataviz in practice (tools, file formats)
- Chart types (line charts, bars, etc.)
- Accessibility
- Grammar of Graphics

**Used for:** Foundational principles, accessibility guidelines, structured methodology

### 3. m2.material.io (9 files)

**Content:** Google Material Design guidelines for data visualization
**Type:** Angular SPA, HTML
**Status:** Partial extraction (requires JavaScript rendering)

**Used for:** Design system conventions, UI patterns

### 4. hype4.academy (2 files)

**Content:** Hype4 Academy learning platform — data visualization courses
**Type:** Next.js SPA, HTML
**Pages:**
- `index.html` — Courses overview
- `learn.tmp.html` — Learning section

**Used for:** Course-based learning structure, visualization curriculum

**Status:** Requires JavaScript rendering for full content

### 4. UrbanInstitute/graphics-styleguide (470+ files, full git clone)

**Content:** Full repository with CSS, chart guidelines, and PDFs
**Type:** Git clone + PDFs
**Key PDFs:**
- `img/Pie Chart Design from WSJ.pdf` — Wall Street Journal graphics department guidelines on pie charts
- `img/urban_pdf.pdf` — Urban Institute chart styling
- `2023/old source files/tpc_graphinstructions_final.pdf` — Tax Policy Center graph instructions

**Used for:** Professional styling, chart-specific guidance, authoritative design patterns

### 5. ibcs.com (1 file)

**Content:** IBCS standards overview
**Type:** HTML (landing page)
**Status:** Minimal extraction — ibcs.com may block crawling

**Used for:** Reference to IBCS standards (standards themselves referenced from other sources)

### 6. datavizstyleguide.com, scientificdiscovery.dev, hype4.academy

**Status:** Not fully extracted (may have failed or incomplete)

---

## Extracted PDFs (10 total)

| Source | File | Description |
|--------|------|-------------|
| playfairdata.com | Study-Guide-Visual-Analytics-Practioner-Exam.pdf | Visual Analytics certification prep |
| playfairdata.com | Study-Guide-Advanced-Analytics-Practioner-Exam-1.pdf | Advanced Analytics certification |
| playfairdata.com | Guides-from-Playfair-The-Problem-with-Plastic.pdf | Storytelling guide |
| playfairdata.com | Playfair-Data-Privacy-Policy-2024-08-15-1.pdf | (Not relevant) |
| graphics-styleguide | Pie Chart Design from WSJ.pdf | **WSJ graphics guidelines** |
| graphics-styleguide | urban_pdf.pdf | Urban Institute styling |
| graphics-styleguide | tpc_graphinstructions_final.pdf | Tax Policy Center graph instructions |
| graphics-styleguide | TaxPolicyCenter_Logo_Guidelines.pdf | Logo guidelines |

---

## Content Quality

| Source | Quality | Coverage |
|--------|---------|----------|
| playfairdata.com | High | Excellent — 600+ pages, practical tutorials |
| data.europa.eu | High | Excellent — structured guide, 7 topics |
| UrbanInstitute | Medium | CSS-focused, some chart patterns |
| m2.material.io | Low | Requires JS rendering, limited extraction |
| ibcs.com | Low | Blocked/failed extraction |

---

## How to Use

**For building KB files:**
1. Use `visualization/docs/viz-kb-full/https:/playfairdata.com/` for chart-specific guidance
2. Use `visualization/docs/viz-kb-full/https:/data.europa.eu/apps/data-visualisation-guide/` for principles
3. Reference Urban Institute CSS for styling conventions

**For future extraction:**
- Consider using a headless browser for JS-heavy sites (Material Design)
- Add `--no-check-certificate` for sites with cert issues
- Consider Scrapy or dedicated crawler for better handling

---

## Files Not Yet Extracted

If needed, consider re-extracting:
- datavizstyleguide.com
- scientificdiscovery.dev  
- hype4.academy
- Full ibcs.com content

---

## Last Updated

2026-04-01