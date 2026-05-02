# REGULATORY COMPLIANCE BRIEF

**Prepared by:** Compliance Audit Division — VCS Standard v4 Review
**Subject:** VCS832 — Cikel Brazilian Amazon REDD APD (Avoiding Planned Deforestation)
**Audit Date:** 2025
**Document Status:** DRAFT FOR REGULATORY REVIEW

---

## 1. PROJECT IDENTIFICATION

| Field | Detail |
|---|---|
| **Registry ID** | VCS832 |
| **Project Name** | Cikel Brazilian Amazon REDD APD — Avoiding Planned Deforestation |
| **Country / Jurisdiction** | Brazil (Amazon biome) |
| **Registered Area** | 27,435 hectares |
| **Project Start Date** | 1 April 2009 |
| **Registry URL** | https://registry.verra.org/app/projectDetail/VCS/832 |
| **Known Credit Purchaser** | Microsoft (per project metadata) |
| **Boundary Source** | Real registered KML polygon; analysis reflects registered project geometry |
| **Primary Data Sources** | Hansen Global Forest Change v1.11 (2001–2023); Sentinel-2 NDVI time series (2018–2024) |

---

## 2. COMPLIANCE FLAGS

### FLAG 1 — ADDITIONALITY CONCERN (PARTIALLY MITIGATED)
**Applicable Standard:** VCS Standard v4, Section 3.4 (Additionality)

VCS Standard §3.4 requires demonstration that GHG emission reductions are additional to what would have occurred in the absence of the project. This is typically demonstrated by showing the project scenario diverges materially from the baseline scenario.

**Finding:** The satellite evidence presents a **facially strong additionality signal**. The post-project-start forest loss rate within the project boundary is **2.12%** over the 2009–2023 period (14 years), compared to a mean control-area loss rate of **27.1%** across five nearby unprotected areas in the same latitude band — a difference of **24.98 percentage points**. This differential is substantial and directionally consistent with genuine avoided deforestation.

**However, the following sub-findings require regulatory scrutiny:**

**(a) Control Area Heterogeneity:** Control area loss rates range from **8.44%** (Control 2) to **37.28%** (Control 1). The spread of ~29 percentage points across controls introduces significant uncertainty into the baseline deforestation rate used to quantify avoided emissions. If the registered baseline was calibrated against the higher-loss controls while Control 2 is more comparably situated, the baseline — and therefore issued credits — may be materially overstated. Verification bodies should confirm which controls, and which weighting methodology, were used in the registered Project Description and Monitoring Reports.

**(b) Pre-Project Loss Trend:** Pre-start loss (2001–2008) totaled **1,622 ha**, with a pronounced spike in 2005 (**546.3 ha**) and 2008 (**489.8 ha**). The substantial year-to-year variance in the pre-project baseline period may have inflated the historical deforestation reference rate. §3.4 requires that the additionality demonstration not rely on a baseline period that is unrepresentative or selectively chosen.

---

### FLAG 2 — QUANTIFICATION CONCERN (SIGNIFICANT)
**Applicable Standard:** VCS Standard v4, Section 3.5 (Quantification of GHG Emission Reductions and Removals)

**Finding:** Post-project-start Hansen-detected loss totals **4,363 ha** across 2009–2023, representing **2.1%** of the 2000 forest extent within the project boundary (**205,961 ha**). While the aggregate rate is low, the **year-level loss distribution reveals a sharply non-uniform pattern** that raises quantification concerns:

| Period | Years | Total Loss (ha) | Annual Mean (ha/yr) |
|---|---|---|---|
| Early project (2009–2014) | 6 | 368.1 | 61.4 |
| Mid project (2015–2018) | 4 | 2,551.4 | 637.9 |
| Late project (2019–2023) | 5 | 1,443.4 | 288.7 |

The **2015–2018 sub-period is anomalous**. Loss in 2016 alone reached **1,233.5 ha** — more than **25 times** the annual average of the 2009–2014 period and representing **28.3%** of all post-start loss in a single year. Loss in 2017 (**517.9 ha**) and 2018 (**413.3 ha**) likewise remain substantially elevated. This surge coincides with known deterioration in Brazilian forest governance under shifts in IBAMA enforcement capacity and political pressure on forest agencies during 2015–2019.

§3.5 requires that emission reductions be accurately quantified and that monitoring and quantification account for actual conditions. **If monitoring reports for the 2016–2018 vintages did not fully capture and deduct the ~2,165 ha of loss occurring in those three years from credit issuance calculations, credits issued for those periods may be overstated.** Verification bodies and Verra should confirm that ex-post monitoring adjustments were applied.

---

### FLAG 3 — NON-PERMANENCE / BUFFER POOL ADEQUACY (SIGNIFICANT)
**Applicable Standard:** VCS Standard v4, Section 3.7 (Non-Permanence Risk); AFOLU Requirements Section 3.1.6

**Finding:** The project's post-start loss trajectory — specifically the **2015–2019 elevated loss episode** — constitutes a documented **temporary reversal event** that must be assessed against the non-permanence risk framework under §3.7. VCS AFOLU projects are required to hold buffer credits in the AFOLU Pooled Buffer Account calibrated to their non-permanence risk score.

Key concerns:

**(a) Reversal Materiality:** The 2016 loss event (1,233.5 ha) and the cumulative 2015–2019 loss (~2,579 ha) represent a significant intra-project departure from the early-project performance baseline. Under §3.7.10–3.7.15, reversals of this magnitude in an AFOLU project trigger reassessment of buffer contributions and, potentially, cancellation of buffer credits.

**(b) Forest Persistence Evidence from NDVI:** NDVI data offers partial reassurance. The 2020 scene records a mean NDVI of **0.861** and forest cover of **97.7%**, suggesting partial recovery or stabilization following the loss spike. However, the 2024 scene records a decline to mean NDVI **0.827** and **deforested fraction of 2.2%** — the highest deforested fraction in the NDVI record — indicating continued or renewed pressure. This trajectory should be flagged to the buffer pool administrator.

**(c) Caveat — NDVI Snapshot Limitation:** The NDVI record comprises **four single-scene observations** (2018, 2020, 2022, 2024), not a continuous time series. Seasonal phenology differences between scenes (e.g., the 2018 scene acquired 23 October vs. 2020 scene acquired 8 August) may affect NDVI comparability. The 2018 lower NDVI (0.774) may partly reflect late-dry-season senescence rather than structural forest degradation. **These NDVI observations should be treated as indicative, not definitive**, pending full dense time-series analysis.

---

### FLAG 4 — MONITORING DEFICIENCY RISK (MODERATE)
**Applicable Standard:** VCS Standard v4, Section 3.14 (Monitoring); AFOLU Requirements Section 3.1.6 (Baseline and Monitoring for REDD)

**Finding:** §3.14 requires that monitoring reports accurately capture actual carbon stock changes within the project boundary at each verification period. §3.1.6 specifically requires REDD projects to monitor forest cover change using an approved methodology and to report deforestation annually or at each monitoring interval.

**(a) 2016 Loss Anomaly:** The 1,233.5 ha loss in 2016 should have been captured in the monitoring report covering that period. Given that the project area is only **27,435 ha**, a single-year loss of **1,233.5 ha represents 4.5% of the total registered area** — a loss magnitude that would be conspicuous in any remotely sensed monitoring exercise. Regulatory review should confirm whether this