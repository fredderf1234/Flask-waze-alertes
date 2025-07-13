from flask import Flask, jsonify
from flask_cors import CORS
import requests
import os
import time
import json

app = Flask(__name__)
CORS(app)

RADARS_URL = "https://your-data-source-link/radars.json"  # Remplace par le vrai lien officiel
CACHE_FILE = "/tmp/radars.json"
CACHE_DURATION = 86400  # 24 heures en secondes

def download_and_cache_radars():
    try:
        response = requests.get(RADARS_URL)
        if response.status_code == 200:
            with open(CACHE_FILE, "w") as f:
                f.write(response.text)
            return response.json()
        else:
            print(f"Erreur téléchargement radars : {response.status_code}")
            return None
    except Exception as e:
        print(f"Erreur réseau : {e}")
        return None

def get_cached_radars():
    if os.path.exists(CACHE_FILE):
        file_time = os.path.getmtime(CACHE_FILE)
        if time.time() - file_time < CACHE_DURATION:
            with open(CACHE_FILE, "r") as f:
                return json.load(f)
    return download_and_cache_radars()

@app.route("/")
def home():
    return "API radars opérationnelle. Utilisez /radars pour les données."

@app.route("/radars")
def radars():
    data = get_cached_radars()
    if data:
        return jsonify(data)
    else:
        return jsonify({"error": "Données indisponibles"}), 500

if __name__ == "__main__":
    app.run(debug=True)
