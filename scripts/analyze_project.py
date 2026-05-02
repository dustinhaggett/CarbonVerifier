"""Day 2: compute NDVI time series, run additionality test, generate Claude reports.

Usage:
    uv run python scripts/analyze_project.py VCS981
    uv run python scripts/analyze_project.py VCS981 --skip-reports   # analysis only, no Claude API calls
    uv run python scripts/analyze_project.py VCS981 --reports-only   # skip analysis, just regenerate reports

Requires: scripts/fetch_project.py to have been run first for the target project.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cv.ndvi import ndvi_time_series  # noqa: E402
from cv.additionality import run_additionality  # noqa: E402
from cv.paths import CACHE, PROCESSED  # noqa: E402
from cv.projects import get_project  # noqa: E402
from cv.timelapse import build_gif  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project_id")
    parser.add_argument("--skip-reports", action="store_true", help="Skip Claude report generation")
    parser.add_argument("--reports-only", action="store_true", help="Only generate reports (requires prior analysis)")
    args = parser.parse_args()

    proj = get_project(args.project_id)
    dataset_path = PROCESSED / f"{proj.id}_dataset.json"

    if not dataset_path.exists():
        print(f"ERROR: run scripts/fetch_project.py {proj.id} first")
        return 1

    dataset = json.loads(dataset_path.read_text())
    forest_loss_summary = dataset["forest_loss_summary"]

    ndvi_data = None
    additionality_data = None

    if not args.reports_only:
        # --- NDVI time series ---
        years = sorted(int(y) for y in dataset["sentinel"].keys())
        print(f"[ndvi] computing NDVI for {years}…")
        ndvi_data = ndvi_time_series(proj.id, proj.geometry, years)
        for entry in ndvi_data:
            if entry.get("status") == "ok" and entry.get("mean") is not None:
                print(
                    f"  {entry['year']}: mean={entry['mean']:.3f}  "
                    f"forest={entry['pct_forest']:.1f}%  "
                    f"deforested={entry['pct_deforested']:.1f}%"
                )
            else:
                print(f"  {entry['year']}: {entry.get('status', 'error')} (valid_px={entry.get('valid_pixels', '?')})")

        # --- Additionality ---
        print(f"\n[additionality] comparing to 5 control areas…")
        start_year = int(proj.project_start[:4])
        additionality_data = run_additionality(proj.id, proj.geometry, start_year)
        p = additionality_data["project"]
        print(f"  Project loss rate: {p['loss_rate_pct']}%")
        print(f"  Mean control rate: {additionality_data['mean_control_loss_rate_pct']}%")
        print(f"  Verdict: {additionality_data['additionality_verdict']}")

        # --- Time-lapse GIF ---
        print(f"\n[timelapse] rendering animated GIF…")
        gif_path = build_gif(proj.id, proj.effective_bbox, years)
        if gif_path:
            print(f"  -> {gif_path.relative_to(ROOT)} ({gif_path.stat().st_size / 1024:.0f} KB)")
        else:
            print("  no frames built (missing visual assets?)")
    else:
        # Load cached analysis
        ndvi_cache = CACHE / f"{proj.id}_ndvi_timeseries.json"
        add_cache = CACHE / f"{proj.id}_additionality.json"
        if ndvi_cache.exists():
            ndvi_data = json.loads(ndvi_cache.read_text())
        if add_cache.exists():
            additionality_data = json.loads(add_cache.read_text())

    if not args.skip_reports:
        print(f"\n[claude] generating 3 audit reports…")
        from cv.audit_reports import generate_all_reports

        project_info = dataset["project"]
        # Add scandal info from the fixture
        project_info["scandal_notes"] = proj.scandal_notes
        project_info["buyers_known"] = proj.buyers_known

        reports = generate_all_reports(
            project=project_info,
            forest_loss=forest_loss_summary,
            ndvi_series=ndvi_data,
            additionality=additionality_data,
        )
        for rtype, text in reports.items():
            print(f"\n{'='*60}")
            print(f"  {rtype.upper()} REPORT")
            print(f"{'='*60}")
            print(text[:500] + "…" if len(text) > 500 else text)
            print(f"  [full report: data/cache/{proj.id}_{rtype}_report.md]")

    print("\n[done]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
