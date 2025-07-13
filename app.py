from flask import Flask, jsonify from flask_cors import CORS import requests import json import os import time

app = Flask(name) CORS(app)

CACHE_FILE = "/tmp/radars_cache.json" TIMESTAMP_FILE = "/tmp/last_update.txt" GOUV_URL = "https://data.gouv.fr/fr/datasets/r/45076942-9e4c-4a18-9c2b-1be0d3aef083"  # Exemple URL à remplacer par la bonne UPDATE_INTERVAL = 24 * 60 * 60  # 24 heures

def is_cache_stale(): if not os.path.exists(CACHE_FILE) or not os.path.exists(TIMESTAMP_FILE): return True with open(TIMESTAMP_FILE, "r") as f: last_update = float(f.read().strip()) return time.time() - last_update > UPDATE_INTERVAL

def update_cache(): try: response = requests.get(GOUV_URL) if response.status_code == 200: with open(CACHE_FILE, "w", encoding="utf-8") as f: f.write(response.text) with open(TIMESTAMP_FILE, "w") as t: t.write(str(time.time())) print("Cache mis à jour avec succès.") else: print(f"Erreur HTTP {response.status_code} lors de la mise à jour.") except Exception as e: print(f"Exception lors du téléchargement des radars: {e}")

@app.route("/") def home(): return "API radars opérationnelle. Utilisez /radars pour obtenir les données."

@app.route("/radars") def get_radars(): if is_cache_stale(): update_cache() if os.path.exists(CACHE_FILE): with open(CACHE_FILE, "r", encoding="utf-8") as f: try: data = json.load(f) return jsonify(data) except json.JSONDecodeError: return jsonify({"error": "JSON invalide dans le cache."}), 500 else: return jsonify({"error": "Cache introuvable."}), 404

if name == "main": app.run(host="0.0.0.0", port=5000)

