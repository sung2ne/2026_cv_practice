# 01. OpenCV 기초 — 이미지 입출력과 변환

- 생성일시: 2026-06-21 17:18
- 수정일시: 2026-06-21 17:18

> 실습 파일: `02_opencv_basics/01_io_transform.py`

## 학습 목표

- 이미지를 읽고 저장하는 법을 익힌다.
- 그레이스케일 변환, 크기 조절, 회전을 적용해 본다.
- OpenCV 가 이미지를 숫자 배열(NumPy)로 다룬다는 것을 이해한다.

## 이미지는 숫자다

OpenCV 에서 이미지는 가로×세로×3(파랑·초록·빨강) 크기의 숫자 배열입니다.
각 픽셀은 0~255 사이의 밝기 값으로 표현됩니다. 그래서 이미지를 자르고, 크기를
바꾸고, 회전하는 일이 모두 "배열을 다루는 일" 이 됩니다.

한 가지 기억할 점은 OpenCV 가 색 순서를 **BGR(파랑·초록·빨강)** 로 쓴다는 것입니다.
우리가 흔히 말하는 RGB 와 순서가 반대입니다.

## 핵심 코드

```python
import cv2

img = cv2.imread("../data/images/sample.jpg")   # 읽기
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)     # 그레이스케일 변환
resized = cv2.resize(img, (w // 2, h // 2))      # 절반 크기로

center = (w // 2, h // 2)
matrix = cv2.getRotationMatrix2D(center, 45, 1.0)  # 중심 기준 45도
rotated = cv2.warpAffine(img, matrix, (w, h))

cv2.imwrite("../output/gray.jpg", gray)          # 저장
```

핵심 함수는 네 가지입니다.

- `cv2.imread` / `cv2.imwrite` 로 읽고 씁니다.
- `cv2.cvtColor` 로 색공간을 바꿉니다(여기서는 컬러를 흑백으로).
- `cv2.resize` 로 크기를 조절합니다.
- `cv2.getRotationMatrix2D` 와 `cv2.warpAffine` 으로 회전합니다.

## 실행

```bash
cd 02_opencv_basics
uv run 01_io_transform.py
```

원본·흑백·회전 결과 창이 뜨고, `output/` 폴더에 변환된 이미지가 저장됩니다.
창을 닫으려면 아무 키나 누릅니다.

## 직접 해보기

- 회전 각도 `45` 를 `90` 이나 `30` 으로 바꿔 결과를 비교합니다.
- `cv2.resize` 의 크기를 `(w*2, h*2)` 로 바꾸면 어떻게 되는지 확인합니다.
- `data/images/` 의 다른 이미지(`people.jpg`)로 경로를 바꿔 실행해 봅니다.
