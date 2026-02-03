#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import csv
import time
from datetime import datetime
import os

def scrape_real_324():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        print("🔍 Cargando app...")
        driver.get("https://app.transporteya.com.ar/app/")
        time.sleep(5)
        
        # Busca "324"
        search_box = driver.find_element(By.CSS_SELECTOR, "input[placeholder*='buscar']")
        search_box.send_keys("324")
        time.sleep(3)
        
        # Extrae ETAs del mapa/lista
        etas = driver.find_elements(By.CSS_SELECTOR, "[class*='eta'], [class*='arrival'], time")
        print(f"📊 {len(etas)} llegadas encontradas")
        
        # Guarda CSV
        os.makedirs("data", exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open("data/324_real.csv", "a", newline="") as f:
            writer = csv.writer(f)
            if f.tell() == 0:
                writer.writerow(["timestamp", "eta", "ramal", "distancia"])
            
            for eta in etas[:3]:  # Primeras 3
                text = eta.text.strip()
                if any(x in text for x in ['324', '5', '6']):
                    writer.writerow([timestamp, text, "324-5/6", "live"])
        
        print("✅ Datos REALES guardados")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_real_324()
