import os
import requests

# 2026 CV 특강 실습 에셋
ASSETS = {
    "images": {
        "sample.jpg": "https://images.unsplash.com/photo-1542037104857-ffbb0b9155fb?w=800",
        "people.jpg": "https://images.unsplash.com/photo-1517841905240-472988babdf9?w=1200",
        "face_test.jpg": "https://images.unsplash.com/photo-1554151228-14d9def656e4?w=800"
    },
    "models": {
        "haarcascade_frontalface_default.xml": "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml"
    }
}

def download_file(url, filename):
    if os.path.exists(filename):
        print(f"Skipping {filename} (already exists)")
        return
    
    print(f"Downloading {filename}...")
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Successfully downloaded {filename}")
    except Exception as e:
        print(f"Error downloading {filename}: {e}")

def setup():
    # 데이터 저장 폴더 생성
    dirs = ["data/images", "data/models", "output"]
    for d in dirs:
        os.makedirs(d, exist_ok=True)
    
    # 이미지 다운로드
    for name, url in ASSETS["images"].items():
        download_file(url, f"data/images/{name}")
    
    # 모델 다운로드
    for name, url in ASSETS["models"].items():
        download_file(url, f"data/models/{name}")

if __name__ == "__main__":
    setup()
    print("\n--- 2026 CV Asset Setup Complete ---")
