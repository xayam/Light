import os
from math import sqrt, sin, pi

from PIL import Image
from numpy import empty
from pylab import imshow, gray, show

files = [
    # "video1.zip",
    "fb536381.txt",
    # "fb536381.zip",
]

xi0 = 1.0
separation = 1.0  # Separation of centers in cm
side = 256.0  # Side of the square in cm
width = int(side)
spacing = side / width  # Spacing of points in cm


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
                values1[-1][-1].append({
                    "x": x,
                    "y": y,
                    "v": int(b)
                })
                x += 1
                if x == width:
                    values1[-1].append([])
                    x = 0
                    y += 1
                if y == width:
                    x = 0
                    y = 0
                    values1.append([[]])
    return values1


def add_appendix(file_name, value):
    output_file = f"{file_name}.aaaaa.light"
    print(f"Added appendix file '{output_file}'")
    if value:
        with open(output_file, mode="wb") as f:
            for y in range(len(value)):
                for x in range(len(value[y])):
                    buf = int.to_bytes(value[y][x]["v"], length=1, byteorder="little")
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
    folder = "_" + file_name + "_"
    # assert not os.path.exists(folder)
    if not os.path.exists(folder):
        os.mkdir(folder)
    file_name2 = f"{folder}/{file_name}"
    x = [i for i in range(width)]
    x = list(map(lambda i: i + separation / 2, x))
    y = x[:]
    r = [0. for _ in range(width)]
    for c in range(len(values)):
        count = 0
        img = Image.new(mode="L", size=(width, width), color=255)
        xi = empty([width, width], float)
        for i in range(width):
            yy = spacing * i
            for j in range(width):
                wavelength = values[c][i][j]["v"] + 1
                k = 2 * pi / wavelength
                xx = spacing * j
                for t in range(len(r)):
                    r[t] = sqrt((xx - x[t]) ** 2 + (yy - y[t]) ** 2)
                xi[i, j] = sum(list(map(lambda z: xi0 * sin(k * z), r)))
                img.putpixel((i, j), value=int(xi[i, j]))
        imshow(xi, origin="lower", extent=[0, side, 0, side])
        gray()
        show()
        output_file = f"{file_name2}.{str(c).rjust(5, '0')}.light.png"
        img.save(output_file, format="PNG")
        break
    add_appendix(file_name2, appendix)
    return folder


def decode(file_name):
    vals = [[int.to_bytes(32, 1, byteorder="little")
             for _ in range(width)] for _ in range(width)]
    buf = Image.open(file_name)
    for y in range(buf.height):
        for x in range(buf.width):
            pass

    return vals


def decompress(folder):
    print(f"Decompress folder '{folder}'")
    assert os.path.exists(folder)
    lists = [f for f in os.listdir(folder) if f.endswith(".light.png")]
    output_file = f"uncompress_{folder[1:-1]}"
    # assert not os.path.exists(output_file)
    output = open(output_file, mode="wb")
    for f in lists:
        print(f)
        data = decode(folder + "/" + f)
        for y in range(len(data)):
            for x in range(len(data[y])):
                output.write(data[y][x])
    output.close()
    return output_file


if __name__ == "__main__":
    for file in files:
        compress_folder = compress(file)
        # decompress_file = decompress(compress_folder)
        break
        # if check(decompress_file, file):
        #     print("Поздравляю, распакованный файл соответствует оригиналу")
