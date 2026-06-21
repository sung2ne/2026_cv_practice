"""Haar Cascade 얼굴 검출 (2일차)

가장 빠르고 고전적인 얼굴 검출 방식. 웹캠에서 정면 얼굴을 실시간으로 찾습니다.

실행 (저장소 루트에서 00_asset_downloader.py 를 먼저 실행):
    cd 04_face_detection
    uv run 01_haar_detect.py

ESC : 종료
"""

import os

import cv2

CASCADE = "../data/models/haarcascade_frontalface_default.xml"


def main():
    if not os.path.exists(CASCADE):
        print(f"[오류] 모델이 없습니다: {CASCADE}")
        print("       저장소 루트에서 'uv run 00_asset_downloader.py' 를 먼저 실행하세요.")
        return

    detector = cv2.CascadeClassifier(CASCADE)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[오류] 카메라를 열 수 없습니다.")
        return

    print("ESC 로 종료")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5,
                                          minSize=(80, 80))

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, f"Faces: {len(faces)}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        cv2.imshow("Haar Face Detection", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
