import unittest
from pathlib import Path
import cv2
import numpy as np
import tempfile
import shutil
from src.utils import get_image_files, create_output_directory, save_image, is_valid_image

class TestUtils(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test resources"""
        # Create temporary directory for test files
        cls.test_dir = Path(tempfile.mkdtemp())
        
        # Create test images
        cls.test_image = np.zeros((100, 100, 3), dtype=np.uint8)
        cls.valid_images = [
            cls.test_dir / f"test{i}.jpg" for i in range(3)
        ]
        for img_path in cls.valid_images:
            cv2.imwrite(str(img_path), cls.test_image)
        
        # Create invalid file
        cls.invalid_file = cls.test_dir / "invalid.txt"
        cls.invalid_file.touch()

    def test_get_image_files(self):
        """Test getting image files from directory"""
        image_files = get_image_files(self.test_dir)
        self.assertEqual(len(image_files), len(self.valid_images))
        for file in image_files:
            self.assertTrue(file.suffix.lower() in {'.jpg', '.jpeg', '.png', '.bmp'})

    def test_create_output_directory(self):
        """Test output directory creation"""
        output_base = self.test_dir / "output"
        test_name = "test_folder"
        
        output_dir = create_output_directory(output_base, test_name)
        self.assertTrue(output_dir.exists())
        self.assertTrue(output_dir.is_dir())
        
        # Clean up
        output_dir.rmdir()

    def test_save_image(self):
        """Test image saving functionality"""
        output_path = self.test_dir / "saved_image.jpg"
        result = save_image(self.test_image, output_path)
        
        self.assertTrue(result)
        self.assertTrue(output_path.exists())
        
        # Clean up
        output_path.unlink()

    def test_is_valid_image(self):
        """Test image validation"""
        # Test valid image
        self.assertTrue(is_valid_image(self.valid_images[0]))
        
        # Test invalid file
        self.assertFalse(is_valid_image(self.invalid_file))
        
        # Test non-existent file
        self.assertFalse(is_valid_image(self.test_dir / "nonexistent.jpg"))

    @classmethod
    def tearDownClass(cls):
        """Clean up test resources"""
        try:
            # Use shutil.rmtree to remove directory and all its contents
            shutil.rmtree(cls.test_dir, ignore_errors=True)
        except Exception as e:
            print(f"Warning: Failed to clean up test directory: {e}") 