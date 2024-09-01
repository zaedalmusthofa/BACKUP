import cv2
import matplotlib.pyplot as plt

# Read image from disk
img = cv2.imread('behind_lab.jpg')

# convert brg to rgb
image_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# image rotation parameter
center = (image_rgb.shape[1] // 2, image_rgb.shape[0] // 2)
angle = 30
scale = 1

# getRotationmatrix2D creates matrix needed transformation
rotation_matrix = cv2.getRotationMatrix2D(center, angle, scale)

# we want matrix for the rotation w.r.t center to 30 degree wihout scaling
rotated_image = cv2.warpAffine(image_rgb, rotation_matrix, (img.shape[1], img.shape[0]))

# create subplot
fig, axs = plt.subplots(1, 2, figsize =(7,4))

# plot the original image
axs[0].imshow(image_rgb)
axs[0].set_title('Original Image')

# plot the New image
axs[1].imshow(rotated_image)
axs[1].set_title('Image Rotation')

# Remove ticks from the subplot
for ax in axs:
    ax.set_xticks([])
    ax.set_yticks([])

# Display the Subplot
plt.tight_layout()
plt.show()