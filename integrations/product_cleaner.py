from integrations.woocommerce import WooCommerceClient
from utils.helpers import (
    detect_description_type,
    process_text_description,
    process_html_description
)
from utils.logger import setup_logger
from tqdm import tqdm
import time

wc = WooCommerceClient()

logger = setup_logger()

def process_category(category_id = 163):
    page = 1
    total_processed = 0

    while True:
        products = wc.retrieve_products(
            category_id=category_id,
            page=page
        )

        if not products:
            logger.warning(f"No products found for category {category_id}")
            return

        logger.info(
            f"Starting processing | Category: {category_id} | Products: {len(products)}"
        )

        for product in tqdm(
            products,
            desc=f"Page {page}",
            unit="product"
        ):
            try:
                product_id = product["id"]
                name = product.get('name', 'unknown')
                description = product.get("description", "")

                if not description:
                    logger.warning(f"[{product_id}] {name} → No description")
                    continue

                desc_type = detect_description_type(description)

                # detect type
                if desc_type == "text":
                    new_desc = process_text_description(description)

                elif desc_type == "html":
                    new_desc = process_html_description(description)

                else:
                    logger.error(
                        f"[{product_id}] {name} → Unknown description type"
                    )   
                    continue

                wc.update_product(product_id, {"description": new_desc, "meta_data": [{"key": "_old_description_backup", "value": description}]})
                
                ### Successully Updated Product Description
                logger.info(
                    f"[{product_id}] {name} → Updated successfully ({desc_type})"
                )

                total_processed += 1

                ### Prevent Rate-limiting issue
                time.sleep(0.45)

            except Exception as e:
                logger.exception(
                    f"[{product.get('id')}] Processing failed"
                )
        
        page += 1
    
    print(f"\n✅ Done. Total products updated: {total_processed}")
    logger.info(
        f"Finished processing category {category_id}"
    )
            

process_category()
