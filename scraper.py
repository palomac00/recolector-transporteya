#!/usr/bin/env python3
import requests
import csv
import json
import time
from datetime import datetime
import re

BASE_URL = "https://app.transporteya.com.ar"
session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://app.transporteya.com.ar/app/",
    "Origin": "https://app.transporteya.com.ar"
})

def safe_json(resp):
    """Evita JSONDecodeError - debuggea primero"""
    print(f"Status: {resp.status_code}")
    print(f"Headers Content-Type: {resp.headers.get('content-type', 'N/A')}")
    print(f"Response preview: {resp.text[:300]}...")
    
    if resp.status_code != 200:
        print(f"❌ Error HTTP {resp.status_code}")
        return None
    
    if 'application/json' not in resp.headers.get('content-type', ''):
        print("❌ No es JSON")
        return None
    
    try:
        return resp.json()
    except:
        print("❌ JSON inválido")
        return None

def test_endpoints():
    """Prueba TODOS los endpoints posibles"""
    endpoints = [
        "/api/lines?q=324",
        "/api/search?q=324", 
        "/api/lineas/324",
        "/api/line/324",
        "/api/routes/324"
    ]
    
    for endpoint in endpoints:
        print(f"\n🧪 Probando: {BASE_URL}{endpoint}")
        resp = session.get(BASE_URL + endpoint)
        data = safe_json(resp)
        if data:
            print(f"✅ FUNCIONA! {len(data)} items")
            print(json.dumps(data, indent=2)[:500])
            return data
    return None

def scrape_324():
    print("🔍 Descubriendo endpoints reales...")
    
    # 1. Buscar líneas 324
    lines_data = test_endpoints()
    if not lines_data:
        print("❌ No se encontraron endpoints de líneas")
        return
    
    # 2. TODO: extraer stops desde lines_data y filtrar ramal 5/6
    print("✅ Endpoints encontrados - revisar output arriba")
    print("\n📋 Próximo paso: copiar el endpoint que funcionó + buscar 'stops' en Network tab")

if __name__ == "__main__":
    scrape_324()
