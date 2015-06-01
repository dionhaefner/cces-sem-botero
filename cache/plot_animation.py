import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os

images = []

for subdir, dirs, files in os.walk("./"):
	for f in files:
		print(files)
		if f.endswith(".png"):
			images.append(plt.imread(f))

fig = plt.figure()
plt.imshow(images[0])

im_ani = animation.ArtistAnimation(fig, ims, interval=50, repeat_delay=3000,
    blit=True)
im_ani.save('im.mp4')