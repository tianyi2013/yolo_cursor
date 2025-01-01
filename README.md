# YOLO Object Detection Application

This application provides object detection using YOLO, with a FastAPI backend and React frontend.
This application is entirely built with Cursor (including this README file).

## Project Structure

```
project_root/
├── backend/                    # FastAPI backend
│   ├── src/
│   │   ├── api.py             # FastAPI endpoints
│   │   ├── object_detection.py # YOLO detection implementation
│   │   ├── pdf_generator.py    # PDF report generation
│   │   ├── utils.py           # Utility functions
│   │   ├── download_models.py  # YOLO model downloader
│   │   └── run_server.py      # Server startup
│   ├── test/                  # Unit tests
│   │   ├── test_utils.py      # Utils tests
│   │   ├── test_object_detection.py # Detection tests
│   │   ├── test_pdf_generator.py    # PDF tests
│   │   └── run_tests.py       # Test runner with coverage
│   ├── models/                # YOLO model files
│   ├── test_reports/         # Test results and coverage
│   ├── temp/                 # Temporary processing files
│   ├── requirements.txt      # Python dependencies
│   └── build_local.bat       # Setup script
└── frontend/                  # React frontend
    ├── src/
    │   ├── components/
    │   │   ├── ImageProcessor.js  # Image upload component
    │   │   ├── CameraView.js      # Camera feed component
    │   │   └── ImageViewer.js     # Image display component
    │   ├── services/
    │   │   └── api.js         # API client
    │   ├── App.js             # Main React component
    │   └── index.js           # React entry point
    ├── public/
    │   ├── index.html         # HTML template
    │   ├── manifest.json      # Web app manifest
    │   └── robots.txt         # Robots file
    └── package.json           # Node.js dependencies
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
