from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "API Waze opérationnelle ✅"

@app.route("/alerts")
def get_alerts():
    # Cette partie sera remplacée par le scraping Playwright
    # Pour l’instant, retourne un exemple simple
    example_data = [
        {"type": "police", "latitude": 43.6, "longitude": -1.4, "distance_km": 2.4},
        {"type": "accident", "latitude": 43.61, "longitude": -1.42, "distance_km": 5.1}
    ]
    return jsonify(example_data)
