import json
import sys

from brands.brands_scraper import scrape_brands
from brands.push_brands import push_brands_fast


if len(sys.argv) < 2:
    print("Usage: python main_brands.py <brands_page_url>")
    sys.exit(1)

brands_url = sys.argv[1]

with open("selectors/brands.json", "r", encoding="utf-8") as f:
    selectors = json.load(f)

brands = scrape_brands(brands_url, selectors)

print(f"Found {len(brands)} brands")

results = push_brands_fast(brands)

print("\n--- Summary ---")
for r in results:
    print(r)
