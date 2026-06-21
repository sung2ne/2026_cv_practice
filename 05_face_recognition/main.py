"""실시간 얼굴 인식 (2일차) — LBPH 얼굴 인식 3단계

학습한 trainer/trainer.yml 로 웹캠 속 얼굴을 인식하고, names.json 의 이름을 표시합니다.
출입 통제 시스템의 기본 원리(등록된 사용자만 'Verified')를 보여줍니다.

실행:
    cd 05_face_recognition
    uv run main.py

ESC : 종료

참고: confidence 는 0에 가까울수록 정확. CONF_THRESHOLD 보다 작아야 '인증'으로 봅니다.
     너무 많이 통과하면 값을 낮추고(엄격), 본인도 Unknown 이면 값을 높이세요(완화).
"""

import json
import os

import cv2

CASCADE = "../data/models/haarcascade_frontalface_default.xml"
MODEL = "trainer/trainer.yml"
NAMES_FILE = "names.json"
CONF_THRESHOLD = 70   # LBPH 거리 임계값 (보통 50~80 사이에서 튜닝)


def load_names():
    if os.path.exists(NAMES_FILE):
        with open(NAMES_FILE, encoding="utf-8") as f:
            # JSON 키는 문자열이므로 int 로 변환
            return {int(k): v for k, v in json.load(f).items()}
    return {}


def main():
    if not os.path.exists(MODEL):
        print(f"[오류] '{MODEL}' 이 없습니다. 먼저 02_trainer.py 를 실행하세요.")
        return
    if not os.path.exists(CASCADE):
        print(f"[오류] 모델이 없습니다: {CASCADE} (00_asset_downloader.py 먼저 실행)")
        return

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(MODEL)
    face_cascade = cv2.CascadeClassifier(CASCADE)
    names = load_names()

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[오류] 카메라를 열 수 없습니다.")
        return
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    print("ESC 로 종료")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.2, 5, minSize=(100, 100))

        for (x, y, w, h) in faces:
            user_id, confidence = recognizer.predict(gray[y:y + h, x:x + w])
            if confidence < CONF_THRESHOLD:
                name = names.get(user_id, f"ID {user_id}")
                label = f"{name} ({round(100 - confidence)}%)"
                color = (0, 255, 0)   # 인증됨
            else:
                label = "Unknown"
                color = (0, 0, 255)   # 미인증

            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, label, (x + 5, y - 8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

        cv2.imshow("Face Recognition", frame)
        if cv2.waitKey(10) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
