import cv2
import numpy as np
import matplotlib.pyplot as plt

# Read image from disk
img = cv2.imread('behind_lab.jpg')

# Convert BRG to RGB
image_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Split the image into channels
b, g, r = cv2.split(image_rgb)

# Normalization Parameter
min_value = 0
max_value = 1
norm_type = cv2.NORM_MINMAX

# Normalization each channel
b_normalized = cv2.normalize(b.astype('float'), None, min_value, max_value, norm_type)
g_normalized = cv2.normalize(b.astype('float'), None, min_value, max_value, norm_type)
r_normalized = cv2.normalize(b.astype('float'), None, min_value, max_value, norm_type)

# Merge the normalized channels back into an image
normalized_image = cv2.merge((b_normalized, g_normalized, r_normalized))

# Normalized Image
print(normalized_image[:,:,0])

plt.imshow(normalized_image)
plt.xticks([])
plt.yticks([])
plt.title('Normalized Image')
plt.show()