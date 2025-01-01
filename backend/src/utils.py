from pathlib import Path
import cv2
import logging

logger = logging.getLogger(__name__)

def is_valid_image(image_path):
    """Check if the image is valid and can be opened"""
    try:
        img = cv2.imread(str(image_path))
        return img is not None
    except Exception:
        return False

def get_image_files(directory):
    """Get all valid image files from the specified directory"""
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp'}
    directory = Path(directory)
    files = []
    for f in directory.glob('*'):
        if f.suffix.lower() in image_extensions and is_valid_image(f):
            files.append(f)
        else:
            logger.warning(f"Skipping invalid or unsupported image: {f}")
    logger.info(f"Found {len(files)} valid images in {directory}")
    return files

def create_output_directory(base_dir, image_name):
    """Create output directory for results"""
    output_dir = Path(base_dir) / image_name
    output_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Created output directory: {output_dir}")
    return output_dir

def save_image(image, output_path):
    """Save image to the specified path"""
    try:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        success = cv2.imwrite(str(output_path), image)
        if success:
            logger.info(f"Successfully saved image to {output_path}")
            return True
        else:
            logger.error(f"Failed to save image to {output_path}")
            return False
    except Exception as e:
        logger.error(f"Error saving image to {output_path}: {e}")
        return False 