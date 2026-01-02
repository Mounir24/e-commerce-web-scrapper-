import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CACHE_FILE = BASE_DIR / "cache" / "brands.json"


def save_brand_cache(brands: dict):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(brands, f, ensure_ascii=False, indent=2)


def load_brand_cache() -> dict:
    if not CACHE_FILE.exists():
        print(f"No Brands Cache file at {CACHE_FILE}")
        return {}

    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("Brand cache file is corrupted")
        return {}
