
from flask import Flask, request, jsonify
import csv
import math

app = Flask(__name__)

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))

@app.route('/')
def home():
    return 'API Flask opérationnelle. Utilisez /alertes?lat=...&lon=...&rayon=...'

@app.route('/alertes')
def alertes():
    lat = float(request.args.get('lat'))
    lon = float(request.args.get('lon'))
    rayon = float(request.args.get('rayon', 30))

    alertes_proches = []

    with open('radars.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                radar_lat = float(row['latitude'])
                radar_lon = float(row['longitude'])
                distance = haversine(lat, lon, radar_lat, radar_lon)
                if distance <= rayon:
                    row['distance_km'] = round(distance, 2)
                    alertes_proches.append(row)
            except Exception as e:
                continue

    alertes_proches.sort(key=lambda x: x['distance_km'])
    return jsonify(alertes_proches)
