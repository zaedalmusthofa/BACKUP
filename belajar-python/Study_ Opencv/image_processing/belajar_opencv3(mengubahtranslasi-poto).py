import cv2
import matplotlib.pyplot as plt
import numpy as np

# Read image from disk
img = cv2.imread('zaed.jpeg')
# Convert BRG to RGB
image_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

width = image_rgb.shape[1]
height = image_rgb.shape[0]

tx = -70
ty = -100

# Translation Matrix
translation_matrix = np.array([[1,0,tx],[0,1,ty]],dtype = np.float32)

# warpAffine does appropriate shifting given the translation matrix
translated_image = cv2.warpAffine(image_rgb, translation_matrix,(width, height))
# Create Subplot
fig, axs = plt.subplots(1,2, figsize = (7, 4))

# Plot the original image
axs[0].imshow(image_rgb)
axs[0].set_title('Original Image')

# Plot the translation Image
axs[1].imshow(translated_image)
axs[1].set_title('Translation Image')

# Remove ticks from the subplots
for ax in axs:
    ax.set_xticks([])
    ax.set_yticks([])

# Display the subplot
plt.tight_layout()
plt.show()