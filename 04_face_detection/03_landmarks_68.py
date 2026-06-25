"""68점 얼굴 랜드마크 (2일차)

얼굴을 검출(Haar)한 뒤, OpenCV FacemarkLBF 모델로 68개의 특징점
(눈/눈썹/코/입/턱선)을 찾아 표시합니다.

dlib 없이 opencv-contrib-python 만으로 동작합니다.

실행 (저장소 루트에서 00_asset_downloader.py 를 먼저 실행 — lbfmodel.yaml 필요):
    cd 04_face_detection
    uv run 03_landmarks_68.py            # 웹캠
    uv run 03_landmarks_68.py image      # 샘플 이미지(../data/images/face_test.jpg)

웹캠은 ESC 로, 이미지 창은 아무 키나 눌러 종료합니다.
"""

import os
import sys

import cv2
import numpy as np

CASCADE = "../data/models/haarcascade_frontalface_default.xml"
LBF_MODEL = "../data/models/lbfmodel.yaml"
IMAGE = "../data/images/face_test.jpg"


def detect(frame, detector, facemark):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(gray, 1.2, 5, minSize=(100, 100))

    if len(faces) > 0:
        ok, landmarks = facemark.fit(gray, np.array(faces))
        if ok:
            for marks in landmarks:
                for (px, py) in marks[0]:
                    cv2.circle(frame, (int(px), int(py)), 2, (0, 255, 0), -1)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 1)

    cv2.putText(frame, "68 Landmarks", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    return frame


def run_image(detector, facemark):
    if not os.path.exists(IMAGE):
        print(f"[오류] 이미지가 없습니다: {IMAGE} (00_asset_downloader.py 먼저 실행)")
        return
    out = detect(cv2.imread(IMAGE), detector, facemark)
    cv2.imshow("68 Face Landmarks (image)", out)
    print("아무 키나 누르면 종료")
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def run_webcam(detector, facemark):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[오류] 카메라를 열 수 없습니다. (카메라 없이 보려면 'image' 인자로 실행)")
        return
    print("ESC 로 종료")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow("68 Face Landmarks", detect(cv2.flip(frame, 1), detector, facemark))
        if cv2.waitKey(1) & 0xFF == 27:
            break
    cap.release()
    cv2.destroyAllWindows()


def main():
    for path in (CASCADE, LBF_MODEL):
        if not os.path.exists(path):
            print(f"[오류] 파일이 없습니다: {path}")
            print("       저장소 루트에서 'uv run 00_asset_downloader.py' 를 먼저 실행하세요.")
            return

    detector = cv2.CascadeClassifier(CASCADE)
    facemark = cv2.face.createFacemarkLBF()
    facemark.loadModel(LBF_MODEL)

    if len(sys.argv) > 1 and sys.argv[1] == "image":
        run_image(detector, facemark)
    else:
        run_webcam(detector, facemark)


if __name__ == "__main__":
    main()
