import cv2
import os

# 얼굴 식별용 Haar Cascade 로드
face_detector = cv2.CascadeClassifier('../data/models/haarcascade_frontalface_default.xml')

# 사용자 정보 입력
user_id = input("\n[Enter User ID (Number)]: ")
print(f"\n[Info] Capturing 100 faces for ID {user_id}. Look at the camera!")

# 웹캠 초기화
cap = cv2.VideoCapture(0)
count = 0

if not os.path.exists('dataset'):
    os.makedirs('dataset')

while True:
    ret, frame = cap.read()
    if not ret: break
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        count += 1
        # 얼굴 부분만 저장 (dataset/User.ID.Count.jpg)
        cv2.imwrite(f"dataset/User.{user_id}.{count}.jpg", gray[y:y+h, x:x+w])
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cv2.putText(frame, f"Captured: {count}/100", (x, y-10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

    cv2.imshow('Collecting Face Data', frame)

    # 100장 촬영 완료 시 종료
    if cv2.waitKey(100) & 0xFF == 27 or count >= 100:
        break

print("\n[Success] 100 images captured! Proceed to trainer.py")
cap.release()
cv2.destroyAllWindows()
