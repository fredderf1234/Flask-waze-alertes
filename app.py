import time
import json
import requests
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

RADAR_URL = "https://www.data.gouv.fr/fr/datasets/r/ad6db29d-1b7a-4b00-a8e8-21beeb2a3a1a"  # fichier JSON radars
CACHE_DURATION = 24 * 60 * 60  # 24 heures en secondes

radar_data = None
last_update_time = 0

def fetch_radar_data():
    global radar_data, last_update_time
    try:
        response = requests.get(RADAR_URL)
        if response.status_code == 200:
            radar_data = response.json()
            last_update_time = time.time()
            print("✔️ Données radars mises à jour depuis la source")
        else:
            print(f"❌ Erreur de récupération des radars : {response.status_code}")
    except Exception as e:
        print(f"❌ Exception pendant récupération des radars : {e}")

@app.route("/radars", methods=["GET"])
def get_radars():
    global radar_data, last_update_time
    if radar_data is None or (time.time() - last_update_time > CACHE_DURATION):
        fetch_radar_data()
    return jsonify(radar_data)

@app.route("/")
def home():
    return "API radars opérationnelle. Utilisez /radars pour récupérer les données."

if __name__ == "__main__":
    app.run()
