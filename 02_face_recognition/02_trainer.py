import cv2
import os
import numpy as np
from PIL import Image

# LBPH 인식기 생성
recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier("../data/models/haarcascade_frontalface_default.xml")

def get_images_and_labels(path):
    image_paths = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.jpg')]
    face_samples = []
    ids = []

    for image_path in image_paths:
        # 그레이스케일 변환
        PIL_img = Image.open(image_path).convert('L')
        img_numpy = np.array(PIL_img, 'uint8')
        
        # 파일명에서 ID 추출 (User.ID.Count.jpg)
        user_id = int(os.path.split(image_path)[-1].split(".")[1])
        
        faces = detector.detectMultiScale(img_numpy)
        for (x, y, w, h) in faces:
            face_samples.append(img_numpy[y:y+h, x:x+w])
            ids.append(user_id)

    return face_samples, ids

print("\n[Training] Training faces... please wait.")
faces, ids = get_images_and_labels('dataset')
recognizer.train(faces, np.array(ids))

# 모델 저장
if not os.path.exists('trainer'):
    os.makedirs('trainer')
recognizer.save('trainer/trainer.yml')

print(f"\n[Success] {len(np.unique(ids))} faces trained. Saved as 'trainer/trainer.yml'")
