# REGULATORY COMPLIANCE BRIEF

**Prepared by:** Remote Sensing Compliance Analysis Unit
**Document Reference:** AUDIT-2025-ADPML-001
**Standard Applied:** Verra VCS Standard v4.0; AFOLU Requirements
**Date:** 2025

---

## 1. PROJECT IDENTIFICATION

| Field | Detail |
|---|---|
| **Project Name** | Pacajai REDD+ (Portel-Pará) |
| **Registry Acronym** | ADPML |
| **Country** | Brazil |
| **Registry** | Verra (verra.org) |
| **Registered Area** | 148,975 hectares |
| **Project Start Date** | 1 January 2009 |
| **Boundary Source** | Registered KML polygon (real geometry; not bounding-box approximation) |
| **Forest Baseline (2000)** | 123,276 ha (≥30% canopy cover, Hansen GFC) |
| **Known Credit Buyers** | None disclosed in project metadata |

---

## 2. COMPLIANCE FLAGS

### FLAG 1 — Additionality: Contested Counterfactual Scenario
**Applicable Standard:** VCS Standard v4, §3.4 (Additionality); AFOLU Requirements §3.1.6 (Baseline Scenario)

The additionality analysis produces a **WEAK** determination. The project area experienced a post-start forest loss rate of **6.46%** (7,963 ha of 123,276 ha, 2009–2023) against a mean control-area loss rate of **9.98%**. The gross difference of **3.52 percentage points** is marginal and, critically, is undermined by the **extreme heterogeneity of the control portfolio**:

| Control Area | Forest at 2000 (ha) | Post-Period Loss (ha) | Loss Rate |
|---|---|---|---|
| Control 0 | 102,223 | 12,396 | 12.13% |
| Control 1 | 99,326 | 5,266 | **5.30%** |
| Control 2 | 106,946 | 12,122 | 11.34% |
| Control 3 | 86,045 | 3,144 | **3.65%** |
| Control 4 | 90,732 | 15,871 | 17.49% |

Control areas 1 and 3 recorded loss rates of **5.30% and 3.65% respectively — both below the project's own 6.46%**. These observations indicate that comparable unprotected landscapes in the same latitude band experienced *less* deforestation than the project site over the same period. Under VCS Standard §3.4, the project developer must demonstrate that, in the absence of the project activity, land-use change would have continued at or above the baseline rate. Where a subset of plausible counterfactual comparators underperforms the project itself, the baseline scenario selection is materially questionable and may not satisfy the performance standard or regulatory tests required under §3.4.

**Caveat:** Control area selection methodology, spatial adjacency criteria, and weighting logic are not available in this evidence package. The heterogeneity observed may partly reflect legitimate landscape stratification. However, the inclusion of outlier controls (3.65% and 17.49%) without documented justification is itself a compliance concern.

---

### FLAG 2 — Baseline Integrity and Pre-Project Deforestation Pattern
**Applicable Standard:** VCS Standard v4, §3.5 (Quantification); AFOLU Requirements §3.1.6

Pre-project loss (2001–2008) totalled **1,459 ha**, with a pronounced acceleration in the final pre-project year: **485.2 ha in 2008** alone — more than three times the annual average for 2001–2007 (~138.8 ha/year). This spike is noted as follows:

| Period | Total Loss (ha) | Annual Average (ha/yr) |
|---|---|---|
| 2001–2007 | 973.5 | 139.1 |
| 2008 (final pre-project year) | 485.2 | 485.2 |
| 2009–2023 (post-start) | 7,963.0 | 530.9 |

A sharp pre-project deforestation peak in the year immediately preceding project registration is a recognized indicator of **baseline inflation risk** — wherein elevated reference-period emissions artificially increase the credited abatement volume. VCS Standard §3.5 and AFOLU §3.1.6 require that baseline emission rates reflect a realistic counterfactual and are not inflated by anomalous land-use activity. The 2008 spike warrants scrutiny as to whether it reflects genuine landscape pressure or was influenced by project proponent activity or strategic timing of registration.

---

### FLAG 3 — Quantification Integrity: Continued and Substantial Post-Project Loss
**Applicable Standard:** VCS Standard v4, §3.5 (Quantification of GHG Emission Reductions)

Notwithstanding the project's credited operation since 2009, **7,963 ha of forest loss** has been recorded within the project boundary across the 2009–2023 period — equivalent to **6.5% of the entire 2000 forest stock** and an annual average of **530.9 ha/year**. Several post-project years recorded losses that individually exceed the entire pre-project annual average:

| Year | Loss (ha) | Significance |
|---|---|---|
| 2016 | 998.8 | Highest single year on record |
| 2017 | 984.7 | Second highest |
| 2023 | 828.5 | Third highest; recent acceleration |
| 2014 | 641.2 | Exceeds 2008 peak |
| 2020 | 701.1 | Elevated during monitoring period |

The recurrence of high-loss years throughout the project's operational life — including in 2023, the most recent data year — raises material concerns under §3.5 regarding whether gross emission reductions are being overstated in verification reports relative to actual forest conditions. Auditors should compare these Hansen-derived loss figures against loss figures submitted in project monitoring reports and validated Verification Reports (VRs) for discrepancies.

---

### FLAG 4 — NDVI Data Inconsistency with Forest Loss Record
**Applicable Standard:** VCS Standard v4, §3.14 (Monitoring); AFOLU Requirements §3.1.6

The Sentinel-2 NDVI time series presents a significant apparent contradiction with the Hansen GFC loss record:

| Scene Date | Mean NDVI | Classified Forest (%) | Classified Deforested (%) | Cloud Cover |
|---|---|---|---|---|
| 2018-09-01 | 0.785 | 96.1% | 0.1% | 5.5% |
| 2020-09-05 | 0.827 | 99.6% | 0.0% | 1.2% |
| 2022-10-05 | 0.765 | 97.1% | 0.1% | 9.4% |
| 2024-07-11 | 0.823 | 99.7% | 0.0% | 9.0% |

The NDVI scenes consistently classify **96.1%–99.7% of the project area as forested** and record near-zero deforestation fractions. Yet Hansen GFC records **cumulative post-2009 losses of 7,963 ha**, including **828.5 ha in 2023 alone**. This divergence may reflect: (a) vegetation regrowth masking prior clearance in single-scene snapshots; (b) seasonal NDVI bias (all scenes are dry-season acquisitions, July–October); (c) cloud-masking artifacts at 9.0–9.4% cloud cover in 2022 and 2024 scenes; or (d) NDVI classification thresholds not calibrated to distinguish degraded from intact forest.

**Critical Caveat:** These NDVI values are derived from **single annual scenes**, not multi-temporal composites. Single-scene NDVI snapshots are methodologically insufficient to characterize annual deforestation dynamics and do not constitute an adequate monitoring dataset under VCS Standard §3.14, which requires that monitoring systems be capable of detecting and quantifying all material sources of emission reductions and removals.

If a project's internal monitoring relies on single-scene NDVI analysis