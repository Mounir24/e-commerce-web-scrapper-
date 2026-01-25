import re
from bs4 import BeautifulSoup

### Detect Product Description (Text-based / Rich-HTML)
SIMPLE_TAGS = {"p", "br", "strong", "b", "em", "i", "u", "span"}
RICH_TAGS = {"div", "section", "article", "ul", "ol", "li", "figure"}
IGNORED_TAGS = {"html", "body"}

def detect_description_type(description: str) -> str:
    if not description or not description.strip():
        return "empty"

    # Pure text
    if "<" not in description and ">" not in description:
        return "text"

    soup = BeautifulSoup(description, "lxml")

    found_tags = set(tag.name for tag in soup.find_all(True) if tag.name not in IGNORED_TAGS)

    # Rich html
    if found_tags & RICH_TAGS:
        return "html"

    # Treat as text
    if found_tags.issubset(SIMPLE_TAGS):
        return "text"

    # Fallback safety
    return "html"


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
    "Livraison & Paiement",
    "votre pharmacien Nova Parapharmacie",
    "Prix de vente",
    "Prix Nova Para",
    "CONSEIL EXPERT NOVA PARA",
    "POURQUOI CHOISIR NOVA PARA",
    "OFFRE EXCEPTIONNELLE NOVA PARA",
    "Livraison Premium"
]
def process_html_description(html: str) -> str:
    html = remove_block_by_text(
        html,
        UNWANTED_BLOCKS
    )

    return html


### Decompose Unwanted Blocks by Providing Text keywords String
BLOCK_TAGS_PRIORITIES = ['div', 'section', 'ul', 'p','h2', 'article']
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

