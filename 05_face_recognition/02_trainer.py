"""얼굴 모델 학습 (2일차) — LBPH 얼굴 인식 2단계

dataset/ 의 얼굴 이미지를 LBPH 알고리즘으로 학습하여 trainer/trainer.yml 을 만듭니다.

실행:
    cd 05_face_recognition
    uv run 02_trainer.py
"""

import os

import cv2
import numpy as np
from PIL import Image

DATASET = "dataset"


def get_images_and_labels(path):
    image_paths = [os.path.join(path, f) for f in os.listdir(path) if f.endswith(".jpg")]
    face_samples, ids = [], []
    for image_path in image_paths:
        gray = np.array(Image.open(image_path).convert("L"), "uint8")
        # 파일명 형식: User.<ID>.<count>.jpg
        user_id = int(os.path.split(image_path)[-1].split(".")[1])
        # 수집 단계에서 이미 얼굴만 잘라 저장했으므로 이미지 전체를 사용
        face_samples.append(gray)
        ids.append(user_id)
    return face_samples, ids


def main():
    if not os.path.isdir(DATASET) or not os.listdir(DATASET):
        print(f"[오류] '{DATASET}' 폴더가 비어 있습니다. 먼저 01_data_collection.py 를 실행하세요.")
        return

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    print("\n[학습 중] 얼굴을 학습합니다...")
    faces, ids = get_images_and_labels(DATASET)
    recognizer.train(faces, np.array(ids))

    os.makedirs("trainer", exist_ok=True)
    recognizer.save("trainer/trainer.yml")
    print(f"[완료] {len(np.unique(ids))}명 학습. trainer/trainer.yml 저장됨 → 다음: uv run main.py")


if __name__ == "__main__":
    main()
