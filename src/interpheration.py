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
    print(f"Added appendix file '{output_file}'...")
    if not value:
        return
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
    vals = read_values(file_name)
    values = vals[:-1]
    appendix = vals[-1]
    if len(appendix) == width and len(appendix[-1]) == width:
        values = vals[:]
        appendix = False

    # buf = Image.new(mode="L", size=(width, width), color=0)
    # for j in range(width):
    #     for i in range(width):
    #         value = values[0][i, j]
    #         buf.putpixel((i, j), value=int(value))
    # buf.save(file_name + ".png", format="PNG")
    folder = "_" + file_name + "_"
    # assert not os.path.exists(folder)
    if not os.path.exists(folder):
        os.mkdir(folder)
    file_name2 = f"{folder}/{file_name}"
    for chunk in range(len(values)):
        img = Image.new(mode="L", size=(width, width), color=0)
        xi = empty([width, width], float)
        for time in range(1, 2):
            output_file = \
                f"{folder}/{str(chunk).rjust(5, '0')}.png.light"
            if os.path.exists(output_file):
                continue
            for j in range(width):
                progress(f"CHUNK={chunk + 1}/{len(values)}:J={j}/{width}")
                for i in range(width):
                    phi = 2 * math.pi / (values[chunk][i][j] + wavelength)
                    # k = j * width + i
                    xi[i, j] = sum(list(map(
                        lambda z: sin(2 * math.pi * z + phi), r)))
                    xi[i, j] = (xi[i, j] / width ** 2 + 1) * 128
                    img.putpixel((i, j), value=int(xi[i][j]))
            img.save(output_file, format="PNG")
    add_appendix(file_name2, appendix)
    return folder


def decompress(folder):
    print(f"Decompress folder '{folder}'...")
    # assert os.path.exists(folder)
    chunks = [f for f in os.listdir(folder) if f.endswith(".png.light")]
    output_file = f"decompress{folder[:-1]}"
    # # assert not os.path.exists(output_file)
    output = open(output_file, mode="wb")
    for c in range(len(chunks)):
        progress(f"CHUNK={c + 1}/{len(chunks)}")
        buf1 = Image.open(folder + "/" + chunks[c])
        data = []
        for y in range(buf1.height):
            for x in range(buf1.width):
                buffer = buf1.getpixel((x, y))
                data.append(buffer)
        rate = len(data)
        n = rate
        yf = np.abs(rfft(data))
        xf = rfftfreq(n, 1 / rate)
        # plt.plot(xf[:])
        # plt.show()
        # sys.exit()

        dm = decode_matrix(width)
        buf = Image.new(mode="L", size=(width, width), color=0)
        result = []
        for b in range(width):
            for a in range(width):
                index = a + b * width
                # value = xf[data[index] * width // 2] / (a + 1)
                value = (index / width) * (index % width) / (b + 1)
                value = int(str(value).split(".")[0])
                result.append(value)
                    # buf.putpixel((b, a // width), value=round(value))
                output.write(int.to_bytes(value, 1, byteorder="little"))
        plt.plot(result)
        plt.show()
        # buf.save(folder + ".png", format="PNG")
    output.close()
    return output_file


def check(file_name1, file_name2):
    print("")
    print(f"Checking files '{file_name1}' and '{file_name2}'...")
    print("")
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
    for file in files:
        compress_folder = compress(file)
        decompress_file = decompress(compress_folder)
        if check(file, decompress_file):
            print("Ok, check success.")
        else:
            print("Sorry, check files is failed.")
