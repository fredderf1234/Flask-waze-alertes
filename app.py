from flask import Flask, request, jsonify
from flask_cors import CORS
import math
import requests

app = Flask(__name__)
CORS(app)

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # rayon de la Terre en km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * \
        math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

@app.route("/")
def home():
    return "API Waze : en ligne"

@app.route("/alerts", methods=["GET"])
def get_alerts():
    lat = request.args.get("lat", type=float)
    lon = request.args.get("lon", type=float)

    if lat is None or lon is None:
        return jsonify({"error": "Latitude et longitude requises."}), 400

    try:
        url = f"https://www.waze.com/row-rtserver/web/TGeoRSS?tk=community&types=alerts&lat={lat}&lon={lon}&radius=30000"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        data = response.json()

        alertes = []
        for item in data.get("alerts", []):
            distance = haversine(lat, lon, item["location"]["y"], item["location"]["x"])
            if distance <= 30:
                alertes.append({
                    "type": item.get("type"),
                    "subtype": item.get("subtype"),
                    "latitude": item["location"]["y"],
                    "longitude": item["location"]["x"],
                    "distance": round(distance, 2),
                    "reportDescription": item.get("reportDescription")
                })

        return jsonify({"count": len(alertes), "alerts": alertes})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
