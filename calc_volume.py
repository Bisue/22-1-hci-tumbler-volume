import math


def calc_volume(image, px_per_cm):
    height, width = image.shape[:2]

    volume = 0  # 회전체 부피

    # 회전체 부피 적분하여 계산
    for y in range(0, height):
        count = 0  # 해당 y 픽셀 수 (지름 px)
        for x in range(0, width):
            # 유효 픽셀이면 카운트
            if image.item(y, x) > 200:
                count += 1
        # 반지름 px
        radius = count / 2
        # 텀블러 두께 보정
        radius = radius * 0.92
        # 단위 변환 (px -> cm)
        radius = radius / px_per_cm

        # 원 넓이 계산
        circle = math.pi * radius * radius

        # 부피에 추가 (높이 px -> cm 단위 변환)
        volume += circle / px_per_cm

    return volume
