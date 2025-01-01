import cv2
import numpy as np
from pathlib import Path

class ObjectDetector:
    def __init__(self):
        # Update paths to look in models directory
        models_dir = Path("models")
        
        # Load YOLO model
        self.net = cv2.dnn.readNet(
            str(models_dir / "yolov3.weights"),
            str(models_dir / "yolov3.cfg")
        )
        
        # Load COCO names
        with open(models_dir / "coco.names", "r") as f:
            self.classes = [line.strip() for line in f.readlines()]
        
        self.layer_names = self.net.getLayerNames()
        self.output_layers = [self.layer_names[i - 1] for i in self.net.getUnconnectedOutLayers()]
        self.colors = np.random.uniform(0, 255, size=(len(self.classes), 3))

    def detect_objects(self, image):
        height, width, _ = image.shape
        blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        
        self.net.setInput(blob)
        outs = self.net.forward(self.output_layers)

        # Showing information on the screen
        class_ids = []
        confidences = []
        boxes = []

        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    # Object detected
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    # Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        return boxes, class_ids, confidences

    def draw_annotations(self, image, boxes, class_ids, confidences):
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        annotated_image = image.copy()
        
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(self.classes[class_ids[i]])
                confidence = confidences[i]
                color = self.colors[class_ids[i]]

                cv2.rectangle(annotated_image, (x, y), (x + w, y + h), color, 2)
                cv2.putText(
                    annotated_image,
                    f"{label} {confidence:.2f}",
                    (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    color,
                    2
                )

        return annotated_image 