#!/usr/bin/env python3
import requests
import csv
import json
from datetime import datetime
from time import sleep

BASE_URL = "https://app.transporteya.com.ar"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
    "Referer": "https://app.transporteya.com.ar/app/",
    "Accept": "application/json"
}

def get_324_stops():
    resp = requests.get(f"{BASE_URL}/api/line/324/stops", headers=HEADERS)
    return resp.json()

def get_stop_eta(stop_id):
    url = f"{BASE_URL}/api/stop/{stop_id}/arrivals?line=324"
    resp = requests.get(url, headers=HEADERS)
    return resp.json()

def find_parada(stops):
    target = "calle 622".lower()
    for stop in stops:
        if target in stop.get("name", "").lower():
            return stop["id"], stop["name"]
    return None, "No encontrada"

def scrape_324_ramal56():
    stops = get_324_stops()
    stop_id, stop_name = find_parada(stops)
    
    if not stop_id:
        print("❌ Parada 'Calle 622' no encontrada")
        return
    
    print(f"🚌 Scraping parada: {stop_name} (ID: {stop_id})")
    eta_data = get_stop_eta(stop_id)
    
    # Filtra solo ramales 5/6
    arrivals = [a for a in eta_data.get("arrivals", []) 
                if any(ramal in a.get("route", "") for ramal in ["5", "6"])]
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open("data/324_ramal56.csv", "a", newline="") as f:
        writer = csv.writer(f)
        if f.tell() == 0:  # Header
            writer.writerow(["timestamp", "parada", "ramal", "eta", "distancia"])
        
        for arrival in arrivals:
            writer.writerow([
                timestamp,
                stop_name,
                arrival.get("route", ""),
                arrival.get("eta", ""),
                arrival.get("distance", "")
            ])
    
    print(f"✅ Guardado {len(arrivals)} llegadas: {arrivals}")

if __name__ == "__main__":
    scrape_324_ramal56()
