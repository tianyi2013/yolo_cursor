import urllib.request
from pathlib import Path

def download_file(url, filename):
    print(f"Downloading {filename}...")
    urllib.request.urlretrieve(url, filename)
    print(f"Downloaded {filename}")

def download_yolo_files():
    # Create models directory if it doesn't exist
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)

    # URLs for YOLOv3 files
    files = {
        "yolov3.weights": "https://pjreddie.com/media/files/yolov3.weights",
        "yolov3.cfg": "https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/yolov3.cfg",
        "coco.names": "https://raw.githubusercontent.com/pjreddie/darknet/master/data/coco.names"
    }

    # Download each file
    for filename, url in files.items():
        output_path = models_dir / filename
        if not output_path.exists():
            try:
                download_file(url, str(output_path))
            except Exception as e:
                print(f"Error downloading {filename}: {e}")
                return False
    
    return True

if __name__ == "__main__":
    if download_yolo_files():
        print("All model files downloaded successfully!")
    else:
        print("Error downloading model files!") 