from integrations.woocommerce import WooCommerceClient
from integrations.product_mapper import map_product_to_wc
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import time
import hashlib
import random


def generate_sku(product, prefix="CRMP"):
    """
    Generate a stable SKU when supplier does not provide one
    """
    slug = product.get("title")
    source_url = product.get('source_url')
    base = slug + source_url
    hash_part = hashlib.md5(base.encode("utf-8")).hexdigest()[:8]

    numeric_part = str(int(hash_part[:8], 16))[:8]
    random_part = random.randint(1000, 9999)

    return f"{prefix}-{numeric_part}-{random_part}"


BATCH_SIZE = 10        # safe value
BATCH_DELAY = 1.0      # seconds between batches



def chunked(iterable, size):
    for i in range(0, len(iterable), size):
        yield iterable[i:i + size]


### Batch Push - Multi Products Push 
def push_products_batch(products):
    wc = WooCommerceClient()

    ### SKU Checking
    def ensure_sku(product):
        if product.get("reference"):
            product["sku"] = product["reference"]
        else:
            product["sku"] = generate_sku(product)

    for batch in tqdm(list(chunked(products, BATCH_SIZE)), desc="Batch uploading"):
        payload = {
            "create": [],
            "update": []
        }

        try:
            for product in batch:
                ensure_sku(product)
                sku = product["sku"]
                wc_product = map_product_to_wc(product)


                existing = wc.product_exists(sku)

                if existing:
                    wc_product["id"] = existing["id"]
                    payload["update"].append(wc_product)
                else:
                    payload["create"].append(wc_product)

            if payload["create"] or payload["update"]:
                response = wc.batch_products(payload)

                if response.status_code not in (200, 201):
                    print("Batch failed:", response.text)
                else:
                    print(
                        f"Batch success "
                        f"(Created: {len(payload['create'])}, "
                        f"Updated: {len(payload['update'])})"
                    )

        except Exception as e:
            print("Batch exception:", e)

        time.sleep(1.2)  # server cooldown

### Single Product Push 
def push_products_to_woocommerce(products):
    wc = WooCommerceClient()

    for product in tqdm(products, desc="Uploading to WooCommerce"):
        sku = product.get("reference")

        if not sku:
            sku = generate_sku(product)
            print(f"SKU generated & hashed: {sku}")

        # Assign SKU to product before mapping
        product["reference"] = sku

        payload = map_product_to_wc(product)

        try:
            existing = wc.product_exists(sku)

            if existing:
                r = wc.update_product(existing["id"], payload)
                action = "UPDATED"
            else:
                r = wc.create_product(payload)
                action = "CREATED"

            # CRITICAL: check API response
            if r.status_code not in (200, 201):
                print(f"\nFAILED [{r.status_code}] {action} SKU={sku}")
                print(r.text)
            else:
                print(f"{action} SKU={sku}")

        except Exception as e:
            print(f"\nException for SKU={sku}: {e}")

        time.sleep(0.3)
