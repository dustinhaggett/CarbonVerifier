"""Claude-powered audit report generator.

Three voices, same satellite data:
1. Executive Brief — for corporate sustainability buyers (1 page, business-focused)
2. Investigative Article — journalism style (600 words, narrative)
3. Regulator Compliance Brief — flags specific Verra Standard violations

Each function returns the generated text as a string.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import anthropic
from dotenv import load_dotenv

load_dotenv(override=True)

MODEL = "claude-sonnet-4-6"


def _client() -> anthropic.Anthropic:
    return anthropic.Anthropic()


def _build_evidence_block(
    project: dict,
    forest_loss: dict,
    ndvi_series: list[dict] | None = None,
    additionality: dict | None = None,
) -> str:
    """Format the satellite evidence into a structured text block for Claude."""
    src = project["boundary_source"]
    if src.startswith("real_kml") or src.startswith("wdpa") or "polygon" in src:
        boundary_label = f"REAL POLYGON ({src}) — analysis reflects the registered project geometry, not a bounding-box approximation."
    elif src.startswith("approximate_bbox"):
        boundary_label = f"BBOX APPROXIMATION ({src}) — headline numbers are computed inside a rectangular approximation centered on the project centroid; exact registered polygon was not available."
    else:
        boundary_label = src

    lines = [
        "=== SATELLITE EVIDENCE PACKAGE ===",
        "",
        f"Project: {project['name']} ({project['id']})",
        f"Country: {project['country']}",
        f"Registered area: {project['hectares']:,} hectares",
        f"Project start: {project['project_start']}",
        f"Boundary: {boundary_label}",
        f"Registry: {project.get('registry_url', 'N/A')}",
    ]

    buyers = project.get("buyers_known") or []
    if buyers:
        lines.append(f"Known credit buyers (from project metadata): {', '.join(buyers)}")
    else:
        lines.append("Known credit buyers: none disclosed in project metadata")

    lines += [
        "",
        "--- HANSEN GLOBAL FOREST CHANGE (2001–2023) ---",
        f"Forest in 2000 (>=30% canopy): {forest_loss['forest_2000_ha']:,.0f} ha",
        f"Loss BEFORE project start: {forest_loss['loss_pre_project_start_ha']:,.0f} ha",
        f"Loss AFTER project start: {forest_loss['loss_post_project_start_ha']:,.0f} ha",
        "",
        "Year-by-year loss (hectares):",
    ]

    for year_str, ha in sorted(forest_loss["loss_by_year_ha"].items(), key=lambda x: int(x[0])):
        year = int(year_str)
        marker = " <<<" if year >= int(project["project_start"][:4]) else ""
        lines.append(f"  {year}: {ha:>8.1f} ha{marker}")

    if forest_loss["forest_2000_ha"] > 0:
        pct = forest_loss["loss_post_project_start_ha"] / forest_loss["forest_2000_ha"] * 100
        lines.append(f"\nPost-start loss as % of 2000 forest: {pct:.1f}%")

    if ndvi_series:
        lines.append("")
        lines.append("--- NDVI TIME SERIES (Sentinel-2, cloud-masked) ---")
        for entry in ndvi_series:
            if entry.get("status") != "ok":
                lines.append(f"  {entry['year']}: {entry.get('status', 'unknown')}")
                continue
            lines.append(
                f"  {entry['year']}: mean={entry['mean']:.3f}  "
                f"forest={entry['pct_forest']:.1f}%  "
                f"deforested={entry['pct_deforested']:.1f}%  "
                f"(scene: {entry['scene_date'][:10]}, cloud: {entry['cloud_cover']:.1f}%)"
            )

    if additionality:
        lines.append("")
        lines.append("--- ADDITIONALITY TEST ---")
        p = additionality["project"]
        lines.append(f"Project loss rate (post-start): {p['loss_rate_pct']}%")
        lines.append(f"Mean control-area loss rate:     {additionality['mean_control_loss_rate_pct']}%")
        if additionality.get("rate_difference_pct") is not None:
            lines.append(f"Difference (control − project):  {additionality['rate_difference_pct']}pp")
        lines.append(f"Verdict: {additionality['additionality_verdict']}")
        lines.append("")
        lines.append("Control areas (nearby unprotected, same latitude band):")
        for c in additionality["controls"]:
            if c.get("error"):
                lines.append(f"  Control {c['index']}: ERROR — {c['error']}")
            else:
                lines.append(
                    f"  Control {c['index']}: "
                    f"forest@2000={c['forest_2000_ha']:,.0f}ha  "
                    f"loss={c['loss_post_start_ha']:,.0f}ha  "
                    f"rate={c['loss_rate_pct']}%"
                )

    lines.append("")
    lines.append("=== END EVIDENCE ===")
    return "\n".join(lines)


EXECUTIVE_SYSTEM = """You are a carbon-credit due-diligence analyst writing for a corporate sustainability officer.

Write a 1-page EXECUTIVE BRIEF. Structure:
1. **Risk Rating** — one of: CRITICAL / HIGH / MODERATE / LOW — with a one-sentence justification
2. **Key Finding** — 2-3 sentences summarizing the satellite evidence
3. **Timeline** — bullet list of the most important dates and deforestation events
4. **Additionality Assessment** — did the project reduce deforestation versus nearby unprotected areas?
5. **Recommended Action** — what should the buyer do? (retire, investigate, write down, hold)

Tone: direct, evidence-based, no hedging. Use numbers from the evidence. Do not speculate beyond what the data shows. If the boundary is approximate, note that in a caveat line at the bottom."""

JOURNALIST_SYSTEM = """You are an investigative environmental journalist at The Guardian.

Write a 600-word article about this carbon credit project based ONLY on the satellite evidence provided. Structure it as a narrative:
- Lead with the most damning or surprising finding
- Walk through the satellite timeline — what the data shows year by year
- Include the additionality comparison if available
- End with what this means for the voluntary carbon market

STRICT FACTUAL CONSTRAINTS — do not violate:
- Name only the buyers explicitly listed in the "Known credit buyers" line of the evidence block. If the line says "none disclosed," do not name any buyer. Never use buyers from training-data knowledge or "similar projects."
- Do not invent quotes, sources, or named individuals.
- Every numeric claim must trace to a number in the evidence block. No estimates, no rounding into different orders of magnitude.
- If a fact is not in the evidence block, leave it out — do not fall back on background knowledge.
- Attribute analytic claims with: "satellite data analyzed by CarbonVerifier".
- If the boundary is approximate, include a caveat paragraph noting that headline numbers reflect a bounding-box approximation, not the registered polygon."""

REGULATOR_SYSTEM = """You are a compliance auditor reviewing this project against the Verra VCS Standard v4.

Write a REGULATORY COMPLIANCE BRIEF. Structure:
1. **Project Identification** — ID, name, country, registered area
2. **Compliance Flags** — for each finding, cite the specific VCS Standard section that may be violated:
   - VCS Standard 3.4 (Additionality)
   - VCS Standard 3.5 (Quantification of GHG emission reductions)
   - VCS Standard 3.7 (Permanence / Non-permanence risk)
   - VCS Standard 3.14 (Monitoring)
   - AFOLU Requirements Section 3.1.6 (Baseline and monitoring for REDD)
3. **Evidence Summary** — key satellite metrics in a table-like format
4. **Recommended Regulatory Action** — investigation, credit invalidation, or corrective action request

Tone: formal, precise, regulatory. Cite section numbers. Use numbers from the evidence. Flag data limitations (approximate boundary, single-scene NDVI snapshots) as caveats."""


def generate_report(
    report_type: str,
    project: dict,
    forest_loss: dict,
    ndvi_series: list[dict] | None = None,
    additionality: dict | None = None,
) -> str:
    """Generate one of three report types.

    report_type: "executive" | "journalist" | "regulator"
    """
    systems = {
        "executive": EXECUTIVE_SYSTEM,
        "journalist": JOURNALIST_SYSTEM,
        "regulator": REGULATOR_SYSTEM,
    }
    if report_type not in systems:
        raise ValueError(f"Unknown report type: {report_type}. Choose from: {list(systems.keys())}")

    evidence = _build_evidence_block(project, forest_loss, ndvi_series, additionality)

    client = _client()
    response = client.messages.create(
        model=MODEL,
        max_tokens=2048,
        system=systems[report_type],
        messages=[
            {
                "role": "user",
                "content": f"Analyze this satellite evidence package and produce your report.\n\n{evidence}",
            }
        ],
    )
    return response.content[0].text


def generate_all_reports(
    project: dict,
    forest_loss: dict,
    ndvi_series: list[dict] | None = None,
    additionality: dict | None = None,
    output_dir: Path | None = None,
) -> dict[str, str]:
    """Generate all three report types. Cache to output_dir if provided."""
    from .paths import CACHE

    out_dir = output_dir or CACHE
    reports = {}

    for rtype in ("executive", "journalist", "regulator"):
        cache_path = out_dir / f"{project['id']}_{rtype}_report.md"
        if cache_path.exists():
            reports[rtype] = cache_path.read_text()
            continue
        text = generate_report(rtype, project, forest_loss, ndvi_series, additionality)
        cache_path.write_text(text)
        reports[rtype] = text

    return reports
