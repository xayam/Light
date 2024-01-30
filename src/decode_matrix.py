import math
import sys

import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
from scipy.fft import irfft


def decode_matrix(width):
    light = f"{width}.light.cp"
    original = f"{width}.original.cp"
    image_light = Image.open(light)
    image_original = Image.open(original)
    decode_matrix1 = []
    for j in range(width):
        for i in range(width):
            c1 = image_light.getpixel((i, j))
            c2 = image_original.getpixel((i, j))
            d = (c2 + 1) / (c1 + 1)
            if d > 1.:
                decode_matrix1.append(d)
            elif d == 0.:
                decode_matrix1.append(0)
            else:
                decode_matrix1.append(1 / d)
    # return decode_matrix1
    # ifft = irfft(decode_matrix1)
    # amp = ifft[1:width ** 2 + 1]
    # amp = irfft(amp)[1:width ** 2 + 1]
    # print("")
    # print(len(decode_matrix1))
    # plt.plot(decode_matrix1)
    # plt.show()
    # sys.exit()
    return decode_matrix1


def codepages(width):
    with open(f"{width}.1.cp", mode="wb") as f:
        for c in range(width):
            for i in range(width):
                f.write(c.to_bytes(1, byteorder="little"))
    with open(f"{width}.2.cp", mode="wb") as f:
        for i in range(width):
            for c in range(width):
                f.write(c.to_bytes(1, byteorder="little"))
