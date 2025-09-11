# Import Modules
from flask import Flask, jsonify
from flask_cors import CORS
import random
import sentence_getter, nltk_path_setter, sentence_dataset

# Set NLTK Path
nltk_path_setter.setPath()

# Load Predefined Sentences and Topics
predefined_sentences, topics_list = sentence_dataset.get_data()

# Create Flask App with CORS
app = Flask(__name__)
CORS(app)


@app.route("/") # Route: Base
def index():
    return "SERVER ONLINE - 200"


@app.route("/toc128_api/get-sentences-on-random-topic/") # Route: Get Sentences Set
def get_random_topic_sentences():
    value = [None, None, None]
    while (not value[0]):
        random_topic = topics_list[random.randint(0, len(topics_list)-1)].title()
        print("Topic:", random_topic)
        value = sentence_getter.get_all_sentences(random_topic)
        print(value)
    return jsonify(value)


@app.route("/toc128_api/get-predefined-sentences-list/") # Route: Get Predefined Sentences
def get_predefined_list():
    return jsonify(predefined_sentences)


# Run app (Debug purposes. Use Gunicorn in final build.)
if (__name__ == "__main__"):
    app.run(host="0.0.0.0", port=10000, debug=True)
