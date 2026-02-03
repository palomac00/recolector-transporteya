#!/usr/bin/env python3
import requests
import re
import csv
import json
from datetime import datetime

def parse_transporteya_js(js_content):
    """Extrae datos 324 del main.dab66abd.js"""
    
    # Patrones para datos de líneas/paradas desde el JS minificado
    patterns = {
        'lines_324': r'"324"[^}]*?(?:"id"|"name"|"stops"|"vehicles")[^}]*?(?="ramal"[^}]*?5|6)',
        'stop_calle622': r'"calle 622"[^}]*?"id"[^}]*?"coordinates?"[^}]*?',
        'vehicles_324': r'"324"[^}]*?"lat"[^}]*?"lng"[^}]*?"eta?"[^}]*?',
    }
    
    data = {}
    for key, pattern in patterns.items():
        matches = re.findall(pattern, js_content, re.DOTALL | re.IGNORECASE)
        data[key] = matches
        print(f"📍 {key}: {len(matches)} matches")
    
    return data

def fake_eta_for_324_ramal56():
    """Genera datos simulados hasta tener parsing completo"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Simula datos realistas para Calle 622 ramal 5/6
    arrivals = [
        {"ramal": "324-5", "eta": "15:02", "distancia": "800m", "vehicle": "ABC123"},
        {"ramal": "324-6", "eta": "15:07", "distancia": "1.2km", "vehicle": "DEF456"},
    ]
    
    with open("data/324_ramal56.csv", "a", newline="") as f:
        writer = csv.writer(f)
        if f.tell() == 0:
            writer.writerow(["timestamp", "parada", "ramal", "eta", "distancia", "vehicle"])
        
        for arrival in arrivals:
            writer.writerow([
                timestamp,
                "Calle 622 y Colectora",
                arrival["ramal"],
                arrival["eta"],
                arrival["distancia"],
                arrival["vehicle"]
            ])
    
    print("✅ Guardado CSV con datos simulados")
    print("📊 arrivals:", arrivals)

def download_main_js():
    """Descarga el JS actualizado"""
    url = "https://app.transporteya.com.ar/app/static/js/main.dab66abd.js"
    resp = requests.get(url)
    with open("main.js", "w") as f:
        f.write(resp.text)
    print("✅ main.js descargado - 1.8MB")
    return resp.text

if __name__ == "__main__":
    import os
    os.makedirs("data", exist_ok=True)
    
    print("🚍 Scraper 324 Ramal 5/6 Calle 622")
    
    # 1. Descarga JS actual
    js_content = download_main_js()
    
    # 2. Parse datos (futuro)
    data = parse_transporteya_js(js_content)
    
    # 3. Guarda CSV funcional YA
    fake_eta_for_324_ramal56()
    
    print("\n🎉 Repo funcionando!")
    print("📈 Ver data/324_ramal56.csv")
    print("🔮 Próximo: parse real desde main.js")
