from flask import Flask, request, jsonify
from flask_cors import CORS
from waze_scraper import obtenir_waze_alertes

app = Flask(__name__)
CORS(app)  # Autorise les appels depuis le navigateur

@app.route('/')
def index():
    return jsonify({"message": "API Waze opérationnelle"})

@app.route('/alertes', methods=['GET'])
def alertes():
    try:
        lat = float(request.args.get("lat"))
        lon = float(request.args.get("lon"))
    except (TypeError, ValueError):
        return jsonify({"error": "Paramètres lat et lon requis"}), 400

    alertes = obtenir_waze_alertes(lat, lon)
    return jsonify(alertes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
