# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import requests
# import os
# from smart_checker import is_text_suspicious

# app = Flask(__name__)
# CORS(app)

# API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"
# HUGGINGFACE_API_TOKEN = os.environ.get("HUGGINGFACE_API_TOKEN")
# headers = {"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"}

# def query_huggingface(payload):
#     response = requests.post(API_URL, headers=headers, json=payload)
#     if response.status_code != 200:
#         raise Exception(f"Huggingface API error: {response.status_code} - {response.text}")
#     return response.json()

# @app.route('/predict', methods=['POST'])
# def predict():
#     try:
#         data = request.json
#         text = data.get('text', '')

#         if is_text_suspicious(text):
#             prediction = "Fake"
#             confidence = 90.0
#         else:
#             payload = {
#                 "inputs": text,
#                 "parameters": {
#                     "candidate_labels": ["real", "fake"]
#                 }
#             }
#             result = query_huggingface(payload)
#             prediction = result["labels"][0]
#             confidence = round(result["scores"][0] * 100, 2)

#         return jsonify({
#             'result': prediction.capitalize(),
#             'confidence': confidence
#         })
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500  # 👈 Safe error response in JSON

# if __name__ == '__main__':
#     app.run(debug=False)

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from smart_checker import is_text_suspicious

app = Flask(__name__)

# ✅ Replace this:
# CORS(app)

# ✅ With this:
CORS(app, resources={r"/predict": {"origins": "https://vivek-dixit-fake-news-detection.onrender.com"}})

API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"
HUGGINGFACE_API_TOKEN = os.environ.get("HUGGINGFACE_API_TOKEN")
headers = {"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"}

def query_huggingface(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code != 200:
        raise Exception(f"Huggingface API error: {response.status_code} - {response.text}")
    return response.json()

@app.route('/predict', methods=['POST'])
def predict():
    try:
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
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False)
