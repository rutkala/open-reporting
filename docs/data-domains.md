# Data domain taxonomy — what topics we collect data about

The **subject** framework for source discovery: the topics/domains we want data for,
independent of *who* publishes (that's the source category a–f). Aligned to the
**EU DCAT-AP themes** used by dane.gov.pl and the EU data portal — so it's standard,
internationally comparable, and future-proof for European-scope expansion.

A source can serve several domains; a domain is served by many sources. The goal:
for **every** domain/subdomain below, have at least one source feeding it.

| # | Domain (DCAT) | Subdomains / topics | Lead sources |
|---|---|---|---|
| **1** | **Government & public sector** (GOVE) | public administration · state budget execution · public procurement · elections · legislation · public registers (REGON/KRS/TERYT) · public-entity catalogue | MF OpenBudget, UZP, PKW, Sejm, KRS, GUS BDL/DBW, dane.gov.pl |
| **2** | **Economy & finance** (ECON) | GDP & national accounts · prices/inflation (HICP) · public finance & debt · taxes · business & companies · **financial markets** (GPW, Stooq) · banking · money & rates (NBP, ECB) · foreign trade (WTO) · **labour market** (employment, unemployment, wages) | GUS BDL/DBW, MF, NBP, GPW, KNF, Eurostat, IMF, WB, UZP, KRS RDF, PSZ |
| **3** | **Population & society** (SOCI) | demographics (births/deaths/migration) · households · social welfare & benefits · pensions (ZUS/KRUS) · NGOs / civil society (OPP) · equality | GUS, ZUS, KRUS, MRiPS/CAS, UN WPP, OPP/NIW, Eurostat |
| **4** | **Health** (HEAL) | healthcare providers (RPWDL) · services & contracts (NFZ) · drugs (URPL) · sanitary/epidemiology (GIS) · mortality/morbidity · pharma | NFZ, RPWDL, URPL, GIS, GUS, Eurostat |
| **5** | **Education, culture & sport** (EDUC) | schools & pupils (RSPO) · higher education & science (OPI RAD-on, NCN) · exams (CKE) · libraries (BN) · cultural institutions (RIK) · heritage · sport · media | RSPO, MEN, OPI RAD-on, BN, RIK, GUS, CKE |
| **6** | **Environment** (ENVI) | air quality (GIOŚ) · water (Wody Polskie) · nature protection (GDOŚ) · climate · waste · geology (PIG) · meteorology (IMGW) · radiation (PAA) | GIOŚ, IMGW, GDOŚ, Wody Polskie, PIG, GUS, Eurostat |
| **7** | **Agriculture, fisheries, forestry, food** (AGRI) | farms & crops (ARiMR) · livestock · forests (Lasy/BDL) · fisheries · food quality (IJHARS) · plant/animal health (GIORiN/GIW) · agri markets (KOWR) | ARiMR, Lasy Państwowe, GUS, FAOSTAT, inspectorates |
| **8** | **Energy** (ENER) | electricity production & grid (PSE) · fuel & gas (Orlen, Gaz-System, PERN) · renewables · nuclear (PEJ) · tariffs & market (URE) · mining/coal (JSW, Węglokoks) | URE, PSE, ORLEN, Gaz-System, state companies, Eurostat |
| **9** | **Transport** (TRAN) | roads (GDDKiA) · rail (UTK, PKP PLK) · air (ULC) · maritime · traffic (GITD) · infrastructure · vehicles | GDDKiA, UTK, ULC, PKP PLK, GUS, Eurostat |
| **10** | **Justice & public security** (JUST) | courts & caseloads (ISWS) · prosecution · crime (Police) · prisons · fire/rescue (PSP) · border (SG) · audit (NIK) | ISWS, Police, NIK, SAOS, GUS |
| **11** | **Science & technology** (TECH) | R&D · patents (UPRP) · innovation · telecom & broadband (UKE) · digital economy · geodesy/spatial (GUGiK) | OPI RAD-on, UPRP, UKE, GUGiK, NCN, Eurostat |
| **12** | **Regions & cities** (REGI) | local government finance · spatial/geography (GUGiK/TERYT) · **real-estate prices** (RCN) · urban statistics · regional development | GUS BDL, GUGiK, TERYT, dane.gov.pl (local), RCN, Eurostat |
| **13** | **International affairs** (INTR) | cross-country comparisons · foreign affairs · development aid · EU funds | Eurostat, OECD, IMF, WB, ECB, ILOSTAT, WTO, UN |

## How this reframes source discovery

- The **6 source categories (a–f)** answer *who holds the data*.
- The **13 domains** answer *what topic it's about*.
- Coverage target: every domain × subdomain has ≥1 feeding source. Gaps in the
  matrix = where to look for new sources (and what new products are possible).

## Subdomain depth (for the richest domains)

GUS BDL exposes ~33 K-subject categories and DBW ~14 thematic domains that map under
the above (e.g. BDL K27 Public finance → ECON; K3 Population → SOCI). These are the
**subdomain** granularity — the level at which we actually pull and model data.

## Status
Taxonomy defined. Next: tag every registry source with the domain(s) it serves, then
generate a **domain × source coverage matrix** to expose topic gaps.
