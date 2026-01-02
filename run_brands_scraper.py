import json
from brands.brands_scraper import scrape_brands, export_brands_csv, export_brands_json

BRANDS_URL = "https://www.paranewera.com/brands"

with open("selectors/brands.json", "r", encoding="utf-8") as f:
    selectors = json.load(f)

brands = scrape_brands(BRANDS_URL, selectors)

export_brands_csv(brands)
export_brands_json(brands)

print(f"{len(brands)} brands scraped successfully")
