#!/usr/bin/env python3
import os
import json
import requests
from datetime import datetime

# --- API Key (vai ser passada como GitHub Secret) ---

api_key = os.environ.get("STORMGLASS_API_KEY")
if not api_key:
    raise ValueError("API key StormGlass não encontrada! Configure o secret STORMGLASS_API_KEY no GitHub.")


# --- Local do JSON final ---
OUTPUT_DIR = "docs/"

# --- Coordenadas ---
SPOTS = {
  "peniche":   { "lat": 39.363007, "lng": -9.414682 },
  "ericeira":  { "lat": 38.966127, "lng": -9.424674 },
  "lisboa":    { "lat": 38.646397, "lng": -9.330245 },
  "sines":     { "lat": 37.850821, "lng": -8.805547 },
  "sagres":    { "lat": 37.038705, "lng": -8.875115 },
}


# --- Parâmetros a buscar ---
PARAMS = [
    "windSpeed",
    "windDirection",
    "swellHeight",
    "swellPeriod",
    "swellDirection",
    "secondarySwellHeight",
    "secondarySwellPeriod",
    "secondarySwellDirection",
    "waveHeight",
    "wavePeriod",
    "waveDirection",
    "windWaveHeight",
    "windWavePeriod",
    "windWaveDirection",
    "airTemperature",
    "waterTemperature",
    "cloudCover",
    "precipitation"
]

# --- URL StormGlass ---
url = f"https://api.stormglass.io/v2/weather/point?lat={LAT}&lng={LNG}&params={','.join(PARAMS)}"

headers = {
    "Authorization": api_key
}

# --- Fazer fetch ---
print("🔹 A buscar dados StormGlass...")
response = requests.get(url, headers=headers, timeout=20)
response.raise_for_status()  # falha se status != 200
data = response.json()

# --- Criar estrutura final com timestamp ---
output = {
    "generated_at": datetime.utcnow().isoformat() + "Z",
    "location": {"lat": lat, "lng": lng},
    "data": data.get("hours", [])
}

# --- Escrever no ficheiro docs/forecast.json ---
for name, spot in SPOTS.items():
    data = fetch_stormglass(spot["lat"], spot["lng"])
    save_json(f"docs/{name}.json", data)

print(f"✅ {name}.json atualizado em {OUTPUT_DIR}")
