import html
import re


# --------------------------------------------------
# TEXT CONTENT FORMATER (ESCAPE NON-BREAKING SPACES & ENCODED CHARS)
# --------------------------------------------------

def clean_text(text: str) -> str:
    if not text:
        return ""

    text = html.unescape(text)
    text = text.replace("\xa0", " ")

    # Normalize multiple spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()



# --------------------------------------------------
# PRODUCT PRICE FORMAT CLEANER (CURRENCY, Espace non-breaeking space encoded character)
# --------------------------------------------------

def clean_price(raw_price: str) -> str:
   
    if not raw_price:
        return ""

    # Remove non-breaking spaces
    price = raw_price.replace("\xa0", " ")

    # Remove currency letters (MAD, €, $, etc.)
    price = re.sub(r"[^\d,\.]", "", price)

    # Convert comma decimal to dot
    price = price.replace(",", ".")

    return price.strip()



# --------------------------------------------------
# Clean Raw Rich-HTML Content & Decode HTLM Entities
# --------------------------------------------------
def clean_html(raw_html: str) -> str:
    if not raw_html:
        return ""

    # Decode HTML entities
    raw_html = html.unescape(raw_html)

    # Replace non-breaking spaces
    raw_html = raw_html.replace("\xa0", " ")

    return raw_html.strip()


# --------------------------------------------------
# Extract Raw Rich-HTML Content
# --------------------------------------------------

def extract_html(soup, selector):
    el = soup.select_one(selector)
    if not el:
        return ""

    # Keep raw HTML (including emojis)
    raw_html = el.decode_contents(formatter="html")

    # Decode entities but keep Unicode (emojis stay)
    cleaned_html = html.unescape(raw_html).replace("\xa0", " ").strip()

    # If HTML still contains tags → rich content
    if re.search(r"<[^>]+>", cleaned_html):
        return cleaned_html

    # Otherwise fallback to plain text
    return clean_text(el.get_text(separator=" ", strip=True))



# --------------------------------------------------
# NORMALIZE THE STRING 
# --------------------------------------------------
def normalize(text: str) -> str:
    return (
        text.upper()
        .replace("-", " ")
        .replace("+", " ")
        .strip()
    )


# --------------------------------------------------
# EXTRACT BRAND FROM THE NORMALIZED TITLE 
# --------------------------------------------------

def extract_brand_from_title(title: str, brands_lookup: dict) -> str | None:
    if not title:
        return None

    title_norm = normalize(title)

    # Sort brands by length (longest first → avoids partial matches)
    brands_sorted = sorted(
        brands_lookup.keys(),
        key=lambda b: len(b),
        reverse=True
    )

    for brand in brands_sorted:
        brand_norm = normalize(brand)

        # Brand MUST be at the beginning of the title
        if title_norm.startswith(brand_norm + " ") or title_norm == brand_norm:
            return brand

    return None