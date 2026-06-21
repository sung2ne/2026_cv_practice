"""색깔 빙고 게임 (1일차 프로젝트) — 실행 진입점

웹캠 앞에 9가지 색의 물건을 비춰 3x3 빙고판을 채우는 게임입니다.
한 줄(가로/세로/대각선)을 완성하면 '빙고!'.

실행:
    cd 03_color_bingo_game
    uv run main.py

조작:
    SPACE : 게임 시작 / 다시 시작
    R     : 빙고판 새로 섞기(리셋)
    ESC   : 종료
"""

import cv2
import numpy as np

from config import COLORS
from game import ColorBingoGame
import ui

CAM_W, CAM_H = 640, 480
PANEL_W = 360          # 오른쪽 빙고판 패널 너비
CELL = PANEL_W // 3    # 칸 한 변


def draw_panel(game, started):
    """오른쪽 3x3 빙고 패널을 그려 BGR 이미지로 반환."""
    panel = np.full((CAM_H, PANEL_W, 3), 30, dtype=np.uint8)
    text_items = []

    for idx, name in enumerate(game.board):
        r, c = divmod(idx, 3)
        x, y = c * CELL, r * CELL + 60
        bgr = COLORS[name]["bgr"]
        found = game.found[name]

        # 찾은 칸은 진하게, 못 찾은 칸은 흐리게
        fill = bgr if found else tuple(int(v * 0.30) for v in bgr)
        cv2.rectangle(panel, (x + 4, y + 4), (x + CELL - 4, y + CELL - 4), fill, -1)
        cv2.rectangle(panel, (x + 4, y + 4), (x + CELL - 4, y + CELL - 4), (200, 200, 200), 2)

        label_color = (255, 255, 255)
        text_items.append((name, (x + 18, y + CELL // 2 - 14), 22, label_color))
        if found:
            text_items.append(("O", (x + CELL // 2 - 12, y + 8), 26, (255, 255, 255)))

    # 상단 상태 표시 (점수 / 시간)
    text_items.append((f"점수 {game.score}", (12, 12), 24, (255, 255, 255)))
    text_items.append((f"시간 {game.time_left()}s", (PANEL_W - 150, 12), 24, (255, 255, 255)))

    panel = ui.put_texts(panel, text_items)
    return panel


def overlay_message(frame, text, sub=""):
    h, w = frame.shape[:2]
    box = frame.copy()
    cv2.rectangle(box, (0, h // 2 - 60), (w, h // 2 + 60), (0, 0, 0), -1)
    frame = cv2.addWeighted(box, 0.6, frame, 0.4, 0)
    items = [(text, (w // 2 - 130, h // 2 - 45), 40, (0, 255, 255))]
    if sub:
        items.append((sub, (w // 2 - 150, h // 2 + 20), 24, (255, 255, 255)))
    return ui.put_texts(frame, items)


def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[오류] 카메라를 열 수 없습니다. 01_env_check.py 로 연결을 확인하세요.")
        return
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAM_W)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAM_H)

    game = ColorBingoGame()
    started = False
    print("SPACE: 시작 / R: 리셋 / ESC: 종료")

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (CAM_W, CAM_H))

        if started and not game.won and game.time_left() > 0:
            game.detect_color(frame)

        panel = draw_panel(game, started)

        if not started:
            frame = overlay_message(frame, "색깔 빙고", "SPACE 를 눌러 시작")
        elif game.won:
            frame = overlay_message(frame, "빙고!", f"점수 {game.score} · R 로 다시")
        elif game.time_left() == 0:
            frame = overlay_message(frame, "시간 종료", f"점수 {game.score} · R 로 다시")

        combined = np.hstack([frame, panel])
        cv2.imshow("Color Bingo", combined)

        key = cv2.waitKey(1) & 0xFF
        if key == 27:        # ESC
            break
        elif key == 32:      # SPACE
            game.reset_game()
            started = True
        elif key in (ord("r"), ord("R")):
            game.reset_game()
            started = True

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
