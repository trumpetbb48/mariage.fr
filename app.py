from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os

app = Flask(__name__, static_folder="static")
CORS(app)

COMMANDES_FILE = "commandes.json"

def load_commandes():
    if not os.path.exists(COMMANDES_FILE):
        with open(COMMANDES_FILE, 'w') as f:
            json.dump([], f)
    with open(COMMANDES_FILE, 'r') as f:
        return json.load(f)

def save_commande(commande):
    commandes = load_commandes()
    commandes.append(commande)
    with open(COMMANDES_FILE, 'w') as f:
        json.dump(commandes, f, indent=4)

@app.route('/commande', methods=['POST'])
def recevoir_commande():
    data = request.get_json()
    save_commande(data)
    return f"Commande de la table {data.get('table')} bien reçue !"

@app.route('/commandes', methods=['GET'])
def afficher_commandes():
    return jsonify(load_commandes())

# Routes pour afficher les pages
@app.route('/')
def menu_page():
    return send_from_directory('static', 'menu.html')

@app.route('/admin')
def admin_page():
    return send_from_directory('static', 'commandes.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
