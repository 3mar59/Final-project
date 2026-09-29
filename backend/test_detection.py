from ultralytics import YOLO
import csv
import os

from config import CONFIDENCE_THRESHOLD

model = YOLO("yolov8n.pt")

TEST_FOLDER = "test_images"
OUTPUT_FILE = "test_results.csv"
SUPPORTED_FORMATS = (".jpg", ".jpeg", ".png")

results_list = []

if not os.path.isdir(TEST_FOLDER):
    os.makedirs(TEST_FOLDER)

for filename in os.listdir(TEST_FOLDER):
    if not filename.lower().endswith(SUPPORTED_FORMATS):
        continue

    path = os.path.join(TEST_FOLDER, filename)
    results = model.predict(
        source=path,
        conf=CONFIDENCE_THRESHOLD,
        verbose=False,
    )

    detections = []

    for result in results:
        for box in result.boxes:
            class_id = int(box.cls[0])
            confidence = float(box.conf[0])
            label = model.names[class_id]
            detections.append((label, confidence))

    if detections:
        label, confidence = max(detections, key=lambda item: item[1])
    else:
        label = "No detection"
        confidence = 0

    results_list.append({
        "image": filename,
        "prediction": label,
        "confidence": round(confidence, 3),
    })

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=["image", "prediction", "confidence"],
    )
    writer.writeheader()
    writer.writerows(results_list)

print(f"Tested {len(results_list)} image(s). Results saved to {OUTPUT_FILE}.")
