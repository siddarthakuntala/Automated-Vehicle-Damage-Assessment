from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch
import os

# Initialize app
app = Flask(__name__)
CORS(app)

# Load fine-tuned CLIP model
model_dir = os.path.join(os.path.dirname(__file__), "model")
model = CLIPModel.from_pretrained(model_dir)
processor = CLIPProcessor.from_pretrained(model_dir)

# Predefined descriptions and costs
descriptions = [
    "Minor scratch on front bumper. Estimated cost: ₹1500",
    "Major dent on rear door and broken tail light. Estimated cost: ₹12000",
    "Shattered windshield and bent hood. Estimated cost: ₹18000",
    "Flat rear tire and minor rear panel dent. Estimated cost: ₹2500",
    "No visible damage. Estimated cost: ₹0"
]

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    # Load image from request
    file = request.files['image']
    image = Image.open(file.stream).convert("RGB")

    # Preprocess and predict
    inputs = processor(text=descriptions, images=image, return_tensors="pt", padding=True)
    outputs = model(**inputs)
    probs = outputs.logits_per_image.softmax(dim=1)
    pred_idx = torch.argmax(probs, dim=1).item()

    return jsonify({
        'description': descriptions[pred_idx]
        # 'confidence': float(probs[0][pred_idx])  # Removed as per request
    })

if __name__ == '__main__':
    app.run(debug=True)
