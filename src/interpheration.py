import json
import os
from math import sin
from decode_matrix import decode_matrix
import numpy as np
from PIL import Image
from numpy import empty
from matplotlib import pyplot as plt
from scipy.fft import rfft, rfftfreq
from config import *


def read_values(file_name):
    print(f"Reading file '{file_name}'...")
    with open(file_name, mode="rb") as f:
        buffer = True
        values1 = [[]]
        y = 0
        s = ""
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
    return values1


def add_appendix(file_name, value):
    output_file = f"{file_name}.aaaaa.light"
    if not value:
        return
    print(f"Added appendix file '{output_file}'...")
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
    print(f"Compress file '{file_name}'...")
    file__name = file_name.replace("/", "__")
    vals = read_values(file_name)
    values = vals[:-1]
    appendix = vals[-1]
    if len(appendix) == width and len(appendix[-1]) == width:
        values = vals[:]
        appendix = False

    buf = Image.new(mode="L", size=(width, width), color=0)
    for j in range(width):
        for i in range(width):
            value = values[0][i][j]
            buf.putpixel((i, j), value=int(value))
    buf.save(file__name + ".png", format="PNG")
    folder = "_" + file__name + "_"
    # assert not os.path.exists(folder)
    if not os.path.exists(folder):
        os.mkdir(folder)
    # file_name2 = f"{folder}/{file_name}"
    for chunk in range(len(values)):
        img = Image.new(mode="L", size=(width, width), color=0)
        xi = empty([width, width], float)
        for time in range(1, 2):
            output_file = \
                f"{folder}/{str(chunk).rjust(5, '0')}.png.light"
            if os.path.exists(output_file):
                continue
            for j in range(width):
                progress(f"CHUNK={chunk + 1}/{len(values)}:J={j + 1}/{width}")
                for i in range(width):
                    phi = 2 * math.pi / (values[chunk][i][j] + wavelength)
                    # k = j * width + i
                    xi[i, j] = sum(list(map(
                        lambda z: sin(2 * math.pi * z + phi), r)))
                    xi[i, j] = (xi[i, j] / width ** 2 + 1) * 128
                    img.putpixel((i, j), value=int(xi[i][j]))
            img.save(output_file, format="PNG")
        break
    print("")
    # add_appendix(file_name2, appendix)
    return folder


def get_data(file_name):
    buf1 = Image.open(file_name)
    data = []
    for y in range(buf1.height):
        for x in range(buf1.width):
            buffer = buf1.getpixel((x, y))
            data.append(buffer)
    rate = len(data)
    n = rate
    yf = rfft(data)
    xf = rfftfreq(n, 1 / rate)
    return yf


def decompress(folder):
    print(f"Decompress folder '{folder}'...")
    # assert os.path.exists(folder)
    chunks = [f for f in os.listdir(folder) if f.endswith(".png.light")]
    output_file = f"decompress{folder[:-1]}"
    # # assert not os.path.exists(output_file)
    output = open(output_file, mode="wb")
    for c in range(len(chunks)):
        progress(f"CHUNK={c + 1}/{len(chunks)}")
        yf1 = get_data(folder + "/" + chunks[c])
        yf2 = get_data(folder[1:-1] + ".png")
        print("")
        return output_file, yf1, yf2
        # return output_file, xf[1:width], yf[1:width], \
        #     xf[width:width ** 2 // 2 + 1:width // 2], \
        #     yf[width:width ** 2 // 2 + 1:width // 2]

        dm = decode_matrix(width)
        buf = Image.new(mode="L", size=(width, width), color=0)
        x = []
        y = []
        for b in range(width):
            for a in range(width):
                # index1 = a + b * width
                # index2 = a * width + b
                # if b == width - 1 and a == b:
                #     value1 = 0
                # elif b > 0 and a == width - 1:
                #     value1 = (index1 / width) * (index1 % width) / width
                # else:
                #     value1 = ((index1 + 1) / width) * ((index1 + 1) % width) / (a + 1)
                # value1 = int(str(value1).split(".")[0])
                #
                # if a == width - 1 and b == width - 1:
                #     value2 = 255
                # elif a > 0 and b == width - 1:
                #     value2 = (index2 / width) * (index2 % width) / width
                # else:
                #     value2 = ((index2 + 1) / width) * ((index2 + 1) % width) / (b + 1)
                #
                # value1 = int(str(value1).split(".")[0])
                # value2 = int(str(value2).split(".")[0])
                # value = int(str(value2).split(".")[0])
                index = a + b * width
                value = data[index] * dm[index]
                x.append(value)
                # x.append(data[value1 * width + value2])
                # y.append(value2)
                # print(value1, value2, sep=":")
                # result.append({"value": value})
                # buf.putpixel((b, a // width), value=round(value))
                # output.write(int.to_bytes(value, 1, byteorder="little"))
        # plt.plot(x)
        # plt.show()
        break
        # buf.save(folder + ".png", format="PNG")
    print("")
    output.close()
    return output_file


def check(file_name1, file_name2):
    print(f"Checking files '{file_name1}' and '{file_name2}'...")
    fsize1 = os.path.getsize(file_name1)
    fsize2 = os.path.getsize(file_name2)
    if fsize1 != fsize2:
        return False
    with open(file_name1, mode="rb") as f1:
        with open(file_name2, mode="rb") as f2:
            b1 = True
            b2 = True
            count = 0
            while b1 and b2:
                b1 = f1.read(1)
                if b1:
                    b2 = f2.read(1)
                    if b2:
                        c1 = int.from_bytes(b1, byteorder="little")
                        c2 = int.from_bytes(b2, byteorder="little")
                        count += 1
                        progress(f"{count}/{fsize1}")
                        if c1 != c2:
                            return False
    return True


if __name__ == "__main__":

    decompress_files = []
    result = []

    for file in files:
        compress_folder = compress(file)
        decompress_file = decompress(compress_folder)
        decompress_files.append([file, decompress_file])

    for file in decompress_files:
        output_file = file[1][0] + ".json"
        # print(output_file)
        yf1 = np.asarray(file[1][1], dtype=np.complex_)
        yf2 = np.asarray(file[1][2], dtype=np.complex_)

        # xf = xf1 / xf2
        # yf = yf1 / yf2
        # print(xf1[0], xf1[-1], yf2[0], yf2[-1], sep=":")
        # print(xf[0], xf[-1], yf[0], yf[-1], sep=":")
        # print(len(xf), len(yf))
        # count1, count2  = 0, 0
        # for i in range(len(yf)):
        #     if not np.isnan(xf[i].real):
        #         count1 += 1
        #         # print(i)
        #     if not np.isnan(yf[i].real):
        #         count2 += 1
        #         # print(i)
        # print(count1, count2, sep=":")
        # sys.exit()
        x2 = []
        y2 = []
        yf = yf1[:]
        for i in range(len(yf)):
            x2.append(yf[i].real)
            y2.append(yf[i].imag)
        x2 = np.asarray(x2)
        y2 = np.asarray(y2)

        x4 = []
        y4 = []
        yf = yf2[:]
        for i in range(len(yf)):
            x4.append(yf[i].real)
            y4.append(yf[i].imag)
        x4 = np.asarray(x4)
        y4 = np.asarray(y4)
        x = x4 - x2
        y = y4 - x2
        plt.plot(x, y)
        plt.show()
        print(x)
        print(y)
        json_string = json.dumps([x.tolist(), y.tolist()])
        result.append(json_string)
        print("len result json_string =", len(json_string), "bytes")

    for r in result[1:]:
        assert result[0] == r
    print("TRUE tests complete!!!")
    # for file in decompress_files:
    #     if check(file[0], file[1]):
    #         print("\nOK, check success.")
    #     else:
    #         raise Exception("\nSORRY, check files is failed.")
