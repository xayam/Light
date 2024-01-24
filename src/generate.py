import math
from PIL import Image
import cv2
import os

size = 9
width = 256
width2 = width * 2
values = []
image_folder = 'images'
video_name = 'video.avi'


def png2video():
    images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width1, layers = frame.shape

    video = cv2.VideoWriter(video_name, 0, 24, (width1, height))

    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))

    cv2.destroyAllWindows()
    video.release()


def compress():
    global values
    with open("fb536381.zip", mode="rb") as f:
        buffer = True
        values = [[]]
        y = 0
        x = 0
        while buffer and (y < width):
            buffer = f.read(1)
            if buffer:
                b = int.from_bytes(buffer, "little")
                values[-1].append({
                    "x": x,
                    "y": y,
                    "v": int(b)
                })
                x += 1
                if x == width:
                    values.append([])
                    x = 0
                    y += 1
    values = values[:-1]
    for t in range(0, 1):
        print(t)
        img = Image.new(mode="L", size=(width2, width2), color=0)
        for k in range(len(values)):
            for v in range(len(values[k])):
                gz = values[k][v]["v"]
                amp = gz * width2 / width / 2 ** 0.5 + 1
                phi = math.pi / width * k / 255
                time = t / 255
                x = amp * math.sin(math.pi * time + phi)
                x = (x - 1) / 2 + width2 / 2
                x = int(str(x).split(".")[0])
                y = amp * math.cos(math.pi * time + phi)
                y = (y - 1) / 2 + width2 / 2
                y = int(str(y).split(".")[0])
                img.putpixel((x, y), value=v)
        img.save(f"orig.png", format="PNG")
        # _{str(t+width2).rjust(4, '0')}


def decompress(file_name):
    buf = Image.open(file_name)
    vals = [["_" for _ in range(width)] for _ in range(width)]
    c = ""
    amps = []
    count = 0
    output = open("output.txt", mode="wb")
    for y in range(buf.height):
        for x in range(buf.width):
            v = buf.getpixel((x, y))
            assert v in range(width)
            if v == 0:
                count += 1

            yy = 2 * (y - buf.height / 2) + 1
            xx = 2 * (y - buf.width / 2) + 1

            amp = (xx ** 2 + yy ** 2) ** 0.5
            # print(xx, yy, amp, yy / amp, sep=":")
            phi = math.asin(yy / amp)

            gz = amp / width2 * width / 2 ** 0.5
            amps.append(gz)
            gz = int(str(gz).split(".")[0])
            assert gz in range(width)

            k = (phi + math.pi / 2) / math.pi * 255
            k = int(str(k).split(".")[0])
            assert k in range(width)
            if v > 0:
                buffer = int.to_bytes(gz, 1, byteorder="little")
                output.write(buffer)
                buffer = buffer.decode("windows-1251", errors="ignore")
                vals[k][v] = buffer

    output.close()

    assert len(set(amps)) == width

    for y in range(len(vals)):
        for x in range(len(vals[y])):
            c += vals[y][x]

    # pp = pprint.PrettyPrinter(width=64)
    # chnk_len = 64
    # result = [c[idx: idx + chnk_len] for idx in range(0, len(c), chnk_len)]
    # print(pp.pprint(result))

    print(count, len(amps), sep=":")


def check(file_name1, file_name2):
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


compress()
decompress("orig.png")
# check("_time.png", "orig.png")
# png2video()
