"""Screenshot each top-level tab in the Streamlit app.

Usage:
    uv run python scripts/screenshot_tabs.py http://localhost:8767/ /tmp/cv
"""

from __future__ import annotations

import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

TABS = ["MAP", "TIME-LAPSE", "NDVI", "LOSS", "ADDITIONALITY", "BRIEFS"]


def main(url: str, out_prefix: str) -> int:
    out_dir = Path(out_prefix).parent
    out_dir.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(viewport={"width": 1600, "height": 1100}, device_scale_factor=2)
        page = ctx.new_page()
        page.goto(url, wait_until="networkidle", timeout=45000)
        page.wait_for_timeout(3500)

        for tab in TABS:
            try:
                # Streamlit tabs: <button role="tab"> with the label text inside
                tab_button = page.locator(f'button[role="tab"]:has-text("{tab}")').first
                tab_button.click(timeout=5000)
            except Exception as e:
                print(f"  ! could not click {tab}: {e}")
                continue

            page.wait_for_timeout(2500)
            slug = tab.lower().replace("-", "_")
            out_path = f"{out_prefix}_{slug}.png"
            page.screenshot(path=out_path, full_page=False)
            print(f"  saved -> {out_path}")
        browser.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "/tmp/cv"))
