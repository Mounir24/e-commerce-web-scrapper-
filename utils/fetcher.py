import requests
from playwright.sync_api import sync_playwright


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}


def fetch_html(url, use_browser=False):
    if not use_browser:
        r = requests.get(url, headers=HEADERS, timeout=30)
        r.encoding = 'utf-8'
        r.raise_for_status()
        return r.text

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=60000)
        html = page.content()
        browser.close()
        return html
