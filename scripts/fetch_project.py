"""Day 1: pull boundary + Sentinel-2 + Hansen forest-loss for one project,
write everything to disk, and render a Folium HTML map.

Usage:
    uv run python scripts/fetch_project.py VCS981
    uv run python scripts/fetch_project.py VCS981 --year 2023
    uv run python scripts/fetch_project.py VCS981 --years 2018,2020,2022,2024

Idempotent: re-running skips downloads that are already cached on disk.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import folium  # noqa: E402

from cv import sentinel, hansen, forest_loss  # noqa: E402
from cv.paths import CACHE, PROCESSED  # noqa: E402
from cv.projects import get_project  # noqa: E402


def _parse_years(s: str) -> list[int]:
    return sorted({int(x.strip()) for x in s.split(",") if x.strip()})


def fetch(project_id: str, years: list[int], force: bool = False) -> dict:
    proj = get_project(project_id)
    eff_bbox = proj.effective_bbox
    print(f"[fetch] {proj.id} — {proj.name}  ({proj.country}, {proj.hectares:,} ha)")
    print(f"[fetch] bbox = {eff_bbox}  source={proj.boundary_source}")

    print(f"[sentinel-2] fetching {len(years)} year(s) of best-cloud-free scenes…")
    sentinel_manifests: dict[int, dict] = {}
    for y in years:
        m = sentinel.fetch_year(
            proj.id,
            eff_bbox,
            y,
            asset_keys=("red", "nir", "scl", "visual"),
            preferred_mgrs_tile=proj.preferred_mgrs_tile,
            require_contains_bbox=proj.sentinel_require_contains_bbox,
            force=force,
        )
        sentinel_manifests[y] = m
        if m.get("scene"):
            tile = m["scene"].get("mgrs_tile") or "?"
            print(
                f"  - {y}: {m['scene']['id']}  cloud={m['scene']['cloud_cover']:.2f}%"
                f"  tile={tile}  assets={list(m['local_paths'].keys())}"
            )
        else:
            print(f"  - {y}: no scene under cloud threshold inside dry-season window")

    print("[hansen] fetching tiles for bbox…")
    hansen_paths = hansen.fetch_layers_for_bbox(eff_bbox)
    for layer, paths in hansen_paths.items():
        for p in paths:
            print(f"  - {layer}: {p.name}  ({p.stat().st_size / 1e6:.1f} MB)")

    print("[forest-loss] computing loss summary inside project geometry…")
    summary = forest_loss.loss_summary(
        lossyear_paths=hansen_paths["lossyear"],
        treecover_paths=hansen_paths["treecover2000"],
        geometry=proj.geometry,
        project_start_year=int(proj.project_start[:4]),
    )
    print(
        f"  forest@2000 inside bbox: {summary['forest_2000_ha']:,.0f} ha"
        f" | pre-start loss: {summary['loss_pre_project_start_ha']:,.0f} ha"
        f" | post-start loss: {summary['loss_post_project_start_ha']:,.0f} ha"
    )

    out = {
        "project": {
            "id": proj.id,
            "name": proj.name,
            "country": proj.country,
            "hectares": proj.hectares,
            "project_start": proj.project_start,
            "centroid": [proj.centroid_lat, proj.centroid_lon],
            "bbox": list(eff_bbox),
            "registry_url": proj.registry_url,
            "boundary_source": proj.boundary_source,
        },
        "sentinel": {str(y): m for y, m in sentinel_manifests.items()},
        "hansen": {layer: [str(p) for p in paths] for layer, paths in hansen_paths.items()},
        "forest_loss_summary": summary,
        "fetched_at": datetime.now(UTC).isoformat(),
    }
    out_path = PROCESSED / f"{proj.id}_dataset.json"
    out_path.write_text(json.dumps(out, indent=2))
    print(f"[done] dataset manifest -> {out_path.relative_to(ROOT)}")
    return out


def render_map(project_id: str, dataset: dict) -> Path:
    from shapely.geometry import mapping

    proj = get_project(project_id)
    minx, miny, maxx, maxy = proj.effective_bbox
    centre = [(miny + maxy) / 2.0, (minx + maxx) / 2.0]

    m = folium.Map(location=centre, zoom_start=10, tiles=None, control_scale=True)

    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri World Imagery",
        name="Esri Satellite",
        overlay=False,
        control=True,
    ).add_to(m)
    folium.TileLayer("OpenStreetMap", name="OpenStreetMap", control=True).add_to(m)

    if proj.kml_path:
        folium.GeoJson(
            data=mapping(proj.geometry),
            style_function=lambda _f: {
                "color": "#ff3366", "weight": 2, "fillColor": "#ff3366", "fillOpacity": 0.10,
            },
            tooltip=f"{proj.id} — {proj.name}",
        ).add_to(m)
    else:
        folium.Rectangle(
            bounds=[[miny, minx], [maxy, maxx]],
            color="#ff3366",
            weight=3,
            fill=True,
            fill_opacity=0.05,
            tooltip=f"{proj.id} — {proj.name}",
            popup=folium.Popup(
                f"<b>{proj.name}</b><br>"
                f"{proj.country} — {proj.hectares:,} ha<br>"
                f"Project start: {proj.project_start}<br>"
                f"Boundary: {proj.boundary_source}",
                max_width=320,
            ),
        ).add_to(m)

    folium.CircleMarker(
        location=[proj.centroid_lat, proj.centroid_lon],
        radius=5,
        color="#ffd166",
        fill=True,
        fill_opacity=1.0,
        tooltip="Centroid",
    ).add_to(m)

    folium.LayerControl(collapsed=False).add_to(m)

    out_path = CACHE / f"{proj.id}_map.html"
    m.save(str(out_path))
    print(f"[map] -> {out_path.relative_to(ROOT)}")
    return out_path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project_id")
    parser.add_argument("--years", default="2018,2020,2022,2024")
    parser.add_argument("--force", action="store_true",
                        help="Bypass manifest cache; re-search STAC and re-download assets")
    args = parser.parse_args()
    years = _parse_years(args.years)
    dataset = fetch(args.project_id, years, force=args.force)
    render_map(args.project_id, dataset)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
