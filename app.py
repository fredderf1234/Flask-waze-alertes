from flask import Flask, request, jsonify
import requests
import time

app = Flask(__name__)

@app.route('/')
def accueil():
    return 'Serveur Flask opérationnel.'

@app.route('/alertes')
def alertes():
    try:
        lat = float(request.args.get('lat'))
        lon = float(request.args.get('lon'))
        rayon = float(request.args.get('rayon', 30)) * 1000

        url = f'https://www.waze.com/row-rtserver/web/TGeoRSS?bottom={lat - 0.3}&left={lon - 0.3}&ma=600&mj=300&right={lon + 0.3}&top={lat + 0.3}&types=alerts'
        r = requests.get(url)
        data = r.json()

        def distance(a, b):
            from math import radians, cos, sin, asin, sqrt
            lon1, lat1, lon2, lat2 = map(radians, [a[1], a[0], b[1], b[0]])
            dlon = lon2 - lon1
            dlat = lat2 - lat1
            a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
            return 6371000 * 2 * asin(sqrt(a))

        result = []
        now = time.time()
        emoji_map = {
            "ACCIDENT": "💥",
            "JAM": "🚗",
            "POLICE": "👮",
            "HAZARD": "⚠️",
            "ROAD_CLOSED": "⛔",
            "CONSTRUCTION": "🚧",
            "MISC": "❓"
        }

        for alert in data.get("alerts", []):
            position = alert.get("location", {})
            alert_lat = position.get("y")
            alert_lon = position.get("x")
            if alert_lat is None or alert_lon is None:
                continue

            dist = distance((lat, lon), (alert_lat, alert_lon))
            if dist <= rayon:
                age = int((now - alert.get("pubMillis", now * 1000) / 1000) / 60)
                result.append({
                    "type": alert.get("type", "UNKNOWN"),
                    "latitude": alert_lat,
                    "longitude": alert_lon,
                    "distance": round(dist),
                    "votes": alert.get("nThumbsUp", 0),
                    "age_minutes": age,
                    "emoji": emoji_map.get(alert.get("type", "MISC"), "❓")
                })

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
