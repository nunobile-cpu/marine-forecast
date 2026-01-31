import requests
import json
from datetime import datetime, timezone

API_KEY = os.environ["STORMGLASS_API_KEY"]

LAT = 38.969
LNG = -9.420

PARAMS = ",".join([
    "windSpeed",
    "windDirection",
    "waveHeight",
    "wavePeriod",
    "waveDirection",
    "airTemperature",
    "waterTemperature"
])

URL = (
    f"https://api.stormglass.io/v2/weather/point"
    f"?lat={LAT}&lng={LNG}&params={PARAMS}"
)

headers = {
    "Authorization": API_KEY
}

print("🌊 Fetch Stormglass...")
r = requests.get(URL, headers=headers)
r.raise_for_status()

data = r.json()

forecast = {
    "meta": {
        "source": "stormglass",
        "generated_at": datetime.now(timezone.utc).isoformat()
    },
    "hours": []
}

for h in data["hours"][:72]:  # 3 dias
    forecast["hours"].append({
        "time": h["time"],
        "windSpeed": h["windSpeed"]["sg"],
        "windDirection": h["windDirection"]["sg"],
        "waveHeight": h["waveHeight"]["sg"],
        "wavePeriod": h["wavePeriod"]["sg"],
        "waveDirection": h["waveDirection"]["sg"],
        "airTemperature": h["airTemperature"]["sg"],
        "waterTemperature": h["waterTemperature"]["sg"]
    })

with open("public/forecast.json", "w") as f:
    json.dump(forecast, f, indent=2)

print("✅ forecast.json atualizado")
