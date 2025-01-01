from fpdf import FPDF
import cv2
from pathlib import Path
import logging
import tempfile

logger = logging.getLogger(__name__)

class PDFGenerator:
    def __init__(self, output_dir):
        self.output_dir = Path(output_dir)

    def convert_to_jpg(self, image_path):
        """Convert image to JPG format and save to a temporary file"""
        try:
            # Read the image
            img = cv2.imread(str(image_path))
            if img is None:
                return None
            
            # Create temporary file with .jpg extension
            temp = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
            temp_path = temp.name
            
            # Save as JPG
            cv2.imwrite(temp_path, img)
            return temp_path
        except Exception as e:
            logger.error(f"Error converting image to JPG: {e}")
            return None

    def add_image_page(self, pdf, image_path, title):
        """Add a page with an image and title to the PDF"""
        try:
            pdf.add_page()
            pdf.set_font('Arial', 'B', 16)
            pdf.cell(0, 10, title, 0, 1, 'C')
            pdf.image(image_path, x=10, y=30, w=190)
            return True
        except Exception as e:
            logger.error(f"Error adding {title} to PDF: {e}")
            return False

    def create_pdf(self, original_image_path, annotated_image_path, output_filename):
        temp_files = []  # Keep track of temporary files to clean up
        try:
            # Convert paths to Path objects and validate
            original_image_path = Path(original_image_path)
            annotated_image_path = Path(annotated_image_path)
            
            for path, desc in [(original_image_path, "Original"), (annotated_image_path, "Annotated")]:
                if not path.exists():
                    logger.error(f"{desc} image not found: {path}")
                    return False

            # Convert images to JPG format
            image_paths = []
            for path, desc in [(original_image_path, "original"), (annotated_image_path, "annotated")]:
                jpg_path = self.convert_to_jpg(path)
                if not jpg_path:
                    logger.error(f"Failed to convert {desc} image to JPG: {path}")
                    return False
                temp_files.append(jpg_path)
                image_paths.append(jpg_path)

            # Create PDF
            pdf = FPDF()
            
            # Add both images to PDF
            if not (self.add_image_page(pdf, image_paths[0], 'Original Image') and 
                   self.add_image_page(pdf, image_paths[1], 'Annotated Image')):
                return False

            # Save PDF
            try:
                output_path = self.output_dir / output_filename
                pdf.output(str(output_path))
                logger.info(f"Successfully created PDF: {output_path}")
                return True
            except Exception as e:
                logger.error(f"Error saving PDF: {e}")
                return False

        except Exception as e:
            logger.error(f"Error creating PDF: {e}")
            return False
        finally:
            # Clean up temporary files
            for temp_file in temp_files:
                try:
                    Path(temp_file).unlink()
                except Exception:
                    pass 