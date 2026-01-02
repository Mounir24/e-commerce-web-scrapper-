from woocommerce import WooCommerceClient
from brands_cache import save_brand_cache


def fetch_wc_brands():
    wc = WooCommerceClient()
    page = 1
    brands = {}

    while True:
        print('Brands fetching call ...')
        r = wc.session.get(
            f"{wc.base_url.replace('/wc/v3', '')}/wp/v2/product_brand",
            params={"per_page": 100, "page": page},
            timeout=20
        )

        if not r.ok or not r.json():
            break

        for brand in r.json():
            brands[brand["name"].upper()] = brand["id"]

        page += 1

    save_brand_cache(brands)
    print(f"Cached {len(brands)} brands")


if __name__ == "__main__":
    fetch_wc_brands()
