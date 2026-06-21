"""HSV 색공간과 색상 마스킹 (1일차)

웹캠 영상에서 특정 색(기본: 파랑)만 추출해 보여줍니다.
빙고 게임(03번 실습)의 핵심 원리인 inRange + bitwise_and 를 먼저 체험합니다.

실행:
    cd 02_opencv_basics
    uv run 02_hsv_masking.py

조작:
    1~5 : 추출할 색 바꾸기 (빨강/노랑/초록/파랑/보라)
    ESC  : 종료

학습 포인트:
    - BGR → HSV 변환이 색 검출에 유리한 이유
    - cv2.inRange 로 색 범위 마스크 생성
    - cv2.bitwise_and 로 마스크 영역만 남기기
"""

import cv2
import numpy as np

# (이름, [하한, 상한] 리스트) — 빨강은 H가 양 끝으로 나뉘어 범위가 2개
COLOR_RANGES = {
    "1 Red":    [((0, 80, 80), (10, 255, 255)), ((170, 80, 80), (180, 255, 255))],
    "2 Yellow": [((20, 80, 80), (35, 255, 255))],
    "3 Green":  [((40, 80, 80), (85, 255, 255))],
    "4 Blue":   [((95, 80, 80), (130, 255, 255))],
    "5 Purple": [((130, 60, 60), (160, 255, 255))],
}
KEYS = list(COLOR_RANGES.keys())


def build_mask(hsv, ranges):
    mask = np.zeros(hsv.shape[:2], dtype=np.uint8)
    for low, high in ranges:
        mask |= cv2.inRange(hsv, np.array(low), np.array(high))
    return mask


def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[오류] 카메라를 열 수 없습니다. 01_env_check.py 로 연결을 확인하세요.")
        return

    selected = "4 Blue"
    print("1~5 키로 색 변경, ESC 종료")

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)  # 거울 모드

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = build_mask(hsv, COLOR_RANGES[selected])
        result = cv2.bitwise_and(frame, frame, mask=mask)

        cv2.putText(result, f"Color: {selected}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv2.imshow("Original", frame)
        cv2.imshow("Masked", result)

        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # ESC
            break
        if ord("1") <= key <= ord("5"):
            selected = KEYS[key - ord("1")]

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
