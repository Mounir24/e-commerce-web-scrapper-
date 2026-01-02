import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from tqdm import tqdm


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}


def scrape_brands(brands_page_url, selectors):
    
    response = requests.get(brands_page_url, headers=HEADERS, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")
    brands = []

    brand_elements = soup.select(selectors["brand_item"])

    for el in tqdm(brand_elements, desc="Scraping brands"):
        name = None
        link = None
        image = None

        # Brand name
        name_el = el.select_one(selectors.get("brand_name"))
        if name_el:
            name = name_el.get_text(strip=True)

        # Brand URL
        link_el = el.select_one(selectors.get("brand_link"))
        if link_el and link_el.get("href"):
            link = urljoin(brands_page_url, link_el["href"])

        # Brand logo
        img_el = el.select_one(selectors.get("brand_image"))
        if img_el and img_el.get("src"):
            image = urljoin(brands_page_url, img_el["src"])

        if name:
            brands.append({
                "name": name,
                "url": link,
                "image": image
            })

    return brands


"""def export_brands_csv(brands, output_path="output/brands.csv"):
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["name", "url", "image"]
        )
        writer.writeheader()
        writer.writerows(brands)


def export_brands_json(brands, output_path="output/brands.json"):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(brands, f, indent=2, ensure_ascii=False)
"""