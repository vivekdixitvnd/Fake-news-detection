# # app_bert.py

# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from transformers import pipeline
# from smart_checker import is_text_suspicious  # 👈 Import the smart checker

# app = Flask(__name__)
# CORS(app)

# # Load zero-shot classification pipeline
# classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# @app.route('/predict', methods=['POST'])
# def predict():
#     data = request.json
#     text = data.get('text', '')

#     # 👇 Pehle smart checker se check karo
#     if is_text_suspicious(text):
#         prediction = "Fake"
#         confidence = 90.0
#     else:
#         # 👇 Agar kuch suspicious nahi mila to model se predict karo
#         labels = ["real", "fake"]
#         result = classifier(text, candidate_labels=labels)

#         prediction = result["labels"][0]
#         confidence = round(result["scores"][0] * 100, 2)

#     return jsonify({
#         'result': prediction.capitalize(),
#         'confidence': confidence
#     })

# if __name__ == '__main__':
#     app.run(debug=False)



from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os  # 👈 NEW: For environment variables
from smart_checker import is_text_suspicious

app = Flask(__name__)
CORS(app)

# Hugging Face API setup
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"
HUGGINGFACE_API_TOKEN = os.environ.get("HUGGINGFACE_API_TOKEN")  # 👈 Fetch from environment
headers = {"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"}

def query_huggingface(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    text = data.get('text', '')

    if is_text_suspicious(text):
        prediction = "Fake"
        confidence = 90.0
    else:
        payload = {
            "inputs": text,
            "parameters": {
                "candidate_labels": ["real", "fake"]
            }
        }
        result = query_huggingface(payload)
        prediction = result["labels"][0]
        confidence = round(result["scores"][0] * 100, 2)

    return jsonify({
        'result': prediction.capitalize(),
        'confidence': confidence
    })

if __name__ == '__main__':
    app.run(debug=False)
