
from flask import Flask, jsonify, request
import requests
import json

app = Flask(__name__)

@app.route('/alertes')
def get_alertes():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    rayon = request.args.get('rayon')

    if not lat or not lon or not rayon:
        return jsonify({'error': 'Paramètres lat, lon et rayon requis'}), 400

    try:
        url = f"https://www.waze.com/row-rtserver/web/TGeoRSS?bottom={float(lat)-0.2}&left={float(lon)-0.2}&ma=600&mj=100&right={float(lon)+0.2}&top={float(lat)+0.2}&types=alerts&region=EU"
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            return jsonify({'error': f"Erreur Waze {response.status_code}"}), 502

        try:
            data = response.json()
        except json.JSONDecodeError:
            return jsonify({'error': 'Réponse Waze invalide (pas du JSON)'}), 502

        alertes = data.get("alerts", [])
        resultats = []

        for alerte in alertes:
            resultats.append({
                "type": alerte.get("type"),
                "latitude": alerte.get("location", {}).get("y"),
                "longitude": alerte.get("location", {}).get("x"),
                "description": alerte.get("reportDescription", ""),
                "route": alerte.get("roadType", ""),
                "confidence": alerte.get("confidence", 0)
            })

        return jsonify(resultats)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()