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
    # "__fb536381.zip_.7z_.7z",
    # "fb536381.zip",
]

xi0 = 1.0
separation = 1.0
side = 16.0  # 4, 16 or 256
width = int(side)
spacing = side / width
c = 299792458
e0 = 10 ** 7 / 4 / math.pi / c ** 2

assert width in [4, 16, 256]

x = [(i % width) + separation / 2 for i in range(width ** 2)]
y = x[:]
r = [0. for _ in range(width ** 2)]
for i in range(width):
    for j in range(width):
        r[j * width + i] = \
            sqrt((i - x[j * width + i]) ** 2 + \
                 (j - y[j * width + i]) ** 2)


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
    v = np.asarray(vals[0])
    v = v.transpose()
    # plt.imshow(v, origin="lower", extent=[0, side, 0, side])
    plt.gray()
    # plt.show()
    plt.imsave(file_name + ".png", v)
    folder = "_" + file_name + "_"
    # img = Image.new(mode="L", size=(width, width), color=255)
    # for i in range(width):
    #     for j in range(width):
    #         img.putpixel((i, j), value=vals[0][i][j])
    # img.save("__" + file_name + ".png", format="PNG")
    # assert not os.path.exists(folder)
    if not os.path.exists(folder):
        os.mkdir(folder)
    file_name2 = f"{folder}/{file_name}"
    for chunk in range(len(values)):
        img = Image.new(mode="L", size=(width // 2, width), color=0)
        xi = empty([width, width], float)
        buffer = 0
        for j in range(width):
            for i in range(width):
                wavelength = values[chunk][i][j] + 1
                phi = 2 * math.pi / wavelength
                k = width ** 2
                xi[i, j] = sum(list(map(
                    lambda z: xi0 *
                              sin(2 * math.pi * k * (j * width + i + 1) * z + phi), r)))
                if i % 2 == 0:
                    buffer = int(xi[i, j])
                else:
                    buffer2 = int(xi[i, j])
                    buffer = (buffer << 4) & buffer2
                    img.putpixel((i // 2 , j), value=buffer)
                # print(i * width + j)
        # plt.imshow(np.asarray(xi).transpose(),
        #            origin="lower", extent=[0, side, 0, side])
        # plt.gray()
        # plt.show()
        output_file = f"{folder}/{str(chunk).rjust(5, '0')}.light.png"
        img.save(output_file, format="PNG")
        break
    add_appendix(file_name2, appendix)
    return folder


def decode(file_name):
    buf = Image.open(file_name)
    vals = []
    for y in range(buf.height):
        for x in range(buf.width):
            buffer = buf.getpixel((x, y))
            buffer1 = buffer & (15 << 4) >> 4
            buffer2 = buffer & 15
            vals.append(buffer1)
            vals.append(buffer2)
            # print(buffer1)
            # print(buffer2)
    print(len(set(vals)))
    # plot.plot(vals)
    # plot.show()
    rate = len(vals)
    n = rate
    yf = rfft(vals)
    xf = rfftfreq(n, 1 / rate)
    # plot.plot(xf, yf)
    # plot.show()

    gz = xf[:]
    amp = np.abs(yf)[:]

    # phi = gz - r[y * width + x]
    # vals[y * width + x] = int(vals[y * width + x] / math.sin(phi))
    # # vals[y * width + x] = 2 * math.pi * r[y * width + x] / gz - 1
    # print(vals[y * width + x])
    yf = irfft(vals)

    ampt = np.abs(yf)[:width ** 2]
    print(len(gz), len(amp), len(ampt), sep=":")

    plot.plot(gz, amp)
    plot.show()
    plot.plot(ampt)
    plot.show()
    wl = []
    index = 0
    for time in range(len(ampt)):
        for a2 in range(len(amp)):
            if gz[a2] > 0:
                if amp[a2] > 0:
                    # print(I, gz[a2], amp[a2], sep=":")
                    waveLenght = \
                        2 * math.pi / (gz[a2] -
                                       2 * math.pi * width ** 2 * (time + 1) * r[time])
                    # print(waveLenght)
                    wl.append(waveLenght + 1)
                    index += 1
                    break
    wl = [{'index': index, 'data': data} for index, data in enumerate(wl)]
    # wl.sort(key=lambda item: item["data"])
    # print(wl, wl[0], len(wl))
    lambdas = [0. for _ in range(width ** 2)]
    for w in wl:
        # print(w)
        lambdas[w["index"]] = w["data"]
    mini = np.min(lambdas)
    maxi = np.max(lambdas)
    lambdas = (width - 1) * (np.asarray(lambdas) - mini) / (maxi - mini)
    for time in range(len(vals)):
        vals[time] = int(lambdas[time])
        print(vals[time])
    print(max(vals))
    # plt.plot(wl)
    # plt.show()

    # new_sig = irfft(amp)
    # plt.plot(new_sig)
    # plt.show()
    return vals

    # color = []
    # for i in range(width):
    #     for j in range(width):
    #         x.append(gz[i])
    #         y.append(amp[j])
    #         color.append(1. / (vals[j * width + i] + 1.))
    # colors = plot.get_cmap()(color)
    # plot.scatter(x, y, c=colors)
    # plot.show()


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
        buf = Image.new(mode="L", size=(width, width), color=0)
        buffer1 = 0
        x = 0
        y = 0
        for a in range(len(data)):
            if a % 2 == 0:
                buffer1 = data[a]
            else:
                buffer2 = data[a]
                buffer = (buffer1 << 4) | buffer2
                # print(x, y, buffer)
                buf.putpixel((x, y), value=buffer)
                output.write(int.to_bytes(buffer, 1, byteorder="little"))
                x += 1
            if x == width // 2:
                x = 0
                y += 1

        buf.save(folder + ".png", format="PNG")
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
