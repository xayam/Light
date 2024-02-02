import math
import sys

import numpy as np

files = [
    "data/video1.zip",
    "data/256.1.cp",
    "data/256.2.cp",
    # "data/fb637407.txt",
    # "data/fb536381.txt",
    # "data/fb536381.zip",
    # "data/fb536381_2.zip",
    # "data/two/032_192.two.cp",
    # "data/two/000_255.two.cp",
    # "data/two/000_032.two.cp",
    # "data/ones/000.ones.cp",
    # "data/ones/255.ones.cp",
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
            math.sin(2 * math.pi * \
                     math.sqrt((i - x[j * width + i]) ** 2 +
                               (j - y[j * width + i]) ** 2))
r = np.asarray(r)


def progress(message):
    sys.stdout.write("\r" + message)
    sys.stdout.flush()
