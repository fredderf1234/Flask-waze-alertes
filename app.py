from flask import Flask, request, jsonify
import requests
import xml.etree.ElementTree as ET
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return 'API Flask opérationnelle'

@app.route('/alertes', methods=['GET'])
def get_alertes():
    try:
        lat = float(request.args.get('lat'))
        lon = float(request.args.get('lon'))
        rayon = float(request.args.get('rayon'))

        # Nouvelle URL Waze à jour
        url = f"https://www.waze.com/live-map/api/georss?bottom={lat - 0.2}&left={lon - 0.2}&right={lon + 0.2}&top={lat + 0.2}&types=alerts"
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            return jsonify({"error": f"Erreur Waze {response.status_code}"}), 502

        # Traitement XML
        xml_root = ET.fromstring(response.text)
        alertes = []

        for item in xml_root.findall('.//item'):
            title = item.findtext('title')
            description = item.findtext('description')
            pub_date = item.findtext('pubDate')
            lat_elem = item.find('{http://www.georss.org/georss}point')

            if lat_elem is not None:
                latlon = lat_elem.text.split()
                if len(latlon) == 2:
                    alertes.append({
                        'title': title,
                        'description': description,
                        'date': pub_date,
                        'latitude': float(latlon[0]),
                        'longitude': float(latlon[1])
                    })

        return jsonify(alertes)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)