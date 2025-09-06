from flask import Flask, jsonify
from flask_cors import CORS
import random

nicknames = ["dude","guy","bob","thanos","idiot","boi","stupid"]

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return jsonify({
        "name": "dude",
        "age": 420,
        "nickname": "guy"
    })

@app.route("/api/random_nick")
def get_random_nickname():
    return jsonify({
        "id": random.randint(1000, 9999),
        "nickname": random.choice(nicknames)
    })

if (__name__ == "__main__"):
    app.run(host="0.0.0.0", port=5000, debug=True)
