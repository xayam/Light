import random

import numpy as np
from PIL import Image


width = 256
file_name = "fb536381.zip.png"

def create_random(width):
    image = Image.new(mode="L", size=(width, width), color=0)
    for j in range(width):
        for i in range(width):
            image.putpixel((i, j), value=random.randint(0, 255))
    image.save(file_name, format="PNG")


def reorder(file_name):
    image = Image.open(file_name)
    moves = []
    colors = [[] for _ in range(width)]
    for j in range(width):
        for i in range(width):
            value = image.getpixel((i, j))
            colors[j].append(value)
    char = image.getpixel((0, 0))
    for i in range(1, width):
        for j in range(i, width):
            char2 = image.getpixel((i, j - 1))
            if char == char2:
                break
            value = image.getpixel((i, j))
            if value != char:
                pass

            print(j, len(set(colors[j])), sep=":")


reorder(file_name)
