import cv2
import numpy as np
from calc_volume import calc_volume
from utils.timer import CustomTimer
from find_tumbler import find_tumbler


timer = CustomTimer()
video = cv2.VideoCapture(0)

if video.isOpened() == False:
    print("카메라 디바이스를 찾지 못했습니다!")
    exit()

cv2.namedWindow("Guide")
cv2.createTrackbar("size", "Guide", 0, 640, lambda x: x)
cv2.setTrackbarPos("size", "Guide", 150)

# 웹캠 루프
while True:
    # Original 웹캠 입력
    (ret, original_image) = video.read()

    # 마커 크기 계산
    marker_real_width = 8.6
    marker_real_hegiht = 5.6
    marker_ratio = (
        marker_real_hegiht / marker_real_width
    )  # 마커 가로/세로 비율 (민증: 5.6cm/8.6cm)
    # marker_ratio = 5398 / 8560  # 마커 가로/세로 비율 (카드(ID-1 규격): 5.398cm/8.560cm)
    marker_width = cv2.getTrackbarPos("size", "Guide")  # 마커 width (변경)
    marker_height = marker_width * marker_ratio  # 마커 height

    # 마커 위치 설정
    (height, width, _) = original_image.shape
    marker_p1 = (int(width / 2 - marker_width / 2), int(height / 2 - marker_height / 2))
    marker_p2 = (int(width / 2 + marker_width / 2), int(height / 2 + marker_height / 2))
    # marker_p1 = (0, int(height - marker_height))
    # marker_p2 = (marker_width, int(height))

    # guide_image: 사용자에게 보여줄 가이드(마커박스, 타이머 등)가 포함된 이미지
    guide_image = original_image.copy()
    cv2.rectangle(guide_image, marker_p1, marker_p2, (255, 0, 0), 2, cv2.LINE_AA)

    # 타이머 실행중이면 처리하고 숫자 Display
    if timer.is_capturing():
        tr = timer.process_timer()
        if not timer.done():
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(
                guide_image, str(tr), (50, 100), font, 4, (0, 255, 255), 4, cv2.LINE_AA,
            )

    # 가이드 이미지 출력
    cv2.imshow("Guide", guide_image)

    # (테스트) filled contours
    tumbler = find_tumbler(original_image)
    cv2.imshow("Result", tumbler)
    # tumbler_divided = tumbler.copy()
    # # (배경이 더 밝을 때 - 반전)
    # # 원본 이미지에 추출 영역 시각적으로 표현
    # tumbler_divided = cv2.divide(tumbler_divided, np.ones_like(tumbler_divided) * 255)
    # tumbler_divided = cv2.cvtColor(tumbler_divided, cv2.COLOR_GRAY2BGR)
    # cv2.imshow("Original - Result", cv2.multiply(original_image, tumbler))

    # 타이머 끝나면 캡쳐
    if timer.is_capturing() and timer.done():
        cv2.destroyAllWindows()
        # 캡쳐 후 출력/저장
        cv2.imshow("Original", original_image)
        cv2.imwrite("./outputs/original.png", original_image)
        # 가이드 캡쳐 후 출력/저장
        cv2.imshow("Guide", guide_image)
        cv2.imwrite("./outputs/guide.png", guide_image)
        # (테스트) filled contours 캡쳐 후 출력/저장
        cv2.imshow("Filled Contours", tumbler)
        cv2.imwrite("./outputs/filled_contours.png", tumbler)
        break

    # 키보드 입력
    k = cv2.waitKey(1)

    # Q를 누르면 카운트다운 시작
    if k == ord("q"):
        timer.start_timer(5)
    # T를 누르면 볼륨 계산
    elif k == ord("t"):
        print("volume", calc_volume(tumbler, marker_width / marker_real_width))

    # ESC를 누르면 캡쳐하지 않고 종료
    elif k == 27:
        break

video.release()

cv2.waitKey()
cv2.destroyAllWindows()
