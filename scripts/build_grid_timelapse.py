"""Compose a 2×2 grid time-lapse from the per-project GIFs.

For Lovable / marketing pages: a single GIF showing all four fully-analyzed
demo projects evolving year-by-year in parallel. Each cell carries the
project ID + country in the corner so it's legible standalone.

Output: docs/screenshots/00_quad_timelapse.gif
"""

from __future__ import annotations

from io import BytesIO
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]

PROJECTS = [
    ("VCS832", "Cikel · Pará, Brazil",          ROOT / "data/cache/VCS832_timelapse.gif"),
    ("VCS981", "Pacajai · Pará, Brazil",        ROOT / "data/cache/VCS981_timelapse.gif"),
    ("VCS985", "Cordillera Azul · Peru",        ROOT / "data/cache/VCS985_timelapse.gif"),
    ("VCS934", "Mai Ndombe · DRC",              ROOT / "data/cache/VCS934_timelapse.gif"),
]

CELL_W = 380       # per-cell pixel width after resize
CELL_H = 380       # per-cell pixel height after resize
GUTTER = 4         # inter-cell gap
LABEL_PAD = 8


def _font(size: int = 18) -> ImageFont.ImageFont:
    for p in [
        "/System/Library/Fonts/Supplemental/SF-Mono-Bold.otf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ]:
        if Path(p).exists():
            try:
                return ImageFont.truetype(p, size)
            except OSError:
                pass
    return ImageFont.load_default()


def _frames_from_gif(path: Path, n_frames: int) -> list[Image.Image]:
    """Extract the first ``n_frames`` frames, crop the burned-in year-stamp from
    the top-left, and resize to CELL_W × CELL_H."""
    img = Image.open(path)
    frames: list[Image.Image] = []
    try:
        for i in range(n_frames):
            img.seek(i)
            f = img.convert("RGB")
            w, h = f.size
            # Crop ~80px from the top to remove the per-project year-stamp burned
            # in by cv/timelapse.py — we replace it with our own grid-cell label.
            crop_top = 80
            f = f.crop((0, crop_top, w, h))
            # Square-crop the centre after the top-strip removal
            w2, h2 = f.size
            side = min(w2, h2)
            f = f.crop(((w2 - side) // 2, (h2 - side) // 2,
                       (w2 - side) // 2 + side, (h2 - side) // 2 + side))
            f = f.resize((CELL_W, CELL_H), Image.LANCZOS)
            frames.append(f)
    except EOFError:
        pass
    return frames


def _stamp_label(img: Image.Image, vcs_id: str, name: str) -> Image.Image:
    """Burn a project ID / location label into the top-left of the cell."""
    out = img.copy()
    d = ImageDraw.Draw(out, "RGBA")
    f_id = _font(20)
    f_name = _font(13)

    pad = LABEL_PAD
    # Background pill
    id_bbox = d.textbbox((0, 0), vcs_id, font=f_id)
    name_bbox = d.textbbox((0, 0), name, font=f_name)
    box_w = max(id_bbox[2] - id_bbox[0], name_bbox[2] - name_bbox[0]) + pad * 2
    box_h = (id_bbox[3] - id_bbox[1]) + (name_bbox[3] - name_bbox[1]) + pad * 2 + 4

    d.rectangle([0, 0, box_w, box_h], fill=(11, 15, 25, 220))
    d.text((pad, pad), vcs_id, fill=(74, 222, 128), font=f_id)
    d.text((pad, pad + (id_bbox[3] - id_bbox[1]) + 4), name,
           fill=(229, 226, 226), font=f_name)
    return out


def main() -> int:
    n_frames = 4  # each per-project GIF has 4 frames
    grids: list[Image.Image] = []

    # Pre-extract every project's frames
    project_frames: list[list[Image.Image]] = []
    for vcs_id, name, gif_path in PROJECTS:
        if not gif_path.exists():
            print(f"  ! missing {gif_path}; skipping")
            project_frames.append([])
            continue
        frames = _frames_from_gif(gif_path, n_frames)
        labelled = [_stamp_label(f, vcs_id, name) for f in frames]
        project_frames.append(labelled)
        print(f"  ✓ {vcs_id}: {len(frames)} frames")

    # Years in our pipeline
    years = ["2018", "2020", "2022", "2024"]
    grid_w = CELL_W * 2 + GUTTER
    grid_h = CELL_H * 2 + GUTTER + 60   # extra space at top for the year header

    for i in range(n_frames):
        canvas = Image.new("RGB", (grid_w, grid_h), (11, 15, 25))
        d = ImageDraw.Draw(canvas)

        # Top header: year + tagline
        f_yr = _font(36)
        f_tag = _font(14)
        d.text((LABEL_PAD * 2, 8), years[i], fill=(74, 222, 128), font=f_yr)
        d.text((LABEL_PAD * 2 + 110, 28),
               "// 4 verra projects · sentinel-2 satellite record",
               fill=(148, 163, 184), font=f_tag)

        # 2×2 grid
        for idx, frames in enumerate(project_frames):
            if not frames or i >= len(frames):
                continue
            r, c = idx // 2, idx % 2
            x = c * (CELL_W + GUTTER)
            y = 60 + r * (CELL_H + GUTTER)
            canvas.paste(frames[i], (x, y))

        grids.append(canvas)

    # Resize the final grids down for web use (~1100px wide)
    target_w = 1100
    if grids and grids[0].width > target_w:
        ratio = target_w / grids[0].width
        new_size = (target_w, int(grids[0].height * ratio))
        grids = [g.resize(new_size, Image.LANCZOS) for g in grids]

    out = ROOT / "docs/screenshots/00_quad_timelapse.gif"
    grids[0].save(
        out,
        save_all=True,
        append_images=grids[1:],
        duration=1700,
        loop=0,
        optimize=True,
    )
    sz = out.stat().st_size / 1024
    print(f"  → {out.relative_to(ROOT)}  ({sz:.0f} KB · {len(grids)} frames · {grids[0].size})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
