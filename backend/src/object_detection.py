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

        # Apply Non-Maximum Suppression
        if boxes:
            indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
            filtered_boxes = []
            filtered_class_ids = []
            filtered_confidences = []
            for i in indices.flatten():
                x, y, w, h = boxes[i]
                filtered_boxes.append(np.array([x, y, x + w, y + h]))
                filtered_class_ids.append(class_ids[i])
                filtered_confidences.append(confidences[i])
            return filtered_boxes, filtered_class_ids, filtered_confidences

        return [], [], []

    def draw_annotations(self, image, boxes, class_ids, confidences):
        """Draw bounding boxes and labels on the image"""
        h, w = image.shape[:2]
        
        for box, class_id, confidence in zip(boxes, class_ids, confidences):
            x1, y1, x2, y2 = box.astype(int)
            
            # Draw bounding box
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # Prepare label text
            label = f"{self.classes[class_id]}: {confidence:.2f}"
            
            # Get text size and background size
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.6
            thickness = 2
            (text_width, text_height), baseline = cv2.getTextSize(label, font, font_scale, thickness)
            
            # Calculate text position (inside the box, near top)
            text_x = x1 + 5
            text_y = y1 + text_height + 10  # 10 pixels padding from top
            
            # Draw white background for text
            cv2.rectangle(image, 
                         (text_x - 2, text_y - text_height - 6),
                         (text_x + text_width + 2, text_y + 2),
                         (255, 255, 255), 
                         -1)  # Filled rectangle
            
            # Draw text
            cv2.putText(image, 
                        label,
                        (text_x, text_y),
                        font,
                        font_scale,
                        (0, 0, 0),  # Black text
                        thickness)
        
        return image 