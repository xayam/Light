import os
from math import sin
from decode_matrix import decode_matrix
import numpy as np
from PIL import Image
from numpy import empty
from matplotlib import pyplot as plot
from config import *


def read_values(file_name):
    print(f"Reading file '{file_name}'")
    with open(file_name, mode="rb") as f:
        buffer = True
        values1 = [[]]
        y = 0
        s = ""
        L = 8 // int(math.log2(width))
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


# def write_values(file_name, vals):
#     for chunk in range(len(vals[:-1])):
#         img = Image.new(mode="L", size=(width, width), color=0)
#         for i in range(width):
#             for j in range(width):
#                 img.putpixel((i, j), value=vals[chunk][i][j])
#         img.save(f"images/{file_name}.{str(chunk).rjust(5, '0')}.light.png", format="PNG")
#     add_appendix("images/" + file_name, vals[-1])


def compress(file_name):
    print(f"Compress file '{file_name}'")
    vals = read_values(file_name)
    appendix = vals[-1]
    values = np.asarray(vals[:-1])
    buf = Image.new(mode="L", size=(width, width), color=0)
    for j in range(width):
        for i in range(width):
            value = values[0][i, j]
            buf.putpixel((i, j), value=int(value))
    buf.save(file_name + ".png", format="PNG")
    folder = "_" + file_name + "_"
    # assert not os.path.exists(folder)
    if not os.path.exists(folder):
        os.mkdir(folder)
    file_name2 = f"{folder}/{file_name}"
    minimum = 256
    maximum = 0
    print(len(values))
    for chunk in range(len(values)):
        img = Image.new(mode="L", size=(width, width), color=0)
        xi = empty([width, width], float)
        for time in range(1, 2):
            output_file = \
                f"{folder}/{str(chunk).rjust(5, '0')}.light.png"
            if os.path.exists(output_file):
                continue
            for j in range(width):
                # print(j)
                for i in range(width):
                    phi = 2 * math.pi / (values[chunk][i][j] + wavelength)
                    # k = j * width + i
                    xi[i, j] = sum(list(map(
                        lambda z: sin(2 * math.pi * z + phi), r)))
                    xi[i, j] = (xi[i, j] / width ** 2 + 1) * 128
                    if xi[i, j] > maximum:
                        maximum = xi[i, j]
                    if xi[i, j] < minimum:
                        minimum = xi[i, j]
                    # print(chunk, j, xi[i, j], sep=":")
                    img.putpixel((i, j), value=int(xi[i][j]))
            img.save(output_file, format="PNG")
        print(chunk)
        print(minimum, maximum, sep=":")
        break
    add_appendix(file_name2, appendix)
    return folder


def decompress(folder):
    print(f"Decompress folder '{folder}'")
    # assert os.path.exists(folder)
    chunks = [f for f in os.listdir(folder) if f.endswith(".light.png")]
    output_file = f"_uncompress_fb536381.txt"
    # # assert not os.path.exists(output_file)
    output = open(output_file, mode="wb")
    for c in chunks:
        print(c)
        buf1 = Image.open(folder + "/" + c)
        data = []
        for y in range(buf1.height):
            for x in range(buf1.width):
                buffer = buf1.getpixel((x, y))
                data.append(buffer)
        dm = decode_matrix(width)
        buf = Image.new(mode="L", size=(width, width), color=0)
        print(len(data))
        points = []

        for b in range(width):
            for a in range(0, len(data), width):
                index = a + b
                value = data[index] * dm[index]
                if value > 255:
                    value = 32
                # if round(value) > 255:
                #     value = 32
                print(index, a, b, data[index], dm[index], value, sep=":")
                buf.putpixel((b, a // width), value=round(value))
                # print(a, dm[a + b], round(value), sep=":")
                points.append(round(value))
                output.write(int.to_bytes(int(str(value).split(".")[0]), 1, byteorder="little"))
        # buf.save(folder + ".png", format="PNG")
        # print(max(points), min(points))
        # break
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
        if check(file, decompress_file):
            print("Check success!!!")
