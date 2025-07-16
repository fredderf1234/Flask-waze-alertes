from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return "API Waze : en ligne"

@app.route("/alerts")
def alerts():
    return jsonify({
        "status": "ok",
        "message": "Le serveur fonctionne, Playwright est désactivé pour le test"
    })
