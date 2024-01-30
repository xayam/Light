import sys
import numpy as np
from PIL import Image
from matplotlib import pyplot as plot


def decode_matrix(width):
    light = f"{width}.light"
    original = f"{width}.original"
    image_light = Image.open(light)
    image_original = Image.open(original)
    decode_matrix = []
    for j in range(width):
        for i in range(width):
            c1 = image_light.getpixel((i, j))
            c2 = image_original.getpixel((i, j))
            d =  c2 / c1
            if d > 1.:
                decode_matrix.append(d)
            elif d != 0.:
                decode_matrix.append(1 / d)
            else:
                decode_matrix.append(0)
    return decode_matrix
    # plt.plot(decode_matrix)
    # plt.show()
    # sys.exit()

