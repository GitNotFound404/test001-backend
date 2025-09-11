# Import Modules
from flask import Flask, jsonify
from flask_cors import CORS
import sentence_dataset

# Create Flask App with CORS
app = Flask(__name__)
CORS(app)

sentences = sentence_dataset.getSentences()

@app.route("/") # Route: Base
def index():
    return "SERVER ONLINE - 200"


@app.route("/toc128_api/get_sentences_list/") # Route: Get Sentences List
def get_sentences_list():
    return jsonify(sentences)


# Run app (Debug purposes. Use Gunicorn in final build.)
# if (__name__ == "__main__"):
#    app.run(host="0.0.0.0", port=10000, debug=True)
