import cv2
import numpy as np
from ultralytics import YOLO

# Load model once
model = YOLO("yolov8n.pt") 

def analyze_streetlight(image_path):
    print(f"🔍 Analyzing {image_path}...")
    
    img = cv2.imread(image_path)
    if img is None:
        return {"success": False, "reason": "Image not found."}

    # 1. Object Detection (Context)
    results = model(img, verbose=False)
    valid_classes = [0, 1, 2, 3, 5, 7, 9, 11, 13] 
    objects_detected = []
    
    for r in results:
        for box in r.boxes:
            cls_id = int(box.cls[0])
            if cls_id in valid_classes:
                objects_detected.append(model.names[cls_id])

    # 2. THE BLOB SIZE CHECK (Distinguish Sky vs Bulb)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Step A: Find "Pure White" areas (Value > 250)
    # This creates a black-and-white mask where white = bright spots
    _, bright_mask = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY)
    
    # Step B: Calculate what % of the image is "Pure White"
    total_pixels = gray.size
    bright_pixels = np.count_nonzero(bright_mask)
    bright_percentage = (bright_pixels / total_pixels) * 100
    
    print(f"💡 Brightness Analysis: {bright_percentage:.2f}% of image is pure white.")

    # LOGIC UPDATE:
    # 1. If > 30% of the image is pure white -> It's likely the SKY (Daytime). REJECT.
    # 2. If < 0.1% of the image is pure white -> It's pitch black. REJECT.
    # 3. If between 0.1% and 30% -> It's a concentrated light source. VERIFY.
    
    is_valid_light = 0.1 < bright_percentage < 30.0

    if is_valid_light:
        return {
            "success": True, 
            "status": f"Verified: Concentrated Light Source ({bright_percentage:.1f}% size) 💡", 
            "confidence": 0.95, 
            "tags": list(set(objects_detected))
        }
    elif bright_percentage >= 30.0:
        return {
            "success": False, 
            "status": f"Rejected: Area too bright ({bright_percentage:.1f}%). Likely daytime sky. ☀️",
            "confidence": 0.0,
            "tags": list(set(objects_detected))
        }
    else:
        return {
            "success": False, 
            "status": "Rejected: Too dark. No light source found. 🌑",
            "confidence": 0.0,
            "tags": list(set(objects_detected))
        }