import math
import sys

files = [
    # "video1.zip",
    "256.1.cp",
    "256.2.cp",
    # "fb637407.txt",
    # "fb536381.txt",
    # "fb536381.zip",
    # "fb536381_2.zip",
    # "two/032_192.two.cp",
    # "two/000_255.two.cp",
    # "two/000_032.two.cp",
    # "ones/000.ones.cp",
    # "ones/255.ones.cp",
]

separation = 1.0
side = 256.0
wavelength = 1.
width = int(side)
spacing = side / width

assert width == 256

x = [(i % width) + separation / 2 for i in range(width ** 2)]
y = x[:]
r = [0. for _ in range(width ** 2)]
for i in range(width):
    for j in range(width):
        r[j * width + i] = \
            math.sqrt((i - x[j * width + i]) ** 2 +
                      (j - y[j * width + i]) ** 2)


def progress(message):
    sys.stdout.write("\r" + message)
    sys.stdout.flush()
