"""Clip Hansen tiles to a project geometry and summarise forest loss inside it.

Uses rasterio.mask.mask with crop=True so we read only the geometry's bbox
window and then null out any pixel outside the actual polygon. Falls back to
a bbox window read if no shapely geometry is supplied (legacy path)."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import rasterio
from rasterio.mask import mask as rio_mask
from rasterio.merge import merge
from rasterio.windows import from_bounds
from shapely.geometry import MultiPolygon, Polygon, box, mapping
from shapely.geometry.base import BaseGeometry


def _as_geom(
    bbox: tuple[float, float, float, float] | None,
    geometry: BaseGeometry | None,
) -> BaseGeometry:
    if geometry is not None:
        return geometry
    if bbox is None:
        raise ValueError("Either bbox or geometry must be supplied")
    return MultiPolygon([box(*bbox)])


def _open_clipped(paths: list[Path], geom: BaseGeometry):
    """Mosaic tiles (if multiple) and return the array clipped to the geometry."""
    if len(paths) == 1:
        with rasterio.open(paths[0]) as src:
            arr, transform = rio_mask(src, [mapping(geom)], crop=True, all_touched=False, filled=True, nodata=0)
            crs = src.crs
        return arr[0], transform, crs

    sources = [rasterio.open(p) for p in paths]
    try:
        minx, miny, maxx, maxy = geom.bounds
        mosaic, transform = merge(sources, bounds=(minx, miny, maxx, maxy))
        crs = sources[0].crs
    finally:
        for s in sources:
            s.close()

    # Re-mask the in-memory mosaic against the actual polygon
    from rasterio.io import MemoryFile

    profile = {
        "driver": "GTiff",
        "height": mosaic.shape[1],
        "width": mosaic.shape[2],
        "count": mosaic.shape[0],
        "dtype": mosaic.dtype,
        "crs": crs,
        "transform": transform,
    }
    with MemoryFile() as memfile:
        with memfile.open(**profile) as dst:
            dst.write(mosaic)
        with memfile.open() as src:
            arr, transform = rio_mask(src, [mapping(geom)], crop=True, filled=True, nodata=0)
    return arr[0], transform, crs


def loss_summary(
    lossyear_paths: list[Path],
    treecover_paths: list[Path],
    bbox: tuple[float, float, float, float] | None = None,
    *,
    geometry: BaseGeometry | None = None,
    project_start_year: int,
    treecover_threshold: int = 30,
) -> dict:
    """Forest-loss summary inside the project geometry.

    Pass either ``bbox`` (legacy) or ``geometry`` (shapely Polygon/MultiPolygon).
    treecover_threshold: minimum 2000 canopy cover (%) for a pixel to be counted
    as 'forest'. 30% is the threshold the Hansen team uses for headline numbers."""
    geom = _as_geom(bbox, geometry)
    bounds = geom.bounds

    loss_arr, loss_tf, _ = _open_clipped(lossyear_paths, geom)
    tc_arr, _, _ = _open_clipped(treecover_paths, geom)

    if tc_arr.shape != loss_arr.shape:
        h = min(tc_arr.shape[0], loss_arr.shape[0])
        w = min(tc_arr.shape[1], loss_arr.shape[1])
        tc_arr = tc_arr[:h, :w]
        loss_arr = loss_arr[:h, :w]

    forest_mask = tc_arr >= treecover_threshold

    pixel_size_deg_x = abs(loss_tf.a)
    pixel_size_deg_y = abs(loss_tf.e)
    mid_lat = (bounds[1] + bounds[3]) / 2.0
    m_per_deg_lat = 111_320.0
    m_per_deg_lon = 111_320.0 * np.cos(np.radians(mid_lat))
    pixel_area_m2 = (pixel_size_deg_x * m_per_deg_lon) * (pixel_size_deg_y * m_per_deg_lat)
    pixel_area_ha = pixel_area_m2 / 10_000.0

    by_year: dict[int, float] = {}
    for code in range(1, 24):
        year = 2000 + code
        m = (loss_arr == code) & forest_mask
        ha = float(m.sum()) * pixel_area_ha
        by_year[year] = round(ha, 2)

    forest_2000_ha = float(forest_mask.sum()) * pixel_area_ha
    pre_start_loss = sum(v for y, v in by_year.items() if y < project_start_year)
    post_start_loss = sum(v for y, v in by_year.items() if y >= project_start_year)

    return {
        "bbox": list(bounds),
        "treecover_threshold_pct": treecover_threshold,
        "pixel_area_ha": round(pixel_area_ha, 4),
        "forest_2000_ha": round(forest_2000_ha, 2),
        "loss_by_year_ha": by_year,
        "loss_pre_project_start_ha": round(pre_start_loss, 2),
        "loss_post_project_start_ha": round(post_start_loss, 2),
        "project_start_year": project_start_year,
    }
