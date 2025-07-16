import os
from flask import Flask, jsonify, send_file
from playwright.async_api import async_playwright

app = Flask(__name__)

@app.route('/scan')
def scan_image():
    path = "capture/latest.jpg"
    if not os.path.exists(path):
        return jsonify({"error": f"No screenshot found at '{path}'"})
    return send_file(path, mimetype='image/jpeg')

async def capture_screenshot():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("https://www.waze.com/fr/live-map/")
        await page.wait_for_timeout(8000)
        os.makedirs("capture", exist_ok=True)
        await page.screenshot(path="capture/latest.jpg")
        await browser.close()

@app.route('/refresh')
def refresh_capture():
    import asyncio
    try:
        asyncio.run(capture_screenshot())
        return jsonify({"status": "Capture OK"})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/')
def root():
    return jsonify({"message": "API Waze opérationnelle", "endpoints": ["/refresh", "/scan"]})

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 3000))
    app.run(host='0.0.0.0', port=port)
