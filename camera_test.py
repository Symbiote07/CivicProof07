from ultralytics import YOLO
import cv2

# Load the model
model = YOLO("yolov8n.pt") 

# Open the Webcam (0 is usually the default camera)
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, frame = cap.read()
    if success:
        # Run YOLO on the frame
        results = model(frame)
        
        # Plot the results (draw boxes) on the frame
        annotated_frame = results[0].plot()
        
        # Show the video
        cv2.imshow("YOLOv8 Live Detection", annotated_frame)
        
        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()