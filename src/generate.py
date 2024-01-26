import math
import pprint
from PIL import Image
import cv2
import os

size = 9
width = 256
width2 = width
image_folder = 'images'
video_name = 'video.avi'
files = [
    # "video1.zip",
    "fb536381.txt",
    # "fb536381.zip",
]
pp = pprint.PrettyPrinter(width=64)


def png2video():
    images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width1, layers = frame.shape

    video = cv2.VideoWriter(video_name, 0, 24, (width1, height))

    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))

    cv2.destroyAllWindows()
    video.release()


def add_appendix(file_name, value):
    output_file = f"{file_name}.aaaaa.light"
    print(f"Added appendix file '{output_file}'")
    if value:
        with open(output_file, mode="wb") as f:
            for y in range(len(value)):
                for x in range(len(value[y])):
                    buf = int.to_bytes(value[y][x]["v"], length=1, byteorder="little")
                    f.write(buf)


def decode(file_name):
    vals = [[int.to_bytes(32, 1, byteorder="little")
             for _ in range(width)] for _ in range(width)]
    amps = []
    count = 0
    buf = Image.open(file_name)
    for y in range(buf.height):
        for x in range(buf.width):
            d = buf.getpixel((x, y))
            assert d in range(width)

            yy = 2 * (y - buf.height / 2)
            xx = 2 * (y - buf.width / 2)
            amp = (xx ** 2 + yy ** 2) ** 0.5
            # print(xx, yy, amp, yy / amp, sep=":")
            phi = math.atan2(yy, xx)
            # phi = 2 * math.pi * k / 255 - math.pi + 2 * math.pi / 255 / 255 * amp
            # k = (phi + math.pi) / 2 / math.pi * 255
            phi = d / 127
            # distance = (k ** 2 + v ** 2) ** 0.5 / 2 ** 0.5 * 2
            # phi = distance / 127
            # amp = gz * width2 / width / phi
            # phi = (phi * amp * 2 - 1) * math.pi
            phi = (phi * amp * 2 - 1) * math.pi
            k = 0
            # k = abs(k)
            # print(k)
            k = int(str(k).split(".")[0])
            # assert k in range(width)


            gz = amp * width / width2
            gz = int(str(gz).split(".")[0])

            try:
                assert gz in range(width)
                count += 1
                amps.append({"gz": gz, "x": x, "y": y, "v": 0, "k": 0})
            except AssertionError:
                amps.append({"gz": 0, "x": x, "y": y, "k": 0, "v": 0})
            # print(gz)
    print(count)
    # amps = [{'index': index, 'data': data} for index, data in enumerate(amps)]
    # amps.sort(key=lambda item:
    #           (item["data"]["gz"], item["data"]["k"], item["data"]["v"]))
    # print(len(amps), sep=":")
    # index = 0
    # result = [amps[index]]
    # for i in range(1, len(amps)):
    #     if amps[i]["data"]["k"] == amps[index]["data"]["k"] and \
    #             amps[i]["data"]["v"] == amps[index]["data"]["v"] and \
    #             amps[i]["data"]["gz"] == amps[index]["data"]["gz"]:
    #         pass
    #     else:
    #         result.append(amps[i])
    #         index = i
    # print(len(result), sep=":")
    # res = [{'gz': 0, 'k': 0, 'v': 0, 'd': 0} for _ in range(width2 ** 2)]
    # for r in result:
    #     res[r["index"]]["gz"] = r["data"]["gz"]
    #     res[r["index"]]["k"] = r["data"]["k"]
    #     # res[r["index"]]["d"] = r["data"]["d"]
    #     res[r["index"]]["v"] = r["data"]["v"]
    # for y in range(len(vals)):
    #     for x in range(len(vals[y])):
    #         xx = int(str(x * width2 / width).split(".")[0])
    #         yy = int(str(y * width2 / width).split(".")[0])
    #         a = y * width + x
    for a in range(len(amps)):
            x = amps[a]["x"] * width // width2
            y = amps[a]["y"] * width // width2
            k = amps[a]["k"]
            v = amps[a]["v"]
            gz = int.to_bytes(amps[a]["gz"], 1, byteorder="little")
            vals[k][v] = gz
    return vals


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

    for c in range(len(values)):
        count = 0
        img = Image.new(mode="L", size=(width2, width2), color=255)
        for k in range(len(values[c])):
            for v in range(len(values[c][k])):
                gz = values[c][k][v]["v"]
                distance = (k ** 2 + v ** 2) ** 0.5 / 2 ** 0.5 * 2
                phi = distance / 127 + 1
                amp = gz * width2 / width / phi
                phi = (phi * amp * 2 - 1) * math.pi
                time = 0 / 255
                x = amp * math.sin(math.pi * time + phi) # + v
                x = (x - 1) / 2 + width2 / 2
                x = int(str(x).split(".")[0])
                y = amp * math.cos(math.pi * time + phi) # + k
                y = (y - 1) / 2 + width2 / 2
                y = int(str(y).split(".")[0])
                img.putpixel((x, y), value=int(distance))
        print(count)
        output_file = f"{file_name2}.{str(c).rjust(5, '0')}.light.png"
        img.save(output_file, format="PNG")
        break
    add_appendix(file_name2, appendix)
    return folder


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
        break
        # if check(decompress_file, file):
        #     print("Поздравляю, распакованный файл соответствует оригиналу")
    # png2video()
