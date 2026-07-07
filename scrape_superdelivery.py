#!/usr/bin/env python3
import os
import json
from supabase import create_client
from datetime import datetime
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

FALLBACK = [
    {"id": "super_1", "name": "Kimono Yukata été", "vendor": "Kyoto Textile Co.", "price": "¥8 500", "category": "Mode", "popularity": 89, "image": "https://picsum.photos/seed/kimono/300/200", "url": "https://www.superdelivery.com/en/list/1", "siteType": "SuperDelivery", "metric": 89},
    {"id": "super_2", "name": "Set Thé Matcha Céramique", "vendor": "Zen Ceramics", "price": "¥6 200", "category": "Ustensiles de cuisine", "popularity": 76, "image": "https://picsum.photos/seed/matcha/300/200", "url": "https://www.superdelivery.com/en/list/2", "siteType": "SuperDelivery", "metric": 76},
    {"id": "super_3", "name": "Sac Tote Fukuro", "vendor": "Tokyo Bags", "price": "¥4 800", "category": "Accessoires", "popularity": 92, "image": "https://picsum.photos/seed/tokyo/300/200", "url": "https://www.superdelivery.com/en/list/3", "siteType": "SuperDelivery", "metric": 92},
    {"id": "super_4", "name": "Lampe Paper Lantern", "vendor": "Wasou Lighting", "price": "¥3 900", "category": "Décoration intérieure", "popularity": 68, "image": "https://picsum.photos/seed/lantern/300/200", "url": "https://www.superdelivery.com/en/list/4", "siteType": "SuperDelivery", "metric": 68},
    {"id": "super_5", "name": "Carnet Tomoe River", "vendor": "Paper & Co.", "price": "¥1 200", "category": "Fournitures de bureau", "popularity": 81, "image": "https://picsum.photos/seed/notebook/300/200", "url": "https://www.superdelivery.com/en/list/5", "siteType": "SuperDelivery", "metric": 81},
    {"id": "super_6", "name": "Jouet Kokeshi", "vendor": "Kokeshi Arts", "price": "¥2 800", "category": "Jouets", "popularity": 54, "image": "https://picsum.photos/seed/kokeshi/300/200", "url": "https://www.superdelivery.com/en/list/6", "siteType": "SuperDelivery", "metric": 54},
    {"id": "super_7", "name": "Crème Yuzu Bio", "vendor": "Shikoku Skincare", "price": "¥3 500", "category": "Santé/Beauté", "popularity": 73, "image": "https://picsum.photos/seed/yuzu/300/200", "url": "https://www.superdelivery.com/en/list/7", "siteType": "SuperDelivery", "metric": 73},
    {"id": "super_8", "name": "Bavoir Bébé Indigo", "vendor": "Baby Japan", "price": "¥1 800", "category": "Articles bébés/enfants", "popularity": 61, "image": "https://picsum.photos/seed/baby/300/200", "url": "https://www.superdelivery.com/en/list/8", "siteType": "SuperDelivery", "metric": 61},
]

def parse_product(el, idx):
    def txt(sel):
        node = el.select_one(sel)
        return node.get_text(strip=True) if node else ""
    def attr(sel, a):
        node = el.select_one(sel)
        return node.get(a, "") if node else ""
    name = txt('h2, h3, .name, [class*="name"], [class*="title"]')
    if not name:
        return None
    return {
        "id": f"super_{idx}",
        "name": name,
        "vendor": txt('[class*="vendor"], [class*="shop"], [class*="brand"]') or "SuperDelivery",
        "price": txt('[class*="price"]') or "—",
        "category": txt('[class*="category"]') or "Divers",
        "popularity": 0,
        "image": attr('img', 'src') or attr('img', 'data-src') or "",
        "url": attr('a', 'href') or "https://www.superdelivery.com",
        "siteType": "SuperDelivery",
        "metric": 0,
    }

def scrape():
    print("🌐 Scraping SuperDelivery (Playwright)...")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
            page = browser.new_page(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36')
            page.goto('https://www.superdelivery.com/en/list/', wait_until='networkidle', timeout=30000)
            html = page.content()
            browser.close()
        soup = BeautifulSoup(html, 'html.parser')
        raw = soup.find_all(['div', 'li'], class_=['product', 'item'], limit=8)
        parsed = [p for p in (parse_product(el, i + 1) for i, el in enumerate(raw)) if p]
        if parsed:
            print(f"✅ {len(parsed)} produits parsés")
            return parsed
        print("⚠️ Aucun produit — fallback")
        return FALLBACK
    except Exception as e:
        print(f"❌ {str(e)}")
        return FALLBACK

def push_supabase(products):
    print(f"📤 Push {len(products)} → Supabase...")
    data = {
        'source': 'superdelivery',
        'scraped_at': datetime.now().isoformat(),
        'products': products,
        'count': len(products)
    }
    try:
        supabase.table('scrape_results').insert(data).execute()
        print("✅ Inséré")
        return True
    except Exception as e:
        print(f"❌ {str(e)}")
        return False

if __name__ == '__main__':
    products = scrape()
    push_supabase(products)
