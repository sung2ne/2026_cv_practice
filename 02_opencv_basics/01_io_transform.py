"""OpenCV 입출력 및 기본 변환 (1일차)

이미지를 읽고, 그레이스케일 변환 / 크기 조절 / 회전을 적용한 뒤 저장합니다.

실행 (저장소 루트에서 00_asset_downloader.py 를 먼저 실행해 두세요):
    cd 02_opencv_basics
    uv run 01_io_transform.py

학습 포인트:
    - cv2.imread / cv2.imwrite          : 이미지 읽기/쓰기
    - cv2.cvtColor(..., COLOR_BGR2GRAY) : 색공간 변환
    - cv2.resize                        : 크기 조절
    - cv2.getRotationMatrix2D + warpAffine : 회전
"""

import os

import cv2

# 저장소 루트의 data/ 폴더를 참조 (이 스크립트는 02_opencv_basics 안에서 실행)
IMG_PATH = "../data/images/sample.jpg"
OUT_DIR = "../output"


def main():
    if not os.path.exists(IMG_PATH):
        print(f"[오류] 이미지가 없습니다: {IMG_PATH}")
        print("       저장소 루트에서 'uv run 00_asset_downloader.py' 를 먼저 실행하세요.")
        return

    os.makedirs(OUT_DIR, exist_ok=True)

    # 1) 읽기
    img = cv2.imread(IMG_PATH)
    h, w = img.shape[:2]
    print(f"원본 크기: {w} x {h}")

    # 2) 그레이스케일 변환
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 3) 크기 조절 (가로 절반)
    resized = cv2.resize(img, (w // 2, h // 2))

    # 4) 회전 (중심 기준 45도)
    center = (w // 2, h // 2)
    matrix = cv2.getRotationMatrix2D(center, 45, 1.0)
    rotated = cv2.warpAffine(img, matrix, (w, h))

    # 5) 저장
    cv2.imwrite(f"{OUT_DIR}/gray.jpg", gray)
    cv2.imwrite(f"{OUT_DIR}/resized.jpg", resized)
    cv2.imwrite(f"{OUT_DIR}/rotated.jpg", rotated)
    print(f"결과 저장 완료: {OUT_DIR}/ (gray.jpg, resized.jpg, rotated.jpg)")

    # 6) 화면 표시 (창을 닫으려면 아무 키나 누르세요)
    try:
        cv2.imshow("Original", img)
        cv2.imshow("Gray", gray)
        cv2.imshow("Rotated 45", rotated)
        print("아무 키나 누르면 창이 닫힙니다.")
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    except cv2.error:
        print("[참고] 헤드리스 환경이라 화면 표시는 생략합니다. (output/ 결과를 확인하세요)")


if __name__ == "__main__":
    main()
