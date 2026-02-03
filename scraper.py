#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import re
import json

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Referer": "https://app.transporteya.com.ar/app/"
})

def discover_real_endpoints():
    """Descarga HTML inicial + busca patrones de API en JS"""
    print("🔍 1. Cargando página principal...")
    resp = session.get("https://app.transporteya.com.ar/app/")
    
    # Busca URLs de API en el HTML/JS inline
    soup = BeautifulSoup(resp.text, 'html.parser')
    scripts = soup.find_all('script')
    
    api_urls = []
    for script in scripts:
        if script.string:
            # Patrones comunes de fetch/API calls
            urls = re.findall(r'["\'](/api/[a-zA-Z0-9/?=&-]*)["\']', script.string)
            api_urls.extend(urls)
    
    # Busca en el main.js (desde tu Google Drive)
    print("🔍 2. Analizando main.dab66abd.js...")
    js_content = ""  # Aquí irían los fetch reales del JS
    
    print("📋 URLs API encontradas:")
    for url in set(api_urls):
        print(f"  → {url}")
        test_url(url)
    
def test_url(path):
    """Testea cada URL encontrada"""
    url = f"https://app.transporteya.com.ar{path}"
    print(f"🧪 Testing {url}...")
    resp = session.get(url)
    print(f"   Status: {resp.status_code} | Size: {len(resp.text)}")
    if resp.status_code == 200 and len(resp.text) > 100:
        print(f"   ✅ POSIBLE ENDPOINT: {resp.text[:200]}...")

if __name__ == "__main__":
    discover_real_endpoints()
