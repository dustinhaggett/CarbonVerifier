"""Build a downloadable ZIP bundle of a project's analysis outputs.

Used by the EXPORT_DATA pill in the dashboard top-bar to package, in one click,
everything needed to reproduce or hand off the audit:

  - data/processed/{id}_dataset.json     (boundary, sentinel manifests, hansen
                                           tile paths, forest-loss summary)
  - data/cache/{id}_ndvi_timeseries.json (year-by-year NDVI stats)
  - data/cache/{id}_additionality.json   (project + N controls)
  - data/cache/{id}_*_report.md          (executive / journalist / regulator)
  - data/cache/{id}_timelapse.gif        (animated time-lapse, if rendered)
  - data/cache/{id}_map.html             (Folium boundary preview)
  - manifest.json                         (provenance — ids, model, timestamp)
"""

from __future__ import annotations

import io
import json
import zipfile
from datetime import UTC, datetime

from .paths import CACHE, PROCESSED


def build_zip(project_id: str, project_meta: dict | None = None) -> bytes:
    """Return a single-shot ZIP archive for ``project_id`` as bytes.

    ``project_meta`` is an optional dict (e.g., the in-memory Project) merged
    into the bundle's ``manifest.json`` for provenance."""
    buf = io.BytesIO()
    files: list[tuple[str, bytes]] = []

    # Processed dataset (always)
    for p in [PROCESSED / f"{project_id}_dataset.json"]:
        if p.exists():
            files.append((f"{project_id}/processed/{p.name}", p.read_bytes()))

    # Cache artifacts
    for name in (
        f"{project_id}_ndvi_timeseries.json",
        f"{project_id}_additionality.json",
        f"{project_id}_executive_report.md",
        f"{project_id}_journalist_report.md",
        f"{project_id}_regulator_report.md",
        f"{project_id}_timelapse.gif",
        f"{project_id}_map.html",
    ):
        p = CACHE / name
        if p.exists():
            files.append((f"{project_id}/cache/{p.name}", p.read_bytes()))

    manifest = {
        "project_id": project_id,
        "bundled_at": datetime.now(UTC).isoformat(),
        "files": [name for name, _ in files],
        "tooling": {
            "python": "3.13",
            "model": "claude-sonnet-4-6",
            "package": "CarbonVerifier",
        },
    }
    if project_meta:
        manifest["project"] = project_meta

    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        zf.writestr(f"{project_id}/manifest.json", json.dumps(manifest, indent=2))
        for name, data in files:
            zf.writestr(name, data)

    return buf.getvalue()
