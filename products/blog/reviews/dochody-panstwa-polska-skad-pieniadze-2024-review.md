# Review: dochody-panstwa-polska-skad-pieniadze-2024
*2026-06-05T12:30 UTC*

**Gate result:** ✅ PUBLISHED
**URL:** https://www.open-reporting.dev/dochody-panstwa-polska-skad-pieniadze-2024/


---

## Reviewer: content
**Verdict:** PASS

## Content Review

### P1 — Blocks Publication
None

### P2 — Should Fix Before Publication
None

### P3 — Noted
- **Abbreviation not defined on first use:** "STIR w 2018 roku" appears in the VAT-gap paragraph without expansion (System Teleinformatyczny Izby Rozliczeniowej). All other abbreviations (PKB, PIT, CIT, ZUS, VAT, JPK_VAT, OFE, NFZ, V4, DST, EA20, S13) are correctly expanded on first use.
- **No methodology note for the 87% derived figure:** The article states "Trzy bloki razem stanowiły 87 procent wszystkich dochodów sektora publicznego" without a footnote showing the calculation (37,3 / 42,8). The internal verification block containing this check is marked for deletion before publication; once removed, no public trace of the derivation remains. A brief parenthetical would improve transparency.
- **Missing humanisation:** The "Konsekwencje struktury" section partially connects numbers to lived experience (consumer spending every złoty on VAT, cap on contribution base for high earners), but the article remains predominantly analytical. A concrete household-level illustration would strengthen reader engagement.

### Verdict
PASS

### Reasoning
The article is rigorously sourced (Eurostat gov_10a_main dataset code cited throughout, legislative and EC sources named specifically), all derived values are arithmetically correct (87% = 37,3/42,8; all pp differentials verified), causal language is consistently avoided or explicitly qualified, and Polish unit conventions (comma decimal separator, "pp" for percentage-point deltas) are applied correctly throughout. The three P3 findings are minor traceability and engagement items that do not affect factual integrity or publication readiness.


---

## Reviewer: analytical
**Verdict:** CONDITIONAL

## Analytical Validation

### MISLEADING — Blocks Publication

None

### QUESTIONABLE — Should Fix

- **Aggregate change without compositional decomposition** — The article traces D61 (składki społeczne) rising from 12,2% PKB (1995) to 15,1% PKB (2024) and identifies several structural drivers qualitatively (reforma OFE 2011–2014, Polski Ład 2022, wzrost płacy minimalnej). However, the contributions of these factors to the aggregate shift are not quantified or rank-ordered. A reader cannot assess whether the OFE re-routing alone explains the post-2013 acceleration, or whether the Polski Ład health-contribution reform is the dominant driver of the jump to 15,1%. Simpson's paradox risk is low for a % of GDP series, but the unquantified compositional narrative could mislead about the relative magnitudes. Practical fix: add one sentence noting the approximate magnitude of the OFE effect (the redirected ~5 pp of gross wage transferred back to S13) versus the Polski Ład effect, or explicitly caveat that decomposition is outside scope.

### NOTED — Minor

- The article cites D5 for 2020 as 7,8% PKB and adds a parenthetical "(rok pandemii, gdy deklaracje odpowiadały dochodom sprzed kryzysu)" — this mixes ESA2010 accrual-basis national accounts logic with cash-flow PIT-declaration logic. ESA2010 national accounts record taxes on an accrual basis, not when declarations are filed. The explanation is not wrong in spirit, but the stated mechanism is imprecise for the data source cited.
- No long-run trend anchor at the 2004 EU-accession baseline is missing — the article does include 2004 data but does not explicitly frame it as the EU-accession structural break reference point for international comparability (NOTED per KB rule on 2004 baseline for labour/fiscal indicators).

### Verdict

CONDITIONAL

### Reasoning

No findings rise to MISLEADING: causal language is consistently hedged ("zbiegła się w czasie z", "co podnosi" used only for direct legal mechanisms), all pp/percentage-point distinctions are correct, no CAGR is used, and population comparisons draw from a single consistent Eurostat series. One QUESTIONABLE finding requires attention before publication: the aggregate D61 trend narrative asserts multiple structural drivers but does not quantify their relative contributions, leaving the key claim — that the 15,1% level is a structural shift rather than a reform artefact — incompletely supported.


---

## Reviewer: domain
**Verdict:** CONDITIONAL

## Domain Review: Public Finance — Government Revenue Structure (Poland)

### BLOCK — Must fix before publication
None

### CONDITIONAL — Should address

1. **ZUS contribution cap — critical definitional error citing a specific law article.** The text states: *"powyżej trzydziestokrotności przeciętnego wynagrodzenia **rocznego** nie płaci się składek emerytalnych i rentowych (art. 19 ustawy o SUS)."* Art. 19 ustawy o SUS reads: *"trzydziestokrotność prognozowanego przeciętnego wynagrodzenia **miesięcznego** w gospodarce narodowej."* The cap is 30× the average **monthly** wage (≈ PLN 225–240k annually in 2024), not 30× the annual wage (which would be ~12× higher). Using "rocznego" overstates the threshold by a factor of ~12. The claim is verifiable against the cited statutory provision and must be corrected.

2. **Minimum wage 2024 — dual-rate year not disclosed.** Poland had two statutory minimum wage rates in 2024: PLN 4,242 from 1 January and PLN 4,300 from 1 July (Rozporządzenie RM from September 2023). Citing only 4,242 zł is not wrong but should be qualified as the January 2024 rate; omitting the mid-year uplift is materially misleading in a structural-context paragraph about the contribution base.

### NOTE — Good to address

1. **"UE27 (średnia)" table label.** Eurostat gov_10a_main reports the EU27 and EA20 aggregates as **GDP-weighted aggregates**, not arithmetic means. Labelling them "średnia" is standard journalistic shorthand but technically imprecise; "agregat (wagi PKB)" or a footnote would avoid misreading by technically literate readers.

2. **2025 flash-estimate availability in gov_10a_main.** The series gov_10a_main follows EDP notification deadlines (March/September), meaning 2025 annual data published by June 2026 would be a preliminary first transmission estimate, not a Eurostat "flash" in the usual sense. The methodology note correctly flags it as preliminary; the body text could make the same caveat explicit where the 14.2% figure appears.

3. **Ireland — GNI\* not named.** The article correctly flags Ireland as a structural outlier driven by MNE profit relocation. Adding a single phrase — Ireland's CSO publishes modified GNI (GNI\*) to correct for this — would let quantitatively literate readers verify the claim directly and reinforces the analytical credibility of the comparison.

4. **Pre-2004 ESA2010 data provenance.** The 1995–2003 series for Poland in gov_10a_main is compiled by GUS using ESA2010 methodology applied retroactively (Poland was not yet an EU member). This is standard practice accepted by Eurostat, but a single sentence acknowledging it would strengthen the 30-year comparison claim.

### Verdict
CONDITIONAL

### Reasoning
The article is methodologically strong: ESA2010 indicator taxonomy (D2/D5/D61/S13), OFE structural-break disclosure, Polski Ład reform note, and VAT-gap sourcing are all handled correctly and at a level above typical data journalism. The single blocking-quality issue — citing Art. 19 of the SUS Act while using "rocznego" instead of "miesięcznego" — is a verifiable factual error in a specific legal reference that must be corrected before publication.
