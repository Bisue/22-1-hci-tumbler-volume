from pickletools import read_unicodestring1
import cv2
import math


def calc_volume(image, px_per_cm):
    (height, width) = image.shape

    volume = 0

    # 1. 적분형
    for y in range(0, height):
        count = 0
        for x in range(0, width):
            if image.item(y, x) > 200:
                count += 1
        radius = ((count / 2) / px_per_cm) * 0.92
        circle = math.pi * radius * radius
        volume += circle / px_per_cm
        # print("count, radius, circle, volume: ", count, radius, circle, volume)

    # 2. 원통형 가정
    # c_height = 0
    # sum = 0
    # for y in range(0, height):
    #     count = 0
    #     for x in range(0, width):
    #         if image.item(y, x) > 200:
    #             count += 1
    #     if count > 0:
    #         sum += count
    #         c_height += 1

    # sum /= c_height
    # c_height /= px_per_cm
    # print("height: ", c_height)
    # c_width = sum / px_per_cm
    # radius = c_width / 2
    # print("width, radius: ", c_width, radius)
    # volume = c_height * radius * radius * math.pi

    return volume


# image = cv2.imread("./outputs/filled_contours.png", 0)
# print(calc_volume(image, 135 / 8.6))
