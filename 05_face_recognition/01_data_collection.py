"""얼굴 데이터 수집 (2일차) — LBPH 얼굴 인식 1단계

웹캠으로 본인 얼굴 100장을 촬영해 dataset/ 폴더에 저장합니다.
ID와 이름을 입력하면 names.json 에 매핑이 기록되어, 나중에 인식 시 이름이 표시됩니다.

실행 (저장소 루트에서 00_asset_downloader.py 를 먼저 실행):
    cd 05_face_recognition
    uv run 01_data_collection.py

ESC : 중간에 종료
"""

import json
import os

import cv2

CASCADE = "../data/models/haarcascade_frontalface_default.xml"
NAMES_FILE = "names.json"
TARGET = 100


def main():
    if not os.path.exists(CASCADE):
        print(f"[오류] 모델이 없습니다: {CASCADE} (00_asset_downloader.py 먼저 실행)")
        return
    detector = cv2.CascadeClassifier(CASCADE)

    user_id = input("\n사용자 ID (숫자, 예: 1): ").strip()
    user_name = input("사용자 이름 (영문 권장, 예: Hong): ").strip()
    if not user_id.isdigit():
        print("[오류] ID는 숫자여야 합니다.")
        return

    # 이름 매핑 저장/갱신
    names = {}
    if os.path.exists(NAMES_FILE):
        with open(NAMES_FILE, encoding="utf-8") as f:
            names = json.load(f)
    names[user_id] = user_name
    with open(NAMES_FILE, "w", encoding="utf-8") as f:
        json.dump(names, f, ensure_ascii=False, indent=2)

    os.makedirs("dataset", exist_ok=True)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[오류] 카메라를 열 수 없습니다.")
        return

    print(f"\nID {user_id}({user_name})의 얼굴 {TARGET}장을 촬영합니다. 카메라를 봐 주세요!")
    count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.3, 5, minSize=(100, 100))

        for (x, y, w, h) in faces:
            count += 1
            cv2.imwrite(f"dataset/User.{user_id}.{count}.jpg", gray[y:y + h, x:x + w])
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(frame, f"{count}/{TARGET}", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

        cv2.imshow("Collecting Face Data", frame)
        if (cv2.waitKey(100) & 0xFF == 27) or count >= TARGET:
            break

    print(f"\n[완료] {count}장 촬영. 다음 단계: uv run 02_trainer.py")
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
