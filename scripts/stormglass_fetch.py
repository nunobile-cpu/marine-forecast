#!/usr/bin/env python3
import os
import json
import requests
from datetime import datetime

# --- API Key (vai ser passada como GitHub Secret) ---

api_key = os.environ.get("STORMGLASS_API_KEY")
if not api_key:
    raise ValueError("API key StormGlass não encontrada! Configure o secret STORMGLASS_API_KEY no GitHub.")

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

# --- Fetch ---
for name, spot in SPOTS.items():
    lat = spot["lat"]
    lng = spot["lng"]

    url = (
        "https://api.stormglass.io/v2/weather/point"
        f"?lat={lat}&lng={lng}&params={','.join(PARAMS)}"
    )

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()

    with open(f"docs/{name}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✔️ {name}.json atualizado")
