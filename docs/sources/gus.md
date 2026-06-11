# GUS — Główny Urząd Statystyczny (Statistics Poland)
# Source: https://stat.gov.pl (redirects to new.stat.gov.pl)

GUS is Poland's central statistical office. Its web ecosystem consists of 13 database systems accessible
under "Bazy danych" on stat.gov.pl, plus 9 programmatic APIs, and 8 thematic dashboards.

---

## Bazy danych — Database Systems

| # | Name (PL) | Name (EN) | URL | Storage type | Bulk download | Auth | Coverage | Ingestion status |
|---|-----------|-----------|-----|--------------|---------------|------|----------|-----------------|
| 1 | Atlas Regionów | Regional Atlas | atlas.stat.gov.pl | Interactive map (JS SPA) | No | None | Regional comparisons visualised on BDL data | — visualisation layer only, no separate data |
| 2 | Bank Danych Lokalnych (BDL) | Local Data Bank | bdl.stat.gov.pl | REST API (JSON/XML) | No — API only | Optional (higher limits with key) | 40 000+ variables, NUTS2/3/4, gmina level, 1995–present, CC BY 4.0 | **Partial** — subjects tree only; full variable data NOT pulled |
| 3 | Bank Danych Makroekonomicznych (BDM) | Macroeconomic Data Bank | bdm.stat.gov.pl | Web UI (JS SPA) | Unknown — no documented API | None | National accounts, money supply, CPI, trade, employment, finance | **Not started** |
| 4 | Bank Danych Polska (BDP) | Data Bank Poland | bdp.stat.gov.pl | JS SPA — content unknown | Unknown | None | Unclear — may aggregate cross-GUS data for Poland-level view | **Not started** |
| 5 | Baza organizacji polskich za granicą | Polish organisations abroad | new.stat.gov.pl (menu link only) | Web UI | No | None | Directory of Polish organisations and institutions abroad | Not a priority data source |
| 6 | Demografia | Demographics | demografia.stat.gov.pl | Web UI (redirects, JS SPA) | Unknown | None | Population, births, deaths, migration, projections | **Not started** |
| 7 | Dziedzinowe Bazy Wiedzy (DBW) | Domain Knowledge Bases | dbw.stat.gov.pl | Two modes: (a) static file downloads via `/api_app/getCatalogValues` for HVD subset; (b) REST API via `/api_app/wsk/getIndicatorsTree` + `/api_app/getTimeSeries` for full indicator set | **Yes (HVD only)** | None | GDP, labour, finance, poverty, demographics, environment. HVD: 21 categories, 426 ZIP/CSV files. Full API: 1547 indicators across Gospodarka (800), Społeczeństwo (632), Środowisko (115) | **DONE (HVD)** — 426 files in `landing/gus_dbw_bulk/`. Non-HVD API (1547 indicators) not yet pulled → `gus_dbw_api` |
| 8 | SDDS — Dane gospodarcze i finansowe | Special Data Dissemination Standard | dsbb.imf.org (Poland entry at IMF) | IMF portal link | IMF bulk export | None | Fiscal, monetary, external sector data submitted to IMF under SDDS+ | Covered by IMF/Eurostat sources; not a separate GUS database |
| 9 | SDG — Cele Zrównoważonego Rozwoju | Sustainable Development Goals | sdg.gov.pl | Excel bulk download + REST API (`api.stat.gov.pl/Home/SDGApi`) | **Yes** (Excel per category) | None | ~250 UN SDG indicators for Poland, CC BY 4.0 | **Not started** |
| 10 | SMUP | Public Services Monitoring | smup.gov.pl | REST API (`api.stat.gov.pl/Home/SMUPApi`) | Via API | None | Education, healthcare, transport, social services at gmina level | **Not started** |
| 11 | Statystyczne Vademecum Samorządowca (SVS) | Statistical Handbook for Local Government | svs.stat.gov.pl | Web UI (profile sheets per unit) | No documented API | None | ~100 key stats per gmina/powiat/województwo — population, economy, infrastructure | **Not started** — web-only, scraping needed |
| 12 | STRATEG | Development Strategy Monitoring | strateg.stat.gov.pl | REST API (`api.stat.gov.pl/Home/StrategApi`) | Via API | None | EU cohesion policy + national strategy indicators, NUTS2 | **Not started** |
| 13 | TranStat — statystyki eksperymentalne | Transport Statistics (experimental) | transtat.stat.gov.pl | REST API (`api-transtat.stat.gov.pl/apidocs/`) | Via API | None | Road, rail, air transport statistics (experimental series) | **Not started** — note: server returning 500 errors as of 2026-06 |

---

## APIs (stat.gov.pl API hub: api.stat.gov.pl)

| API | URL | Data | Auth | Rate limit | Bulk? | Priority |
|-----|-----|------|------|------------|-------|----------|
| **BDL API** | api.stat.gov.pl/Home/BdlApi | 40k variables, all admin levels, 1995–present | Optional key (`X-ClientId` header) | Anon: 10k/week · Registered: 50k/week | No — paginated queries | **HIGH** — richest regional dataset |
| **REGON API** | api.stat.gov.pl/Home/RegonApi | Business register — search by REGON/NIP/KRS | Key required (email registration to regon_bir@stat.gov.pl) | 6 000/h peak, 10 000/h off-peak | No — entity-level queries only | Medium — useful for company data |
| **TERYT API** | api.stat.gov.pl/Home/TerytApi | Official geographic unit codes (gmina/powiat/województwo TERYT codes) | None | Unknown | Yes — can dump full hierarchy | **HIGH** — needed as dimension table for all regional models |
| **SDP API** | api.stat.gov.pl/Home/SDPApi | Statistical publication index | None | Unknown | Partial | Low |
| **DBW API** | api.stat.gov.pl/Home/DBWApi | Thematic domain data (complements HVD files) | None | Unknown | Via API | Low — already have HVD bulk files |
| **SMUP API** | api.stat.gov.pl/Home/SMUPApi | Public services monitoring | None | Unknown | Via API | Medium |
| **STRATEG API** | api.stat.gov.pl/Home/StrategApi | Development strategy indicators | None | Unknown | Via API | Medium |
| **SDG API** | api.stat.gov.pl/Home/SDGApi | SDG indicators for Poland | None | Unknown | Via API | Low — Excel bulk preferred |
| **TRANSTAT API** | api-transtat.stat.gov.pl/apidocs/ | Transport statistics | None | Unknown | Via API | Low — experimental/unstable |

---

## Thematic Dashboards (data visualisations — not direct data sources)

| Dashboard | URL | Topic |
|-----------|-----|-------|
| Koniunktura Gospodarcza | dashboard-koniunktura.stat.gov.pl | Business sentiment |
| REGON Dashboard | dashboard-regon.stat.gov.pl | Business register statistics |
| Dashboard Gospodarczy | dashboard.stat.gov.pl | Economic overview |
| Turystyka+ | turystyka.stat.gov.pl | Tourism statistics |
| Ukraińcy w Polsce | ukraincywpolsce.stat.gov.pl | Ukrainian refugees/residents |
| Zdrowie uchodźców | healthofrefugees.stat.gov.pl | Refugee health data |
| Atlas Polonii | dashboard-polonia.stat.gov.pl | Polish diaspora abroad |
| Osoby Niepełnosprawne Prawnie | dashboard-niepelnosprawni.stat.gov.pl | Disability statistics |

> These are visualisation layers built on BDL/DBW data. Not ingestion targets — get data from the underlying sources.

---

## Current Ingestion State Summary

| Source ID | Files in landing | Method | Gap |
|-----------|-----------------|--------|-----|
| `gus_dbw_bulk` | 426 files | `bulk/run_bulk.py` → `get_gus_hvd_files()` | HVD complete. Non-HVD (1547 indicators) = API only, separate source |
| `gus_dbw_api` | 1 file (area tree) | `bulk/run_bulk.py` (1 URL) | Full 1547-indicator pull via `getTimeSeries` not yet built |
| `gus_bdl_api` | 1 file (subjects tree) | `bulk/run_bulk.py` (1 URL) | **Full variable data missing** |
| `gus_teryt_bulk` | 51 JSON pages | `bulk/run_bulk.py` → `get_gus_teryt_files()` | **DONE** — 7 admin levels, BDL page-size=100, ceiling-paged |
| `gus_sdg_bulk` | 2 JSON files | `bulk/run_bulk.py` → `get_gus_sdg_files()` | **DONE** — 144 national + 250 global SDG indicators |
| `gus_biuletyn_bulk` | 63 XLSX | `bulk/run_bulk.py` → `get_gus_biuletyn_files()` | **DONE** — scraped from `new.stat.gov.pl/biuletyn-statystyczny-dlugie-szeregi` |
| `gus_bdm_api` | 0 | Not implemented | Need to find download endpoint (JS SPA) |
| `gus_smup_api` | 0 | Not implemented | API available via api.stat.gov.pl/Home/SMUPApi |
| `gus_strateg_api` | 0 | Not implemented | API available via api.stat.gov.pl/Home/StrategApi |

---

## BDL Full Ingestion — Design Notes

BDL has 40 000+ variables and no bulk dump — data must be retrieved variable-by-variable or by
territorial unit. Practical strategy:

1. **Subject tree** (done): `GET /api/v1/subjects` → hierarchy of ~20 top-level domains
2. **Variable enumeration**: `GET /api/v1/variables?subject-id={id}&page={n}` — paginate all variables
3. **Data pull per variable**: `GET /api/v1/data/by-variable/{varId}?unit-level=5&year={years}` → JSON
4. **Rate limit**: registered key gives 50 000 requests/week → ~7k/day → can pull ~7k variables/day
   → full pull of 40k variables takes ~6 days at registered rate, or incrementally over weeks

> **Recommendation**: Register for a BDL API key first (free), then implement incremental subject-by-subject
> pull prioritising the domains relevant to our dashboards (public finance, labour, demographics).

---

## TERYT Full Ingestion — Design Notes

TERYT provides the official Polish administrative unit code hierarchy used by all GUS systems.
Essential as a `dim_geo` dimension table.

- `GET /api/v1/units?level=0` through `level=7` — six levels: kraj → makroregion → województwo →
  podregion → powiat → gmina → miejscowość
- Response: TERYT code, name, parent code
- No auth required; no rate limit documented
- Full hierarchy: ~2500 gmin + ~380 powiatów + 16 województw → small enough to dump in one batch

> **Priority**: implement `gus_teryt` bulk fetcher. This unblocks BDL regional joins and all
> future regional modelling.
