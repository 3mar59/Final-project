from ultralytics import YOLO

model = YOLO("yolov8n.pt")

model.train(
    data="training/product_classes.yaml",
    epochs=50,
    imgsz=640,
    batch=8,
    project="runs",
    name="product_model",
    hsv_h=0.015,
    hsv_s=0.7,
    hsv_v=0.4,
    degrees=5,
    translate=0.1,
    scale=0.4,
    fliplr=0.5,
    mosaic=1.0,
)
