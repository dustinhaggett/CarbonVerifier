# REGULATORY COMPLIANCE BRIEF

**Prepared by:** Compliance Auditing Division
**Standard Applied:** Verra Verified Carbon Standard (VCS) v4.0 and VCS AFOLU Requirements
**Reference Registry Entry:** VCS985
**Brief Classification:** CONFIDENTIAL — FOR REGULATORY USE

---

## 1. PROJECT IDENTIFICATION

| Field | Detail |
|---|---|
| **VCS Registry ID** | VCS985 |
| **Project Name** | Cordillera Azul National Park REDD+ |
| **Country** | Peru |
| **Registered Area** | 1,351,964 hectares |
| **Project Start Date** | 22 December 2008 |
| **Project Type** | REDD+ (Reducing Emissions from Deforestation and Forest Degradation) |
| **Boundary Source** | WDPA polygon 303320 — registered project geometry; analysis conducted against actual registered boundary, not a bounding-box approximation |
| **Forest Cover at 2000 Baseline** | 1,360,318 ha (Hansen GFC, ≥30% canopy threshold) |
| **Known Credit Offtakers** | Shell; TotalEnergies |
| **Registry URL** | https://registry.verra.org/app/projectDetail/VCS/985 |

---

## 2. COMPLIANCE FLAGS

### FLAG 1 — Additionality (VCS Standard §3.4)

**Severity: HIGH**

VCS Standard §3.4 requires that a project demonstrate GHG emission reductions or removals that are *additional* to what would have occurred in the absence of the project. For REDD+ projects, this requires credible evidence that deforestation was genuinely suppressed relative to a plausible counterfactual baseline scenario.

**Findings:**

The automated additionality comparison against four valid control areas (Control 3, which reports zero forest cover, has been excluded from substantive analysis as non-informative) yields the following results:

| Control Area | Forest @ 2000 (ha) | Post-2008 Loss (ha) | Loss Rate |
|---|---|---|---|
| Control 0 | 1,359,224 | 41,893 | 3.08% |
| Control 1 | 100,167 | 2,156 | 2.15% |
| Control 2 | 1,312,611 | 94,117 | 7.17% |
| Control 4 | 1,351,306 | 40,804 | 3.02% |
| **Mean (Controls 0,1,2,4)** | — | — | **3.86%** |
| **VCS985 (project)** | 1,360,318 | 8,345 | **0.61%** |

The project area lost **0.61%** of its 2000 forest cover post-commencement, against a mean control-area loss rate of **3.86%** — a differential of **3.24 percentage points**. On its face, this differential appears to support an additionality claim.

However, **this audit raises a material additionality concern** for the following reasons:

1. **Pre-existing Protected Status.** Cordillera Azul is a nationally designated National Park. Its low deforestation rate may be substantially attributable to its pre-existing legal protection status rather than to the REDD+ intervention *per se*. VCS Standard §3.4 and the Performance Tool for Estimating Leakage explicitly require that the counterfactual baseline not conflate pre-existing legal restrictions with project-specific interventions. If the park's protected status already suppressed deforestation prior to 2008, the incremental additionality of the REDD+ mechanism requires a higher burden of demonstration.

2. **Pre-Project Loss Rate Was Already Low.** Pre-project loss (2001–2008, inclusive of the partial year 2008) totals approximately **1,777 ha** across approximately 7–8 years (~222–254 ha/year). Post-project loss averages approximately **540 ha/year** (8,345 ha ÷ ~15.5 years). This represents a modest *increase* in average annual loss post-project commencement rather than a reduction, which is inconsistent with the narrative of active forest protection driving carbon credits. This finding warrants scrutiny of whether the baseline scenario adequately accounted for the pre-existing trajectory.

3. **Spike Years Not Adequately Explained.** Years 2013 (1,310.8 ha), 2015 (1,633.6 ha), and 2019 (1,086.8 ha) each represent loss events substantially exceeding the pre-project average annual loss rate. The absence of documented disturbance events or crediting adjustments for these years in the monitoring record would constitute a potential violation of §3.4 (baseline integrity) and §3.14 (monitoring).

**Applicable Standard Provision:** VCS Standard v4.0 §3.4.2; AFOLU Requirements §3.1.6 (baseline credibility for REDD).

---

### FLAG 2 — Quantification of GHG Emission Reductions (VCS Standard §3.5)

**Severity: HIGH**

VCS Standard §3.5 requires that emission reductions be quantified conservatively, completely, and consistently, using approved methodologies, and that claimed reductions reflect actual performance against the approved baseline.

**Findings:**

1. **Aggregate Post-Project Loss Is Non-Trivial.** The satellite record confirms **8,345 ha of forest loss** within the registered project boundary after project start. Depending on the carbon stock assumptions applied under the approved methodology, this represents a potentially significant unaccounted emission source within the project zone. If these losses are not fully deducted from gross credits issued — whether as baseline exceedances, buffer pool contributions, or direct deductions — credits may be over-issued.

2. **Year-on-Year Volatility Suggests Methodological Sensitivity.** The annual loss series is highly variable (range: 66.2 ha in 2010 to 1,633.6 ha in 2015). VCS §3.5.4 requires that quantification methods be applied consistently across monitoring periods. Auditors should verify that loss spikes in 2013, 2015, and 2019 were captured in monitoring reports and reflected in credit issuance adjustments rather than smoothed into multi-year averages.

3. **NDVI Data Inconsistency with Hansen Loss Data.** NDVI snapshots (Sentinel-2, 2018–2024) report deforested area fractions that appear markedly lower than cumulative Hansen-derived loss figures would predict:

| Year | NDVI-Derived Deforested % | Hansen Cumulative Loss (approx. ha) |
|---|---|---|
| 2018 | 1.1% (~14,942 ha implied) | ~5,379 ha |
| 2020 | 0.5% (~6,793 ha implied) | ~5,941 ha |
| 2022 | 0.1% (~1,374 ha implied) | ~6,196 ha |
| 2024 | 0.0% | ~8,345 ha (projected) |

The declining NDVI-deforested percentage across 2018–2024 — despite continued Hansen-detected loss — is anomalous. Possible explanations include forest regrowth on previously disturbed areas (which if occurring would need to be accounted for separately under VCS §3.5), differences in canopy closure thresholds between the two datasets, or cloud-masking artefacts. **This discrepancy has not been resolved and constitutes an unquantified uncertainty in emission reduction claims.**

**Applicable Standard Provision:** VCS Standard v4.0 §3.5.1, §3.5.3, §3.5.4.

---

### FLAG 3 — Non-Permanence Risk (VCS Standard §3.7)

**Severity: MEDIUM**

VCS Standard §3.7 requires that AFOLU projects contribute credits to the AFOLU Pooled Buffer Account commensurate with their assessed non-permanence risk, calculated using the Non-Permanence Risk Tool (NPRT).

**Findings:**

1. **Documented In-Project Loss of 8,345 ha Post-Commencement** increases the empirical non-permanence risk score. The NPRT requires that internal management and socio-economic risk factors be assessed at each verification event. Three high-loss years (2013, 2015, 2019) suggest episodic pressure events that may