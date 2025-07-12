import requests
import time

def obtenir_waze_alertes(lat, lon, rayon_km=25):
    url = "https://www.waze.com/row-rtserver/web/TGeoRSS"
    params = {
        "bottom": lat - 0.2,
        "left": lon - 0.2,
        "right": lon + 0.2,
        "top": lat + 0.2,
        "types": "alerts",
    }

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        alertes = []
        if "alerts" in data:
            for a in data["alerts"]:
                alertes.append({
                    "type": a.get("type", "Inconnu"),
                    "subtype": a.get("subtype", ""),
                    "location": {
                        "lat": a["location"]["y"],
                        "lon": a["location"]["x"]
                    },
                    "distance": None,  # sera calculée côté client JS si besoin
                    "reportRating": a.get("nThumbsUp", 0),
                    "reportBy": a.get("reportDescription", ""),
                    "pubMillis": a.get("pubMillis", int(time.time() * 1000))
                })

        return alertes

    except Exception as e:
        print("Erreur récupération alertes Waze :", str(e))
        return []
