import cv2
import matplotlib.pyplot as plt
import numpy as np

# Read image from disk
img = cv2.imread('zaed.jpeg')

# Convert BGR to RGB
image_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Image shape along X and y
width = image_rgb.shape[1]
height = image_rgb.shape[0]

# Define the shearing factors
shear_X = 0.10
shear_Y = 0.10

# Define the Transformation matrix for shearing
transformation_matrix = np.array([[1, shear_X, 0],
                                  [0, 1, shear_Y]])
dtype=np.float32

# Apply Shearing
sheared_image = cv2.warpAffine(image_rgb, transformation_matrix, (width, height))

# Create Subplot
fig, axs = plt.subplots(1, 2, figsize=(7, 4))

# Plot the original image
axs[0].imshow(image_rgb)
axs[0].set_title('Original Image')

# Plot the sheared image
axs[1].imshow(sheared_image)
axs[1].set_title('Sheared Image')

# Remove ticks from the subplots
for ax in axs:
    ax.set_xticks([])
    ax.set_yticks([])

# Display the subplot
plt.tight_layout()
plt.show()
