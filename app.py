

from flask import Flask, request, jsonify from flask_cors import CORS from waze_scraper import obtenir_waze_alertes

app = Flask(name) CORS(app)

@app.route('/alertes', methods=['GET']) def alertes(): lat = request.args.get('lat', type=float) lon = request.args.get('lon', type=float)

if lat is None or lon is None:
    return jsonify({"error": "Latitude ou longitude manquante"}), 400

donnees_alertes = obtenir_waze_alertes(lat, lon)
return jsonify(alertes=donnees_alertes)

if name == 'main': app.run(debug=True)

