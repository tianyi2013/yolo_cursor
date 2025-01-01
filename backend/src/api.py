from fastapi import FastAPI, File, UploadFile, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import shutil
from pathlib import Path
import tempfile
import cv2
import numpy as np
from object_detection import ObjectDetector
from pdf_generator import PDFGenerator
import uuid

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize object detector
detector = ObjectDetector()

# Create temp directory for processed files
TEMP_DIR = Path("temp")
TEMP_DIR.mkdir(exist_ok=True)

@app.post("/process-image/")
async def process_image(file: UploadFile = File(...)):
    # Create unique ID for this request
    request_id = str(uuid.uuid4())
    request_dir = TEMP_DIR / request_id
    request_dir.mkdir(exist_ok=True)

    try:
        # Save uploaded file
        input_path = request_dir / file.filename
        with input_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Read and process image
        image = cv2.imread(str(input_path))
        boxes, class_ids, confidences = detector.detect_objects(image)
        annotated_image = detector.draw_annotations(image, boxes, class_ids, confidences)

        # Save annotated image
        annotated_path = request_dir / f"annotated_{file.filename}"
        cv2.imwrite(str(annotated_path), annotated_image)

        # Generate PDF
        pdf_generator = PDFGenerator(request_dir)
        pdf_path = request_dir / f"{file.filename}_report.pdf"
        pdf_generator.create_pdf(input_path, annotated_path, pdf_path.name)

        return {
            "request_id": request_id,
            "filename": file.filename,
            "annotated_filename": f"annotated_{file.filename}",
            "pdf_filename": pdf_path.name
        }

    except Exception as e:
        return {"error": str(e)}

@app.get("/download/{request_id}/{filename}")
async def download_file(request_id: str, filename: str):
    file_path = TEMP_DIR / request_id / filename
    if not file_path.exists():
        return {"error": "File not found"}
    return FileResponse(file_path)

# Cleanup endpoint (optional)
@app.delete("/cleanup/{request_id}")
async def cleanup(request_id: str):
    request_dir = TEMP_DIR / request_id
    if request_dir.exists():
        shutil.rmtree(request_dir)
    return {"status": "cleaned"}

@app.post("/process-frame/")
async def process_frame(file: UploadFile = File(...)):
    """Process a single frame from video stream"""
    try:
        # Read image data
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            return {"error": "Invalid image data"}

        # Resize image for faster processing
        scale = 0.5
        small_image = cv2.resize(image, None, fx=scale, fy=scale)

        # Detect objects
        boxes, class_ids, confidences = detector.detect_objects(small_image)
        
        # Only draw annotations if objects were detected
        if len(boxes) > 0:
            # Scale boxes back to original size
            boxes = [box / scale for box in boxes]  # boxes are already numpy arrays
            annotated_image = detector.draw_annotations(image, boxes, class_ids, confidences)
        else:
            annotated_image = image
        
        # Convert back to bytes with reduced quality
        _, buffer = cv2.imencode('.jpg', annotated_image, [cv2.IMWRITE_JPEG_QUALITY, 75])
        image_bytes = buffer.tobytes()
        
        return Response(content=image_bytes, media_type="image/jpeg")

    except Exception as e:
        print(f"Error processing frame: {str(e)}")  # Add logging
        return {"error": str(e)} 