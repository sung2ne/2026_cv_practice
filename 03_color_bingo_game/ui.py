"""한글 텍스트 그리기 헬퍼

OpenCV의 putText 는 한글을 그리지 못하므로(□□□로 표시) PIL로 그립니다.
OS별 한글 폰트를 자동 탐색하고, 폰트를 못 찾으면 로마자로 대체해 깨지지 않게 합니다.
"""

import os

import numpy as np
from PIL import Image, ImageDraw, ImageFont

# 운영체제별 흔한 한글 폰트 경로 (위에서부터 시도)
_FONT_CANDIDATES = [
    "/System/Library/Fonts/AppleSDGothicNeo.ttc",          # macOS
    "/System/Library/Fonts/Supplemental/AppleGothic.ttf",  # macOS
    "C:/Windows/Fonts/malgun.ttf",                         # Windows
    "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",     # Linux (nanum)
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",  # Linux (noto)
]

# 폰트가 전혀 없을 때 한글 → 로마자 대체표
_ROMAN = {
    "빨강": "Red", "주황": "Orange", "노랑": "Yellow", "초록": "Green",
    "청록": "Cyan", "파랑": "Blue", "보라": "Purple", "분홍": "Pink", "검정": "Black",
    "빙고!": "BINGO!", "시간": "Time", "점수": "Score",
}

_HAS_FONT = any(os.path.exists(p) for p in _FONT_CANDIDATES)
_font_cache = {}


def _get_font(size):
    if size not in _font_cache:
        path = next((p for p in _FONT_CANDIDATES if os.path.exists(p)), None)
        _font_cache[size] = ImageFont.truetype(path, size) if path else ImageFont.load_default()
    return _font_cache[size]


def _display_text(text):
    return text if _HAS_FONT else _ROMAN.get(text, text)


def put_texts(img_bgr, items):
    """여러 텍스트를 한 번의 변환으로 그림. items: (text, (x,y), size, bgr_color) 리스트."""
    pil = Image.fromarray(img_bgr[:, :, ::-1])  # BGR → RGB
    draw = ImageDraw.Draw(pil)
    for text, pos, size, color in items:
        draw.text(pos, _display_text(text), font=_get_font(size), fill=color[::-1])
    return np.array(pil)[:, :, ::-1].copy()  # RGB → BGR


def put_text(img_bgr, text, pos, size=24, color=(255, 255, 255)):
    """img_bgr(numpy BGR) 위에 text 하나를 그려 새 이미지를 반환."""
    return put_texts(img_bgr, [(text, pos, size, color)])
