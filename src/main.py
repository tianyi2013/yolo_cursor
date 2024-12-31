from pathlib import Path
from object_detection import ObjectDetector
from pdf_generator import PDFGenerator
from utils import get_image_files, create_output_directory, save_image
import cv2
import logging

def process_images(input_dir, output_base_dir):
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    # Initialize object detector
    detector = ObjectDetector()
    
    # Get all image files
    image_files = get_image_files(input_dir)
    
    if not image_files:
        logger.warning(f"No images found in {input_dir}")
        return
    
    for image_file in image_files:
        try:
            logger.info(f"Processing {image_file.name}")
            
            # Create output directory
            output_dir = create_output_directory(output_base_dir, image_file.stem)
            
            # Read image
            image = cv2.imread(str(image_file))
            if image is None:
                logger.error(f"Failed to read image: {image_file}")
                continue
            
            # Detect objects
            boxes, class_ids, confidences = detector.detect_objects(image)
            
            # Draw annotations
            annotated_image = detector.draw_annotations(image, boxes, class_ids, confidences)
            
            # Save annotated image
            annotated_image_path = output_dir / f"{image_file.stem}_annotated{image_file.suffix}"
            success = save_image(annotated_image, annotated_image_path)
            if not success:
                logger.error(f"Failed to save annotated image to {annotated_image_path}")
                continue
            
            # Create PDF
            pdf_generator = PDFGenerator(output_dir)
            try:
                pdf_success = pdf_generator.create_pdf(
                    image_file,
                    annotated_image_path,
                    f"{image_file.stem}_report.pdf"
                )
                if pdf_success:
                    logger.info(f"Successfully processed {image_file.name}")
                else:
                    logger.error(f"Failed to create PDF for {image_file.name}")
            except Exception as e:
                logger.error(f"Failed to create PDF for {image_file.name}: {e}")
                
        except Exception as e:
            logger.error(f"Error processing {image_file.name}: {e}")

if __name__ == "__main__":
    input_directory = Path("resources/images")
    output_directory = Path("resources/output")
    
    # Ensure input directory exists
    if not input_directory.exists():
        print(f"Input directory {input_directory} does not exist!")
        exit(1)
    
    # Create output directory if it doesn't exist
    output_directory.mkdir(parents=True, exist_ok=True)
    
    process_images(input_directory, output_directory) 