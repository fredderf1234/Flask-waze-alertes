from flask import Flask, jsonify
from playwright.sync_api import sync_playwright

app = Flask(__name__)

@app.route("/alerts")
def get_alerts():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://www.waze.com/live-map/", timeout=60000)
        page.wait_for_timeout(8000)  # Attendre que les alertes apparaissent

        # Exemple de récupération très simple (à adapter si les alertes sont dans JS)
        content = page.content()
        browser.close()
        return jsonify({"html_snapshot": content})