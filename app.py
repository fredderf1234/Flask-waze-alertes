
from flask import Flask, jsonify
import requests
import csv
from io import StringIO

app = Flask(__name__)

RADAR_DATA_URL = "https://static.data.gouv.fr/resources/radars-routiers/20230425-115722/radars.csv"

def get_radar_data():
    try:
        response = requests.get(RADAR_DATA_URL)
        response.raise_for_status()
        csv_data = response.text
        f = StringIO(csv_data)
        reader = csv.DictReader(f, delimiter=';')
        radars = []
        for row in reader:
            if row.get("latitude") and row.get("longitude"):
                radars.append({
                    "latitude": float(row["latitude"]),
                    "longitude": float(row["longitude"]),
                    "categorie": row.get("type", "Inconnu"),
                    "info": row.get("emplacement", "")
                })
        return radars
    except Exception as e:
        return {"error": str(e)}

@app.route("/radars", methods=["GET"])
def radars():
    data = get_radar_data()
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
