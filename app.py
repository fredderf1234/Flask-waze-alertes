
import os
import time
import json
import requests
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/radars')
def get_radars():
    # Exemple de données à remplacer par une récupération dynamique si besoin
    data = {
        "radars": [
            {"type": "Radar Fixe", "latitude": 43.6, "longitude": 1.44},
            {"type": "Radar Feu Rouge", "latitude": 43.61, "longitude": 1.45}
        ]
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
