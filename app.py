
from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright
import os

app = Flask(__name__)

@app.route("/alertes", methods=["GET"])
def get_alertes():
    lat = request.args.get("lat")
    lon = request.args.get("lon")

    if not lat or not lon:
        return jsonify({"error": "lat and lon are required"}), 400

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()
            url = f"https://www.waze.com/live-map?ll={lat}%2C{lon}&z=13"
            page.goto(url, timeout=60000)
            page.wait_for_timeout(10000)

            elements = page.query_selector_all('img[src*="Traffic_Police"], img[src*="Traffic_Jam"], img[src*="Accident"]')
            alertes = []

            for el in elements:
                box = el.bounding_box()
                src = el.get_attribute("src")
                if box and src:
                    alert_type = "police" if "Traffic_Police" in src else "bouchon" if "Traffic_Jam" in src else "accident"
                    alertes.append({
                        "type": alert_type,
                        "position": {"x": box["x"], "y": box["y"]}
                    })

            browser.close()
            return jsonify({"alertes": alertes})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 80))
    app.run(host="0.0.0.0", port=port)
