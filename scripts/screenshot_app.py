"""Boot streamlit (assumed already running on a port) and screenshot the page
with Playwright after the JS renders. Usage:

    uv run python scripts/screenshot_app.py http://localhost:8767/ /tmp/app.png
"""

from __future__ import annotations

import sys
from playwright.sync_api import sync_playwright


def main(url: str, out: str) -> int:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(viewport={"width": 1600, "height": 1100}, device_scale_factor=2)
        page = ctx.new_page()
        page.goto(url, wait_until="networkidle", timeout=45000)
        # Streamlit injects content asynchronously after first network idle
        page.wait_for_timeout(3500)
        page.screenshot(path=out, full_page=False)
        browser.close()
    print(f"saved -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1], sys.argv[2]))
