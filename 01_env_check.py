import cv2
import numpy as np
import sys

def check_env():
    print(f"Python Version: {sys.version}")
    print(f"OpenCV Version: {cv2.__version__}")
    print(f"NumPy Version: {np.__version__}")
    
    # 가상 캔버스 테스트
    test_img = np.zeros((200, 400, 3), dtype=np.uint8)
    cv2.putText(test_img, "2026 CV OK", (50, 110), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    # 카메라 인덱스 시도
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("\n[Warning] Camera not found (index 0)")
    else:
        print("\n[Success] Camera found!")
        cap.release()
    
    print("\n[Environment Check Pass!]")
    cv2.imshow("Environment Test", test_img)
    cv2.waitKey(2000) # 2초간 표시
    cv2.destroyAllWindows()

if __name__ == "__main__":
    check_env()
