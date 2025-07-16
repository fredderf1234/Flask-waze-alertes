from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright
import math

app = Flask(__name__)

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Rayon terrestre en km
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = math.sin(d_lat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(d_lon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

@app.route("/alertes")
def get_alertes():
    lat = float(request.args.get("lat", "0"))
    lon = float(request.args.get("lon", "0"))
    radius = float(request.args.get("radius", "30"))

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://www.waze.com/livemap")

        page.wait_for_timeout(5000)  # Laisse Waze charger les données

        alerts = page.evaluate("() => W.map.getModel().alerts.toArray().map(a => ({ 
            id: a.attributes.id, 
            type: a.attributes.type, 
            subtype: a.attributes.subtype, 
            location: a.attributes.location, 
            reportDescription: a.attributes.reportDescription || '', 
            reliability: a.attributes.reliability 
        }))")

        browser.close()

    filtered = []
    for alert in alerts:
        a_lat = alert["location"]["y"]
        a_lon = alert["location"]["x"]
        distance = haversine(lat, lon, a_lat, a_lon)
        if distance <= radius:
            alert["distance_km"] = round(distance, 2)
            filtered.append(alert)

    filtered.sort(key=lambda x: x["distance_km"])
    return jsonify(filtered)
