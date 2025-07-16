
from flask import Flask, request, jsonify
import asyncio
from playwright.async_api import async_playwright
from math import radians, cos, sin, asin, sqrt

app = Flask(__name__)

def haversine(lon1, lat1, lon2, lat2):
    R = 6371  # Rayon de la Terre en km
    dlon = radians(lon2 - lon1)
    dlat = radians(lat2 - lat1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    return 2 * R * asin(sqrt(a))

@app.route("/alertes")
async def alertes():
    lat = request.args.get("lat", type=float)
    lon = request.args.get("lon", type=float)
    if lat is None or lon is None:
        return jsonify({"error": "Missing lat/lon"}), 400

    radius_km = 30

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://www.waze.com/livemap")
        await page.wait_for_timeout(5000)

        alerts = await page.evaluate("() => W.map.getModel().alerts.toArray()")
        await browser.close()

    filtered_alerts = []
    for alert in alerts:
        alert_lat = alert.get("location", {}).get("y")
        alert_lon = alert.get("location", {}).get("x")
        if alert_lat is not None and alert_lon is not None:
            distance = haversine(lon, lat, alert_lon, alert_lat)
            if distance <= radius_km:
                alert["distance_km"] = round(distance, 1)
                filtered_alerts.append(alert)

    filtered_alerts.sort(key=lambda x: x.get("distance_km", 9999))
    return jsonify(filtered_alerts)
