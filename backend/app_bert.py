from flask import Flask, request, jsonify
import requests
import os
from smart_checker import is_text_suspicious
from flask_cors import CORS

app = Flask(__name__)

# ✅ Allow specific origin globally for all routes (safer and simpler)
CORS(app, origins=['https://vivek-dixit-fake-news-detection.onrender.com'])

API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"
HUGGINGFACE_API_TOKEN = os.environ.get("HUGGINGFACE_API_TOKEN")
headers = {"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"}

def query_huggingface(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code != 200:
        raise Exception(f"Huggingface API error: {response.status_code} - {response.text}")
    return response.json()

@app.route('/predict', methods=['POST', 'OPTIONS'])
def predict():
    if request.method == 'OPTIONS':
        # ✅ Preflight response
        response = jsonify({'status': 'OK'})
        response.headers.add('Access-Control-Allow-Origin', 'https://vivek-dixit-fake-news-detection.onrender.com')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'POST,OPTIONS')
        return response, 200

    try:
        data = request.get_json()
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

        response = jsonify({'result': prediction.capitalize(), 'confidence': confidence})
        response.headers.add('Access-Control-Allow-Origin', 'https://vivek-dixit-fake-news-detection.onrender.com')
        return response, 200

    except Exception as e:
        response = jsonify({'error': str(e)})
        response.headers.add('Access-Control-Allow-Origin', 'https://vivek-dixit-fake-news-detection.onrender.com')
        return response, 500

if __name__ == '__main__':
    app.run(debug=False)
