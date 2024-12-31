@echo off
echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing basic build requirements...
python -m pip install --upgrade pip
pip install setuptools wheel

echo Installing dependencies...
pip install -r requirements.txt

echo Downloading YOLO model files...
python src/download_models.py

echo Creating required directories...
mkdir resources\images 2>nul
mkdir resources\output 2>nul
mkdir test_reports 2>nul

echo Running tests...
python test/run_tests.py

echo.
echo Setup complete! Virtual environment is activated and dependencies are installed.
echo YOLO model files have been downloaded to the 'models' directory.
echo Place your input images in the 'resources/images' directory.
echo To deactivate the virtual environment, type 'deactivate'
echo.
pause
