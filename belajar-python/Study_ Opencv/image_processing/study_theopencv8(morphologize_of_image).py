import cv2
import numpy as np
import matplotlib.pyplot as plt

# Read Image from Disk
img = cv2.imread('ganeshji.jpg')

# Convert BRG to RGB
image_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Create a Structuring element
kernel = np.ones((3, 3), np.uint8)

# Perform Dilation
dilated = cv2.dilate(image_gray, kernel, iterations=2)

# Perform Erotion
eroded = cv2.erode(image_gray, kernel, iterations=2)

# Perform Opening (erosiom folowed by dilatiom)
opening = cv2.morphologyEx(image_gray, cv2.MORPH_OPEN, kernel)

# Perform Closing (dilation followed by erision)
closing = cv2.morphologyEx(image_gray, cv2.MORPH_CLOSE, kernel)

# Create Subplots
fig, axs = plt.subplots(2,2, figsize=(7, 7))

# Plot the dilated image
axs[0,0].imshow(dilated, cmap='Greys')
axs[0,0].set_title('Dilated Image')
axs[0,0].set_xticks([])
axs[0,0].set_yticks([])

# Plot the eroded image
axs[0,1].imshow(eroded, cmap='Greys')
axs[0,1].set_title('Eroded Image')
axs[0,1].set_xticks([])
axs[0,1].set_yticks([])

# Plot the opening(erosed by followed by dilation)
axs[1,0].imshow(opening, cmap='Greys')
axs[1,0].set_title('Opening')
axs[1,0].set_xticks([])
axs[1,0].set_yticks([])

# Plot the Closing(dilation followed by erosion)
axs[1,1].imshow(closing, cmap='Greys')
axs[1,1].set_title('Closing')
axs[1,1].set_xticks([])
axs[1,1].set_yticks([])

# Display the subplots
plt.tight_layout()
plt.show()