import cv2
import numpy as np
from pkg_resources import BINARY_DIST


def find_tumbler(image):
    # grayscaled 이미지 변환
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 이진화(otsu)
    th, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # cv2.bitwise_not(binary, binary)
    cv2.imwrite("./outputs/mid-binary-otsu.png", binary)

    # contours 찾기
    contours = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    big_contour = max(contours, key=cv2.contourArea)

    # 검정 배경에 흰색 filled contour 그리기
    result = np.zeros_like(binary)
    cv2.drawContours(result, [big_contour], 0, (255, 255, 255), cv2.FILLED)

    return result
