import sys
import json
from urllib.parse import urlparse

from scraper_engine import collect_product_links, scrape_products_fast, scrape_product
from integrations.push_products import push_products_to_woocommerce, push_products_batch
from exporters.woo_csv import export_to_csv

import sys
sys.stdout.reconfigure(encoding="utf-8")
from utils.formater import human_delay
from tqdm import tqdm



def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <category_url>")
        sys.exit(1)

    category_url = sys.argv[1]
    domain = urlparse(category_url).netloc.replace("www.", "")

    # Load selectors
    with open("selectors/sites.json", "r", encoding="utf-8") as f:
        sites = json.load(f)

    config = sites.get(domain)
    if not config:
        print(f"No selectors found for domain: {domain}")
        sys.exit(1)

    #Collect product URLs
    print(f"Collecting product URLs from {category_url}")
    product_urls = collect_product_links(category_url, config)

    if not product_urls:
        print("No product URLs found.")
        sys.exit(1)

    print(f"Found {len(product_urls)} products\n")

    #Scrape products (FAST -  Multi-Thread)
    ###products = scrape_products_fast(product_urls, config, workers=8)

    products = []

    for url in tqdm(product_urls, desc="Scraping products", unit="product"):
        product = scrape_product(url, config)

        if product:
            products.append(product)

        human_delay()

    if not products:
        print("No products scraped.")
        sys.exit(1)

    
    #Push to Woocommerce REST API (Single product / Batch products push)
    ###push_products_batch(products)

    print("\nDone! Products exported & pushed to WooCommerce (CERMEP.COM)")

if __name__ == "__main__":
    main()
