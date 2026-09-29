from flask import Flask, request, jsonify
from flask_cors import CORS
from ultralytics import YOLO
from PIL import Image
import base64
import io

from config import CATEGORY_MAP, CONFIDENCE_THRESHOLD

app = Flask(__name__)
CORS(app)

model = YOLO("yolov8n.pt")


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

        results = model.predict(
            source=image,
            conf=CONFIDENCE_THRESHOLD,
            verbose=False,
        )

        detections = []

        for result in results:
            for box in result.boxes:
                class_id = int(box.cls[0])
                confidence = float(box.conf[0])
                label = model.names[class_id]
                category = CATEGORY_MAP.get(label, "general object")

                detections.append({
                    "label": label,
                    "category": category,
                    "confidence": round(confidence, 3),
                })

        detections.sort(key=lambda item: item["confidence"], reverse=True)

        if not detections:
            return jsonify({
                "detected": False,
                "detections": [],
                "speech": "No object detected. Please try again.",
            })

        best_detection = detections[0]
        speech_text = (
            f"Detected item: {best_detection['label']}. "
            f"Category: {best_detection['category']}."
        )

        return jsonify({
            "detected": True,
            "best_detection": best_detection,
            "detections": detections,
            "number_of_objects": len(detections),
            "speech": speech_text,
        })

    except Exception as error:
        return jsonify({"error": str(error)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
