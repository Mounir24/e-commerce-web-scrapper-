from integrations.woocommerce import WooCommerceClient
from utils.logger import setup_logger
from tqdm import tqdm
import time
import re

wc = WooCommerceClient()
logger = setup_logger()


def retrieve_products(category_id=0):
    page = 1
    all_products = []

    while True:
        products = wc.retrieve_products(
            category_id=category_id,
            page=page
        )

        if not products:
            logger.warning(f"No products found for category {category_id}")
            break  # stop loop cleanly

        logger.info(
            f"Fetched page {page} | Products: {len(products)}"
        )

        all_products.extend(products)
        page += 1

        ### Prevent Rate-limiting issue
        time.sleep(0.40)

    return all_products




### Normalize Slug
def normalize_slug(slug):
    return re.sub(r'-\d+$', '', slug)


### Normalize Name
def normalize_name(name):
    name = name.lower().strip()
    name = re.sub(r'\s+', ' ', name)
    return name


### Detect Duplicate 
def detect_duplicates(products):
    fingerprint_map = {}
    duplicate_ids = []

    for product in products:
        slug = normalize_slug(product.get("slug", ""))
        name = normalize_name(product.get("name", ""))

        fingerprint = f"{slug}|{name}"

        if fingerprint in fingerprint_map:
            logger.warning(f"[{slug}] {name} → Duplicate Product")
            duplicate_ids.append(product["id"])
        else:
            logger.info(
                    f"[{product['id']}] {name} → Product fingerprint added ({fingerprint})"
                )
            fingerprint_map[fingerprint] = product["id"]


    return duplicate_ids



### Batch Duplicated Products by IDs
def batch_delete(ids):
    chunk_size = 100

    logger.info(f"Starting batch delete | Total IDs: {len(ids)}")

    for i in tqdm(
        range(0, len(ids), chunk_size),
        desc="Batch deleting",
        unit="batch"
    ):
        try:
            batch = ids[i:i+chunk_size]

            payload = {
                "delete": [{"id": pid, "force": True} for pid in batch]
            }

            response = wc.batch_products(payload)

            logger.info(
                f"Deleted batch of {len(batch)} products | Status: {response.status_code}"
            )

        except Exception as e:
            logger.exception(
                f"Batch delete failed for IDs: {batch}"
            )

    logger.info("Finished processing batch removal")



### Execution 
if __name__ == "__main__":

    DRY_RUN = False

    ### [163]
    products = retrieve_products(163)

    if not products:
        logger.warning("No products retrieved. Exiting.")
        exit()

    duplicates = detect_duplicates(products)

    logger.info(f"Found {len(duplicates)} duplicate products")
    print(f"Found {len(duplicates)} duplicate products")

    if not DRY_RUN and duplicates:
        batch_delete(duplicates)

    print("---------- SUMMARY ----------")
    print("Total products:", len(products))
    print("Duplicates found:", len(duplicates))
    print("Deleted:", 0 if DRY_RUN else len(duplicates))