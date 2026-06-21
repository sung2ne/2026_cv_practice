"""이미지 다운로드 (1일차) — 컴퓨터 비전의 첫걸음

웹에서 이미지를 내려받아 파일로 저장합니다. 실습에 쓸 사진은 저작권 걱정 없는
무료 이미지 사이트 Unsplash(https://unsplash.com)에서 가져옵니다.

실행:
    cd 02_opencv_basics
    uv run 01_image_download.py

학습 포인트:
    - requests.get 으로 HTTP GET 요청을 보낸다
    - 상태 코드 200 이면 성공
    - 'wb'(바이너리 쓰기) 모드로 이미지 파일을 저장한다

참고: 한 번에 여러 이미지·모델을 받으려면 저장소 루트의 00_asset_downloader.py 를
     쓰면 됩니다. 이 파일은 '다운로드가 어떻게 동작하는지' 직접 보기 위한 학습용입니다.
"""

import requests

# Unsplash 무료 이미지 (저작권 표기 불필요, 상업적 이용 가능)
image_url = "https://images.unsplash.com/photo-1542037104857-ffbb0b9155fb?w=640"
file_name = "sample.jpg"

print(f"내려받는 중: {image_url}")
response = requests.get(image_url, timeout=30)

if response.status_code == 200:
    with open(file_name, "wb") as f:
        f.write(response.content)
    print(f"성공: {file_name} 으로 저장했습니다.")
else:
    print(f"실패: 상태 코드 {response.status_code}")
