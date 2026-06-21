"""색깔 빙고 게임 로직 (1일차 프로젝트)

화면 표시는 main.py 가 담당하고, 이 파일은 순수 게임 규칙만 담습니다.
3x3 빙고판(9칸)을 9가지 색으로 채우고, 한 줄(가로/세로/대각선)을 완성하면 '빙고!'.
"""

import random
import time

import cv2
import numpy as np

from config import COLORS, GAME_TIME, DETECTION_THRESHOLD, COOLDOWN_TIME

# 3x3 빙고 라인 (가로 3, 세로 3, 대각선 2)
LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),   # 가로
    (0, 3, 6), (1, 4, 7), (2, 5, 8),   # 세로
    (0, 4, 8), (2, 4, 6),              # 대각선
]


class ColorBingoGame:
    def __init__(self):
        self.reset_game()

    def reset_game(self):
        # 9가지 색을 무작위로 섞어 3x3 판에 배치
        self.board = list(COLORS.keys())
        random.shuffle(self.board)
        self.found = {name: False for name in self.board}
        self.start_time = time.time()
        self.score = 0
        self.last_detect_time = 0.0
        self.last_color = None
        self.won = False

    def time_left(self):
        return max(0, int(GAME_TIME - (time.time() - self.start_time)))

    def _mask_count(self, hsv, name):
        mask = np.zeros(hsv.shape[:2], dtype=np.uint8)
        for low, high in COLORS[name]["range"]:
            mask |= cv2.inRange(hsv, np.array(low), np.array(high))
        return cv2.countNonZero(mask)

    def detect_color(self, frame):
        """프레임에서 가장 많이 보이는 '아직 못 찾은' 색을 새로 인식하면 그 이름을 반환."""
        if self.won or self.time_left() == 0:
            return None
        now = time.time()
        if now - self.last_detect_time < COOLDOWN_TIME:
            return None

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        best, best_count = None, DETECTION_THRESHOLD
        for name in self.board:
            if self.found[name]:
                continue
            count = self._mask_count(hsv, name)
            if count > best_count:
                best, best_count = name, count

        if best:
            self.found[best] = True
            self.score += 10
            self.last_detect_time = now
            self.last_color = best
            if self.check_bingo():
                self.won = True
            return best
        return None

    def check_bingo(self):
        flags = [self.found[self.board[i]] for i in range(9)]
        return any(flags[i] and flags[j] and flags[k] for i, j, k in LINES)

    def found_count(self):
        return sum(self.found.values())
