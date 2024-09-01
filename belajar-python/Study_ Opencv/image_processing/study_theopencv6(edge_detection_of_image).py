import cv2
import matplotlib.pyplot as plt
import numpy as np

# Read image from disk
img = cv2.imread('behind_lab.jpg')

# Convert BRG to RGB
image_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Apply Canny edge detection detection
edge = cv2.Canny(image= image_rgb, threshold1=50, threshold2=150)

# Create Subplots
fig, axs = plt.subplots(1, 2, figsize = (7, 4))

# Plot the original image_rgb
axs[0].imshow(image_rgb)
axs[0].set_title('original Image')

# Plot the blurred image
axs[1].imshow(edge)
axs[1].set_title('Image Edges')

# Remove ticks from subplots
for ax in axs :
    ax.set_xticks([])
    ax.set_yticks([])

# Display the subplots
plt.tight_layout()
plt.show()