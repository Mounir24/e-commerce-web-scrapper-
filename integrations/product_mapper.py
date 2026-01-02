from integrations.brands_cache import load_brand_cache
from utils.formater import extract_brand_from_title


# Load brands ONCE (cache)
BRANDS_LOOKUP = load_brand_cache()

def map_product_to_wc(product):
    """images = [
        {"src": img}
        for img in product.get("images", [])
        if img.startswith("http")
    ]"""

    categories = [
        {"id": 389},
        {"id": 390},
    ]

    # Attach existing brand by ID
    brand_term = []

    # explicit brand from DOM
    explicit_brand = (product.get("brand") or "").strip().upper()

    # Fallback: extract from title (novapara.ma case)
    extracted_brand = extract_brand_from_title(
        product.get("title", ""),
        BRANDS_LOOKUP
    )

    brand_name = explicit_brand or extracted_brand

    if brand_name and brand_name in BRANDS_LOOKUP:
        brand_term = [{"id": BRANDS_LOOKUP[brand_name]}]

    return {
        "name": product.get("title"),
        "type": "simple",
        "sku": product.get("sku"),
        "regular_price": product.get("price"),
        "description": product.get("description"),
        "categories": categories,
        "images": product.get('images'),
        "brands": brand_term
    }
