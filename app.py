import requests
import json
import threading
import time
from flask import Flask, jsonify

app = Flask(__name__)

url = "https://api.hiddenclearances.com/api/v1/penny-deals"

with open("keys.json", "r") as f:
    keys = json.load(f)

data_store = {}

def updater():
    while True:
        for name, headers in keys.items():
            try:
                r = requests.get(url, headers=headers, timeout=10)
                if r.status_code == 200:
                    data_store[name] = r.json()
            except:
                pass
        time.sleep(1)

threading.Thread(target=updater, daemon=True).start()

@app.route("/josh.json")
def josh():
    return jsonify(data_store.get("josh", {}))

@app.route("/dem.json")
def dem():
    return jsonify(data_store.get("dem", {}))

@app.route("/")
def home():
    return jsonify({"status": "running"})
