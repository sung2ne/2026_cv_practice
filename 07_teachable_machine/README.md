# Teachable Machine + OpenCV (선택 실습)

노코드 머신러닝 도구인 **Teachable Machine** 으로 학습한 모델을 OpenCV 웹캠과 연동합니다.

## 1. 모델 만들기
1. https://teachablemachine.withgoogle.com → **이미지 프로젝트** 선택
2. 클래스를 2개 이상 만들고(예: `가위`, `바위`, `보`) 각 클래스마다 웹캠으로 샘플 촬영
3. **학습(Train Model)** 클릭

## 2. 모델 내보내기 (중요: TensorFlow Lite)
1. **Export Model** → **TensorFlow Lite** 탭
2. **Floating point** 선택 후 다운로드
3. 압축을 풀면 들어 있는 파일을 이 폴더에 아래 이름으로 둡니다.
   - `model_unquant.tflite` → **`model.tflite`** 로 이름 변경
   - `labels.txt` → 그대로

> Keras(.h5) 대신 TFLite를 쓰는 이유: 최신 Keras 3 환경에서 TM의 .h5 로딩이 자주 실패합니다. .tflite는 버전 영향이 적어 안정적입니다.

## 3. TensorFlow 설치 (이 실습에서만)
TensorFlow는 용량이 커서 기본 설치에서 제외했습니다. 이 실습을 할 때만 추가하세요.
```bash
# 저장소 루트에서
uv sync --extra teachable
```

## 4. 실행
```bash
cd 07_teachable_machine
uv run main.py
```
`ESC` 로 종료합니다.
