"""Try to download a project's KML from the Verra registry.

Walks the project's documentGroups via the public registry API
(``/uiapi/resource/resourceSummary/{vcs_id}``) looking for any document with
documentType == "KML File", then downloads the matching ``Project_ViewFile.asp``
URI to ``data/raw/verra/``.

Usage:
    uv run python scripts/fetch_verra_kml.py 832          # Cikel
    uv run python scripts/fetch_verra_kml.py 832 --out custom_name.kml

Note: Not every project hosts a KML — some only have shapefiles inside ZIP'd
PDD attachments, or no spatial data at all. Run it once per project ID; if no
KML is found the script prints which document types ARE available so you know
what alternative to chase manually.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cv.paths import VERRA_DIR  # noqa: E402

API = "https://registry.verra.org/uiapi/resource/resourceSummary/{vcs_id}"


def _walk_for_kml(node, results):
    if isinstance(node, dict):
        if node.get("documentType") == "KML File" and node.get("uri"):
            results.append(node)
        for v in node.values():
            _walk_for_kml(v, results)
    elif isinstance(node, list):
        for v in node:
            _walk_for_kml(v, results)


def _walk_for_doc_types(node, types):
    if isinstance(node, dict):
        t = node.get("documentType")
        if t:
            types.add(t)
        for v in node.values():
            _walk_for_doc_types(v, types)
    elif isinstance(node, list):
        for v in node:
            _walk_for_doc_types(v, types)


def download_kml(vcs_id: int | str, out_name: str | None = None) -> Path | None:
    url = API.format(vcs_id=vcs_id)
    print(f"[verra] GET {url}")
    with urllib.request.urlopen(url, timeout=30) as resp:
        meta = json.loads(resp.read())

    name = meta.get("resourceName", "?")
    loc = meta.get("location") or {}
    print(f"[verra] {vcs_id}: {name}")
    print(f"[verra] location: lat={loc.get('latitude')}  lon={loc.get('longitude')}")

    kmls: list[dict] = []
    _walk_for_kml(meta.get("documentGroups", []), kmls)

    if not kmls:
        types: set[str] = set()
        _walk_for_doc_types(meta.get("documentGroups", []), types)
        print(f"[verra] no KML files registered. Available document types:")
        for t in sorted(types):
            print(f"          - {t}")
        return None

    print(f"[verra] {len(kmls)} KML file(s) found:")
    for k in kmls:
        print(f"          - {k.get('documentName','?')}  ({k.get('uploadDate','')})")

    target = kmls[0]
    fname = out_name or f"VCS{vcs_id}_{target.get('documentName','project').replace('/', '_')}"
    out_path = VERRA_DIR / fname
    print(f"[verra] downloading -> {out_path}")
    urllib.request.urlretrieve(target["uri"], out_path)
    print(f"[verra] done · {out_path.stat().st_size / 1024:.1f} KB")
    return out_path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("vcs_id", help="Verra project ID, e.g. 832 for Cikel")
    parser.add_argument("--out", help="Override output filename")
    args = parser.parse_args()
    p = download_kml(args.vcs_id, out_name=args.out)
    return 0 if p else 1


if __name__ == "__main__":
    raise SystemExit(main())
