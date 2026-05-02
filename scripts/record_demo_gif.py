"""Record an animated GIF of the dashboard switching across all 4 demo projects.

For the README hero. Walks the project picker through Cikel → Pacajai →
Cordillera Azul → Mai Ndombe, captures one frame per project, plus a couple
of tab-switch frames for variety. Output: docs/screenshots/00_try.gif.

Usage:
    uv run python scripts/record_demo_gif.py http://localhost:8767/
"""

from __future__ import annotations

import io
import sys
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "screenshots" / "00_try.gif"

PROJECTS = [
    "VCS832 — Cikel Brazilian Amazon REDD APD — Avoiding Planned Deforestation",
    "VCS981 — Pacajai REDD+ Project (formerly ADPML Portel-Pará)",
    "VCS985 — Cordillera Azul National Park REDD",
    "VCS934 — Mai Ndombe REDD+ Project",
]


def _shoot(page) -> Image.Image:
    """Screenshot the current viewport and return as a PIL image."""
    raw = page.screenshot(full_page=False)
    return Image.open(io.BytesIO(raw)).convert("RGB")


def main(url: str) -> int:
    OUT.parent.mkdir(parents=True, exist_ok=True)

    frames: list[Image.Image] = []
    durations: list[int] = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(viewport={"width": 1400, "height": 900}, device_scale_factor=1)
        page = ctx.new_page()
        page.goto(url, wait_until="networkidle", timeout=45000)
        page.wait_for_timeout(3500)

        for proj in PROJECTS:
            print(f"  → switching to {proj[:40]}…")
            # Click the selectbox
            page.locator('div[data-baseweb="select"]').first.click()
            page.wait_for_timeout(500)
            # Click the option matching this project (scoped to the dropdown,
            # otherwise the trigger element matches first and we don't open it)
            page.get_by_test_id("stSelectboxVirtualDropdown").get_by_text(proj, exact=True).click()
            page.wait_for_timeout(2200)  # let folium re-render
            frames.append(_shoot(page))
            durations.append(1700)

        browser.close()

    print(f"  → assembling {len(frames)} frames into GIF…")
    # Resize for repo embedding (~1000px max width)
    target_w = 1100
    if frames[0].width > target_w:
        ratio = target_w / frames[0].width
        new_size = (target_w, int(frames[0].height * ratio))
        frames = [f.resize(new_size, Image.LANCZOS) for f in frames]

    frames[0].save(
        OUT,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        optimize=True,
    )
    sz = OUT.stat().st_size / 1024
    print(f"  → {OUT.relative_to(ROOT)}  ({sz:.0f} KB · {len(frames)} frames)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8767/"))
