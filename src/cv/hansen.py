"""Hansen Global Forest Change (UMD/Google).

10x10-degree tiles named by their NW corner. We pick the tiles that intersect
the project bbox, download once, and clip to the bbox on read.

Latest version available: GFC-2023-v1.11. The 'lossyear' raster encodes the year
of forest loss as 1..23 (= 2001..2023), 0 = no loss.
Reference: https://glad.umd.edu/dataset/global-2010-tree-cover-30-m
"""

from __future__ import annotations

import math
from pathlib import Path

import requests

from .paths import HANSEN_DIR

VERSION = "GFC-2023-v1.11"
BASE_URL = f"https://storage.googleapis.com/earthenginepartners-hansen/{VERSION}"
LATEST_LOSS_YEAR = 2023
LATEST_LOSS_YEAR_CODE = LATEST_LOSS_YEAR - 2000


def _tile_corner(lat: float, lon: float) -> tuple[int, str, int, str]:
    """Return (lat_int, lat_hemi, lon_int, lon_hemi) of the NW corner of the
    10-degree tile that contains (lat, lon)."""
    lat_top = int(math.ceil(lat / 10.0) * 10)
    lon_left = int(math.floor(lon / 10.0) * 10)
    lat_hemi = "N" if lat_top >= 0 else "S"
    lon_hemi = "E" if lon_left >= 0 else "W"
    return abs(lat_top), lat_hemi, abs(lon_left), lon_hemi


def _tile_name(lat: float, lon: float) -> str:
    lat_i, lat_h, lon_i, lon_h = _tile_corner(lat, lon)
    return f"{lat_i:02d}{lat_h}_{lon_i:03d}{lon_h}"


def tiles_for_bbox(bbox: tuple[float, float, float, float]) -> list[str]:
    minx, miny, maxx, maxy = bbox
    names = set()
    lat = miny
    while lat <= maxy + 0.0001:
        lon = minx
        while lon <= maxx + 0.0001:
            names.add(_tile_name(lat, lon))
            lon += 10.0
        lat += 10.0
    names.add(_tile_name(maxy, maxx))
    return sorted(names)


def url_for(layer: str, tile: str) -> str:
    return f"{BASE_URL}/Hansen_{VERSION}_{layer}_{tile}.tif"


def download_tile(layer: str, tile: str) -> Path:
    out = HANSEN_DIR / f"Hansen_{VERSION}_{layer}_{tile}.tif"
    if out.exists() and out.stat().st_size > 0:
        return out
    url = url_for(layer, tile)
    tmp = out.with_suffix(out.suffix + ".part")
    with requests.get(url, stream=True, timeout=300) as r:
        r.raise_for_status()
        with tmp.open("wb") as fh:
            for chunk in r.iter_content(chunk_size=4 * 1024 * 1024):
                if chunk:
                    fh.write(chunk)
    tmp.rename(out)
    return out


def fetch_layers_for_bbox(
    bbox: tuple[float, float, float, float],
    layers: tuple[str, ...] = ("lossyear", "treecover2000"),
) -> dict[str, list[Path]]:
    out: dict[str, list[Path]] = {}
    for layer in layers:
        out[layer] = [download_tile(layer, t) for t in tiles_for_bbox(bbox)]
    return out
