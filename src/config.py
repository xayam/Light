import math
import sys

files = [
    # "video1.zip",
    "fb536381.txt",
    # "fb536381.zip",
]

separation = 1.0
side = 16.0
wavelength = 1.
width = int(side)
spacing = side / width

assert width in [16, 256]

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
