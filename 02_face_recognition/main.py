import cv2
import numpy as np
import os

# 1. 모델 및 인식기 로드
recognizer = cv2.face.LBPHFaceRecognizer_create()

if not os.path.exists('trainer/trainer.yml'):
    print("[Error] 'trainer/trainer.yml' not found. Run 02_trainer.py first.")
    exit()

recognizer.read('trainer/trainer.yml')
cascade_path = "../data/models/haarcascade_frontalface_default.xml"
face_cascade = cv2.CascadeClassifier(cascade_path)

# 2. 사용자 ID와 이름 매핑 (학습 시 입력한 ID와 동일해야 함)
# 예: {1: "Chul-su", 2: "Yeong-hee", 3: "Min-su"}
names = {1: 'Jeong PS', 2: 'Unknown', 3: 'Student A'}

# 3. 실시간 웹캠 인식 시작
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

print("\n--- Real-time Face Recognition Started ---")
print("Press 'ESC' to Exit")

while True:
    ret, frame = cap.read()
    if not ret: break
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(100, 100))

    for (x, y, w, h) in faces:
        # 얼굴 영역 예측 (user_id, confidence)
        user_id, confidence = recognizer.predict(gray[y:y+h, x:x+w])

        # Confidence 해석: 0에 가까울수록 정확함
        if confidence < 100:
            name = names.get(user_id, "Unknown")
            accuracy = f"  {round(100 - confidence)}%"
            color = (0, 255, 0) # Green (Verified)
        else:
            name = "Unknown"
            accuracy = "  0%"
            color = (0, 0, 255) # Red (Unverified)

        # 결과 시각화
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
        cv2.putText(frame, str(name), (x+5, y-5), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        cv2.putText(frame, str(accuracy), (x+5, y+h-5), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 1)

    cv2.imshow('Face Recognition Main', frame)

    if cv2.waitKey(10) & 0xFF == 27: # ESC
        break

print("\n--- Recognition Stopped ---")
cap.release()
cv2.destroyAllWindows()
