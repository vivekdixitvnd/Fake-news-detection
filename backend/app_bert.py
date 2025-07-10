from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from smart_checker import is_text_suspicious

app = Flask(__name__)

# Enable CORS for specific origin
CORS(app, origins=["https://vivek-dixit-fake-news-detection.onrender.com"])

API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"
HUGGINGFACE_API_TOKEN = os.environ.get("HUGGINGFACE_API_TOKEN")

if not HUGGINGFACE_API_TOKEN:
    raise EnvironmentError("HUGGINGFACE_API_TOKEN not set in environment variables")

headers = {"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"}


def query_huggingface(payload):
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=15)
        if response.status_code != 200:
            raise Exception(f"Huggingface API error: {response.status_code} - {response.text}")

        result = response.json()

        if "labels" not in result or "scores" not in result:
            raise Exception(f"Invalid response format: {result}")

        return result

    except requests.exceptions.Timeout:
        raise Exception("Hugging Face API request timed out")

    except Exception as e:
        raise e


@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        text = data.get('text', '')

        if not text:
            raise ValueError("No text provided")

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

        return jsonify({'result': prediction.capitalize(), 'confidence': confidence}), 200

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=False)

