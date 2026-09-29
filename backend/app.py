from flask import Flask, request, jsonify
from flask_cors import CORS
from ultralytics import YOLO
from PIL import Image
import base64
import io

app = Flask(__name__)
CORS(app)

model = YOLO("yolov8n.pt")

CATEGORY_MAP = {
    "bottle": "beverages",
    "cup": "beverages",
    "banana": "food",
    "apple": "food",
    "orange": "food",
    "sandwich": "food",
    "cake": "food",
    "toothbrush": "personal care",
    "cell phone": "electronics",
    "book": "general item",
}


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Assistive Visual Recognition backend is running",
        "model": "YOLOv8n",
    })


@app.route("/detect", methods=["POST"])
def detect_object():
    try:
        data = request.get_json()

        if not data or "image" not in data:
            return jsonify({"error": "No image received"}), 400

        image_base64 = data["image"]

        if "," in image_base64:
            image_base64 = image_base64.split(",", 1)[1]

        image_bytes = base64.b64decode(image_base64)
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        results = model(image, verbose=False)
        detections = []

        for result in results:
            for box in result.boxes:
                class_id = int(box.cls[0])
                confidence = float(box.conf[0])
                label = model.names[class_id]

                detections.append({
                    "label": label,
                    "confidence": confidence,
                })

        if not detections:
            return jsonify({
                "detected": False,
                "label": "No object detected",
                "category": "Unknown",
                "confidence": 0,
                "speech": "No object detected. Please try again.",
            })

        best_detection = max(detections, key=lambda item: item["confidence"])
        label = best_detection["label"]
        confidence = best_detection["confidence"]
        category = CATEGORY_MAP.get(label, "general object")

        speech_text = f"Detected item: {label}. Category: {category}."

        return jsonify({
            "detected": True,
            "label": label,
            "category": category,
            "confidence": round(confidence, 2),
            "speech": speech_text,
        })

    except Exception as error:
        return jsonify({"error": str(error)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
