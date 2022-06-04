import cv2
from calc_volume import calc_volume
from find_tumbler import find_tumbler

if __name__ == "__main__":
    # # 타이머
    # timer = CustomTimer()

    # # 웹캠 이미지 해상도 (16:9)
    # VIDEO_WIDTH = 1280
    # VIDEO_HEIGHT = 720
    # # 웹캠 디바이스
    # video = cv2.VideoCapture(0)
    # video.set(cv2.CAP_PROP_FRAME_WIDTH, VIDEO_WIDTH)
    # video.set(cv2.CAP_PROP_FRAME_HEIGHT, VIDEO_HEIGHT)

    # if video.isOpened() == False:
    #     print("카메라 디바이스를 찾지 못했습니다!")
    #     exit()

    # (ret, original_image) = video.read()
    # original_image = cv2.imread("./outputs/keep-1/original.png")
    # original_image = cv2.imread("./coke-canny/original.png")
    original_image = cv2.imread("./inputs/1.jpg")
    original_image = cv2.resize(original_image, (1200, 900))  # if big
    VIDEO_HEIGHT, VIDEO_WIDTH, _ = original_image.shape

    # 가이드 박스 조정 슬라이더
    cv2.namedWindow("Guide")
    cv2.createTrackbar("size", "Guide", 0, VIDEO_WIDTH, lambda x: x)
    cv2.createTrackbar("x_offset", "Guide", 0, VIDEO_WIDTH, lambda x: x)
    cv2.createTrackbar("y_offset", "Guide", 0, VIDEO_HEIGHT, lambda x: x)
    cv2.setTrackbarPos("size", "Guide", 300)
    cv2.setTrackbarPos("x_offset", "Guide", int(VIDEO_WIDTH / 2))
    cv2.setTrackbarPos("y_offset", "Guide", int(VIDEO_HEIGHT / 2))

    p1p2 = cv2.selectROI("ROI", original_image)
    cv2.destroyWindow("ROI")

    # Original 웹캠 입력
    print(p1p2)
    object_region = original_image[
        p1p2[1] : p1p2[1] + p1p2[3], p1p2[0] : p1p2[0] + p1p2[2]
    ]

    # 웹캠 루프
    while True:
        # cv2.imshow("object", object_region)

        # 마커 크기 계산
        # marker_real_width = 8.6 # 민증 규격(cm)
        # marker_real_height = 5.6
        marker_real_width = 8.56  # 카드 규격(cm)
        marker_real_height = 5.398
        marker_ratio = marker_real_height / marker_real_width  # 마커 가로/세로 비율
        # 마커 픽셀 크기
        marker_width = cv2.getTrackbarPos("size", "Guide")  # 마커 width
        marker_height = marker_width * marker_ratio  # 마커 height

        # 마커 위치 설정
        (height, width, _) = original_image.shape
        x_offset = cv2.getTrackbarPos("x_offset", "Guide") - VIDEO_WIDTH / 2
        y_offset = cv2.getTrackbarPos("y_offset", "Guide") - VIDEO_HEIGHT / 2
        marker_p1 = (
            int(width / 2 - marker_width / 2 + x_offset),
            int(height / 2 - marker_height / 2 + y_offset),
        )
        marker_p2 = (
            int(width / 2 + marker_width / 2 + x_offset),
            int(height / 2 + marker_height / 2 + y_offset),
        )

        # guide_image: 사용자에게 보여줄 가이드(마커박스, 타이머 등)가 포함된 이미지
        guide_image = original_image.copy()
        cv2.rectangle(guide_image, marker_p1, marker_p2, (255, 0, 0), 1, cv2.LINE_AA)

        # # 타이머 실행중이면 처리하고 숫자 Display
        # if timer.is_capturing():
        #     tr = timer.process_timer()
        #     if not timer.done():
        #         font = cv2.FONT_HERSHEY_SIMPLEX
        #         cv2.putText(
        #             guide_image, str(tr), (50, 100), font, 4, (0, 255, 255), 4, cv2.LINE_AA,
        #         )

        # 가이드 이미지 출력
        cv2.imshow("Guide", guide_image)

        # 텀블러 영역 추출
        # tumbler = find_tumbler("otsu", object_region)  # black bg, white obj
        # tumbler = find_tumbler("otsu", object_region, True)  # white bg, black obj
        tumbler = find_tumbler("canny", object_region)

        cv2.imshow("Result", tumbler)

        # # 타이머 끝나면 캡쳐
        # if timer.is_capturing() and timer.done():
        #     cv2.destroyAllWindows()
        #     # 캡쳐 후 출력/저장
        #     cv2.imshow("Original", original_image)
        #     cv2.imwrite("./outputs/original.png", original_image)
        #     # 가이드 캡쳐 후 출력/저장
        #     cv2.imshow("Guide", guide_image)
        #     cv2.imwrite("./outputs/guide.png", guide_image)
        #     # (테스트) filled contours 캡쳐 후 출력/저장
        #     cv2.imshow("Filled Contours", tumbler)
        #     cv2.imwrite("./outputs/filled_contours.png", tumbler)
        #     break

        # 키보드 입력
        k = cv2.waitKey(1)

        # Q를 누르면 카운트다운 시작
        if k == ord("q"):
            # timer.start_timer(5)
            pass
        # T를 누르면 볼륨 계산
        elif k == ord("g"):
            # grabcut = grabCut(original_image)
            # cv2.imshow("grabcut", grabcut)
            # cv2.waitKey()
            pass
        elif k == ord("t"):
            volume = calc_volume(tumbler, marker_width / marker_real_width)

            rect_p1 = (p1p2[0], p1p2[1])
            rect_p2 = (p1p2[0] + p1p2[2], p1p2[1] + p1p2[3])
            cv2.rectangle(
                original_image, rect_p1, rect_p2, (255, 0, 0), 2,
            )
            cv2.putText(
                original_image,
                str(volume),
                rect_p1,
                cv2.FONT_HERSHEY_PLAIN,
                1,
                (0, 0, 255),
            )
            cv2.imshow("final", original_image)
            cv2.waitKey()

            print("volume", calc_volume(tumbler, marker_width / marker_real_width))

        elif k == ord("p"):
            cv2.imwrite("./tumbler_binary.png", tumbler)
        # ESC를 누르면 캡쳐하지 않고 종료
        elif k == 27:
            break

    # video.release()

    cv2.waitKey()
    cv2.destroyAllWindows()
