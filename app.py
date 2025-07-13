import os import time import json import requests from flask import Flask, jsonify

app = Flask(name)

URL officielle de la liste des radars (data.gouv.fr ou autre fiable)

RADAR_DATA_URL = "https://data.gouv.fr/fr/datasets/r/1cb544a7-fc3a-48f7-b9e4-0763616c9ff3"  # Remplacer par le bon lien réel

Fichier local temporaire + temps de cache

RADAR_CACHE_FILE = "radars_cache.json" CACHE_DURATION_SECONDS = 86400  # 24h

def is_cache_valid(): if not os.path.exists(RADAR_CACHE_FILE): return False last_modified = os.path.getmtime(RADAR_CACHE_FILE) return (time.time() - last_modified) < CACHE_DURATION_SECONDS

def update_cache(): try: response = requests.get(RADAR_DATA_URL, timeout=10) if response.status_code == 200: with open(RADAR_CACHE_FILE, 'w', encoding='utf-8') as f: f.write(response.text) print("Cache updated successfully.") else: print(f"Failed to download radar data: {response.status_code}") except Exception as e: print(f"Exception while updating cache: {e}")

def load_cached_radars(): with open(RADAR_CACHE_FILE, 'r', encoding='utf-8') as f: return json.load(f)

@app.route("/radars") def get_radars(): if not is_cache_valid(): update_cache() try: radars = load_cached_radars() return jsonify(radars) except Exception as e: return jsonify({"error": f"Failed to load radar data: {str(e)}"}), 500

if name == "main": app.run(host="0.0.0.0", port=5000)

