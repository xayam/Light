import math
import os
import pprint
import sys
from math import sqrt, sin, pi

import matplotlib
import numpy as np
from PIL import Image
from numpy import empty
import matplotlib.pylab as plt
from matplotlib import pyplot as plot
from scipy.fft import rfft, irfft, rfftfreq

files = [
    # "video1.zip",
    "fb536381.txt",
    # "fb536381.zip",
]

xi0 = 1.0
separation = 1.0
side = 256.0  # 4, 16 or 256
width = int(side)
spacing = side / width
c = 299792458
e0 = 10 ** 7 / 4 / math.pi / c ** 2

assert width in [4, 16, 256]

x = [(i % width) + separation / 2 for i in range(width ** 2)]
r = [0. for _ in range(width ** 2)]
for i in range(width):
    for j in range(width):
        r[j * width + i] = \
            sqrt((i - x[j * width + i]) ** 2 + (j - x[j * width + i]) ** 2)


def read_values(file_name):
    print(f"Reading file '{file_name}'")
    with open(file_name, mode="rb") as f:
        buffer = True
        values1 = [[]]
        y = 0
        s = ""
        L = int(math.log2(width))
        while buffer:
            buffer = f.read(1)
            if buffer:
                b = int.from_bytes(buffer, "little")
                s += f"{b:08b}".rjust(8, "0")
                if len(s) == width * L:
                    values1[-1].append([int(s[i: i + L], 2) for i in range(0, len(s), L)])
                    y += 1
                    s = ""
                if y == width:
                    y = 0
                    values1.append([])
    return values1


def add_appendix(file_name, value):
    output_file = f"{file_name}.aaaaa.light"
    print(f"Added appendix file '{output_file}'")
    if value:
        with open(output_file, mode="wb") as f:
            for x in range(len(value)):
                for y in range(len(value[x])):
                    buf = int.to_bytes(value[x][y], length=1, byteorder="little")
                    f.write(buf)


def compress(file_name):
    print(f"Compress file '{file_name}'")
    vals = read_values(file_name)
    values = vals[:]
    appendix = []
    if (len(vals[-1]) != width + 1) \
            or (len(vals[-1][-1]) != width):
        appendix = vals[-1]
        values = vals[:-1]
    print(vals[0])
    # sys.exit()
    # v = np.asarray(vals[0])
    # v = v.transpose()
    # plt.imshow(v, origin="lower", extent=[0, side, 0, side])
    # plt.gray()
    # plt.show()
    folder = "_" + file_name + "_"
    img = Image.new(mode="L", size=(width, width), color=255)
    for i in range(width):
        for j in range(width):
            img.putpixel((i, j), value=vals[0][i][j])
    img.save("__" + file_name + ".png", format="PNG")
    # assert not os.path.exists(folder)
    if not os.path.exists(folder):
        os.mkdir(folder)
    file_name2 = f"{folder}/{file_name}"
    for chunk in range(len(values)):
        img = Image.new(mode="L", size=(width, width), color=255)
        xi = empty([width, width], float)
        for i in range(width):
            for j in range(width):
                wavelength = values[chunk][i][j] + 1
                k = 2 * pi / wavelength
                xi[i, j] = sum(list(map(lambda z: xi0 * sin(k * z), r)))
                img.putpixel((i, j), value=int(xi[i, j]))
                print(i * width + j)
        # plt.imshow(np.asarray(xi).transpose(),
        #            origin="lower", extent=[0, side, 0, side])
        # plt.gray()
        # plt.show()
        output_file = f"{file_name2}.{str(chunk).rjust(5, '0')}.light.png"
        img.save(output_file, format="PNG")
        break
    add_appendix(file_name2, appendix)
    return folder


def decode(file_name):
    buf = Image.open(file_name)
    vals = []
    for x in range(buf.height):
        for y in range(buf.width):
            vals.append(buf.getpixel((x, y)))
    print(len(set(vals)))
    rate = len(vals)
    n = rate
    yf = rfft(vals)
    xf = rfftfreq(n, 1 / rate)
    plot.plot(xf, yf)
    plot.show()
    # print(len(set(xf)))
    # print(len(set(yf)))
    i = []
    # xf = xf[1:width + 1]
    # yf = yf[1:width + 1]
    amp = yf

    yf = irfft(vals)
    gz = yf[1: width + 1]
    plot.plot(yf)
    plot.show()
    return np.asarray(buf)
    # sys.exit()
    maxi = np.max(amp)
    mini = np.min(amp)
    amp = 255 * (amp - mini) / (maxi - mini)

    maxi = np.max(gz)
    mini = np.min(gz)
    gz = 255 * (gz - mini) / (maxi - mini)
    print(max(vals))
    print(min(vals))
    x = []
    y = []
    color = []
    for i in range(width):
        for j in range(width):
            x.append(gz[i])
            y.append(amp[j])
            color.append(1. / (vals[j * width + i] + 1.))
    colors = plot.get_cmap()(color)
    maxi = np.max(x)
    mini = np.min(x)
    x = 2 * (np.asarray(x) - mini) / (maxi - mini) - 1
    maxi = np.max(y)
    mini = np.min(y)
    y = 2 * (np.asarray(y) - mini) / (maxi - mini) - 1
    plot.scatter(x, y, c=colors)
    plot.show()
    return np.asarray(buf)


def decompress(folder):
    print(f"Decompress folder '{folder}'")
    # assert os.path.exists(folder)
    lists = [f for f in os.listdir(folder) if f.endswith(".light.png")]
    output_file = f"uncompress_{folder[1:-1]}"
    # assert not os.path.exists(output_file)
    output = open(output_file, mode="wb")
    for f in lists:
        print(f)
        data = decode(folder + "/" + f)
        for x in range(len(data)):
            for y in range(len(data[x])):
                output.write(int.to_bytes(int(data[y][x]), 1, byteorder="little"))
        break
    output.close()
    return output_file


def check(file_name1, file_name2):
    print(f"Checking files '{file_name1}' and '{file_name2}'")
    with open(file_name1, mode="rb") as f1:
        with open(file_name2, mode="rb") as f2:
            b1 = True
            b2 = True
            count = 1
            while b1 and b2:
                b1 = f1.read(1)
                b2 = f2.read(1)
                c1 = int.from_bytes(b1, byteorder="little")
                c2 = int.from_bytes(b2, byteorder="little")
                print(c1, c2, count, sep=":")
                count += 1
                assert c1 == c2
    return True


if __name__ == "__main__":
    for file in files:
        compress_folder = compress(file)
        decompress_file = decompress(compress_folder)
        if check(decompress_file, file):
            print("Check success!!!")
