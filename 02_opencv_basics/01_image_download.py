"""이미지 다운로드 (1일차) — 컴퓨터 비전의 첫걸음

웹에서 이미지를 내려받아 파일로 저장합니다. 실습에 쓸 사진은 저작권 걱정 없는
무료 이미지 사이트 Pexels(https://www.pexels.com)에서 가져옵니다.

내려받은 sample.jpg 는 저장소 공용 폴더(../data/images/)에 저장되며,
바로 다음 실습 02_io_transform.py 가 이 파일을 그대로 읽어 씁니다.

실행:
    cd 02_opencv_basics
    uv run 01_image_download.py

학습 포인트:
    - requests.get 으로 HTTP GET 요청을 보낸다
    - 상태 코드 200 이면 성공
    - 'wb'(바이너리 쓰기) 모드로 이미지 파일을 저장한다

참고: 한 번에 여러 이미지·모델을 받으려면 저장소 루트의 00_asset_downloader.py 를
     쓰면 됩니다. 이 파일은 '다운로드가 어떻게 동작하는지' 한 장으로 보는 학습용이고,
     받는 위치(../data/images/sample.jpg)는 00_asset_downloader.py 와 동일합니다.
"""

import os

import requests

# Pexels 무료 이미지 (저작권 표기 불필요, 상업적 이용 가능)
image_url = ("https://images.pexels.com/photos/60628/"
             "flower-garden-blue-sky-hokkaido-japan-60628.jpeg?auto=compress&cs=tinysrgb&w=640")
# 저장소 공용 폴더에 저장 (다음 실습들이 이 경로에서 읽음)
file_name = "../data/images/sample.jpg"

os.makedirs(os.path.dirname(file_name), exist_ok=True)

print(f"내려받는 중: {image_url}")
response = requests.get(image_url, timeout=30)

if response.status_code == 200:
    with open(file_name, "wb") as f:
        f.write(response.content)
    print(f"성공: {file_name} 으로 저장했습니다.")
else:
    print(f"실패: 상태 코드 {response.status_code}")
