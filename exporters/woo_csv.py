import csv
import os


def export_to_csv(products, filename="output/products.csv"):
    os.makedirs("output", exist_ok=True)

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "title",
                "description",
                "brand",
                "category",
                "reference",
                "price",
                "images",
                "source_url",
            ],
        )
        writer.writeheader()

        for p in products:
            p["images"] = ",".join(p["images"]) if isinstance(p["images"], list) else p["images"]
            writer.writerow(p)
