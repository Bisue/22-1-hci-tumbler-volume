import cv2
from cv2 import contourArea
import numpy as np
from pkg_resources import BINARY_DIST
from regex import P


def find_by_canny(image):
    # grayscaled 이미지 변환
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = image.copy()

    # 배경제거
    gray = cv2.GaussianBlur(gray, (11, 11), 1)
    # cv2.imshow("blurred", gray)

    # Applying the Top-Hat operation
    # filterSize =(5,5)
    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, filterSize)
    # gray = cv2.morphologyEx(gray,cv2.MORPH_BLACKHAT, kernel)

    # cv2.imshow("top", gray)

    # edge 추출
    binary = cv2.Canny(gray, 30, 220)
    # cv2.imshow("edge", binary)

    # closing
    kernel = np.ones((7, 7), np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

    # cv2.imshow("closing", binary)

    # contours 찾기
    contours, hierarchy = cv2.findContours(
        binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
    )
    big_contour = max(contours, key=cv2.contourArea)

    # 검정 배경에 흰색 filled contour 그리기
    result = np.zeros_like(binary)
    cv2.drawContours(result, [big_contour], 0, (255, 255, 255), cv2.FILLED)

    return result


def find_by_otsu(image, darker_object=False):
    # grayscaled 이미지 변환
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # otsu 이진화
    (_, binary) = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    if darker_object:
        cv2.bitwise_not(binary, binary)

    # 중간 과정 출력
    cv2.imwrite("./outputs/[temp]otsu-binarization.png", binary)

    # contours 찾기
    contours, hierarchy = cv2.findContours(
        binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
    )
    big_contour = max(contours, key=cv2.contourArea)

    # 검정 배경에 흰색 filled contour 그리기
    result = np.zeros_like(binary)
    cv2.drawContours(result, [big_contour], 0, (255, 255, 255), cv2.FILLED)

    return result


def find_tumbler(type, image, darker_object=False):
    if type == "canny":
        return find_by_canny(image)
    elif type == "otsu":
        return find_by_otsu(image, darker_object)


def grabCut(image):
    rc = cv2.selectROI(image)
    mask = np.zeros(image.shape[:2], np.uint8)

    cv2.grabCut(image, mask, rc, None, None, 5, cv2.GC_INIT_WITH_RECT)

    mask2 = np.where((mask == 0) | (mask == 2), 0, 255).astype("uint8")

    # dst = image * mask2[:, :, np.newaxis ]
    return mask2
