from flask import Flask, request, jsonify
import requests
from datetime import datetime
import time

app = Flask(__name__)

@app.route('/alertes')
def alertes():
    try:
        lat = float(request.args.get('lat'))
        lon = float(request.args.get('lon'))
        rayon = float(request.args.get('rayon', 30))  # rayon par défaut = 30 km

        delta = rayon / 111  # approx. conversion deg -> km

        url = f"https://www.waze.com/row-rtserver/web/TGeoRSS?bottom={lat - delta}&top={lat + delta}&left={lon - delta}&right={lon + delta}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=headers)
        data = r.json()

        alertes = []
        now = int(time.time())

        for item in data.get("alerts", []):
            alert_lat = item.get("location", {}).get("y")
            alert_lon = item.get("location", {}).get("x")
            alert_type = item.get("type", "inconnu").upper()
            n_thumbsup = item.get("nThumbsUp", 0)
            pub_millis = item.get("pubMillis", now * 1000)
            age_min = round((now - pub_millis / 1000) / 60)

            alertes.append({
                "type": alert_type,
                "lat": alert_lat,
                "lon": alert_lon,
                "votes": n_thumbsup,
                "age_minutes": age_min,
                "emoji": type_to_emoji(alert_type)
            })

        return jsonify(alertes)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def type_to_emoji(alert_type):
    mapping = {
        "ACCIDENT": "🚧",
        "POLICE": "👮",
        "JAM": "🚗",
        "ROAD_CLOSED": "⛔",
        "HAZARD": "⚠️",
        "CONSTRUCTION": "🏗️",
        "WEATHERHAZARD": "🌧️",
        "inconnu": "❓"
    }
    return mapping.get(alert_type, "❓")

if __name__ == '__main__':
    app.run()
