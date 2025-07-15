from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return 'API Flask opérationnelle'

@app.route('/alertes', methods=['GET'])
def get_alertes():
    try:
        # Simule des données factices pour test
        alertes = [
            {
                'title': 'Accident sur la route',
                'description': 'Voiture en panne voie de droite',
                'date': 'Tue, 16 Jul 2025 10:00:00 GMT',
                'latitude': 43.9,
                'longitude': -1.1
            },
            {
                'title': 'Radar fixe',
                'description': 'Radar 110 km/h',
                'date': 'Tue, 16 Jul 2025 11:00:00 GMT',
                'latitude': 43.91,
                'longitude': -1.12
            }
        ]
        return jsonify(alertes)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)