import math

files = [
    # "video1.zip",
    "fb536381.txt",
    # "__fb536381.zip_.7z_.7z",
    # "fb536381.zip",
]

xi0 = 1.0
separation = 1.0
side = 256.0
wavelength = 1.
width = int(side)
spacing = side / width

assert width in [4, 16, 256]

x = [(i % width) + separation / 2 for i in range(width ** 2)]
y = x[:]
r = [0. for _ in range(width ** 2)]
for i in range(width):
    for j in range(width):
        r[j * width + i] = \
            math.sqrt((i - x[j * width + i]) ** 2 + \
                 (j - y[j * width + i]) ** 2)