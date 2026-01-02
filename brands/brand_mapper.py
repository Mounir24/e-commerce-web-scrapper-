def map_brand_to_wc(brand):
    payload = {
        "name": brand["name"]
    }

    if brand.get("image"):
        payload["image"] = {
            "src": brand["image"]
        }

    return payload
