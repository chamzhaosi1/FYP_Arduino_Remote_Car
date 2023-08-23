import cv2
# import face_recognize
import numpy as np

# img = cv2.imread("../assets/bill_gates.jpg")
# height, width, rgb = img.shape

# cv2.circle(img, (int(width/2), int(height/2)), 80, (255,255,0), 2)

# ROI = img[0:int(height/2), 0:int(width/2)]
# imgBlur = cv2.GaussianBlur(ROI, (51,51), 0)

# img[0:int(height/2), 0:int(width/2)] = imgBlur


# cv2.imwrite(f'../assets/unknown.jpg', img)

# img = cv2.imread("../assets/bill_gates.jpg")
# # img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)



# hh, ww = img.shape[:2]
# hh2 = hh // 2
# ww2 = ww // 2

# # radius1 = 25
# radius2 = 75
# xc = hh // 2
# yc = ww // 2

# # mask1 = np.zeros_like(img)
# # mask1 = cv2.circle(mask1, (yc,xc), radius1, (255,255,255), -1)
# mask2 = np.zeros_like(img)
# mask2 = cv2.circle(mask2, (yc,xc), radius2, (255,255,255), -1)

# # cv2.imwrite(f'../assets/unknown2.png', mask2)
# mask = cv2.subtract(mask2, img)

# result = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

# result[:, :, 3] = mask2[:,:,0]

# cv2.imwrite(f'../assets/unknown-center.png', result)




# test = cv2.imread(f'../assets/unknown-center.png')
# cv2.imwrite(f'../assets/unknown-center.jpg', test)







# imgBlur = cv2.GaussianBlur(img, (51,51), 0)
# cv2.imwrite(f'../assets/unknown-blur.png', imgBlur)







# imgBlur= cv2.imread("../assets/bill_gates.jpg")
# imgBlur = cv2.GaussianBlur(imgBlur, (51,51), 0)
# # imgBlur.resize(512,512)
# center = cv2.imread("../assets/unknown-center.png")
# # center.resize(512,512)

# result = cv2.bitwise_and(imgBlur, center, mask=None)

# cv2.imwrite(f'../assets/unknown-blend.png', result)






# def blend(list_images): # Blend images equally.

#     equal_fraction = 1.0 / (len(list_images))

#     output = np.zeros_like(list_images[0])

#     for img in list_images:
#         output = output + img * equal_fraction

#     output = output.astype(np.uint8)
#     return output


# apple = cv2.imread("../assets/unknown-blur.png")
# banana = cv2.imread("../assets/unknown-center.png")
# list_images = [apple, banana]
# output = blend(list_images)
# cv2.imwrite(f'../assets/unknown-blend.jpg', output)


img = cv2.imread("../assets/bill_gates.jpg")
blurred_img = cv2.GaussianBlur(img, (51, 51), 0)

hh, ww = img.shape[:2]
hh2 = hh // 2
ww2 = ww // 2

mask = np.zeros((hh, ww, 3), dtype=np.uint8)
mask = cv2.circle(mask, (ww2, hh2-30), 90, (255,255,0), -1)

cv2.imwrite("../assets/unknown-mask.png", mask)

out = np.where(mask==np.array([255, 255, 0]), img, blurred_img)
cv2.circle(out, (ww2, hh2-30), 90, (255,255,0), 1)
cv2.imwrite("../assets/unknown-blend.jpg", out)
