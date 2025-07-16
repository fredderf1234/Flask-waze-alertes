import os
import asyncio
from flask import Flask, jsonify, send_file
from playwright.async_api import async_playwright

app = Flask(__name__)

# Route pour renvoyer l'image actuelle
@app.route('/scan')
def scan_image():
    path = "capture/latest.jpg"
    if not os.path.exists(path):
        return jsonify({"error": "No screenshot available"})
    return send_file(path, mimetype='image/jpeg')


# Route pour déclencher une nouvelle capture
@app.route('/refresh')
def refresh():
    asyncio.run(capture_screenshot())
    return jsonify({"status": "Screenshot captured successfully"})


# Fonction asynchrone pour prendre un screenshot de la carte Waze
async def capture_screenshot():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://www.waze.com/fr/live-map/")
        await page.wait_for_timeout(8000)  # Attend 8 secondes le chargement complet
        os.makedirs("capture", exist_ok=True)
        await page.screenshot(path="capture/latest.jpg")
        await browser.close()


# Lancement de l'app Flask sur le port 3000 (utilisé par Railway)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
