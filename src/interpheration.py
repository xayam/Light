import math
import os
from math import sqrt, sin, pi
import numpy as np
from PIL import Image
from numpy import empty
import matplotlib.pylab as plt
from scipy.fft import rfft  # , rfftfreq

files = [
    # "video1.zip",
    "fb536381.txt",
    # "fb536381.zip",
]

xi0 = 1.0
separation = 1.0
side = 256.0
width = int(side)
spacing = side / width
c = 299792458
e0 = 10 ** 7 / 4 / math.pi / c ** 2
er = width ** 2 / 4
e = e0 * er


def read_values(file_name):
    print(f"Reading file '{file_name}'")
    with open(file_name, mode="rb") as f:
        buffer = True
        values1 = [[[]]]
        y = 0
        x = 0
        while buffer:
            buffer = f.read(1)
            if buffer:
                b = int.from_bytes(buffer, "little")
                values1[-1][-1].append(int(b))
                y += 1
                if y == width:
                    values1[-1].append([])
                    y = 0
                    x += 1
                if x == width:
                    x = 0
                    y = 0
                    values1.append([[]])
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
    plt.imshow(vals[0], origin="lower", extent=[0, side, 0, side])
    plt.gray()
    plt.show()
    folder = "_" + file_name + "_"
    img = Image.new(mode="L", size=(width, width), color=255)
    for i in range(width):
        for j in range(width):
            img.putpixel((i, j), value=vals[0][i][j])
    img.save("64kb_" + file_name + ".png", format="PNG")
    # assert not os.path.exists(folder)
    if not os.path.exists(folder):
        os.mkdir(folder)
    file_name2 = f"{folder}/{file_name}"
    x = [i for i in range(width)]
    x = list(map(lambda i: i + separation / 2, x))
    r = [0. for _ in range(width)]
    for t in range(len(r)):
        for i in range(width):
            for j in range(width):
                r[t] = sqrt((i - x[t]) ** 2 + (j - x[t]) ** 2)
    for chunk in range(len(values)):
        img = Image.new(mode="L", size=(width, width), color=255)
        xi = empty([width, width], float)
        for i in range(width):
            for j in range(width):
                wavelength = values[chunk][i][j] + 1
                k = 2 * pi / wavelength
                xi[i, j] = sum(list(map(lambda z: xi0 * sin(k * z), r)))
                img.putpixel((i, j), value=int(xi[i, j]))
        plt.imshow(xi, origin="lower", extent=[0, side, 0, side])
        plt.gray()
        plt.show()
        output_file = f"{file_name2}.{str(chunk).rjust(5, '0')}.light.png"
        img.save(output_file, format="PNG")
        break
    add_appendix(file_name2, appendix)
    return folder


def decode(file_name):
    xx = [i for i in range(width)]
    xx = list(map(lambda i: i + separation / 2, xx))
    r = [0. for _ in range(width)]
    buf = Image.open(file_name)
    vals = []
    for x in range(buf.height):
        for y in range(buf.width):
            for t in range(len(r)):
                r[t] = sqrt((x - xx[t]) ** 2 + (y - xx[t]) ** 2)
            vals.append(buf.getpixel((x, y)))
    print(len(vals))
    # rate = width ** 2
    # n = rate
    xf = rfft(vals)
    # yf = rfftfreq(n, 1 / rate)
    lambdas = np.zeros((len(vals)))
    amp = max(xf)
    print("Max amplitude = ", amp)
    for index in range(len(vals)):
        lambdas[index] = float(vals[index] / amp ** 2 / e)
    maxi = np.max(lambdas)
    mini = np.min(lambdas)
    lambdas = 255 * (lambdas - mini) / (maxi - mini)
    result = [[0 for _ in range(width)] for _ in range(width)]
    for i in range(width):
        for j in range(width):
            result[i][j] = int(str(lambdas[j * width + i]).split(".")[0])
    plt.imshow(result)
    plt.gray()
    plt.show()
    return result


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
                output.write(int.to_bytes(data[x][y], 1, byteorder="little"))
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
        decompress_file = decompress("_" + file + "_")
        if check(decompress_file, file):
            print("Поздравляю, распакованный файл соответствует оригиналу")
