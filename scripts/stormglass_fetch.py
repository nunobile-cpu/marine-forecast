#!/usr/bin/env python3
import os
import json
import requests
from datetime import datetime

# --- API Key (vai ser passada como GitHub Secret) ---
API_KEY = os.getenv("STORMGLASS_API_KEY")
if not API_KEY:
    raise RuntimeError("ERRO: Defina a variável de ambiente STORMGLASS_API_KEY")

# --- Local do JSON final ---
OUTPUT_FILE = "docs/forecast.json"

# --- Coordenadas da Ericeira ---
LAT, LNG = 38.969, -9.420

# --- Parâmetros a buscar ---
PARAMS = [
    "windSpeed",
    "windDirection",
    "waveHeight",
    "wavePeriod",
    "waveDirection",
    "airTemperature",
    "waterTemperature",
    "cloudCover",
    "precipitation"
]

# --- URL StormGlass ---
url = f"https://api.stormglass.io/v2/weather/point?lat={LAT}&lng={LNG}&params={','.join(PARAMS)}"

headers = {
    "Authorization": API_KEY
}

# --- Fazer fetch ---
print("🔹 A buscar dados StormGlass...")
response = requests.get(url, headers=headers, timeout=20)
response.raise_for_status()  # falha se status != 200
data = response.json()

# --- Criar estrutura final com timestamp ---
output = {
    "generated_at": datetime.utcnow().isoformat() + "Z",
    "location": {"lat": LAT, "lng": LNG},
    "data": data.get("hours", [])
}

# --- Escrever no ficheiro docs/forecast.json ---
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2)

print(f"✅ forecast.json atualizado em {OUTPUT_FILE}")
