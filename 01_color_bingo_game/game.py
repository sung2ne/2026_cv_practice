import cv2
import random
import time
from config import COLORS, GAME_TIME

class ColorBingoGame:
    def __init__(self):
        self.reset_game()

    def reset_game(self):
        self.bingo_board = random.sample(list(COLORS.keys()), 5) # 5개 색상 샘플링
        self.found_colors = {color: False for color in self.bingo_board}
        self.start_time = time.time()
        self.score = 0

    def detect_color(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        for color in self.bingo_board:
            if not self.found_colors[color]:
                for r in COLORS[color]['range']:
                    mask = cv2.inRange(hsv, r[0], r[1])
                    if cv2.countNonZero(mask) > 1000:
                        self.found_colors[color] = True
                        self.score += 10
                        return color
        return None
