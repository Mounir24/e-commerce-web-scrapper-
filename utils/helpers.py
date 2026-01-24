import re
from bs4 import BeautifulSoup

### Detect Product Description (Text-based / Rich-HTML)
def detect_description_type(description: str) -> str:
    if not description:
        return 'empty'

    # If it contains HTML tags (Rich HTML)
    if "<" in description and ">" in description:
        return "html"

    # Text-based type
    return "text"


### Plain text description processing (Text-based)
def process_text_description(text: str) -> str:
    # Normalize spaces
    text = re.sub(r'\s+', ' ', text).strip()

    # Split by sentence endings
    sentences = re.split(r'(?<=[.!?])\s+', text)

    # Rebuild as HTML paragraphs
    paragraphs = [f"<p>{s}</p>" for s in sentences if len(s) > 20]

    return "\n".join(paragraphs)


### Rich-HTML Processor 
UNWANTED_BLOCKS = [
    "livraison rapide",
    "conseil expert nova",
    "Livraison & Paiement Nova Parapharmacie",
    "votre pharmacien Nova Parapharmacie",
    "nova para",
    "Prix de vente",
    "Prix Nova Para",
    "CONSEIL EXPERT NOVA PARA",
    "POURQUOI CHOISIR NOVA PARA",
    "OFFRE EXCEPTIONNELLE NOVA PARA"
]
def process_html_description(html: str) -> str:
    html = remove_block_by_text(
        html,
        UNWANTED_BLOCKS
    )

    return html


### Decompose Unwanted Blocks by Providing Text keywords String
BLOCK_TAGS_PRIORITIES = ['div', 'section', 'ul', 'p', 'article']
def remove_block_by_text(html: str, keywords: list) -> str:
    soup = BeautifulSoup(html, "lxml")
    parents_to_remove = set()

    for keyword in keywords:
        # Find text nodes containing the keyword
        text_nodes = soup.find_all(
            string=lambda text: text and keyword.lower() in text.lower()
        )

        for text_node in text_nodes:

            for tag in BLOCK_TAGS_PRIORITIES:
                parent = text_node.find_parent(tag)

                if parent:
                    parents_to_remove.add(parent)
                    break


    ### REMOVE EACH PARENT ONCE
    for parent in parents_to_remove:
        parent.decompose()

    return str(soup.body or soup)



### Category-Based Processing Flow 
def process_category(category_id: int):
    products = fetch_products_by_category(category_id)

    for product in products:
        desc = product["description"]
        desc_type = detect_description_type(desc)

        if desc_type == "text":
            new_desc = process_text_description(desc)

        elif desc_type == "html":
            new_desc = process_html_description(desc, HTML_RULES)

        else:
            continue

        update_product_description(product["id"], new_desc)

