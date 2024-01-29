import sys

import numpy as np
from PIL import Image
from numpy import empty
import matplotlib.pylab as plt
from matplotlib import pyplot as plot


def decode_matrix(width):
    light = f"{width}light.png"
    original = f"{width}original.png"

    image_light = Image.open(light)
    image_original = Image.open(original)
    image_result = Image.new(mode="L", size=(width, width), color=0)
    x = []
    y = []
    decode_matrix = []
    result = []
    a = 0
    for j in range(width):
        for i in range(width):
            c1 = image_light.getpixel((i, j))
            c2 = image_original.getpixel((i, j))
            d = c2 / c1
            if a == width ** 2 - width:
                decode_matrix.append(0)
            elif d > 1.:
                decode_matrix.append(d)
            elif d != 0.:
                decode_matrix.append(1 / d)
            else:
                decode_matrix.append(0)
            a += 1
            value = c1 * decode_matrix[-1]
            result.append(value)
            # print(value)
            image_result.putpixel((i, j), value=round(value))
            x.append(c1)
            y.append(c2)

    # image_result.save("image_result.png")
    x = np.asarray(x)
    y = np.asarray(y)

    plt.scatter(x, y)
    plt.show()
    sys.exit()
    return decode_matrix
