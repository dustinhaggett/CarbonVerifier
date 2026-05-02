# REGULATORY COMPLIANCE BRIEF

**Prepared by:** Independent Compliance Audit Unit
**Standard Under Review:** Verra Verified Carbon Standard (VCS) v4.0
**Document Status:** DRAFT — FOR REGULATORY REVIEW
**Date:** 2025

---

## 1. PROJECT IDENTIFICATION

| Field | Detail |
|---|---|
| **VCS Registry ID** | VCS981 |
| **Project Name** | Cikel Brazilian Amazon REDD APD |
| **Country** | Brazil |
| **Registered Area** | 27,435 hectares |
| **Project Start Date** | 1 April 2009 |
| **Registry Entry** | https://registry.verra.org/app/projectDetail/VCS/981 |
| **Known Credit Buyers** | Microsoft (from project metadata) |
| **Boundary Data Quality** | ⚠ APPROXIMATE — Analysis conducted on rectangular bounding-box approximation derived from project centroid. Exact registered polygon was unavailable. All hectare and percentage figures should be treated as indicative, not definitive. |

---

## 2. COMPLIANCE FLAGS

### FLAG 1 — ADDITIONALITY FAILURE
**Applicable Standard:** VCS Standard §3.4 (Additionality)

VCS Standard §3.4 requires that a project demonstrate it produces GHG emission reductions or removals that are **additional to what would have occurred in the absence of the project activity**. A REDD project must demonstrate that, but for the project intervention, deforestation would have proceeded at a rate exceeding observed project-area outcomes.

**Finding:** The satellite-derived additionality comparison yields a **negative result**. The project area recorded a post-start forest loss rate of **39.9%** (8,367 ha lost from a 2000 baseline of 20,970 ha), while the mean loss rate across five proximate, unprotected control areas of comparable latitude and forest cover is **22.04%**. The project area therefore lost forest at a rate **17.86 percentage points greater** than surrounding unprotected land.

| Area | Forest (2000 ha) | Post-2009 Loss (ha) | Loss Rate (%) |
|---|---|---|---|
| **Project Area (VCS981)** | **20,970** | **8,367** | **39.9** |
| Control 0 | 14,589 | 6,062 | 41.55 |
| Control 1 | 21,695 | 6,702 | 30.89 |
| Control 2 | 16,135 | 2,292 | 14.20 |
| Control 3 | 20,615 | 2,332 | 11.31 |
| Control 4 | 15,955 | 1,956 | 12.26 |
| **Control Mean** | — | — | **22.04** |

This outcome is **prima facie inconsistent** with §3.4. Rather than preventing deforestation relative to unprotected comparators, the project area experienced **materially worse** deforestation outcomes. The project cannot, on this evidence, satisfy the additionality requirement. This is the most serious finding in this brief.

*Caveat:* Control area selection via same-latitude banding is a proxy method. Peer review of control area selection criteria and leakage belt delineation, as required under the applicable REDD methodology, is warranted before final determination.

---

### FLAG 2 — QUANTIFICATION OF GHG EMISSION REDUCTIONS IN QUESTION
**Applicable Standard:** VCS Standard §3.5 (Quantification of GHG Emission Reductions and Removals)

VCS Standard §3.5 requires that emission reductions be **accurately quantified** against a credible baseline, with no systematic overstatement.

**Finding:** The project's claimed emission reductions are predicated on the assumption that deforestation would have been higher absent project activity. The satellite data directly contradicts this premise. Post-project-start loss (8,367 ha; 39.9% of 2000 forest cover) substantially **exceeds pre-project-start loss** (2,077 ha across 2001–2008). Year-by-year Hansen data further reveals that the three peak loss years occurred **during the project's active crediting period**:

| Year | Loss (ha) | Status |
|---|---|---|
| 2014 | 1,197.0 | Project active |
| 2015 | 1,054.4 | Project active |
| **2016** | **3,072.5** | **Project active — single-year peak** |
| 2022 | 694.2 | Project active |

The single-year 2016 loss of **3,072.5 ha** represents approximately **14.7%** of the 2000 forest baseline lost within a single calendar year while the project was purportedly operational and generating carbon credits. This pattern raises a material risk that the baseline scenario was over-estimated and/or that credited emission reductions are correspondingly overstated, in potential violation of §3.5.

---

### FLAG 3 — PERMANENCE / NON-PERMANENCE RISK
**Applicable Standard:** VCS Standard §3.7 (Non-Permanence Risk)

VCS Standard §3.7 requires that AFOLU projects conduct a non-permanence risk assessment and contribute to the AFOLU Pooled Buffer Account commensurate with assessed risk. Continued loss events must be reported and buffer contributions re-evaluated.

**Finding:** Cumulative post-start loss of **8,367 ha (39.9%)** of the project's 2000 forested area constitutes a severe and ongoing reversal event. The NDVI time series corroborates this trajectory:

| Year | Mean NDVI | Forest Cover (%) | Deforested Cover (%) | Scene Date | Cloud (%) |
|---|---|---|---|---|---|
| 2018 | 0.627 | 74.7 | 16.0 | 2018-10-20 | 1.6 |
| 2019 | 0.693 | 79.9 | 8.9 | 2019-08-09 | 8.8 |
| 2020 | 0.673 | 78.1 | 9.3 | 2020-09-07 | 0.9 |
| 2021 | 0.731 | 83.9 | 6.4 | 2021-08-08 | 0.8 |
| 2022 | 0.681 | 79.0 | 7.9 | 2022-07-29 | 5.2 |
| 2023 | 0.618 | 70.3 | 13.7 | 2023-08-30 | 0.0 |
| 2024 | 0.617 | 69.6 | 18.5 | 2024-09-03 | 0.0 |

The deforested-cover fraction rises from **16.0% in 2018** to **18.5% in 2024**, and mean NDVI declines from 0.693 (2019) to 0.617 (2024). Forest cover drops from a relative high of **83.9% (2021)** to **69.6% (2024)** — a **14.3-percentage-point decline in three years**, indicating an accelerating reversal trajectory in the most recent observation window.

Under §3.7, reversals of this magnitude require mandatory buffer pool cancellation and potential suspension of further credit issuances pending remediation verification.

*Caveat:* NDVI figures derive from single-scene annual snapshots at varying acquisition dates (July–October). Seasonal phenology differences between scenes may introduce inter-annual comparability artefacts. Multi-date compositing would be required for definitive permanence accounting.

---

### FLAG 4 — MONITORING DEFICIENCIES
**Applicable Standard:** VCS Standard §3.14 (Monitoring)

VCS Standard §3.14 requires that the project proponent implement a monitoring plan sufficient to detect and report on carbon stock changes, including reversals, at each verification event.

**Finding:** The magnitude of detected losses — particularly **3,072.5 ha in 2016** and **694.2 ha in 2022** — raises the question of whether these events were disclosed in the project's monitoring reports and verification statements. If verified emission reductions were issued for periods encompassing these loss events without corresponding disclosure and buffer cancellation, this represents a monitoring and reporting failure under