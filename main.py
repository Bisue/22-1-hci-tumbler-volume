import os
import cv2
from calc_volume import calc_volume
from find_tumbler import find_tumbler


# 이미지 비율 고정하고 사이즈 조정 (height 기준)
def resize_aspect_ratio(image, height, inter=cv2.INTER_AREA):
    (h, w) = image.shape[:2]

    r = height / float(h)
    size = (int(w * r), height)

    resized = cv2.resize(image, size, interpolation=inter)

    return resized


# 윈도우 설정
def setup_windows(w, h):
    # Tumbler window
    cv2.namedWindow("Tumbler")
    cv2.moveWindow("Tumbler", w, 0)

    # Guide window
    cv2.namedWindow("Guide")
    cv2.resizeWindow("Guide", w, h)
    cv2.moveWindow("Guide", 0, 0)
    cv2.createTrackbar("size", "Guide", 0, w, lambda x: x)
    cv2.createTrackbar("x_offset", "Guide", 0, w, lambda x: x)
    cv2.createTrackbar("y_offset", "Guide", 0, h, lambda x: x)
    cv2.setTrackbarPos("size", "Guide", 300)
    cv2.setTrackbarPos("x_offset", "Guide", int(w / 2))
    cv2.setTrackbarPos("y_offset", "Guide", int(h / 2))

    # ROI window
    cv2.namedWindow("ROI")
    cv2.moveWindow("ROI", 0, 0)


# main
if __name__ == "__main__":
    # CONFIGs
    IMAGE_PATH = "./inputs/333.jpg"  # 입력 이미지 경로
    MARKER_SIZE_CM = (8.56, 5.398)  # 카드(ID-1 규격)
    # MARKER_SIZE_CM = (8.6, 5.6)  # 민증

    # 이미지 로드
    original_image = cv2.imread(IMAGE_PATH)
    # 이미지 로드 실패
    if original_image is None:
        print("이미지를 불러오지 못했습니다!")
        exit()
    # 너무 크면 화면에 들어오게 축소
    if original_image.shape[0] >= 800:
        original_image = resize_aspect_ratio(original_image, 800)

    # 로드된 이미지 사이즈
    image_height, image_width = original_image.shape[:2]

    # 윈도우 설정 (Trackbar, 위치)
    setup_windows(image_width, image_height)

    # 텀블러 사각 영역 지정
    tbx, tby, tbw, tbh = cv2.selectROI("ROI", original_image)
    cv2.destroyWindow("ROI")

    # 텀블러 사각 영역 이미지 Crop
    object_region = original_image[tby : tby + tbh, tbx : tbx + tbw]

    # 마커 사이즈 조정
    while True:
        # 마커 비율
        marker_ratio = MARKER_SIZE_CM[1] / MARKER_SIZE_CM[0]  # 마커 가로/세로 비율
        # 마커 크기(px)
        marker_width = cv2.getTrackbarPos("size", "Guide")  # 마커 width
        marker_height = marker_width * marker_ratio  # 마커 height

        # 마커 위치 설정
        x_offset = cv2.getTrackbarPos("x_offset", "Guide") - image_width / 2
        y_offset = cv2.getTrackbarPos("y_offset", "Guide") - image_height / 2
        marker_p1 = (
            int(image_width / 2 + x_offset),
            int(image_height / 2 + y_offset),
        )
        marker_p2 = (
            int(image_width / 2 + marker_width + x_offset),
            int(image_height / 2 + marker_height + y_offset),
        )

        # guide_image: 사용자에게 보여줄 가이드 정보(마커 박스)가 포함된 이미지
        guide_image = original_image.copy()
        cv2.rectangle(guide_image, marker_p1, marker_p2, (255, 0, 0), 1, cv2.LINE_AA)

        # 가이드 이미지 출력
        cv2.imshow("Guide", guide_image)

        # 텀블러 영역 추출
        # tumbler = find_tumbler("otsu", object_region)  # black bg, white obj
        # tumbler = find_tumbler("otsu", object_region, True)  # white bg, black obj
        tumbler = find_tumbler("canny", object_region)

        # 추출된 텀블러 이미지 출력
        cv2.imshow("Tumbler", tumbler)

        # 키보드 입력
        k = cv2.waitKey(1)

        # Enter or T를 누르면 용량 계산
        if k == 13 or k == ord("t"):
            # 텀블러 용량 계산
            volume = round(calc_volume(tumbler, marker_width / MARKER_SIZE_CM[0]), 2)
            print("volume", volume)

            # 결과 이미지
            result_image = original_image.copy()

            # 사용자가 선택한 텀블러 사각 영역 그리기
            rect_p1 = (tbx, tby)
            rect_p2 = (tbx + tbw, tby + tbh)
            cv2.rectangle(result_image, rect_p1, rect_p2, (255, 0, 0), 2)

            # 텀블러 용량 텍스트로 그리기
            text_p = (tbx, tby - 5)
            if text_p[1] <= 15:
                text_p = (tbx + tbw + 5, tby + 15)
            cv2.putText(
                result_image,
                str(volume) + "ml",
                text_p,
                cv2.FONT_HERSHEY_PLAIN,
                1,
                (0, 0, 255),
                lineType=cv2.LINE_AA,
            )

            # 결과 이미지 출력
            cv2.imshow("Result", result_image)

            # 결과 파일로 저장
            filename, extension = os.path.splitext(os.path.basename(IMAGE_PATH))
            cv2.imwrite("./outputs/" + filename + "-tumbler." + extension, tumbler)
            cv2.imwrite("./outputs/" + filename + "." + extension, result_image)

            # 키보드 입력
            k = cv2.waitKey()

            # 아무 키나 누르면 다시
            cv2.destroyWindow("Result")
            continue

        # ESC를 누르면 종료
        elif k == 27:
            break

    cv2.destroyAllWindows()
