import cv2
import numpy as np


def find_by_canny(image):
    # Image Blurring
    image = cv2.GaussianBlur(image, (11, 11), 1)

    # Top-Hat
    # filterSize =(5,5)
    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, filterSize)
    # gray = cv2.morphologyEx(gray,cv2.MORPH_BLACKHAT, kernel)

    # Edge 추출
    binary = cv2.Canny(image, 30, 220)

    # Closing (끊어진 edge 연결)
    kernel = np.ones((7, 7), np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

    # Contours 찾고 가장 영역이 넓은 Contour 찾기
    contours, hierarchy = cv2.findContours(
        binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    big_contour = max(contours, key=cv2.contourArea)

    # 검정 이미지에 가장 영역이 넓은 Contour 내부 채워서 그리기
    result = np.zeros_like(binary)
    cv2.drawContours(result, [big_contour], 0, (255, 255, 255), cv2.FILLED)

    # Opening (노이즈 제거)
    kernel = np.ones((3, 3), np.uint8)
    result = cv2.morphologyEx(result, cv2.MORPH_OPEN, kernel)

    return result


def find_by_otsu(image, darker_object=False):
    # Grayscaled 이미지 변환
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Otsu 이진화
    (_, binary) = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # 밝은 배경이면 반전
    if darker_object:
        cv2.bitwise_not(binary, binary)

    # Contours 찾고 가장 영역이 넓은 Contour 찾기
    contours, hierarchy = cv2.findContours(
        binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    big_contour = max(contours, key=cv2.contourArea)

    # 검정 이미지에 가장 영역이 넓은 Contour 내부 채워서 그리기
    result = np.zeros_like(binary)
    cv2.drawContours(result, [big_contour], 0, (255, 255, 255), cv2.FILLED)

    return result


def find_tumbler(type, image, darker_object=False):
    temp = image.copy()
    if type == "canny":
        return find_by_canny(temp)
    elif type == "otsu":
        return find_by_otsu(temp, darker_object)
