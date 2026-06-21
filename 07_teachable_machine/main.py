"""Teachable Machine + OpenCV 통합 (2일차, 선택 실습)

구글 Teachable Machine(teachablemachine.withgoogle.com)에서 학습한 이미지 모델을
'TensorFlow Lite (floating point)' 형식으로 내보내 웹캠 실시간 분류에 사용합니다.

준비:
    1) Teachable Machine 에서 이미지 프로젝트로 클래스(예: 가위/바위/보)를 학습
    2) Export → TensorFlow Lite → Floating point 다운로드
    3) 압축을 풀어 이 폴더에 model.tflite, labels.txt 로 둠
    4) (이 실습만) 무거운 TensorFlow 설치:  uv sync --extra teachable

실행:
    cd 07_teachable_machine
    uv run main.py

ESC : 종료

TFLite 경로를 쓰는 이유: TM이 내보내는 Keras .h5 는 최신 Keras 3 에서 로딩이
자주 깨집니다. .tflite 는 버전 영향이 적어 학생 환경에서 훨씬 안정적입니다.
"""

import os

import cv2
import numpy as np

MODEL = "model.tflite"
LABELS = "labels.txt"
SIZE = 224  # Teachable Machine 이미지 모델 입력 크기


def load_labels(path):
    with open(path, encoding="utf-8") as f:
        # 형식: "0 가위" → 앞 번호 제거
        return [line.strip().split(" ", 1)[-1] for line in f if line.strip()]


def main():
    if not (os.path.exists(MODEL) and os.path.exists(LABELS)):
        print(f"[안내] {MODEL} 과 {LABELS} 가 필요합니다.")
        print("       Teachable Machine 에서 'TensorFlow Lite > Floating point' 로 내보내")
        print("       model.tflite, labels.txt 를 이 폴더에 두세요. (README.md 참고)")
        return

    try:
        import tensorflow as tf
    except ImportError:
        print("[오류] tensorflow 가 없습니다. 이 실습만 추가 설치하세요:")
        print("       uv sync --extra teachable   (또는)  uv add tensorflow")
        return

    interpreter = tf.lite.Interpreter(model_path=MODEL)
    interpreter.allocate_tensors()
    inp = interpreter.get_input_details()[0]
    out = interpreter.get_output_details()[0]
    labels = load_labels(LABELS)

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

        # 전처리: 중앙 정사각형 → 224x224 → RGB → [-1,1] 정규화
        h, w = frame.shape[:2]
        s = min(h, w)
        crop = frame[(h - s) // 2:(h + s) // 2, (w - s) // 2:(w + s) // 2]
        img = cv2.resize(crop, (SIZE, SIZE))
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB).astype(np.float32)
        rgb = (rgb / 127.5) - 1.0
        interpreter.set_tensor(inp["index"], rgb[np.newaxis, ...])
        interpreter.invoke()
        preds = interpreter.get_tensor(out["index"])[0]

        idx = int(np.argmax(preds))
        label = labels[idx] if idx < len(labels) else str(idx)
        conf = float(preds[idx])
        text = f"{label}  {conf*100:.0f}%"
        cv2.putText(frame, text, (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)

        cv2.imshow("Teachable Machine", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
