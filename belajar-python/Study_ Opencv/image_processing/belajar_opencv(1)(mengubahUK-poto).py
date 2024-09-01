import cv2

load = cv2.imread('blur.jpg', 1)
# size_x, size_y = load.shape[1], load.shape[0]
new_image = cv2.resize(load, (0,0), fx=0.5, fy = 0.5)
cv2.imshow('Foto Asli', load)
cv2.imshow('Foto Baru', new_image)

cv2.waitKey(0)
cv2.destroyAllWindows()