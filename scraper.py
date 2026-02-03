#!/usr/bin/env python3
import requests
import re
import json

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "text/html,application/xhtml+xml,*/*;q=0.9",
    "Referer": "https://app.transporteya.com.ar/app/",
    "Sec-Fetch-Mode": "navigate"
})

def discover_api():
    print("🔍 Cargando página principal...")
    resp = session.get("https://app.transporteya.com.ar/app/")
    
    if resp.status_code != 200:
        print(f"❌ Error página principal: {resp.status_code}")
        return
    
    # Busca TODAS las URLs internas posibles
    patterns = [
        r'["\'](/[^"\']*\b(?:api|ws|graphql|line|stop|vehicle)[^"\']*)["\']',
        r'fetch\(["\']([^"\']+)["\']',
        r'"/([^"]+324[^"]*)"',
        r'"/line/(\d+)/[^"]*"'
    ]
    
    urls = []
    for pattern in patterns:
        matches = re.findall(pattern, resp.text, re.IGNORECASE)
        urls.extend(matches)
    
    # URLs únicas limpias
    api_urls = list(set([u for u in urls if any(x in u.lower() for x in ['api','line','stop','324','vehicle'])]))
    
    print(f"\n📋 {len(api_urls)} URLs candidatas encontradas:")
    for i, url in enumerate(api_urls[:10], 1):  # Solo primeras 10
        print(f"{i}. {url}")
        test_api(f"https://app.transporteya.com.ar{url}")
    
    print("\n🔥 Copia las URLs que den Status 200 arriba!")

def test_api(url):
    try:
        resp = session.get(url, timeout=10)
        print(f"   Status: {resp.status_code} | Len: {len(resp.text)}")
        if resp.status_code == 200:
            print(f"   ✅ POSIBLE: {resp.text[:100]}...")
    except Exception as e:
        print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    discover_api()
