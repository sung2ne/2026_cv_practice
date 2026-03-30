# 2026년 컴퓨터 비전 실무 특강 실습 가이드

본 저장소는 2026년 6월 24일~26일 진행되는 "OpenCV를 활용한 컴퓨터 비전 인식 기술" 특강의 실습 자료입니다.

---

## 🛠️ 1단계: 개발 환경 구축

본 과정은 고성능 패키지 관리자인 `uv`를 사용합니다.

### 1. 저장소 클론
```bash
git clone https://github.com/sung2ne/2026_cv_practice.git
cd 2026_cv_practice
```

### 2. 프로젝트 초기화 및 필수 패키지 설치
```bash
# uv가 설치되어 있지 않다면 먼저 설치하세요 (https://astral.sh/uv)
uv init
uv add requests opencv-python numpy pillow
```

---

## 🚀 2단계: 실습 코드 실행 방법

모든 코드는 `uv run` 명령어를 통해 실행됩니다.

### 1. 실습 에셋 다운로드 (필수)
강의에 필요한 이미지와 얼굴 인식 모델을 다운로드합니다.
```bash
uv run 00_asset_downloader.py
```
*결과: `data/images/`, `data/models/` 폴더에 파일이 자동 저장됩니다.*

### 2. 환경 및 카메라 체크
OpenCV 설치 상태와 웹캠 연결을 확인합니다.
```bash
uv run 01_env_check.py
```

### 3. 색깔 빙고 게임 실행
실시간 색상 검출 기술을 활용한 빙고 게임입니다.
```bash
cd 01_color_bingo_game
uv run main.py
```
- `SPACE`: 게임 시작
- `R`: 빙고판 리셋
- `ESC`: 종료

### 4. 얼굴 인식 시스템 실습
얼굴 데이터를 수집하고 학습시켜 실시간으로 인식하는 실습입니다.
```bash
cd 02_face_recognition

# 1. 데이터 수집 (본인 얼굴 100장 촬영)
uv run 01_data_collection.py

# 2. 모델 학습 (데이터 학습 및 trainer.yml 생성)
uv run 02_trainer.py

# 3. 실시간 인식 실행
uv run main.py
```

---

## 💡 실습 팁
- **카메라 오류**: 웹캠이 인식되지 않을 경우 `01_env_check.py`를 실행하여 연결 상태를 먼저 확인하세요.
- **이미지 경로**: 모든 코드는 자동으로 생성되는 `data/` 폴더의 리소스를 참조합니다. 00번 스크립트를 반드시 먼저 실행해 주세요.

