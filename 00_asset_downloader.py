"""실습 에셋 다운로더 (2026 CV 특강)

실습에 필요한 샘플 이미지와 모델 파일을 data/ 폴더에 내려받습니다.
강의 시작 전 가장 먼저 한 번만 실행하세요.

    uv run 00_asset_downloader.py

결과:
    data/images/  - 샘플 이미지 (이미지 처리·HOG 사람 검출용)
    data/models/  - Haar Cascade, 68 랜드마크(LBF) 모델
"""

import os
import requests

# 실습 에셋 목록 ---------------------------------------------------------------
ASSETS = {
    "images": {
        # 색상/이미지 처리 실습용 (다채로운 색이 포함된 사진) — Pexels 무료 이미지
        "sample.jpg": "https://images.pexels.com/photos/60628/"
            "flower-garden-blue-sky-hokkaido-japan-60628.jpeg?auto=compress&cs=tinysrgb&w=800",
        # HOG 사람 검출 실습용 (사람이 여러 명 있는 사진) — Pexels 무료 이미지
        "people.jpg": "https://images.pexels.com/photos/2668720/"
            "pexels-photo-2668720.jpeg?auto=compress&cs=tinysrgb&w=1200",
        # 얼굴 검출/랜드마크 실습용 — Pexels 무료 이미지
        "face_test.jpg": "https://images.pexels.com/photos/3779760/"
            "pexels-photo-3779760.jpeg?auto=compress&cs=tinysrgb&w=800",
    },
    "models": {
        # Haar Cascade 정면 얼굴 검출기 (OpenCV 공식)
        "haarcascade_frontalface_default.xml":
            "https://raw.githubusercontent.com/opencv/opencv/master/"
            "data/haarcascades/haarcascade_frontalface_default.xml",
        # 68점 얼굴 랜드마크 모델 (OpenCV FacemarkLBF용, 약 54MB)
        "lbfmodel.yaml":
            "https://raw.githubusercontent.com/kurnianggoro/GSOC2017/master/"
            "data/lbfmodel.yaml",
    },
}


def download_file(url, filename):
    if os.path.exists(filename):
        print(f"  건너뜀: {filename} (이미 존재)")
        return True

    print(f"  내려받는 중: {filename} ...")
    try:
        response = requests.get(url, stream=True, timeout=60)
        response.raise_for_status()
        with open(filename, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"  완료: {filename}")
        return True
    except Exception as e:
        # 실패한 파일이 0바이트로 남지 않도록 정리
        if os.path.exists(filename):
            os.remove(filename)
        print(f"  [오류] {filename} 내려받기 실패: {e}")
        return False


def setup():
    for d in ["data/images", "data/models", "output"]:
        os.makedirs(d, exist_ok=True)

    ok = True
    print("[1/2] 이미지 내려받기")
    for name, url in ASSETS["images"].items():
        ok &= download_file(url, f"data/images/{name}")

    print("[2/2] 모델 내려받기")
    for name, url in ASSETS["models"].items():
        ok &= download_file(url, f"data/models/{name}")

    return ok


if __name__ == "__main__":
    print("=== 2026 CV 특강 에셋 다운로드 ===")
    success = setup()
    if success:
        print("\n--- 모든 에셋 준비 완료 ---")
    else:
        print("\n[주의] 일부 파일을 내려받지 못했습니다. 네트워크 확인 후 다시 실행하세요.")
