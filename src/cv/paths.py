from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
RAW = DATA / "raw"
PROCESSED = DATA / "processed"
CACHE = DATA / "cache"
SENTINEL_DIR = RAW / "sentinel2"
HANSEN_DIR = RAW / "hansen"
VERRA_DIR = RAW / "verra"
PROJECTS_JSON = DATA / "projects.json"

for p in (RAW, PROCESSED, CACHE, SENTINEL_DIR, HANSEN_DIR, VERRA_DIR):
    p.mkdir(parents=True, exist_ok=True)
