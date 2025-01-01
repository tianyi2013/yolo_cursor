# YOLO Object Detection Application

This application provides object detection using YOLO, with a FastAPI backend and React frontend.
This application is entirely built with Cursor (including this README file).

## Project Structure

```
project_root/
├── backend/                    # FastAPI backend
│   ├── src/
│   │   ├── api.py             # FastAPI endpoints
│   │   ├── object_detection.py
│   │   ├── pdf_generator.py 
│   │   ├── utils.py
│   │   ├── download_models.py
│   │   └── run_server.py      # Server startup
│   ├── test/                  # Unit tests
│   ├── models/                # YOLO model files
│   ├── test_reports/          # Test results
│   ├── temp/                  # Temporary processing files
│   ├── requirements.txt
│   └── build_local.bat
└── frontend/                  # React frontend
    ├── src/
    │   ├── components/
    │   │   ├── ImageProcessor.js
    │   │   └── ImageViewer.js
    │   ├── services/
    │   │   └── api.js
    │   ├── App.js
    │   └── index.js
    ├── public/
    └── package.json
```

## Prerequisites

- Python 3.11 or higher
- Node.js 16 or higher
- npm (comes with Node.js)

## Backend Setup

1. Navigate to the backend directory: 
2. Run the build script:
   ```bash
   build_local.bat
   ```
   This script will:
   - Create a virtual environment
   - Install required dependencies
   - Download YOLO model files
   - Run initial setup checks
   - Start the FastAPI server automatically

   The API will be accessible at http://localhost:8000
   (Use Ctrl+C to stop the server)

3. Run the frontend:
   ```bash
   cd frontend
   npm start
   ```
   This script will start the React frontend, which will be accessible at http://localhost:3000.    

4. Run the tests (optional):
   ```bash
   cd backend
   
   python test/run_tests.py
   ```
   This script will run the unit tests for the backend. 
