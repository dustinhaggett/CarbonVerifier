"""Sentinel-2 STAC client (Element 84, no auth required).

Picks the least-cloudy scene whose footprint FULLY contains the project bbox
(prevents split-MGRS-tile artifacts), inside an optional dry-season month
window (prevents seasonal phenology confounds), then downloads the requested
asset bands. Caches by (project_id, year); idempotent re-runs are a no-op."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

import requests
from pystac_client import Client
from shapely.geometry import box, shape

from .paths import SENTINEL_DIR

STAC_URL = "https://earth-search.aws.element84.com/v1"
COLLECTION = "sentinel-2-l2a"

DEFAULT_ASSET_KEYS = ("red", "nir", "scl", "visual")
DEFAULT_DRY_MONTHS = (8, 10)


def _client() -> Client:
    return Client.open(STAC_URL)


def _date_ranges_for_window(year: int, dry_months: tuple[int, int]) -> str:
    """Build a STAC datetime string covering the specified month window in the year."""
    start_m, end_m = dry_months
    last_day = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,
                7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}[end_m]
    return f"{year}-{start_m:02d}-01T00:00:00Z/{year}-{end_m:02d}-{last_day:02d}T23:59:59Z"


def _mgrs_of(item: dict) -> str | None:
    """Return the MGRS tile id from a STAC item, or None."""
    props = item.get("properties", {})
    return props.get("s2:mgrs_tile") or props.get("mgrs:utm_zone")


def search_scenes(
    bbox: tuple[float, float, float, float],
    start: str,
    end: str,
    max_cloud_cover: float = 20.0,
    limit: int = 30,
    require_contains_bbox: bool = True,
    preferred_mgrs_tile: str | None = None,
) -> list[dict]:
    """Return scenes ordered by (preferred-tile-first, then cloud cover)."""
    search = _client().search(
        collections=[COLLECTION],
        bbox=list(bbox),
        datetime=f"{start}/{end}",
        query={"eo:cloud_cover": {"lt": max_cloud_cover}},
        max_items=limit,
    )
    items = [it.to_dict() for it in search.items()]

    project_geom = box(*bbox)
    project_area = project_geom.area or 1.0

    if require_contains_bbox:
        items = [it for it in items if shape(it["geometry"]).contains(project_geom)]

    def _rank(it: dict) -> tuple:
        cloud = it["properties"].get("eo:cloud_cover", 100.0)
        scene_geom = shape(it["geometry"])
        intersection = scene_geom.intersection(project_geom)
        # Coverage fraction of the project bbox covered by this scene's footprint.
        coverage = (intersection.area / project_area) if project_area > 0 else 0.0
        is_preferred = (preferred_mgrs_tile is not None and _mgrs_of(it) == preferred_mgrs_tile)
        # Sort: preferred tile first → max coverage → min cloud cover.
        return (0 if is_preferred else 1, -coverage, cloud)

    items.sort(key=_rank)
    return items


def best_scene(
    bbox: tuple[float, float, float, float],
    year: int,
    max_cloud_cover: float = 20.0,
    dry_months: tuple[int, int] | None = DEFAULT_DRY_MONTHS,
    require_contains_bbox: bool = True,
    preferred_mgrs_tile: str | None = None,
    intersect_fallback: bool = True,
) -> dict | None:
    """Pick the best scene for a year. Preference order:
       1. dry-season window, preferred MGRS tile, lowest cloud
       2. dry-season window, any tile, lowest cloud
       3. full year, preferred MGRS tile, lowest cloud
       4. full year, any tile, lowest cloud
    Each fallback only fires if the previous tier returned zero matches —
    so we never silently lose a year."""
    if dry_months is not None:
        window = _date_ranges_for_window(year, dry_months)
        start, end = window.split("/")
        items = search_scenes(
            bbox, start, end,
            max_cloud_cover=max_cloud_cover,
            require_contains_bbox=require_contains_bbox,
            preferred_mgrs_tile=preferred_mgrs_tile,
        )
        if items and (preferred_mgrs_tile is None or _mgrs_of(items[0]) == preferred_mgrs_tile):
            return items[0]
        if items:
            # Fall through to full-year search before giving up on tile preference
            pass

    items = search_scenes(
        bbox,
        start=f"{year}-01-01T00:00:00Z",
        end=f"{year}-12-31T23:59:59Z",
        max_cloud_cover=max_cloud_cover,
        require_contains_bbox=require_contains_bbox,
        preferred_mgrs_tile=preferred_mgrs_tile,
    )
    if items:
        return items[0]

    # Last-resort fallback for large bboxes that exceed any single scene.
    # Pick the scene whose footprint OVERLAPS the bbox the most, ranked by
    # intersection-area DESC then cloud cover ASC.
    if require_contains_bbox and intersect_fallback:
        relaxed = search_scenes(
            bbox,
            start=f"{year}-01-01T00:00:00Z",
            end=f"{year}-12-31T23:59:59Z",
            max_cloud_cover=max_cloud_cover,
            require_contains_bbox=False,
            preferred_mgrs_tile=preferred_mgrs_tile,
        )
        if relaxed:
            project_geom = box(*bbox)
            relaxed.sort(
                key=lambda it: (
                    -shape(it["geometry"]).intersection(project_geom).area,
                    it["properties"].get("eo:cloud_cover", 100.0),
                )
            )
            return relaxed[0]
    return None


def download_asset(item: dict, asset_key: str, out_path: Path, force: bool = False) -> Path:
    if not force and out_path.exists() and out_path.stat().st_size > 0:
        return out_path
    href = item["assets"][asset_key]["href"]
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with requests.get(href, stream=True, timeout=120) as r:
        r.raise_for_status()
        tmp = out_path.with_suffix(out_path.suffix + ".part")
        with tmp.open("wb") as fh:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    fh.write(chunk)
        tmp.rename(out_path)
    return out_path


def fetch_year(
    project_id: str,
    bbox: tuple[float, float, float, float],
    year: int,
    asset_keys: tuple[str, ...] = DEFAULT_ASSET_KEYS,
    dry_months: tuple[int, int] | None = DEFAULT_DRY_MONTHS,
    preferred_mgrs_tile: str | None = None,
    require_contains_bbox: bool = True,
    force: bool = False,
) -> dict:
    """Pick best scene and download requested assets, writing a manifest sidecar.

    With ``force=True``, the manifest cache is bypassed and assets are
    re-downloaded — use after tightening selection rules to refresh stale picks."""
    out_dir = SENTINEL_DIR / project_id / str(year)
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = out_dir / "manifest.json"

    if not force and manifest_path.exists():
        manifest = json.loads(manifest_path.read_text())
        if all((out_dir / Path(p).name).exists() for p in manifest.get("local_paths", {}).values()):
            return manifest

    item = best_scene(
        bbox,
        year,
        dry_months=dry_months,
        preferred_mgrs_tile=preferred_mgrs_tile,
        require_contains_bbox=require_contains_bbox,
    )
    if item is None:
        manifest = {"project_id": project_id, "year": year, "scene": None, "local_paths": {}}
        manifest_path.write_text(json.dumps(manifest, indent=2))
        return manifest

    local_paths: dict[str, str] = {}
    for key in asset_keys:
        if key not in item["assets"]:
            continue
        href = item["assets"][key]["href"]
        suffix = ".tif" if href.lower().endswith((".tif", ".tiff")) else Path(href).suffix or ".bin"
        out = out_dir / f"{key}{suffix}"
        download_asset(item, key, out, force=force)
        local_paths[key] = str(out)

    manifest = {
        "project_id": project_id,
        "year": year,
        "scene": {
            "id": item["id"],
            "datetime": item["properties"].get("datetime"),
            "cloud_cover": item["properties"].get("eo:cloud_cover"),
            "bbox": item.get("bbox"),
            "mgrs_tile": item["properties"].get("s2:mgrs_tile") or item["properties"].get("mgrs:utm_zone"),
        },
        "local_paths": local_paths,
        "fetched_at": datetime.now(UTC).isoformat(),
    }
    manifest_path.write_text(json.dumps(manifest, indent=2))
    return manifest
