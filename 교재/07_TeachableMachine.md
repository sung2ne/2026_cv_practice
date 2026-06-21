# 07. Teachable Machine 연동 (2일차, 선택)

- 생성일시: 2026-06-21 17:18
- 수정일시: 2026-06-21 17:30

> 실습 폴더: `07_teachable_machine/` (`main.py`, `README.md`)

## 학습 목표

- 코드 없이 머신러닝 모델을 학습하는 경험을 한다.
- 학습한 모델을 OpenCV 웹캠과 연결한다.
- 직접 만든 분류기(예: 가위·바위·보)를 실시간으로 돌린다.

## Teachable Machine 이란

구글이 만든 노코드 머신러닝 도구입니다. 웹브라우저에서 웹캠으로 사진을 찍어
클래스(분류 항목)를 만들고 버튼 한 번으로 학습할 수 있습니다. 코딩 없이 "이 손모양은
가위, 저 손모양은 바위" 같은 분류기를 만들 수 있습니다.

주소: https://teachablemachine.withgoogle.com

## 전체 흐름

```mermaid
flowchart LR
    A[브라우저에서<br/>클래스별 사진 촬영] --> B[학습 Train]
    B -->|TensorFlow Lite 내보내기| C[model.tflite + labels.txt]
    C -->|tf.lite.Interpreter| D[OpenCV 웹캠 실시간 분류]
```

## 모델 만들고 내보내기

1. 이미지 프로젝트로 클래스를 2개 이상 만들고(예: 가위·바위·보) 각각 사진을 찍습니다.
2. 학습(Train) 버튼을 누릅니다.
3. Export → **TensorFlow Lite → Floating point** 로 내보냅니다.
4. 받은 파일을 `07_teachable_machine/` 폴더에 `model.tflite`, `labels.txt` 로 둡니다.

> 왜 TensorFlow Lite(.tflite)인가: Teachable Machine 이 주는 Keras(.h5) 모델은 최신
> 환경에서 불러오기가 자주 실패합니다. TFLite 형식은 버전 영향이 적어 안정적입니다.

## 설치와 실행

이 실습만 TensorFlow 가 필요합니다(용량이 커서 기본 설치에서 분리했습니다).

```bash
uv sync --extra teachable     # 저장소 루트에서, 이 실습 때만
cd 07_teachable_machine
uv run main.py
```

## 핵심 코드

```python
interpreter = tf.lite.Interpreter(model_path="model.tflite")
interpreter.allocate_tensors()
...
rgb = (cv2.resize(crop, (224, 224)) / 127.5) - 1.0   # 전처리
interpreter.set_tensor(inp["index"], rgb[np.newaxis, ...])
interpreter.invoke()
preds = interpreter.get_tensor(out["index"])[0]
label = labels[int(np.argmax(preds))]                # 가장 확률 높은 클래스
```

웹캠 화면 가운데를 224×224 로 잘라 모델에 넣고, 가장 확률이 높은 클래스의 이름과
확신도를 화면에 표시합니다.

## 직접 해보기

- 가위·바위·보 분류기를 만들어 실시간으로 맞는지 확인합니다.
- 배경이나 손 위치를 바꿔가며 어떤 경우에 분류가 틀리는지 봅니다. 학습 데이터를 더
  다양하게 찍으면 정확도가 어떻게 변하는지 실험합니다.
