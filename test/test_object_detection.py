import unittest
import cv2
import numpy as np
from src.object_detection import ObjectDetector

class TestObjectDetector(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test resources"""
        cls.detector = ObjectDetector()
        # Create a simple test image with a rectangle
        cls.test_image = np.zeros((416, 416, 3), dtype=np.uint8)
        cv2.rectangle(cls.test_image, (100, 100), (300, 300), (255, 255, 255), -1)

    def test_detect_objects(self):
        """Test object detection functionality"""
        boxes, class_ids, confidences = self.detector.detect_objects(self.test_image)
        
        # Basic validation of return types
        self.assertIsInstance(boxes, list)
        self.assertIsInstance(class_ids, list)
        self.assertIsInstance(confidences, list)

    def test_draw_annotations(self):
        """Test annotation drawing functionality"""
        # Sample test data
        boxes = [[100, 100, 200, 200]]
        class_ids = [0]  # Assuming first class in COCO
        confidences = [0.95]
        
        annotated_image = self.detector.draw_annotations(
            self.test_image, boxes, class_ids, confidences
        )
        
        # Verify the output is an image
        self.assertEqual(annotated_image.shape, self.test_image.shape)
        self.assertEqual(annotated_image.dtype, np.uint8) 