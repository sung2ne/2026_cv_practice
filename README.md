# 2026 컴퓨터 비전 실무 특강 실습 코드

2026년 6월 24일~26일 진행되는 "OpenCV를 활용한 컴퓨터 비전 인식 기술" 특강 실습 저장소입니다.
(경남정보대학교 공학기술교육혁신센터)

모든 실습은 **`opencv-contrib-python` 하나로** 동작합니다. dlib처럼 빌드가 필요한 무거운 라이브러리는 쓰지 않습니다. (Teachable Machine 실습만 예외 — 아래 7번 참고)

---

## 1. 개발 환경 구축

빠른 패키지 관리자 [`uv`](https://docs.astral.sh/uv/)를 사용합니다.

### 1) 저장소 클론
```bash
git clone https://github.com/sung2ne/2026_cv_practice.git
cd 2026_cv_practice
```

### 2) 패키지 설치 (한 줄)
저장소에 `pyproject.toml` 과 `uv.lock` 이 포함되어 있어, 아래 한 줄이면 동일한 버전이 그대로 설치됩니다.
```bash
uv sync
```

> ⚠️ **중요**: 반드시 `opencv-contrib-python` 이어야 합니다. `opencv-python`(contrib 없는 버전)을 설치하면 얼굴 인식·랜드마크 실습에서 `cv2.face` 오류가 납니다. `uv sync` 를 쓰면 자동으로 올바른 버전이 설치됩니다.

### 3) 실습 에셋 다운로드 (필수, 한 번만)
샘플 이미지와 모델(Haar Cascade, 68 랜드마크)을 내려받습니다.
```bash
uv run 00_asset_downloader.py
```

### 4) 환경 점검
```bash
uv run 01_env_check.py
```
`cv2.face (contrib) : OK` 와 `카메라 : 연결됨` 이 보이면 준비 완료입니다.

---

## 2. 실습 목록

| 폴더 | 실습 | 핵심 기술 |
|------|------|-----------|
| `02_opencv_basics/` | 이미지 입출력·변환 / HSV 마스킹 | imread, cvtColor, resize, inRange |
| `03_color_bingo_game/` | **색깔 빙고 게임** (1일차 프로젝트) | HSV 색 검출, 실시간 게임 |
| `04_face_detection/` | Haar / HOG / 68 랜드마크 | 객체·얼굴 검출 3종 비교 |
| `05_face_recognition/` | **LBPH 얼굴 인식** (출입통제) | 수집→학습→인식 3단계 |
| `06_motion_security/` | 움직임 감지 보안 시스템 | 배경 차분(MOG2) |
| `07_teachable_machine/` | 노코드 ML 연동 (선택) | TensorFlow Lite |

### 실행 방법 (공통)
각 실습은 해당 폴더로 이동해 `uv run` 으로 실행합니다.
```bash
# 예: 빙고 게임
cd 03_color_bingo_game
uv run main.py
```
대부분의 실습은 웹캠 창에서 **`ESC`** 로 종료합니다.

---

## 3. 1일차 — OpenCV 기초 & 색상 인식

```bash
# 이미지 변환 기초 (그레이/리사이즈/회전)
cd 02_opencv_basics && uv run 01_io_transform.py

# HSV 색 마스킹 (1~5 키로 색 변경)
uv run 02_hsv_masking.py

# 색깔 빙고 게임 (SPACE 시작 / R 리셋 / ESC 종료)
cd ../03_color_bingo_game && uv run main.py
```

## 4. 2일차 — 객체 검출

```bash
cd 04_face_detection
uv run 01_haar_detect.py     # Haar 얼굴 검출
uv run 02_hog_people.py      # HOG 사람 검출 (webcam) / 'image' 인자로 사진 분석
uv run 03_landmarks_68.py    # 68점 얼굴 랜드마크
```

## 5. 2일차 — 얼굴 인식 (3단계)

```bash
cd 05_face_recognition
uv run 01_data_collection.py   # 1) 본인 얼굴 100장 수집 (ID·이름 입력)
uv run 02_trainer.py           # 2) 모델 학습 → trainer/trainer.yml
uv run main.py                 # 3) 실시간 인식
```

## 6. 2일차 — 움직임 감지 보안

```bash
cd 06_motion_security && uv run main.py   # SPACE: 배경 리셋 / ESC: 종료
```
침입 감지 시 `output/` 에 스냅샷과 `security_log.txt` 가 쌓입니다.

## 7. 2일차 — Teachable Machine 연동 (선택)

TensorFlow가 필요한 무거운 실습이라 기본 설치에서 분리했습니다.
```bash
uv sync --extra teachable
```
모델 준비·실행 방법은 [`07_teachable_machine/README.md`](07_teachable_machine/README.md) 참고.

## 8. 3일차 — 생성형 AI 협업 코딩 (워크숍)

별도 실습 코드는 없습니다. 본 저장소의 코드를 소재로 Gemini CLI 등 생성형 AI를 활용해
리팩토링·기능 추가·최적화를 함께 실습합니다.

---

## 문제 해결(FAQ)

- **`AttributeError: module 'cv2' has no attribute 'face'`**
  → `opencv-python` 이 설치된 것입니다. `uv remove opencv-python && uv add opencv-contrib-python` 후 다시 실행.
- **카메라가 안 열려요**
  → `uv run 01_env_check.py` 로 연결을 확인하세요. macOS는 터미널의 카메라 권한을 허용해야 합니다.
- **에셋(이미지/모델)을 못 찾는다는 오류**
  → 저장소 루트에서 `uv run 00_asset_downloader.py` 를 먼저 실행했는지 확인하세요.
- **한글이 □□□ 로 보여요 (빙고 게임)**
  → 한글 폰트가 없는 환경입니다. 코드가 자동으로 영문으로 대체해 표시합니다(기능에는 영향 없음).
