"""Additionality test: compare deforestation inside the project geometry to
nearby control areas of similar shape and biome that have no carbon project.

Methodology: translate the project geometry east/west along the same latitude
band by multiples of its bbox-width to produce N control geometries. Compute
Hansen forest-loss inside each. Report whether the project area outperformed
(less loss than) the controls.

For projects defined by a bbox-only approximation, the control is also a bbox;
for projects with a real polygon, the control is a translated copy of the
exact polygon — same area, same shape, same latitude.
"""

from __future__ import annotations

import json

import numpy as np
from shapely.affinity import translate
from shapely.geometry import MultiPolygon, box
from shapely.geometry.base import BaseGeometry

from .forest_loss import loss_summary
from .hansen import fetch_layers_for_bbox
from .paths import CACHE


def generate_controls(geom: BaseGeometry, n: int = 5) -> list[BaseGeometry]:
    """Place N control geometries at increasing east/west offsets, alternating
    sides, keeping the same latitude band as the project."""
    minx, _, maxx, _ = geom.bounds
    width = maxx - minx
    out: list[BaseGeometry] = []
    for i in range(1, n + 1):
        sign = 1 if i % 2 == 1 else -1
        offset = sign * width * (1.5 + (i // 2))
        out.append(translate(geom, xoff=offset, yoff=0.0))
    return out


def _bounds(geom: BaseGeometry) -> tuple[float, float, float, float]:
    minx, miny, maxx, maxy = geom.bounds
    return (minx, miny, maxx, maxy)


def run_additionality(
    project_id: str,
    project_geom: BaseGeometry | tuple[float, float, float, float],
    project_start_year: int,
    n_controls: int = 5,
) -> dict:
    """Compute loss rates for the project and N controls; return comparison dict."""
    if isinstance(project_geom, tuple):
        project_geom = MultiPolygon([box(*project_geom)])

    controls = generate_controls(project_geom, n_controls)

    project_hansen = fetch_layers_for_bbox(_bounds(project_geom))
    project_summary = loss_summary(
        project_hansen["lossyear"],
        project_hansen["treecover2000"],
        geometry=project_geom,
        project_start_year=project_start_year,
    )

    control_summaries: list[dict] = []
    for i, ctrl_geom in enumerate(controls):
        try:
            ctrl_hansen = fetch_layers_for_bbox(_bounds(ctrl_geom))
            ctrl_summary = loss_summary(
                ctrl_hansen["lossyear"],
                ctrl_hansen["treecover2000"],
                geometry=ctrl_geom,
                project_start_year=project_start_year,
            )
            ctrl_summary["control_index"] = i
            control_summaries.append(ctrl_summary)
        except Exception as e:
            control_summaries.append(
                {"control_index": i, "bbox": list(_bounds(ctrl_geom)), "error": str(e)}
            )

    def _loss_rate(s: dict) -> float | None:
        if s.get("forest_2000_ha", 0) == 0:
            return None
        return s["loss_post_project_start_ha"] / s["forest_2000_ha"] * 100

    project_rate = _loss_rate(project_summary)
    valid_control_rates = [_loss_rate(s) for s in control_summaries if "forest_2000_ha" in s]
    valid_control_rates = [r for r in valid_control_rates if r is not None]
    mean_control_rate = float(np.mean(valid_control_rates)) if valid_control_rates else None

    result = {
        "project_id": project_id,
        "project_start_year": project_start_year,
        "project": {
            "bbox": list(_bounds(project_geom)),
            "forest_2000_ha": project_summary["forest_2000_ha"],
            "loss_post_start_ha": project_summary["loss_post_project_start_ha"],
            "loss_rate_pct": round(project_rate, 2) if project_rate else None,
        },
        "controls": [
            {
                "index": s.get("control_index", i),
                "bbox": s.get("bbox", list(_bounds(controls[i]))),
                "forest_2000_ha": s.get("forest_2000_ha"),
                "loss_post_start_ha": s.get("loss_post_project_start_ha"),
                "loss_rate_pct": round(_loss_rate(s), 2) if _loss_rate(s) is not None else None,
                "error": s.get("error"),
            }
            for i, s in enumerate(control_summaries)
        ],
        "mean_control_loss_rate_pct": round(mean_control_rate, 2) if mean_control_rate else None,
        "additionality_verdict": None,
    }

    if project_rate is not None and mean_control_rate is not None:
        diff = mean_control_rate - project_rate
        if diff > 5:
            verdict = "STRONG — project lost significantly less forest than controls"
        elif diff > 0:
            verdict = "WEAK — project lost slightly less forest than controls"
        elif diff > -5:
            verdict = "NONE — project performed about the same as controls"
        else:
            verdict = "NEGATIVE — project lost MORE forest than surrounding unprotected areas"
        result["additionality_verdict"] = verdict
        result["rate_difference_pct"] = round(diff, 2)

    out_path = CACHE / f"{project_id}_additionality.json"
    out_path.write_text(json.dumps(result, indent=2))
    return result
