import unittest
from pathlib import Path
import cv2
import numpy as np
import tempfile
from src.pdf_generator import PDFGenerator

class TestPDFGenerator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test resources"""
        # Create temporary directory for test outputs
        cls.test_dir = Path(tempfile.mkdtemp())
        cls.pdf_generator = PDFGenerator(cls.test_dir)
        
        # Create test images
        cls.test_image = np.zeros((100, 100, 3), dtype=np.uint8)
        cls.test_image_path = cls.test_dir / "test.jpg"
        cv2.imwrite(str(cls.test_image_path), cls.test_image)

    def test_convert_to_jpg(self):
        """Test image conversion to JPG"""
        jpg_path = self.pdf_generator.convert_to_jpg(self.test_image_path)
        self.assertIsNotNone(jpg_path)
        self.assertTrue(Path(jpg_path).exists())
        self.assertTrue(jpg_path.endswith('.jpg'))
        
        # Clean up
        Path(jpg_path).unlink()

    def test_create_pdf(self):
        """Test PDF creation"""
        output_filename = "test_output.pdf"
        result = self.pdf_generator.create_pdf(
            self.test_image_path,
            self.test_image_path,
            output_filename
        )
        
        self.assertTrue(result)
        pdf_path = self.test_dir / output_filename
        self.assertTrue(pdf_path.exists())
        
        # Clean up
        pdf_path.unlink()

    @classmethod
    def tearDownClass(cls):
        """Clean up test resources"""
        # Remove test image
        cls.test_image_path.unlink()
        # Remove test directory
        cls.test_dir.rmdir() 