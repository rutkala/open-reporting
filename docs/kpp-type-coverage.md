# KPP type coverage — all 87k entities mapped to aggregate sources

The KPP has ~87,000 entities in 225 **types**. Each type is covered by a
national aggregate register (one source per type), not per-entity. This maps
every type → its aggregate source, so the whole KPP universe is accounted for.

- **87,075 entities** across **225 types**
- **85,691** covered by an aggregate source; **1,384** in no-open-data types (military/intelligence/diplomatic)
- Biggest single wins: RSPO (~40k schools), dane.gov.pl/local-govt, RPWDL (health)

| Entities | Type | Aggregate source | Note |
|--:|---|---|---|
| 12,847 | szkoły podstawowe | `rspo` | Register of Schools (RSPO) — api.rspo.gov.pl |
| 8,659 | przedszkola | `rspo` | Register of Schools (RSPO) — api.rspo.gov.pl |
| 8,278 | szkoły średnie | `rspo` | Register of Schools (RSPO) — api.rspo.gov.pl |
| 4,646 | podmioty lecznicze | `rpwdl` | RPWDL healthcare register |
| 3,432 | zespoły szkół | `rspo` | Register of Schools (RSPO) — api.rspo.gov.pl |
| 3,303 | biblioteki | `bn_data` | BN library reports + GUS stats |
| 3,244 | instytucje kultury | `rik_culture` | RIK culture register + GUS |
| 2,809 | jednostki samorządu terytorialnego | `dane_gov_pl` | local-govt units — BDL/TERYT + dane.gov.pl + BIP |
| 2,479 | urzędy miast i gmin | `dane_gov_pl` | local-govt units — BDL/TERYT + dane.gov.pl + BIP |
| 2,382 | ośrodki pomocy społecznej | `mrips_social` | MRiPS CAS/Empatia social-welfare stats |
| 2,256 | urzędy stanu cywilnego | `danegovpl` | uncategorised — default to dane.gov.pl / BIP |
| 1,777 | zespoły szkolno-przedszkolne | `rspo` | Register of Schools (RSPO) — api.rspo.gov.pl |
| 1,760 | żłobki i kluby dziecięce | `danegovpl` | uncategorised — default to dane.gov.pl / BIP |
| 1,635 | spółki | `danegovpl` | business/economic — KRS / dane.gov.pl |
| 1,267 | jednostki wspólnej obsługi podmiotów | `dane_gov_pl` | local-govt units — BDL/TERYT + dane.gov.pl + BIP |
| 1,231 | zakłady usług komunalnych | `dane_gov_pl` | local-govt units — BDL/TERYT + dane.gov.pl + BIP |
| 1,156 | szkoły policealne | `rspo` | Register of Schools (RSPO) — api.rspo.gov.pl |
| 992 | jednostki Policji | `police_stats` | Police — KGP statystyka.policja.pl |
| 975 | placówki opiekuńczo-wychowawcze | `rspo` | Register of Schools (RSPO) — api.rspo.gov.pl |
| 745 | domy pomocy społecznej | `mrips_social` | MRiPS CAS/Empatia social-welfare stats |
| 745 | ośrodki sportu i rekreacji | `reports_only` | medical boards / sport / exams — reports |
| 705 | centra kształcenia zawodowego i ustawicznego | `rspo` | Register of Schools (RSPO) — api.rspo.gov.pl |
| 703 | ośrodki wsparcia | `mrips_social` | MRiPS CAS/Empatia social-welfare stats |
| 651 | szkoły artystyczne | `rspo` | Register of Schools (RSPO) — api.rspo.gov.pl |
| 631 | jednostki Krajowej Administracji Skarbowej | `danegovpl` | KAS / technical-inspection / transport — central body + dane.gov.pl |
| 626 | placówki oświatowo-wychowawcze | `rspo` | Register of Schools (RSPO) — api.rspo.gov.pl |
| 618 | poradnie psychologiczno-pedagogiczne | `rspo` | Register of Schools (RSPO) — api.rspo.gov.pl |
| 566 | zarządy gospodarki mieszkaniowej | `dane_gov_pl` | local-govt units — BDL/TERYT + dane.gov.pl + BIP |
| 552 | organizacje Samorządu Gospodarczego Rzemiosła | `dane_gov_pl` | local-govt units — BDL/TERYT + dane.gov.pl + BIP |
| 534 | internaty, bursy i domy wczasów dziecięcych | `rspo` | Register of Schools (RSPO) — api.rspo.gov.pl |
| 531 | ośrodki szkolno-wychowawcze | `rspo` | Register of Schools (RSPO) — api.rspo.gov.pl |
| 498 | jednostki wojskowe | `no_open_data` | military — no open data |
| 487 | polskie przedstawicielstwa na świecie | `no_open_data` | diplomatic posts abroad |
| 477 | zakłady wodociągów i kanalizacji | `dane_gov_pl` | local-govt units — BDL/TERYT + dane.gov.pl + BIP |
| 429 | nadleśnictwa lasów państwowych | `lasy_bdl` | State Forests — BDL |
| 411 | szkoły wyższe | `rspo` | Register of Schools (RSPO) — api.rspo.gov.pl |
| 402 | straże miejskie i gminne | `reports_only` | fire/municipal-guard statistics; central body |
| 393 | inspektoraty nadzoru budowlanego | `gugik_geo` | spatial/environment — GUGiK/GDOŚ/Wody Polskie WMS/WFS |
| 392 | jednostki Państwowego Gospodarstwa Wodnego Wody Polskie | `danegovpl` | uncategorised — default to dane.gov.pl / BIP |
| 377 | urzędy pracy | `psz_labour` | PSZ public-employment-services stats |
| 375 | prokuratury rejonowe | `isws_justice` | ISWS justice stats + SAOS judgments |
| 372 | zarządy dróg | `dane_gov_pl` | local-govt units — BDL/TERYT + dane.gov.pl + BIP |
| 364 | stacje sanitarno-epidemiologiczne | `danegovpl` | sanitary stations — GIS |
| 351 | inspektoraty weterynarii | `reports_only` | veterinary inspectorates — GIW |
| 351 | komendy Państwowej Straży Pożarnej | `reports_only` | fire/municipal-guard statistics; central body |
| 349 | centra pomocy rodzinie | `mrips_social` | MRiPS CAS/Empatia social-welfare stats |
| 341 | placówki Zakładu Ubezpieczeń Społecznych | `danegovpl` | finance/social-insurance branches — central body |
| 330 | placówki Agencji Restrukturyzacji i Modernizacji Rolnictwa | `arimr_geo` | agriculture — ARiMR/KOWR/inspectorates + dane.gov.pl |
| 328 | sądy rejonowe | `isws_justice` | ISWS justice stats + SAOS judgments |
| 314 | starostwa powiatowe | `dane_gov_pl` | local-govt units — BDL/TERYT + dane.gov.pl + BIP |
| 305 | inspektoraty ochrony roślin i nasiennictwa | `arimr_geo` | agriculture — ARiMR/KOWR/inspectorates + dane.gov.pl |
| 305 | zespoły do spraw orzekania o niepełnosprawności | `mrips_social` | MRiPS CAS/Empatia social-welfare stats |
| 293 | izby gospodarcze | `danegovpl` | business/economic — KRS / dane.gov.pl |
| 289 | zakłady energii i energetyki cieplnej | `dane_gov_pl` | local-govt units — BDL/TERYT + dane.gov.pl + BIP |
| 272 | placówki Kasy Rolniczego Ubezpieczenia Społecznego | `arimr_geo` | agriculture — ARiMR/KOWR/inspectorates + dane.gov.pl |
| 196 | centra usług społecznych | `danegovpl` | uncategorised — default to dane.gov.pl / BIP |
| 191 | związki gminne | `dane_gov_pl` | local-govt units — BDL/TERYT + dane.gov.pl + BIP |
| 188 | zakłady komunikacyjne | `dane_gov_pl` | local-govt units — BDL/TERYT + dane.gov.pl + BIP |
| 170 | instytuty badawcze | `opi_radon_api` | OPI RAD-on science register |
| 162 | ośrodki kuratorskie | `isws_justice` | ISWS justice stats + SAOS judgments |
| 150 | instytucje centralne | `see_central` | see docs/layer2-research-log.md (132 researched) |
| 120 | spółki wodne | `gugik_geo` | spatial/environment — GUGiK/GDOŚ/Wody Polskie WMS/WFS |
| 118 | zakłady karne | `reports_only` | prison service stats (SW) |
| 115 | jednostki Straży Granicznej | `reports_only` | Border Guard statistics (KG SG) |
| 111 | ośrodki i centra doskonalenia nauczycieli | `rspo` | Register of Schools (RSPO) — api.rspo.gov.pl |
| 110 | branżowe centra umiejętności | `rspo` | Register of Schools (RSPO) — api.rspo.gov.pl |
| 106 | warsztaty terapii i szkolne | `rspo` | Register of Schools (RSPO) — api.rspo.gov.pl |
| 105 | samorządowe jednostki organizacyjne | `dane_gov_pl` | local-govt units — BDL/TERYT + dane.gov.pl + BIP |
| 100 | stowarzyszenia | `danegovpl` | business/economic — KRS / dane.gov.pl |
| 94 | wojskowe centra rekrutacji | `no_open_data` | military — no open data |
| 91 | placówki wsparcia dziennego | `mrips_social` | MRiPS CAS/Empatia social-welfare stats |
| 88 | ośrodki ruchu drogowego | `danegovpl` | KAS / technical-inspection / transport — central body + dane.gov.pl |
| 83 | centra integracji społecznej | `mrips_social` | MRiPS CAS/Empatia social-welfare stats |
| 80 | archiwa państwowe | `rik_culture` | RIK culture register + GUS |
| 76 | parki | `rik_culture` | RIK culture register + GUS |
| 73 | centra opiekuńczo-mieszkalne | `mrips_social` | MRiPS CAS/Empatia social-welfare stats |
| 69 | agencje rozwoju | `danegovpl` | business/economic — KRS / dane.gov.pl |
| 69 | zespoły sądowych specjalistów | `isws_justice` | ISWS justice stats + SAOS judgments |
| 68 | inspektoraty transportu drogowego | `danegovpl` | KAS / technical-inspection / transport — central body + dane.gov.pl |
| 67 | areszty śledcze | `police_stats` | Police — KGP statystyka.policja.pl |
| 67 | kuratoria oświaty | `rspo` | Register of Schools (RSPO) — api.rspo.gov.pl |
| 64 | urzędy statystyczne | `gus` | GUS statistical offices |
| 63 | sanatoria i uzdrowiska | `rpwdl` | RPWDL healthcare register |
| 62 | urzędy miar | `reports_only` | metrology/standards/labs — registries |
| 61 | zakłady aktywności zawodowej | `mrips_social` | MRiPS CAS/Empatia social-welfare stats |
| 60 | związki powiatowo-gminne | `dane_gov_pl` | local-govt units — BDL/TERYT + dane.gov.pl + BIP |
| 59 | inspektoraty pracy | `danegovpl` | uncategorised — default to dane.gov.pl / BIP |
| 51 | izby obrachunkowe | `reports_only` | professional self-government chambers — registries |
| 50 | inspektoraty ochrony środowiska | `gugik_geo` | spatial/environment — GUGiK/GDOŚ/Wody Polskie WMS/WFS |
| 50 | instytuty Sieć Badawcza Łukasiewicz | `opi_radon_api` | OPI RAD-on science register |
| 50 | urzędy wojewódzkie | `dane_gov_pl` | local-govt units — BDL/TERYT + dane.gov.pl + BIP |
| 50 | sądy okręgowe | `isws_justice` | ISWS justice stats + SAOS judgments |
| 49 | delegatury Krajowego Biura Wyborczego | `pkw_elections` | PKW election data |
| 49 | inspekcje handlowe | `danegovpl` | UOKiK / trade inspection |
| 49 | urzędy ochrony zabytków | `rik_culture` | RIK culture register + GUS |
| 49 | samorządowe kolegia odwoławcze | `dane_gov_pl` | local-govt units — BDL/TERYT + dane.gov.pl + BIP |
| 48 | prokuratury okręgowe | `isws_justice` | ISWS justice stats + SAOS judgments |
| 47 | inspektoraty farmaceutyczne | `urpl_rpl` | pharmaceutical — GIF / URPL drug register |
| 46 | instytucje naukowe | `opi_radon_api` | OPI RAD-on science register |
| 45 | izby pielęgniarek i położnych | `reports_only` | professional self-government chambers — registries |
| 43 | ośrodki adopcyjne | `mrips_social` | MRiPS CAS/Empatia social-welfare stats |
| 42 | jednostki Żandarmerii Wojskowej | `no_open_data` | military — no open data |
| 35 | jednostki organizacyjne Ministerstwa Obrony Narodowej | `no_open_data` | military — no open data |
| 34 | fundacje | `danegovpl` | business/economic — KRS / dane.gov.pl |
| 34 | laboratoria | `reports_only` | metrology/standards/labs — registries |
| 34 | przedsiębiorstwa państwowe | `danegovpl` | business/economic — KRS / dane.gov.pl |
| 32 | oddziały Urzędu Dozoru Technicznego | `danegovpl` | KAS / technical-inspection / transport — central body + dane.gov.pl |
| 31 | zakłady dla nieletnich | `reports_only` | prison service stats (SW) |
| 30 | biura planowania przestrzennego | `gugik_geo` | spatial/environment — GUGiK/GDOŚ/Wody Polskie WMS/WFS |
| 27 | izby biegłych rewidentów | `isws_justice` | ISWS justice stats + SAOS judgments |
| 27 | wojskowe centra szkolenia | `no_open_data` | military — no open data |
| 26 | wojskowe oddziały gospodarcze | `no_open_data` | military — no open data |
| 25 | jednostki Agencji Bezpieczeństwa Wewnętrznego | `no_open_data` | intelligence/security — no open data |
| 25 | parki naukowo-technologiczne | `opi_radon_api` | OPI RAD-on science register |
| 24 | inspektoraty jakości handlowej artykułów rolno-spożywczych | `arimr_geo` | agriculture — ARiMR/KOWR/inspectorates + dane.gov.pl |
| 24 | izby adwokackie | `isws_justice` | ISWS justice stats + SAOS judgments |
| 23 | biura geodezji | `gugik_geo` | spatial/environment — GUGiK/GDOŚ/Wody Polskie WMS/WFS |
| 23 | centra krwiodawstwa i krwiolecznictwa | `rpwdl` | RPWDL healthcare register |
| 23 | izby lekarskie | `reports_only` | professional self-government chambers — registries |
| 21 | komendy ochotniczych hufców pracy | `psz_labour` | PSZ public-employment-services stats |
| 21 | ministerstwa | `danegovpl` | central-government bodies — dane.gov.pl + own (see central-institution log) |
| 20 | izby aptekarskie | `reports_only` | professional self-government chambers — registries |
| 20 | ośrodki dokumentacji geodezyjnej i kartograficznej | `gugik_geo` | spatial/environment — GUGiK/GDOŚ/Wody Polskie WMS/WFS |
| 19 | izby radców prawnych | `isws_justice` | ISWS justice stats + SAOS judgments |
| 19 | ośrodki przedsiębiorczości | `mrips_social` | MRiPS CAS/Empatia social-welfare stats |
| 19 | placówki Instytutu Pamięci Narodowej | `reports_only` | IPN archives |
| 18 | dzielnice m. st. Warszawy | `dane_gov_pl` | local-govt units — BDL/TERYT + dane.gov.pl + BIP |
| 18 | stacje chemiczno-rolnicze | `arimr_geo` | agriculture — ARiMR/KOWR/inspectorates + dane.gov.pl |
| 18 | oddziały terenowe Krajowego Ośrodka Wsparcia Rolnictwa | `mrips_social` | MRiPS CAS/Empatia social-welfare stats |
| 18 | urzędy dzielnicowe m. st. Warszawy | `dane_gov_pl` | local-govt units — BDL/TERYT + dane.gov.pl + BIP |
| 17 | dyrekcje lasów państwowych | `lasy_bdl` | State Forests — BDL |
| 17 | inspektoraty Służby Więziennej | `reports_only` | prison service stats (SW) |
| 17 | schroniska dla zwierząt | `danegovpl` | uncategorised — default to dane.gov.pl / BIP |
| 17 | ogrody zoologiczne i botaniczne | `rik_culture` | RIK culture register + GUS |
| 17 | przedsiębiorstwa sektora obronnego | `danegovpl` | uncategorised — default to dane.gov.pl / BIP |
| 16 | delegatury Urzędu Komunikacji Elektronicznej | `uke_broadband` | UKE telecom |
| 16 | dyrekcje ochrony środowiska | `gugik_geo` | spatial/environment — GUGiK/GDOŚ/Wody Polskie WMS/WFS |
| 16 | fundusze ochrony środowiska i gospodarki wodnej | `gugik_geo` | spatial/environment — GUGiK/GDOŚ/Wody Polskie WMS/WFS |
| 16 | izby architektów | `reports_only` | professional self-government chambers — registries |
| 16 | izby doradców podatkowych | `isws_justice` | ISWS justice stats + SAOS judgments |
| 16 | izby inżynierów budownictwa | `reports_only` | professional self-government chambers — registries |
| 16 | izby lekarsko-weterynaryjne | `reports_only` | veterinary inspectorates — GIW |
| 16 | izby rolnicze | `arimr_geo` | agriculture — ARiMR/KOWR/inspectorates + dane.gov.pl |
| 16 | urzędy marszałkowskie | `dane_gov_pl` | local-govt units — BDL/TERYT + dane.gov.pl + BIP |
| 16 | stacje doświadczalne Centralnego Ośrodka Badania Odmian Roślin Uprawnych | `arimr_geo` | agriculture — ARiMR/KOWR/inspectorates + dane.gov.pl |
| 16 | oddziały Generalnej Dyrekcji Dróg Krajowych i Autostrad | `danegovpl` | uncategorised — default to dane.gov.pl / BIP |
| 16 | oddziały Narodowego Funduszu Zdrowia | `nfz_bulk` | NFZ health fund |
| 16 | oddziały okręgowe Narodowego Banku Polskiego | `danegovpl` | finance/social-insurance branches — central body |
| 16 | ośrodki doradztwa rolniczego | `arimr_geo` | agriculture — ARiMR/KOWR/inspectorates + dane.gov.pl |
| 16 | sądy administracyjne | `isws_justice` | ISWS justice stats + SAOS judgments |
| 16 | regiony Banku Gospodarstwa Krajowego | `danegovpl` | finance/social-insurance branches — central body |
| 16 | ośrodki zamiejscowe Centralnego Wojskowego Centrum Rekrutacji | `no_open_data` | military — no open data |
| 16 | ośrodki zamiejscowe Głównego Inspektoratu Rybołówstwa Morskiego | `isws_justice` | ISWS justice stats + SAOS judgments |
| 16 | delegatury Najwyższej Izby Kontroli | `reports_only` | professional self-government chambers — registries |
| 15 | wojskowe komisje lekarskie | `no_open_data` | military — no open data |
| 15 | wojskowe biura emerytalne | `no_open_data` | military — no open data |
| 15 | jednostki organizacyjne Ministerstwa Zdrowia | `danegovpl` | central-government bodies — dane.gov.pl + own (see central-institution log) |
| 15 | placówki Rządowej Agencji Rezerw Strategicznych | `no_open_data` | military — no open data |
| 15 | rejonowe komisje lekarskie Zakładu Emerytalno-Rentowego Ministerstwa Spraw Wewnętrznych i Administracji | `danegovpl` | finance/social-insurance branches — central body |
| 14 | inspekcje geodezyjne i kartograficzne | `gugik_geo` | spatial/environment — GUGiK/GDOŚ/Wody Polskie WMS/WFS |
| 12 | komendy Państwowej Straży Rybackiej | `reports_only` | fire/municipal-guard statistics; central body |
| 12 | oddziały Biura Urządzania Lasu i Geodezji Leśnej | `gugik_geo` | spatial/environment — GUGiK/GDOŚ/Wody Polskie WMS/WFS |
| 12 | ośrodki pieczy zastępczej | `mrips_social` | MRiPS CAS/Empatia social-welfare stats |
| 12 | ośrodki polityki społecznej | `mrips_social` | MRiPS CAS/Empatia social-welfare stats |
| 12 | rejonowe zarządy infrastruktury | `danegovpl` | uncategorised — default to dane.gov.pl / BIP |
| 11 | izby komornicze | `isws_justice` | ISWS justice stats + SAOS judgments |
| 11 | izby notarialne | `isws_justice` | ISWS justice stats + SAOS judgments |
| 11 | jednostki Agencji Mienia Wojskowego | `no_open_data` | military — no open data |
| 11 | jednostki Wojskowej Ochrony Przeciwpożarowej | `no_open_data` | military — no open data |
| 11 | urzędy górnicze | `danegovpl` | mining — WUG / dane.gov.pl |
| 11 | lokalne komisje etyczne do spraw doświadczeń na zwierzętach | `danegovpl` | uncategorised — default to dane.gov.pl / BIP |
| 11 | sądy apelacyjne | `isws_justice` | ISWS justice stats + SAOS judgments |
| 11 | prokuratury regionalne | `isws_justice` | ISWS justice stats + SAOS judgments |
| 10 | izby turystyczne | `danegovpl` | business/economic — KRS / dane.gov.pl |
| 10 | wojskowe ośrodki aktywizacji zawodowej | `no_open_data` | military — no open data |
| 10 | sądy wojskowe | `isws_justice` | ISWS justice stats + SAOS judgments |
| 10 | zarządy portów | `danegovpl` | KAS / technical-inspection / transport — central body + dane.gov.pl |
| 10 | delegatury terenowe Głównego Inspektoratu Transportu Drogowego | `danegovpl` | KAS / technical-inspection / transport — central body + dane.gov.pl |
| 9 | szkoły wojskowe i podoficerskie | `rspo` | Register of Schools (RSPO) — api.rspo.gov.pl |
| 9 | ośrodki Centralnego Ośrodka Sportu | `reports_only` | medical boards / sport / exams — reports |
| 8 | delegatury Urzędu Ochrony Konkurencji i Konsumentów | `danegovpl` | UOKiK / trade inspection |
| 8 | wojskowe komendy transportu | `no_open_data` | military — no open data |
| 8 | urzędy żeglugi śródlądowej | `danegovpl` | KAS / technical-inspection / transport — central body + dane.gov.pl |
| 8 | komisje egzaminacyjne | `reports_only` | medical boards / sport / exams — reports |
| 8 | oddziały Urzędu Regulacji Energetyki | `danegovpl` | URE energy |
| 8 | regionalne placówki opiekuńczo-terapeutyczne | `mrips_social` | MRiPS CAS/Empatia social-welfare stats |
| 8 | ośrodki szkolenia Służby Więziennej | `reports_only` | prison service stats (SW) |
| 8 | jednostki organizacyjne Ministerstwa Spraw Wewnętrznych i Administracji | `danegovpl` | central-government bodies — dane.gov.pl + own (see central-institution log) |
| 7 | dowództwa wojsk | `no_open_data` | military — no open data |
| 7 | europejskie ugrupowania współpracy terytorialnej | `isws_justice` | ISWS justice stats + SAOS judgments |
| 7 | jednostki organizacyjne Ministerstwa Rolnictwa i Rozwoju Wsi | `danegovpl` | central-government bodies — dane.gov.pl + own (see central-institution log) |
| 7 | jednostki Wojskowego Dozoru Technicznego | `no_open_data` | military — no open data |
| 7 | oddziały terenowe Transportowego Dozoru Technicznego | `danegovpl` | KAS / technical-inspection / transport — central body + dane.gov.pl |
| 6 | związki powiatowe | `dane_gov_pl` | local-govt units — BDL/TERYT + dane.gov.pl + BIP |
| 6 | wojskowe ośrodki medycyny prewencyjnej | `no_open_data` | military — no open data |
| 6 | jednostki Agencji Uzbrojenia | `no_open_data` | military — no open data |
| 6 | szkoły policyjne | `rspo` | Register of Schools (RSPO) — api.rspo.gov.pl |
| 5 | akademie wojskowe | `no_open_data` | military — no open data |
| 5 | jednostki kontroli Ministerstwa Obrony Narodowej | `no_open_data` | military — no open data |
| 5 | urzędy morskie | `isws_justice` | ISWS justice stats + SAOS judgments |
| 5 | jednostki Wojskowej Inspekcji Gospodarki Energetycznej | `no_open_data` | military — no open data |
| 5 | oddziały Centrum Doradztwa Rolniczego | `arimr_geo` | agriculture — ARiMR/KOWR/inspectorates + dane.gov.pl |
| 4 | duszpasterstwa wojskowe | `no_open_data` | military — no open data |
| 4 | oddziały terenowe Rzecznika Małych i Średnich Przedsiębiorców | `danegovpl` | central-government bodies — dane.gov.pl + own (see central-institution log) |
| 4 | regionalne bazy logistyczne | `no_open_data` | military — no open data |
| 4 | Prokuratury Europejskie (EPPO) | `isws_justice` | ISWS justice stats + SAOS judgments |
| 4 | związki uczelni publicznych | `opi_radon_api` | OPI RAD-on science register |
| 3 | interwencyjne ośrodki preadopcyjne | `mrips_social` | MRiPS CAS/Empatia social-welfare stats |
| 3 | izby morskie | `isws_justice` | ISWS justice stats + SAOS judgments |
| 2 | jednostki metropolitalne | `dane_gov_pl` | local-govt units — BDL/TERYT + dane.gov.pl + BIP |
| 2 | jednostki organizacyjne Kancelarii Prezesa Rady Ministrów | `danegovpl` | central-government bodies — dane.gov.pl + own (see central-institution log) |
| 2 | jednostki organizacyjne Ministerstwa Cyfryzacji | `danegovpl` | central-government bodies — dane.gov.pl + own (see central-institution log) |
| 2 | jednostki organizacyjne Ministerstwa Finansów | `danegovpl` | central-government bodies — dane.gov.pl + own (see central-institution log) |
| 2 | jednostki organizacyjne Ministerstwa Funduszy i Polityki Regionalnej | `danegovpl` | central-government bodies — dane.gov.pl + own (see central-institution log) |
| 2 | jednostki organizacyjne Ministerstwa Klimatu i Środowiska | `danegovpl` | central-government bodies — dane.gov.pl + own (see central-institution log) |
| 2 | jednostki organizacyjne Ministerstwa Rozwoju i Technologii | `danegovpl` | central-government bodies — dane.gov.pl + own (see central-institution log) |
| 2 | urzędy probiercze | `danegovpl` | KAS / technical-inspection / transport — central body + dane.gov.pl |
| 2 | jednostki organizacyjne podległe Prezydentowi RP | `danegovpl` | central-government bodies — dane.gov.pl + own (see central-institution log) |
| 1 | zespoły oświaty | `rspo` | Register of Schools (RSPO) — api.rspo.gov.pl |
| 1 | federacje podmiotów systemu szkolnictwa wyższego i nauki | `opi_radon_api` | OPI RAD-on science register |
| 1 | placówki rodzinne | `mrips_social` | MRiPS CAS/Empatia social-welfare stats |
| 1 | jednostki organizacyjne Ministerstwa Infrastruktury | `danegovpl` | central-government bodies — dane.gov.pl + own (see central-institution log) |
| 1 | jednostki organizacyjne Ministerstwo Rodziny, Pracy i Polityki Społecznej | `mrips_social` | MRiPS CAS/Empatia social-welfare stats |
| 1 | sądy arbitrażowe | `isws_justice` | ISWS justice stats + SAOS judgments |
| 1 |  | `danegovpl` | uncategorised — default to dane.gov.pl / BIP |

## Entity coverage by source

| Source | Types | Entities |
|---|--:|--:|
| `rspo` | 21 | 41,610 |
| `dane_gov_pl` | 21 | 11,059 |
| `danegovpl` | 49 | 8,666 |
| `mrips_social` | 18 | 4,909 |
| `rpwdl` | 3 | 4,732 |
| `rik_culture` | 5 | 3,466 |
| `bn_data` | 1 | 3,303 |
| `reports_only` | 23 | 2,485 |
| `no_open_data` | 25 | 1,384 |
| `isws_justice` | 22 | 1,224 |
| `police_stats` | 2 | 1,059 |
| `arimr_geo` | 9 | 1,002 |
| `gugik_geo` | 10 | 694 |
| `lasy_bdl` | 2 | 446 |
| `psz_labour` | 2 | 398 |
| `opi_radon_api` | 6 | 296 |
| `see_central` | 1 | 150 |
| `gus` | 1 | 64 |
| `pkw_elections` | 1 | 49 |
| `urpl_rpl` | 1 | 47 |
| `uke_broadband` | 1 | 16 |
| `nfz_bulk` | 1 | 16 |
