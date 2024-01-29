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
    # "fb536381.txt",
    # "__fb536381.zip_.7z_.7z",
    "fb536381.zip",
]

xi0 = 1.0
separation = 1.0
side = 16.0
wavelength = 1.
width = int(side)
spacing = side / width

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
        L = 8 // int(math.log2(width))
        need_count_bytes = width * (width // L)
        while buffer:
            buffer = f.read(1)
            if buffer:
                b = int.from_bytes(buffer, "little")
                s += f"{b:08b}".rjust(8, "0")
                if len(s) == int(math.log2(width)) * width:
                    values1[-1].append([int(s[i: i + int(math.log2(width))], 2)
                                        for i in range(0, len(s), int(math.log2(width)))])
                    y += 1
                    s = ""
                if y == width:
                    y = 0
                    values1.append([])
    # print(values1)
    # sys.exit()
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


def write_values(file_name, vals):
    folder = "_" + file_name + "_"
    if not os.path.exists(folder):
        os.mkdir(folder)
    file_name2 = f"{folder}/{file_name}"
    for chunk in range(len(vals[:-1])):
        img = Image.new(mode="L", size=(width, width), color=0)
        for i in range(width):
            for j in range(width):
                img.putpixel((i, j), value=vals[chunk][i][j])
        img.save(file_name2 + f"{str(chunk).rjust(5, '0')}.light.png", format="PNG")
    add_appendix(file_name2, vals[-1])
def compress(file_name):
    print(f"Compress file '{file_name}'")
    vals = read_values(file_name)
    values = vals[:]
    appendix = []
    if (len(vals[-1]) != width + 1) \
            or (len(vals[-1][-1]) != width):
        appendix = vals[-1]
        values = vals[:-1]
    # print(vals[0])
    # sys.exit()
    v = np.asarray(vals[0])
    v = v.transpose()
    # plt.imshow(v, origin="lower", extent=[0, side, 0, side])
    plt.gray()
    # plt.show()
    plt.imsave(file_name + ".png", v)
    # write_values(file_name, vals)
    # sys.exit()
    folder = "_" + file_name + "_"
    # assert not os.path.exists(folder)
    if not os.path.exists(folder):
        os.mkdir(folder)
    file_name2 = f"{folder}/{file_name}"
    for chunk in range(len(values)):
        img = Image.new(mode="L", size=(width, width), color=0)
        xi = empty([width, width], float)
        for time in range(1, 2):
            time_name = str(time).rjust(3, "0")
            for j in range(width):
                for i in range(width):
                    print(j * width + i)
                    phi = 2 * math.pi / (values[chunk][i][j] + wavelength)
                    gz = width
                    xi[i, j] = sum(list(map(
                        lambda z: xi0 * sin(2 * math.pi * time * z + phi), r)))
                    # xi[i, j] = (sin(gz * 2 * math.pi / (time + 1) + phi) + 1) * 128
                    # if i % 2 == 0:
                    #     buffer = int(xi[i, j])
                    # else:
                    # buffer2 = int(xi[i, j])
                    # buffer = (buffer << 4) & buffer2
                    img.putpixel((i, j), value=int(xi[i][j]))
                    # print(i * width + j)
            # plt.imshow(np.asarray(xi).transpose(),
            #            origin="lower", extent=[0, side, 0, side])
            # plt.gray()
            # plt.show()
            output_file = \
                f"{folder}/{str(chunk).rjust(5, '0')}.light.png"
            img.save(output_file, format="PNG")
        break
    add_appendix(file_name2, appendix)
    return folder


def get_intensive(gz, amp, ampt, data):
    wl = []
    # plt.plot(amp)
    # plt.show()
    for time in range(len(ampt)):
        for a2 in range(len(gz)):
            waveLenght = \
                2 * math.pi / (amp[a2] - 2 * math.pi * r[time])
            wl.append({"lenght": round(float(waveLenght)) + 6, "time":
                time, "gz": gz[a2], "amp": int(amp[a2])})
    wl = [{'index': index,
           'lenght': data["lenght"],
           'time': data['time'],
           "gz": data['gz'], "amp": data['amp'] + 30}
          for index, data in enumerate(wl)]
    wl.sort(key=lambda item: item["time"])
    time = wl[0]["time"]
    lambdas = [[wl[0]]]
    for w in wl[1:]:
        if time == w["time"]:
            lambdas[-1].append(w)
        else:
            time = w["time"]
            lambdas.append([])
            lambdas[-1].append(w)
    zz = []
    print(len(lambdas), len(lambdas[0]))
    x = []
    for i in range(len(lambdas)):
        for j in range(len(lambdas[i])):
            # if lambdas[i][j]["amp"] > 0:
            x.append(lambdas[i][j])
    x.sort(key=lambda item: item["time"])
    print(x[0], x[-1])
    xx = []
    yy = []
    c = []
    for i in x:
        value = 2 * math.pi * i["index"] * r[i["time"]] / (i["lenght"] + 1)
        if i["index"] / 129:
            pass
        # rr.append(r[i["time"]] * i["index"])
        a = round(i["time"]) % width + 1
        b = round(i["time"]) // width + 1
        c.append(1. / width ** 2 * value)
        xx.append(value)
        yy.append(b)
        # z = sqrt(xx[-1] * xx[-1] + yy[-1] * yy[-1])
        # z = int(str(float(z)).split(".")[0])
        # zz.append(z)
    print(len(xx))
    colors = plot.get_cmap()(c)
    # plt.scatter(xx, yy, c=colors)
    plt.plot(xx)
    plt.show()
    return zz


def decode_phaze2(img, data):
    d = []
    for i in range(img.width):
        for j in range(img.height):
            d.append(img.getpixel((i, j)))
    rate = len(d)
    n = rate
    yf = rfft(d)
    xf = rfftfreq(n, 1 / rate)
    gz = xf[:]
    amp = yf[:]
    # plot.plot(gz, amp)
    # plot.show()
    ampt = irfft(d)[:]
    # plot.plot(ampt)
    # plot.show()
    intensive = get_intensive(gz, amp, ampt, False)
    # plot.plot(intensive)
    # plot.show()

    s = ""
    maxi = max(intensive)
    for i in range(len(intensive)):
        if intensive[i] > 1 * maxi / 8:
            s += "1"
        else:
            s += "0"
    # print(len(s))
    x = 0
    y = 0
    buf = Image.new(mode="L", size=(width * 2, width * 2))
    for i in range(0, len(s), 8):
        buffer = int(s[i: i + 8], 2)
        buf.putpixel((x, y), value=buffer)
        x += 1
        if x == width * 2:
            x = 0
            y += 1
    return buf, data


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
    rate = len(vals)
    n = rate
    yf = rfft(vals)
    xf = rfftfreq(n, 1 / rate)
    gz = xf[:]
    amp = yf[:]

    reverse = irfft(yf)
    reverses = []
    for index, lenght in enumerate(reverse):
        reverses.append({"index": index, "lenght": lenght + 1})

    yf = irfft(vals)
    ampt = np.abs(yf)[:width ** 2]
    # print(len(gz), len(amp), len(ampt), sep=":")
    intensive = get_intensive(gz, amp, ampt, vals)
    # plt.plot(intensive)
    # plt.show()
    s = ""
    maxi = max(intensive)
    for i in range(len(intensive)):
        if intensive[i] > 7 * maxi / 8:
            s += "1"
        else:
            s += "0"
    x = 0
    y = 0
    img = Image.new(mode="L", size=(8, 129))
    for i in range(0, len(s), 32):
        ss = s[i: i + 32]
        res = ""
        for j in range(0, len(ss), 4):
            buffer = int(ss[j: j + 4], 2)
            if buffer > 1:
                res += "1"
            else:
                res += "0"
        buffer = int(res, 2)
        # print(x, y)
        img.putpixel((x, y), value=buffer)
        x += 1
        if x == 8:
            x = 0
            y += 1
    img = img.crop((0, 0, 8, 8))
    img.save("output.png", format="PNG")
    # buf, data = decode_phaze2(img, vals)
    # buf = buf.crop((0, 0, 8, 8))
    # buf.save("output2.png", format="PNG")
    # buf, data = decode_phaze2(buf, data, "output3.png")
    # buf = buf.crop((0, 0, 8, 8))
    # buf.save("output3.png", format="PNG")
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
    chunks = [f for f in os.listdir(folder) if f.endswith(".light.png")]
    output_file = f"uncompress_{folder[1:-1]}"
    # # assert not os.path.exists(output_file)
    output = open(output_file, mode="wb")
    for c in chunks:
        print(c)
        data = decode(folder + "/" + c)
        buf = Image.new(mode="L", size=(width, width), color=0)
        for a in range(len(data)):
            buf.putpixel((a % width, a // width), value=data[a])
            # if a % 2 == 0:
            #     buffer1 = data[a]
            # else:
            #     buffer2 = data[a]
            #     buffer = (buffer1 << 4) | buffer2
            output.write(int.to_bytes(data[a], 1, byteorder="little"))
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
