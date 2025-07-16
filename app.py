from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return 'API Waze opérationnelle ✅'

@app.route('/alertes')
def alertes():
    lat = request.args.get('lat')
    lon = request.args.get('lon')

    if not lat or not lon:
        return jsonify({'error': 'Latitude et longitude requises'}), 400

    try:
        url = f'https://www.waze.com/row-rtserver/web/TGeoRSS?bottom={float(lat)-0.3}&left={float(lon)-0.3}&ma=600&mj=300&right={float(lon)+0.3}&top={float(lat)+0.3}&types=alerts'
        headers = {
            'User-Agent': 'Mozilla/5.0'
        }
        response = requests.get(url, headers=headers)
        data = response.json()

        alertes_filtrees = []
        for alerte in data.get("alerts", []):
            alertes_filtrees.append({
                "type": alerte.get("type"),
                "latitude": alerte.get("location", {}).get("y"),
                "longitude": alerte.get("location", {}).get("x"),
                "description": alerte.get("reportDescription", ""),
                "distance": 0  # Distance calculée côté PHP si nécessaire
            })

        return jsonify(alertes_filtrees)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
