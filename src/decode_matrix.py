import sys

import numpy as np
from PIL import Image
from numpy import empty
import matplotlib.pylab as plt
from matplotlib import pyplot as plot


def codepage(width):
    with open(f"{width}.codepage", mode="wb") as f:
        for i in range(width):
            for c in range(256):
                f.write(c.to_bytes(1, byteorder="little"))

def decode_matrix(width):
    light = f"{width}light.png"
    original = f"{width}original.png"
    # codepage(16)
    # codepage(256)
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
            d = 256 - (c1 + 1) / (i + 1)
            if d > 1.:
                decode_matrix.append(d)
            elif d != 0.:
                decode_matrix.append(1 / d)
            else:
                decode_matrix.append(0)
            a += 1
            value = c1 * decode_matrix[-1]
            # value =
            result.append(round(d))
            # print(value)
            image_result.putpixel((i, j), value=round(value))
            x.append(c1)
            y.append(c2)

    # image_result.save("image_result.png")
    x = np.asarray(x)
    y = np.asarray(y)
    # result = np.asarray(result)
    # result = result - (np.max(result) - 255)
    return result
    # plt.plot(result)
    # plt.show()
    # sys.exit()

