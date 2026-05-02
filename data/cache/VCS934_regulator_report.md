# REGULATORY COMPLIANCE BRIEF

**Prepared by:** Compliance Audit Division — Remote Sensing & Carbon Market Integrity Unit
**Reference File:** VCS934-AUDIT-2024
**Standard Applied:** Verra Verified Carbon Standard (VCS) v4; AFOLU Requirements v4
**Date of Analysis:** 2024
**Classification:** FORMAL REGULATORY FINDING

---

## 1. PROJECT IDENTIFICATION

| Field | Detail |
|---|---|
| **Registry ID** | VCS934 |
| **Project Name** | Mai Ndombe REDD+ Project |
| **Country** | Democratic Republic of the Congo |
| **Registered Area** | 299,640 hectares |
| **Project Start Date** | 25 February 2011 |
| **Registry Entry** | https://registry.verra.org/app/projectDetail/VCS/934 |
| **Boundary Source** | Registered project geometry (KML polygon); analysis reflects actual registered boundary, not a bounding-box approximation |
| **Known Credit Buyers (from metadata)** | Salesforce, Engie |
| **Data Sources** | Hansen Global Forest Change v1.11 (2001–2023); Sentinel-2 NDVI time series (2018–2024, cloud-masked) |

---

## 2. COMPLIANCE FLAGS

### FLAG 1 — ADDITIONALITY FAILURE
**Applicable Standard:** VCS Standard v4, Section 3.4 (Additionality); AFOLU Requirements v4, Section 3.1.6

**Finding — HIGH SEVERITY**

The satellite-derived additionality test yields a result directly contrary to the project's fundamental eligibility premise. The post-start project-area deforestation rate (**7.08%** of year-2000 forest cover, covering 19,820 ha across the period 2011–2023) exceeds the mean control-area deforestation rate of **5.61%** across five geographically comparable, unprotected control zones in the same latitude band. The directional difference is **−1.47 percentage points**, meaning the project area lost forest at a *higher* rate than controls, not a lower one.

VCS Standard Section 3.4 requires that a project demonstrate it produces GHG emission reductions or removals that are additional to what would have occurred in the absence of the project. Where a REDD+ project's forest loss rate meets or exceeds that of unprotected comparable landscapes, the foundational additionality claim is unsupported by observed outcomes.

**Specific observations of concern:**

- Year 2013 recorded a loss spike of **4,257.6 ha** — the single largest annual loss event in the entire 2001–2023 record, occurring two years *after* project registration and activities were ostensibly underway.
- Years 2018, 2020, 2023 each recorded losses exceeding **1,957–2,451 ha/year**, all substantially above the pre-project annual average of approximately **754 ha/year** (2001–2010, 6,741 ha over 10 years, excluding the anomalous 2010 spike of 1,927.6 ha).
- The post-start 12-year average annual loss rate is approximately **1,524 ha/year**, roughly double the pre-project decadal mean.

**Caveat:** The five control areas show significant internal variance (Control 0: 0.64%; Control 3: 14.75%), indicating landscape heterogeneity. A single mean comparison has statistical limitations. Nonetheless, the direction of the finding is unambiguous and warrants investigation.

---

### FLAG 2 — POTENTIAL OVER-CREDITING / BASELINE MISREPRESENTATION
**Applicable Standard:** VCS Standard v4, Section 3.5 (Quantification of GHG Emission Reductions and Removals); AFOLU Requirements v4, Section 3.1.6

**Finding — HIGH SEVERITY**

Section 3.5 requires that quantification of emission reductions be conservative, accurate, and verifiable, and that baseline scenarios be credibly established. Section 3.1.6 of the AFOLU Requirements specifically mandates that REDD+ baselines reflect projected deforestation rates with adequate reference-region data.

The evidence raises the following quantification concerns:

1. **Elevated post-project loss against a claimed suppressed baseline:** If the project baseline was set using pre-2011 rates (approximately 674 ha/year average 2001–2010), and credits were issued against the claimed reduction in deforestation relative to that baseline, then credits issued during peak-loss years (2013: 4,257.6 ha; 2018: 2,264.1 ha; 2023: 2,450.7 ha) would correspond to periods of *actual net forest destruction*, not conservation. This inverts the crediting logic.

2. **Cumulative post-start loss of 19,820 ha is 193% of pre-start loss (6,741 ha):** If credits were issued for avoided deforestation on the premise that the project reduced pressures relative to business-as-usual, the empirical record does not support that claim across the 2011–2023 period.

3. **Possible baseline manipulation risk:** A project proponent could overstate the counterfactual deforestation rate to inflate the credit volume. The observed outcome — where project-area rates exceed control-area rates — is consistent with, though not conclusively probative of, an inflated baseline scenario.

---

### FLAG 3 — NON-PERMANENCE / BUFFER POOL ADEQUACY
**Applicable Standard:** VCS Standard v4, Section 3.7 (Non-Permanence Risk Assessment and Buffer Withholding)

**Finding — MEDIUM-HIGH SEVERITY**

Section 3.7 requires that AFOLU projects complete a non-permanence risk assessment and withhold an appropriate volume of credits in a pooled buffer account to cover the risk of reversal. Risk factors assessed include political/governance risk, financial viability, land tenure, and deforestation pressure.

The following observed data points are material to the non-permanence risk profile:

- **Post-start loss of 19,820 ha (7.1% of 2000 forest cover)** represents a substantial and continuing reversal of any claimed forest protection.
- **2023 annual loss of 2,450.7 ha** is the highest single-year loss in the entire 23-year record, occurring in the project's 13th year of operation — indicating *accelerating*, not declining, deforestation pressure.
- **NDVI mean decline from 0.746 (2020) to 0.635 (2024):** A drop of **0.111 NDVI units** (approximately 14.9% relative decline) in four years is a material degradation signal. This is the sharpest inter-period NDVI decline in the observed time series and coincides with continued high annual loss figures.

If the buffer pool contribution was calibrated on an initial non-permanence risk assessment that did not anticipate a 13-year trend of elevated deforestation and a late-period NDVI collapse, that buffer may be materially insufficient to cover actual reversals. A reassessment under VCS Standard Section 3.7.14–3.7.15 may be required.

**Caveat on NDVI data:** The NDVI figures are single-scene annual snapshots (one acquisition per year). The 2024 scene (mean NDVI 0.635, 2024-08-04) is the most recent observation but represents a single date and may be influenced by phenological variation or residual cloud contamination (cloud cover 5.2%, within acceptable limits). The declining trend across multiple years nonetheless warrants attention.

---

### FLAG 4 — MONITORING DEFICIENCY RISK
**Applicable Standard:** VCS Standard v4, Section 3.14 (Monitoring); AFOLU Requirements v4, Section 3.1.6

**Finding — MEDIUM SEVERITY**

Section 3.14 requires that monitoring plans detect, measure, and report all material changes in carbon stocks, including degradation events, within the project boundary. Monitoring reports must be submitted to third-party verification at intervals not exceeding five years.

The satellite record raises questions about whether project monitoring has adequately captured and reported:

1. **The 2013 deforestation event (4,257.6 ha in a single year):** This represents a sudden six-fold increase over the prior year (2012: 491.6 ha) and the largest single-year event in the dataset. It is not consistent with a managed, monitored REDD+ project operating under normal conditions without documented explanation (e.g., extreme weather, documented agricultural encroachment response).

2. **The 2018 loss