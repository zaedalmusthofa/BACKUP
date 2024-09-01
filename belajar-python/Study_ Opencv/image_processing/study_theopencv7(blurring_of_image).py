import cv2
import matplotlib.pyplot as plt
import numpy as np

# Read image from disk
img = cv2.imread('behind_lab.jpg')

# Convert BRG to RGB
image_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Apply Gaussian Blur
blurred = cv2.GaussianBlur(image_rgb, (21, 21), 0)

# Convert blurred image to RGB
blurred_rgb = cv2.cvtColor(blurred, cv2.COLOR_BGR2RGB)

# Create Subplots
fig, axs = plt.subplots(1, 2, figsize = (7, 4))

# Plot the original Image
axs[0].imshow(image_rgb)
axs[0].set_title('Original Image')

# Plot the Blurr Image
axs[1].imshow(blurred_rgb)
axs[1].set_title('Blurr Image')

# Remove ticks from suplots
for ax in axs :
    ax.set_xticks([])
    ax.set_yticks([])

# Display the subplots
plt.tight_layout()
plt.show()