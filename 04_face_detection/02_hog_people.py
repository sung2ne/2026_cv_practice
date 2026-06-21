"""HOG 기반 사람(보행자) 검출 (2일차)

HOG(Histogram of Oriented Gradients) + SVM 으로 사람 전신을 검출합니다.
OpenCV에 내장된 보행자 검출기를 사용하므로 추가 설치가 필요 없습니다.

실행:
    cd 04_face_detection
    uv run 02_hog_people.py            # 웹캠
    uv run 02_hog_people.py image      # 샘플 이미지(../data/images/people.jpg)

ESC : 종료
"""

import os
import sys

import cv2

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())


def detect(frame):
    # 너무 크면 느리므로 가로 640 기준으로 축소
    h, w = frame.shape[:2]
    if w > 640:
        frame = cv2.resize(frame, (640, int(h * 640 / w)))
    rects, _ = hog.detectMultiScale(frame, winStride=(8, 8), padding=(8, 8), scale=1.05)
    for (x, y, w, h) in rects:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
    cv2.putText(frame, f"People: {len(rects)}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
    return frame


def run_image():
    path = "../data/images/people.jpg"
    if not os.path.exists(path):
        print(f"[오류] 이미지가 없습니다: {path} (00_asset_downloader.py 먼저 실행)")
        return
    out = detect(cv2.imread(path))
    cv2.imshow("HOG People (image)", out)
    print("아무 키나 누르면 종료")
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def run_webcam():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[오류] 카메라를 열 수 없습니다.")
        return
    print("ESC 로 종료")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow("HOG People (webcam)", detect(cv2.flip(frame, 1)))
        if cv2.waitKey(1) & 0xFF == 27:
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "image":
        run_image()
    else:
        run_webcam()
