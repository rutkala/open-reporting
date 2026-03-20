# Domain Taxonomy

Last updated: 2026-03-17
Based on: Eurostat Statistical Themes (2nd level) + GUS Obszary Tematyczne

This is the master list of content domains for Open Reporting. Domains drive everything: portal sections, dashboard groupings, article categories, data pipelines, and Linear/GitHub issue labels.

## Domain Definitions

| ID | Domain | Eurostat Theme | GUS Equivalent |
| :--- | :--- | :--- | :--- |
| 1 | **Public Finance** | Economy and finance | Finanse publiczne |
| 2 | **National Accounts & Macro** | Economy and finance | Rachunki narodowe, Wskaźniki makroekonomiczne |
| 3 | **Prices & Inflation** | Economy and finance | Ceny |
| 4 | **Financial Markets** | Economy and finance | NBP, GPW, KNF data |
| 5 | **Population & Demographics** | Population and social conditions | Ludność, Stan i struktura ludności |
| 6 | **Labour Market** | Population and social conditions | Rynek pracy, Wynagrodzenia |
| 7 | **Health** | Population and social conditions | Ochrona zdrowia |
| 8 | **Education** | Population and social conditions | Edukacja |
| 9 | **Income, Living & Social** | Population and social conditions | Warunki życia, Dochody, Pomoc społeczna |
| 10 | **Crime & Justice** | Population and social conditions | Wymiar sprawiedliwości |
| 11 | **Culture, Tourism & Sport** | Population and social conditions | Kultura, Turystyka, Sport |
| 12 | **Business & Industry** | Industry, trade, and services | Podmioty gospodarcze, Przemysł, Budownictwo |
| 13 | **Agriculture & Forestry** | Agriculture, fisheries, forestry | Rolnictwo, Leśnictwo |
| 14 | **International Trade** | International trade | Handel zagraniczny |
| 15 | **Transport** | Transport | Transport |
| 16 | **Environment & Climate** | Environment and energy | Środowisko |
| 17 | **Energy** | Environment and energy | Energia |
| 18 | **Science, Tech & Digital** | Science, technology, digital | Nauka i technika, Społeczeństwo informacyjne |

## Subcategories & Usage

The Orchestrator agent should use the **Domain ID** as a primary tag for all related issues, data ingestion pipelines, and dashboard groupings.

*   *Example:* If a task involves R&D spending, it is tagged with `Domain: 18 (Science, Tech & Digital)` and subcategory `R&D spending`.
