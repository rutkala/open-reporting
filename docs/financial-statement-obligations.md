# Financial-statement filing obligations — entity groups & data sources

In Poland, several groups of entities are legally obliged to publish financial
statements. This maps each group to where its data is published (and our source).

| Group | Obligation basis | Where published | Our source |
|---|---|---|---|
| **All KRS entities** — spółki kapitałowe (sp. z o.o., S.A.), spółki osobowe, fundacje, stowarzyszenia (~600k) | Ustawa o rachunkowości art. 69; KRS Act | **KRS RDF** (ekrs.ms.gov.pl/rdf) — XML+PDF per entity | `krs_rdf` |
| **Entities not in KRS** (filing to KAS) | Ustawa o rachunkowości | e-Sprawozdania → Head of KAS (JPK_SF) | via KAS (not public per-entity) |
| **Public-benefit orgs (OPP)** (~9k) | Ustawa o działalności pożytku publicznego | **NIW** sprawozdaniaopp.niw.gov.pl | `opp_niw` |
| **Listed issuers** (GPW/NewConnect/Catalyst, ~750) | MAR / Ustawa o ofercie | **ESPI/EBI** via GPW + own IR | `gpw_espi` + per-company (PGE, KGHM, ORLEN…) |
| **Banks & SKOK** | Prawo bankowe; KNF | KNF + own reports | `knf_bulk` + bank sources (`pko_bp`) |
| **Insurers** | Ustawa o działalności ubezpieczeniowej; KNF | KNF + own reports | `knf_bulk` + `pzu` |
| **Investment / pension funds (TFI/PTE/OFE/PPK)** | Ustawa o funduszach; KNF | KNF + PFR (PPK) | `knf_bulk`, `pfr` |
| **State-owned companies** | + ownership reporting to MAP | own IR + MAP | category-c company sources |

## Extraction notes

- **KRS RDF is the keystone** — it already holds the audited financial statements
  of essentially every company/foundation/association. Strategy: enumerate KRS
  numbers (KRS OpenAPI / bulk dump), pull each entity's documents. Huge —
  prioritise by sector/size; the per-entity API is free, a bulk professional API
  needs registration.
- The big listed companies are *also* in KRS RDF, but their ESPI/IR reports are
  richer/timelier — we keep both (no dedup, per the source strategy).
- e-Sprawozdania (MF/KAS) is the *filing* pipe, not a public per-entity store;
  KRS entities surface in KRS RDF, so we source there.

## Status
All three core sources defined in the registry (`krs_rdf`, `opp_niw`, `gpw_espi`);
extractors still to build (KRS RDF needs the KRS-number enumeration first).
