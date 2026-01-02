from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import time

from utils.fetcher import fetch_html



### IMPORT UTILS / HELPERS
from utils.formater import extract_html, clean_price, clean_text



def is_valid_product_url(url: str) -> bool:
    """
    Ensures URL is valid and usable
    """
    if not url:
        return False

    url = url.strip().lower()

    if url in ("#", "/", "javascript:void(0)", "javascript:void(0);"):
        return False

    if len(url) < 10:
        return False

    return True


### Extract the category
def extract_categories_hierarchy(soup):
    categories = []

    items = soup.select(
        'ol[itemtype="http://schema.org/BreadcrumbList"] '
        'li[itemtype="http://schema.org/ListItem"]'
    )

    for item in items:
        position = item.select_one('meta[itemprop="position"]')
        name = item.select_one('span[itemprop="name"]')

        if not position or not name:
            continue

        pos = int(position["content"])
        text = name.get_text(strip=True)

        # Skip Home (1) and Product (last)
        if pos >= 2:
            categories.append(text)

    # Remove last element (product title)
    return categories[:-1]

# --------------------------------------------------
# CATEGORY SCRAPER (FAST + PAGINATION SAFE)
# --------------------------------------------------

def collect_product_links(category_url, config, max_pages=200):
    product_links = set()
    current_page = category_url
    page_number = 1

    print("Collecting product URLs...")

    for _ in tqdm(range(max_pages), desc="Category pages", unit="page"):
        html = fetch_html(current_page, use_browser=False)
        soup = BeautifulSoup(html, "lxml")

        found_before = len(product_links)

        for el in soup.select(config["category"]["product_links"]):
            href = el.get("href")
            

            if not is_valid_product_url(href):
                continue

            full_url = urljoin(current_page, href)

            # Final safety check
            parsed = urlparse(full_url)
            if not parsed.scheme.startswith("http"):
                continue

            product_links.add(full_url)

        # Stop when no new products appear
        if len(product_links) == found_before:
            break

        page_number += 1
        current_page = f"{category_url}?page={page_number}"

        time.sleep(0.4)

    return list(product_links)


# --------------------------------------------------
# SINGLE PRODUCT SCRAPER
# --------------------------------------------------

def scrape_product(url, config):
    """
    Scrapes one product page.
    Automatically retries with Playwright if static fetch fails.
    """

    # Try fast static request first
    html = fetch_html(url, use_browser=False)
    soup = BeautifulSoup(html, "lxml")

    # If title not found, fallback to browser
    title_selector = config["product"].get("title")
    if title_selector and not soup.select_one(title_selector):
        html = fetch_html(url, use_browser=True)
        soup = BeautifulSoup(html, "lxml")
    

    ### Extract , Clean Images sources helper
    def extract_images(selector):
        images = []
        seen = set()

        for img in soup.select(selector):
            src = img.get("src") or img.get("srcset") or ""

            # srcset or comma-separated URLs
            parts = [p.strip() for p in src.split(",") if p.strip()]

            for part in parts:
                # srcset format: "url 2048w"
                url = part.split(" ")[0]

                # Normalize protocol
                if url.startswith("//"):
                    url = "https:" + url

                if url.startswith("http") and url not in seen:
                    images.append({"src": url})
                    seen.add(url)

        return images
    

    product = {}

    for field, selector in config["product"].items():
        el = soup.select_one(selector)
        el_text = el.get_text(strip=True) if el else ""

        if field == "images":
            product[field] = extract_images(selector)
        elif field == "description":
            product[field] = extract_html(soup, selector)
        elif field == "price":
            product[field] = clean_price(el_text)
        else:
            product[field] = clean_text(el_text)
 

    ### Replace Flaged Word with our brand name 
    """raw_desc = product['short_description'].strip()
    replaced_desc = raw_desc.replace('KINGPHAR', 'CERMEP')"""

    ### UPDATE OBJECT PROPS
    product["source_url"] = url
    ###product['brand'] = extract_brand_from_title(product['title'], BRANDS_LOOKUP)

    """product["short_description"] = clean_text(replaced_desc)"""

    return product


# --------------------------------------------------
# FAST MULTI-PRODUCT SCRAPER (THREADS)
# --------------------------------------------------

def scrape_products_fast(product_urls, config, workers=8):
    """
    Scrapes products concurrently for speed.
    """

    results = []

    print(f"Scraping {len(product_urls)} products...")

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(scrape_product, url, config): url
            for url in product_urls
        }

        for future in tqdm(
            as_completed(futures),
            total=len(futures),
            desc="Scraping products",
            unit="product"
        ):
            try:
                results.append(future.result())
            except Exception as e:
                print(f"Error scraping product: {e}")

    return results
