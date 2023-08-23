import cv2
import numpy as np

img = cv2.imread('/home/engineer/romo/assets/bill_gates.jpg')

# height, width, _ = img.shape
# print(f"H: {height}, W: {width}")

# offset = 20
# radius = round(min(width, height) / 2)
# radius = radius - offset
# print(f"r: {radius}")

# x1, y1 = 0, -40 ## derivative
# center = (round(x1 + width / 2), round(y1 + height / 2))
# print(f"c: {center}")

# mask = np.zeros(img.shape, dtype=np.uint8)
# cv2.circle(mask, center, radius, (255, 255, 255), -1)
# # cv2.imwrite(f'../assets/mask.png', mask)

# ROI = cv2.bitwise_and(img, mask)
# # cv2.imwrite(f'../assets/roi.png', ROI)

# mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
# x, y, w, h = cv2.boundingRect(mask)
# result = ROI[y:y + h, x:x + w]
# mask = mask[y:y + h, x:x + w]
# result[mask == 0] = (255, 255, 255)

# height, width, _ = img.shape
# center = (width//2, height-40//2)
# radius = 

# mask = np.zeros(img.shape, dtype=np.uint8)
# cv2.circle(mask, center, radius, (255, 255, 255), -1)

# ROI = cv2.bitwise_and(img, mask)
# mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
# x, y, w, h = cv2.boundingRect(mask)
# result = ROI[y:y + h, x:x + w]
# mask = mask[y:y + h, x:x + w]
# result[mask == 0] = (255, 255, 255)

# cv2.imwrite(f'../assets/soi.jpg', result)