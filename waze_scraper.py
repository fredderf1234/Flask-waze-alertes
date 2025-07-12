from flask import Flask, jsonify
from flask_cors import CORS
from waze_scraper import get_waze_alertes

app = Flask(__name__)
CORS(app)

@app.route('/alertes', methods=['GET'])
def alertes():
    alertes_data = get_waze_alertes()
    return jsonify(alertes=alertes_data)

if __name__ == '__main__':
    app.run(debug=True)
