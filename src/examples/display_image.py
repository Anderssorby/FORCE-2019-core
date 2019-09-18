import cv2
import matplotlib.pyplot as plt

# modify this if you want to look at a different image.
fname = "data/logimages/6406_3_3/6406_3_3_3938_3939.jpg"

img = cv2.imread(fname)

H, W, n_channels = img.channels
print(f"Height: {H}, width: {W}, number of channels: {n_channels}")
plt.imshow(img)
