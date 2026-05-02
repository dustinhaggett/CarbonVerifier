"""Build an animated GIF time-lapse from per-year Sentinel-2 visual COGs.

Each frame is the same project bbox cropped from that year's least-cloudy
in-window scene (via the manifest written by sentinel.fetch_year), resized to a
common thumbnail size, with a year label burned in. Output: a single GIF
suitable for embedding in the Streamlit dashboard or a slide deck.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import rasterio
from PIL import Image, ImageDraw, ImageFont
from pyproj import Transformer
from rasterio.windows import from_bounds

from .paths import CACHE, SENTINEL_DIR

THUMB_PX = 640
FRAME_MS = 900


def _read_visual_clipped(
    path: Path, bbox_4326: tuple[float, float, float, float]
) -> np.ndarray:
    with rasterio.open(path) as src:
        if src.crs.to_string() != "EPSG:4326":
            t = Transformer.from_crs("EPSG:4326", src.crs, always_xy=True)
            minx, miny = t.transform(bbox_4326[0], bbox_4326[1])
            maxx, maxy = t.transform(bbox_4326[2], bbox_4326[3])
            bbox_native = (minx, miny, maxx, maxy)
        else:
            bbox_native = bbox_4326
        window = from_bounds(*bbox_native, transform=src.transform).round_offsets().round_lengths()
        bands = src.count
        if bands >= 3:
            arr = src.read([1, 2, 3], window=window).transpose(1, 2, 0)
        else:
            arr = src.read(1, window=window)
            arr = np.stack([arr, arr, arr], axis=-1)
    return arr


def _to_uint8_rgb(arr: np.ndarray) -> np.ndarray:
    if arr.dtype == np.uint8:
        return arr
    finite = arr[np.isfinite(arr)] if np.issubdtype(arr.dtype, np.floating) else arr
    if finite.size == 0:
        return np.zeros(arr.shape, dtype=np.uint8)
    p2, p98 = np.percentile(finite, [2, 98])
    if p98 == p2:
        p98 = p2 + 1
    out = np.clip((arr - p2) / (p98 - p2), 0, 1) * 255.0
    return out.astype(np.uint8)


def _font(size: int = 36) -> ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ]
    for p in candidates:
        if Path(p).exists():
            try:
                return ImageFont.truetype(p, size)
            except OSError:
                pass
    return ImageFont.load_default()


def _stamp(img: Image.Image, label: str, sublabel: str | None = None) -> Image.Image:
    draw = ImageDraw.Draw(img, "RGBA")
    font_big = _font(40)
    font_small = _font(18)

    pad = 8
    big_bbox = draw.textbbox((0, 0), label, font=font_big)
    big_w = big_bbox[2] - big_bbox[0]
    big_h = big_bbox[3] - big_bbox[1]

    x, y = 16, 16
    box_w = big_w + pad * 2
    box_h = big_h + pad * 2
    if sublabel:
        small_bbox = draw.textbbox((0, 0), sublabel, font=font_small)
        small_w = small_bbox[2] - small_bbox[0]
        box_w = max(box_w, small_w + pad * 2)
        box_h += (small_bbox[3] - small_bbox[1]) + 4

    draw.rectangle([x - pad, y - pad, x - pad + box_w, y - pad + box_h], fill=(15, 23, 42, 200))
    draw.text((x, y), label, fill="white", font=font_big)
    if sublabel:
        draw.text((x, y + big_h + 6), sublabel, fill=(196, 181, 253), font=font_small)
    return img


def build_gif(
    project_id: str,
    bbox: tuple[float, float, float, float],
    years: list[int] | None = None,
    out_path: Path | None = None,
    thumb_px: int = THUMB_PX,
    frame_ms: int = FRAME_MS,
) -> Path | None:
    """Render one frame per available year (manifest must exist with a 'visual' asset).
    Returns the GIF path, or None if no frames could be built."""
    base = SENTINEL_DIR / project_id
    if not base.exists():
        return None

    discovered = sorted(int(p.name) for p in base.iterdir() if p.name.isdigit())
    target_years = sorted(years) if years else discovered

    frames: list[Image.Image] = []
    for year in target_years:
        manifest_p = base / str(year) / "manifest.json"
        if not manifest_p.exists():
            continue
        manifest = json.loads(manifest_p.read_text())
        scene = manifest.get("scene")
        if scene is None:
            continue
        visual = manifest.get("local_paths", {}).get("visual")
        if not visual:
            continue
        try:
            arr = _read_visual_clipped(Path(visual), bbox)
        except Exception:
            continue
        if arr.size == 0:
            continue
        img = Image.fromarray(_to_uint8_rgb(arr)).convert("RGB")
        img.thumbnail((thumb_px, thumb_px), Image.LANCZOS)
        sublabel = scene.get("datetime", "")[:10] if scene else None
        _stamp(img, str(year), sublabel)
        frames.append(img)

    if not frames:
        return None

    out = out_path or (CACHE / f"{project_id}_timelapse.gif")
    out.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(
        out,
        save_all=True,
        append_images=frames[1:],
        duration=frame_ms,
        loop=0,
        optimize=True,
    )
    return out
