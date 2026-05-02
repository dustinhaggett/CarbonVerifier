"""NDVI computation from Sentinel-2 Red (B04) and NIR (B08) bands.

NDVI = (NIR - Red) / (NIR + Red)
Range: -1 to +1; healthy vegetation > 0.6; bare/deforested < 0.2.

Uses the SCL (Scene Classification Layer) to mask clouds, shadows, and water,
and clips to the project geometry (real polygon or bbox rectangle) via
rasterio.mask.mask before computing zonal stats.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import rasterio
from pyproj import Transformer
from rasterio.mask import mask as rio_mask
from shapely.geometry import MultiPolygon, box, mapping
from shapely.geometry.base import BaseGeometry
from shapely.ops import transform as shp_transform

from .paths import CACHE


# SCL codes to keep (vegetation, soil, water-OK)
# See https://sentinels.copernicus.eu/web/sentinel/technical-guides/sentinel-2-msi/level-2a/algorithm-overview
SCL_VALID = {4, 5, 6, 7}  # vegetation, not-vegetated, water, unclassified-ok
# Excluded: 0=nodata, 1=saturated, 2=dark shadow, 3=cloud shadow,
#           8=cloud med, 9=cloud high, 10=cirrus, 11=snow


def _reproject_geom(geom_4326: BaseGeometry, dst_crs) -> BaseGeometry:
    """Reproject a geometry from EPSG:4326 to the raster's CRS."""
    if str(dst_crs).upper() in ("EPSG:4326", "WGS 84"):
        return geom_4326
    transformer = Transformer.from_crs("EPSG:4326", dst_crs, always_xy=True)
    return shp_transform(lambda x, y, z=None: transformer.transform(x, y), geom_4326)


def _read_band_clipped(path: Path, geom_4326: BaseGeometry) -> np.ndarray:
    with rasterio.open(path) as src:
        geom_native = _reproject_geom(geom_4326, src.crs)
        arr, _ = rio_mask(src, [mapping(geom_native)], crop=True, filled=True, nodata=0)
    return arr[0]


def compute_ndvi(
    red_path: Path,
    nir_path: Path,
    scl_path: Path | None,
    geom_4326: BaseGeometry,
) -> dict:
    """Compute NDVI clipped to geometry, with optional SCL cloud masking."""
    red = _read_band_clipped(red_path, geom_4326).astype(np.float32)
    nir = _read_band_clipped(nir_path, geom_4326).astype(np.float32)

    if red.shape != nir.shape:
        h = min(red.shape[0], nir.shape[0])
        w = min(red.shape[1], nir.shape[1])
        red = red[:h, :w]
        nir = nir[:h, :w]

    # Sentinel-2 L2A reflectance is scaled by 10000
    red = red / 10_000.0
    nir = nir / 10_000.0

    denom = nir + red
    ndvi = np.where(denom > 0, (nir - red) / denom, np.nan)

    # 0 returned by rio_mask for outside-polygon pixels — both bands ==0, denom==0 → NaN, good.

    if scl_path and scl_path.exists():
        scl = _read_band_clipped(scl_path, geom_4326)
        # SCL may be at 20 m while R/NIR are 10 m — resample if needed
        if scl.shape != ndvi.shape:
            from scipy.ndimage import zoom
            scale_y = ndvi.shape[0] / scl.shape[0]
            scale_x = ndvi.shape[1] / scl.shape[1]
            scl = zoom(scl, (scale_y, scale_x), order=0)
            if scl.shape != ndvi.shape:
                h = min(scl.shape[0], ndvi.shape[0])
                w = min(scl.shape[1], ndvi.shape[1])
                scl = scl[:h, :w]
                ndvi = ndvi[:h, :w]
        valid_mask = np.isin(scl, list(SCL_VALID))
        ndvi = np.where(valid_mask, ndvi, np.nan)

    valid = ndvi[~np.isnan(ndvi)]
    if len(valid) == 0:
        return {
            "mean": None, "median": None, "std": None,
            "pct_forest": None, "pct_deforested": None,
            "valid_pixels": 0, "total_pixels": int(ndvi.size),
        }

    return {
        "mean": round(float(np.nanmean(ndvi)), 4),
        "median": round(float(np.nanmedian(ndvi)), 4),
        "std": round(float(np.nanstd(ndvi)), 4),
        "pct_forest": round(float((valid >= 0.4).sum() / len(valid) * 100), 2),
        "pct_deforested": round(float((valid < 0.2).sum() / len(valid) * 100), 2),
        "valid_pixels": int(len(valid)),
        "total_pixels": int(ndvi.size),
    }


def ndvi_time_series(
    project_id: str,
    bbox_or_geom: tuple[float, float, float, float] | BaseGeometry,
    years: list[int],
    sentinel_dir: Path | None = None,
) -> list[dict]:
    """Build a year-by-year NDVI summary for a project.

    Accepts either a (minx, miny, maxx, maxy) tuple or a shapely geometry.
    Reads each year's manifest.json (written by sentinel.fetch_year) to locate
    band paths. Caches result to data/cache/<project_id>_ndvi_timeseries.json."""
    from .paths import SENTINEL_DIR

    if isinstance(bbox_or_geom, tuple):
        geom: BaseGeometry = MultiPolygon([box(*bbox_or_geom)])
    else:
        geom = bbox_or_geom

    base = sentinel_dir or SENTINEL_DIR
    results: list[dict] = []

    for year in sorted(years):
        manifest_path = base / project_id / str(year) / "manifest.json"
        if not manifest_path.exists():
            results.append({"year": year, "status": "not_fetched"})
            continue

        manifest = json.loads(manifest_path.read_text())
        if manifest.get("scene") is None:
            results.append({"year": year, "status": "no_scene"})
            continue

        paths = manifest.get("local_paths", {})
        red_path = Path(paths["red"]) if "red" in paths else None
        nir_path = Path(paths["nir"]) if "nir" in paths else None
        scl_path = Path(paths["scl"]) if "scl" in paths else None

        if not red_path or not nir_path:
            results.append({"year": year, "status": "missing_bands"})
            continue

        stats = compute_ndvi(red_path, nir_path, scl_path, geom)
        stats["year"] = year
        stats["scene_id"] = manifest["scene"]["id"]
        stats["scene_date"] = manifest["scene"]["datetime"]
        stats["cloud_cover"] = manifest["scene"]["cloud_cover"]
        stats["status"] = "ok"
        results.append(stats)

    out_path = CACHE / f"{project_id}_ndvi_timeseries.json"
    out_path.write_text(json.dumps(results, indent=2))
    return results
