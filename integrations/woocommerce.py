import requests
import os
from dotenv import load_dotenv

load_dotenv()

WC_API_URL = os.getenv("WC_API_URL")
WC_KEY = os.getenv("WC_CONSUMER_KEY")
WC_SECRET = os.getenv("WC_CONSUMER_SECRET")


class WooCommerceClient:
    def __init__(self):
        self.base_url = f"{WC_API_URL}/wp-json/wc/v3"
        self.auth = (WC_KEY, WC_SECRET)
        self.session = requests.Session()
        self.session.auth = self.auth
        self.session.headers.update({
            "Content-Type": "application/json"
        })

    def product_exists(self, sku):
        r = self.session.get(
            f"{self.base_url}/products",
            params={"sku": sku},
            timeout=25
        )
        return r.json()[0] if r.ok and r.json() else None

    def create_product(self, payload):
        return self.session.post(
            f"{self.base_url}/products",
            json=payload,
            timeout=30
        )

    def update_product(self, product_id, payload):
        return self.session.put(
            f"{self.base_url}/products/{product_id}",
            json=payload,
            timeout=30
        )
    
    def batch_products(self, payload):
        return self.session.post(
            f"{self.base_url}/products/batch",
            json=payload,
            timeout=60
        )
    
    ### Products Brands Scrapping & Pushing handling
    # 🔹 CHANGE taxonomy if your site uses another one

    BRAND_TAXONOMY = "product_brand"  # sometimes: "pa_brand", "product_brand"

    def brand_exists(self, name):
        r = self.session.get(
            f"{self.base_url}/products/brands",
            params={"search": name},
            timeout=20
        )

        if r.ok:
            for item in r.json():
                if item["name"].lower() == name.lower():
                    return item
        return None

    def create_brand(self, payload):
        return self.session.post(
            f"{self.base_url}/products/brands",
            json=payload,
            timeout=30
        )
