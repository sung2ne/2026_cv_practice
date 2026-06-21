"""환경 점검 스크립트 (2026 CV 특강)

OpenCV 설치 상태, contrib 모듈(cv2.face) 유무, 웹캠 연결을 확인합니다.

    uv run 01_env_check.py

특히 cv2.face 가 False 로 나오면 잘못된 패키지(opencv-python)가 설치된 것입니다.
이 경우 README의 안내대로 opencv-contrib-python 으로 다시 설치하세요.
"""

import sys

import cv2
import numpy as np


def check_env():
    print("=== 환경 점검 ===")
    print(f"Python : {sys.version.split()[0]}")
    print(f"OpenCV : {cv2.__version__}")
    print(f"NumPy  : {np.__version__}")

    # contrib 모듈 확인 (얼굴 인식 LBPH, 68 랜드마크에 필수)
    has_face = hasattr(cv2, "face")
    print(f"cv2.face (contrib) : {'OK' if has_face else '없음 ← opencv-contrib-python 필요!'}")
    if not has_face:
        print("\n[조치] 아래 명령으로 올바른 패키지를 설치하세요:")
        print("    uv remove opencv-python")
        print("    uv add opencv-contrib-python")

    # 카메라 연결 확인
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        print("카메라 : 연결됨 (index 0)")
        cap.release()
    else:
        print("카메라 : 찾을 수 없음 (index 0) — 웹캠 연결/권한을 확인하세요")

    # 간단한 표시 창 테스트 (2초)
    test_img = np.zeros((200, 400, 3), dtype=np.uint8)
    cv2.putText(test_img, "2026 CV OK", (50, 110),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    try:
        cv2.imshow("Environment Test", test_img)
        cv2.waitKey(2000)
        cv2.destroyAllWindows()
    except cv2.error:
        print("[참고] 화면 표시(imshow)를 사용할 수 없는 환경입니다(원격/헤드리스).")

    print("\n[환경 점검 완료]")


if __name__ == "__main__":
    check_env()
