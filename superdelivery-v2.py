# scraper/superdelivery-v2.py
# Scraping SuperDelivery avec login — Playwright headless
# Mode images : SUPABASE_STORAGE (default) ou DIRECT_URL
# Secrets : SD_LOGIN, SD_PASSWORD, SUPABASE_URL, SUPABASE_KEY

import json
import os
import sys
import time
import requests
from io import BytesIO
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright
from supabase import create_client

LOGIN_URL = "https://www.superdelivery.com/p/do/clickMemberLogin"
CATEGORY_URL = os.environ["CATEGORY_URL"]
MAX_PAGES = int(os.environ.get("MAX_PAGES", "3"))
SD_LOGIN = os.environ["SD_LOGIN"]
SD_PASSWORD = os.environ["SD_PASSWORD"]
IMAGE_MODE = os.environ.get("IMAGE_MODE", "SUPABASE_STORAGE")  # ou DIRECT_URL

# Supabase
SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_SERVICE_KEY"]
SB = create_client(SUPABASE_URL, SUPABASE_KEY)


def login(page):
    """Connexion au compte SuperDelivery."""
    page.goto(LOGIN_URL, wait_until="domcontentloaded")
    time.sleep(2)

    page.fill('input[name="emailAddress"]', SD_LOGIN)
    page.fill('input[name="password"]', SD_PASSWORD)
    page.click('button[type="submit"], input[type="submit"]')
    page.wait_for_load_state("networkidle")
    time.sleep(3)

    if "login" in page.url.lower():
        print("❌ Login échoué — vérifie SD_LOGIN / SD_PASSWORD")
        sys.exit(1)
    print("✅ Login OK")


def download_image(url, filename):
    """Télécharge image depuis URL."""
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            return BytesIO(r.content)
        return None
    except Exception as e:
        print(f"⚠️ Erreur DL image {url}: {e}")
        return None


def upload_to_supabase_storage(image_io, filename):
    """Upload vers Supabase Storage, retourne URL publique."""
    try:
        SB.storage.from_("products").upload(filename, image_io)
        # URL publique Supabase Storage
        public_url = f"{SUPABASE_URL}/storage/v1/object/public/products/{filename}"
        return public_url
    except Exception as e:
        print(f"⚠️ Upload Storage échoué {filename}: {e}")
        return None


def process_image(image_url, product_id):
    """
    Mode 1 : SUPABASE_STORAGE — DL + upload Storage
    Mode 2 : DIRECT_URL — retourne URL directe SuperDelivery
    """
    if not image_url:
        return None

    if IMAGE_MODE == "DIRECT_URL":
        # Mode simple : URL directe SuperDelivery (attention CORS)
        return image_url

    elif IMAGE_MODE == "SUPABASE_STORAGE":
        # Mode stockage : DL + upload
        filename = f"products/{product_id}_{urlparse(image_url).path.split('/')[-1]}"
        image_io = download_image(image_url, filename)
        if image_io:
            storage_url = upload_to_supabase_storage(image_io, filename)
            if storage_url:
                return storage_url
        return None

    return image_url


def scrape_category(page, url, max_pages):
    """Scrape produits avec pagination."""
    produits = []

    for num in range(1, max_pages + 1):
        page_url = f"{url}?page={num}" if num > 1 else url
        print(f"📄 Page {num} : {page_url}")
        page.goto(page_url, wait_until="domcontentloaded")
        time.sleep(3)

        items = page.query_selector_all(".item-list .item, .product-item, li.item")
        if not items:
            print("⚠️ Aucun item trouvé — sélecteurs à ajuster ou fin pagination")
            break

        for idx, it in enumerate(items):
            try:
                nom_el = it.query_selector(".item-name, .product-name, h3, h2")
                prix_el = it.query_selector(".price, .item-price")
                lien_el = it.query_selector("a")
                img_el = it.query_selector("img")

                image_url = img_el.get_attribute("src") if img_el else None
                product_id = f"{num}_{idx}"

                # Process image selon mode
                final_image_url = process_image(image_url, product_id)

                produits.append({
                    "nom": nom_el.inner_text().strip() if nom_el else None,
                    "prix": prix_el.inner_text().strip() if prix_el else None,
                    "url": lien_el.get_attribute("href") if lien_el else None,
                    "image": final_image_url,  # URL Supabase ou DirectURL
                    "image_raw": image_url,  # URL originale (backup)
                    "source": "superdelivery",
                    "page": num,
                })
            except Exception as e:
                print(f"⚠️ Item ignoré : {e}")

        time.sleep(2)

    return produits


def push_supabase(produits):
    """Upsert vers Supabase table `products_sd`."""
    if not produits:
        print("⚠️ Rien à pousser")
        return

    # Batch de 100
    for i in range(0, len(produits), 100):
        batch = produits[i:i + 100]
        SB.table("products_sd").upsert(batch, on_conflict="url").execute()

    print(f"✅ {len(produits)} produits → Supabase")
    print(f"📸 Mode images : {IMAGE_MODE}")


def main():
    print(f"🚀 Mode images : {IMAGE_MODE}")

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"],
        )
        ctx = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/126.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1366, "height": 768},
            locale="ja-JP",
        )
        ctx.add_init_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )
        page = ctx.new_page()

        login(page)
        produits = scrape_category(page, CATEGORY_URL, MAX_PAGES)
        browser.close()

    with open("produits.json", "w", encoding="utf-8") as f:
        json.dump(produits, f, ensure_ascii=False, indent=2)
    print(f"💾 {len(produits)} produits → produits.json")

    push_supabase(produits)


if __name__ == "__main__":
    main()
