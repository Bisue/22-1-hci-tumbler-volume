import cv2
from calc_volume import calc_volume

from find_tumbler import find_tumbler, grabCut

image = cv2.imread("./tumbler-canny/original.png")

tumbler1 = find_tumbler("otsu", image)
tumbler2 = find_tumbler("canny", image)
tumbler3 = grabCut(image)

cv2.imshow("Method 1", tumbler1)
cv2.imshow("Method 2", tumbler2)
cv2.imshow("Method 3", tumbler3)

print("Method 1 Volume: ", calc_volume(tumbler1, 125))
print("Method 2 Volume: ", calc_volume(tumbler2, 125))
print("Method 3 Volume: ", calc_volume(tumbler3, 125))

cv2.waitKey()
