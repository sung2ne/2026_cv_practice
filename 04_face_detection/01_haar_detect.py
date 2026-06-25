"""Haar Cascade 얼굴 검출 (2일차)

가장 빠르고 고전적인 얼굴 검출 방식. 정면 얼굴을 찾아 사각형으로 표시합니다.

실행 (저장소 루트에서 00_asset_downloader.py 를 먼저 실행):
    cd 04_face_detection
    uv run 01_haar_detect.py            # 웹캠
    uv run 01_haar_detect.py image      # 샘플 이미지(../data/images/face_test.jpg)

웹캠은 ESC 로, 이미지 창은 아무 키나 눌러 종료합니다.
"""

import os
import sys

import cv2

CASCADE = "../data/models/haarcascade_frontalface_default.xml"
IMAGE = "../data/images/face_test.jpg"


def detect(frame, detector):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5,
                                      minSize=(80, 80))
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.putText(frame, f"Faces: {len(faces)}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    return frame


def run_image(detector):
    if not os.path.exists(IMAGE):
        print(f"[오류] 이미지가 없습니다: {IMAGE} (00_asset_downloader.py 먼저 실행)")
        return
    out = detect(cv2.imread(IMAGE), detector)
    cv2.imshow("Haar Face Detection (image)", out)
    print("아무 키나 누르면 종료")
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def run_webcam(detector):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[오류] 카메라를 열 수 없습니다. (카메라 없이 보려면 'image' 인자로 실행)")
        return
    print("ESC 로 종료")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow("Haar Face Detection", detect(cv2.flip(frame, 1), detector))
        if cv2.waitKey(1) & 0xFF == 27:
            break
    cap.release()
    cv2.destroyAllWindows()


def main():
    if not os.path.exists(CASCADE):
        print(f"[오류] 모델이 없습니다: {CASCADE}")
        print("       저장소 루트에서 'uv run 00_asset_downloader.py' 를 먼저 실행하세요.")
        return

    detector = cv2.CascadeClassifier(CASCADE)
    if len(sys.argv) > 1 and sys.argv[1] == "image":
        run_image(detector)
    else:
        run_webcam(detector)


if __name__ == "__main__":
    main()
