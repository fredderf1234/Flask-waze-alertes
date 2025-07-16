from flask import Flask, jsonify, send_file
import os
from playwright.async_api import async_playwright
import asyncio

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "message": "Bienvenue sur l'API Waze",
        "routes": ["/refresh", "/scan"]
    })

@app.route('/scan')
def scan_image():
    path = "capture/latest.jpg"
    if not os.path.exists(path):
        return jsonify({"error": "No screenshot available"})
    return send_file(path, mimetype='image/jpeg')

@app.route('/refresh')
def refresh():
    asyncio.run(capture_screenshot())
    return jsonify({"status": "screenshot captured"})

async def capture_screenshot():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("https://www.waze.com/live-map")
        await page.wait_for_timeout(8000)  # attendre que la carte charge
        os.makedirs("capture", exist_ok=True)
        await page.screenshot(path="capture/latest.jpg")
        await browser.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 3000)))
