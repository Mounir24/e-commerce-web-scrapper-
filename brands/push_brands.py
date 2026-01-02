from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

from integrations.woocommerce import WooCommerceClient
from brands.brand_mapper import map_brand_to_wc


MAX_WORKERS = 8


def _push_single_brand(wc, brand):
    payload = map_brand_to_wc(brand)

    existing = wc.brand_exists(brand["name"])
    if existing:
        return f"SKIPPED: {brand['name']}"

    r = wc.create_brand(payload)

    if r.status_code not in (200, 201):
        return f"FAILED: {brand['name']} → {r.text}"

    return f"CREATED: {brand['name']}"


def push_brands_fast(brands):
    wc = WooCommerceClient()

    results = []

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [
            executor.submit(_push_single_brand, wc, brand)
            for brand in brands
        ]

        for f in tqdm(as_completed(futures), total=len(futures), desc="Uploading brands"):
            results.append(f.result())

    return results
