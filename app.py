from flask import Flask, send_file, jsonify
import os
import asyncio
from playwright.async_api import async_playwright

app = Flask(__name__)

# Assure que le dossier 'capture' existe
os.makedirs("capture", exist_ok=True)

@app.route('/capture')
def trigger_capture():
    try:
        asyncio.run(capture_screenshot())
        return jsonify({"success": True, "message": "Screenshot captured."})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/scan')
def scan_image():
    path = "capture/latest.jpg"
    if not os.path.exists(path):
        return jsonify({"error": f"No screenshot found at '{path}'"})
    return send_file(path, mimetype='image/jpeg')

async def capture_screenshot():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://www.waze.com/live-map")
        await page.wait_for_timeout(8000)  # Attendre le rendu de la carte
        await page.screenshot(path="capture/latest.jpg")
        await browser.close()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 3000))
    app.run(host='0.0.0.0', port=port)
