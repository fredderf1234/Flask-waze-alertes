from flask import Flask, jsonify, request
from playwright.sync_api import sync_playwright
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/alertes', methods=['GET'])
def get_alertes():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    radius = request.args.get('radius', 30000)

    if not lat or not lon:
        return jsonify({'error': 'lat and lon are required'}), 400

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()
            page.goto("https://www.waze.com/fr/live-map/")

            page.evaluate(f"""
                () => {{
                    window.W = window.W || {{}};
                    window.W.loginManager = {{ isLoggedIn: () => true }};
                    window.W.map = window.W.map || {{
                        getCenter: () => ({{ lat: {lat}, lon: {lon} }}),
                        getZoom: () => 14
                    }};
                }}
            """)

            page.wait_for_timeout(5000)  # attendre le chargement des alertes

            alerts = page.evaluate("""() => 
                W.map.getModel().alerts.toArray().map(a => ({
                    type: a.type,
                    lat: a.lat,
                    lon: a.lon,
                    roadType: a.roadType,
                    reliability: a.reliability,
                    confidence: a.confidence,
                    subtype: a.subtype,
                    reportDescription: a.reportDescription
                }))
            """)

            browser.close()
            return jsonify({'alertes': alerts})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port=port)
