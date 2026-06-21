"""움직임 감지 보안 시스템 (2일차) — 배경 차분(Background Subtraction)

MOG2 배경 차분기로 화면의 움직임을 감지합니다. 움직임이 일정 크기 이상이면
'침입 감지'로 보고 화면에 경고를 표시하고, 스냅샷과 로그를 output/ 에 남깁니다.

실행:
    cd 06_motion_security
    uv run main.py

조작:
    SPACE : 배경 다시 학습(리셋)
    ESC   : 종료

학습 포인트:
    - createBackgroundSubtractorMOG2 로 전경/배경 분리
    - 잡음 제거(morphology) 후 윤곽선(contour)으로 움직임 영역 찾기
    - 이벤트 로깅(보안 시스템의 기본 동작)
"""

import os
import time

import cv2

MIN_AREA = 1500          # 움직임으로 인정할 최소 면적(픽셀)
COOLDOWN = 3.0           # 연속 스냅샷 저장 방지(초)
OUT_DIR = "../output"


def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[오류] 카메라를 열 수 없습니다.")
        return

    os.makedirs(OUT_DIR, exist_ok=True)
    log_path = os.path.join(OUT_DIR, "security_log.txt")
    backsub = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=40,
                                                 detectShadows=True)
    last_alert = 0.0
    print("SPACE: 배경 리셋 / ESC: 종료")

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)

        mask = backsub.apply(frame)
        # 그림자(회색 127)는 제거하고 잡음 정리
        _, mask = cv2.threshold(mask, 200, 255, cv2.THRESH_BINARY)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, None, iterations=2)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        motion = False
        for c in contours:
            if cv2.contourArea(c) < MIN_AREA:
                continue
            motion = True
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

        if motion:
            cv2.putText(frame, "MOTION DETECTED", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
            now = time.time()
            if now - last_alert > COOLDOWN:
                last_alert = now
                stamp = time.strftime("%Y%m%d_%H%M%S")
                cv2.imwrite(f"{OUT_DIR}/intrusion_{stamp}.jpg", frame)
                with open(log_path, "a", encoding="utf-8") as f:
                    f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} 침입 감지\n")
                print(f"[경고] 침입 감지 — 스냅샷 저장 (intrusion_{stamp}.jpg)")
        else:
            cv2.putText(frame, "Monitoring...", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        cv2.imshow("Security Monitor", frame)
        cv2.imshow("Foreground Mask", mask)

        key = cv2.waitKey(1) & 0xFF
        if key == 27:
            break
        elif key == 32:  # SPACE: 배경 재학습
            backsub = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=40,
                                                         detectShadows=True)
            print("배경을 다시 학습합니다.")

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
