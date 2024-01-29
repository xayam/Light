import numpy as np
from PIL import Image
from numpy import empty
import matplotlib.pylab as plt
from matplotlib import pyplot as plot

width = 16
light = "light.png"
original = "original.png"

image_light = Image.open(light)
image_original = Image.open(original)

x = []
y = []
for j in range(width):
    for i in range(width):
        c1 = image_light.getpixel((i, j))
        c2 = image_original.getpixel((i, j))[0]
        x.append(c1)
        y.append(c2)
        print(c1, c2)
x = np.asarray(x)
y = np.asarray(y)

plt.plot(y / x)
plt.show()
