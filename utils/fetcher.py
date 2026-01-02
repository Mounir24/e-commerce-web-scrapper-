import requests
import time
import random
from playwright.sync_api import sync_playwright


USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (X11; Linux x86_64)",
]


def fetch_html(url, use_browser=False, retries=5):
    """
    Fetch HTML using requests.
    Falls back to Playwright if blocked or requested.
    """

    if use_browser:
        return fetch_with_browser(url)

    session = requests.Session()

    for attempt in range(1, retries + 1):
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept-Language": "fr-FR,fr;q=0.9",
            "Referer": "https://www.google.com/",
            "Accept": "text/html,application/xhtml+xml",
        }

        try:
            response = session.get(url, headers=headers, timeout=25)

            # Rate-limit or bot protection
            if response.status_code in (403, 429):
                wait = random.uniform(6, 15) * attempt
                print(f"[BLOCKED {response.status_code}] Sleeping {wait:.1f}s → {url}")
                time.sleep(wait)
                continue

            response.raise_for_status()

            # Human-like delay even on success
            time.sleep(random.uniform(1.5, 3.5))

            return response.text

        except requests.RequestException as e:
            wait = random.uniform(5, 10) * attempt
            print(f"[ERROR] {e} → retry in {wait:.1f}s")
            time.sleep(wait)

    # Final fallback
    print("[FALLBACK] Switching to browser mode")
    return fetch_with_browser(url)


def fetch_with_browser(url):
    """
    Playwright fallback for JS / anti-bot pages
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(
            user_agent=random.choice(USER_AGENTS),
            locale="fr-FR"
        )

        page.goto(url, timeout=60000)
        page.wait_for_timeout(random.randint(2500, 4000))

        html = page.content()
        browser.close()

        return html
