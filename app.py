from flask import Flask, request, jsonify
from flask_cors import CORS
import asyncio
from playwright.async_api import async_playwright

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return "API Waze : en ligne"

@app.route("/alerts", methods=["GET"])
def get_alerts():
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    if not lat or not lon:
        return jsonify({"error": "Coordonnées GPS manquantes"}), 400

    try:
        alerts = asyncio.run(scrape_alerts(lat, lon))
        return jsonify(alerts)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

async def scrape_alerts(lat, lon):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto("https://www.waze.com/fr/livemap")

        await page.wait_for_timeout(5000)  # Attendre le chargement de la carte

        # Tu peux ici cliquer, simuler un zoom, ou interagir avec la carte si besoin
        content = await page.content()

        await browser.close()

        # Exemple de retour factice pour test
        return {
            "status": "ok",
            "position": {"lat": lat, "lon": lon},
            "alerts": ["alert1", "alert2", "alert3"]
        }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
