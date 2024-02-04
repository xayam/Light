import json
import os.path
import random
import sys
import wave

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

width = 256
file_name = "fb536381.txt"


def progress(message):
    sys.stdout.write("\r" + message)
    sys.stdout.flush()


def create_random(width):
    with open("random.txt", mode="wb") as f:
        for _ in range(width):
            for _ in range(width):
                f.write(random.randint(0, 255).to_bytes(1, byteorder="little"))


def create_raw(file_name):
    moves = []
    with open(file_name, mode="rb") as finput:
        buf = True
        count = 0
        while buf:
            buf = finput.read(1)
            if buf:
                moves.append(int.from_bytes(buf, "little"))
            count += 1
            if count == 256 ** 2:
                break
    return moves

def encode(raw):
    moves = []
    pos = 0
    count = 0
    for char in range(len(raw)):
        progress(f"{char + 1}/{len(raw)}")
        while char in raw[pos:]:
            curr = pos + count
            count = 0
            while curr + count < len(raw):
                if raw[curr + count] == char:
                    break
                count += 1
            # raw = raw[:pos] + raw[pos + count:] + raw[pos:pos + count]
            pos += 1
            moves.append(count)
    print("")
    print(len(moves), min(moves), max(moves), sep=":")
    print(len(raw), min(raw), max(raw), sep=":")
    return moves

# def create_wav(file_name):
#     create_raw(file_name)
#     data = reorder(file_name + ".raw")
#     zero = 0
#     result = zero.to_bytes(2, "little")
#     for d in data:
#         result += d.to_bytes(2, "little")
#     with wave.open(file_name + ".raw" + ".wav", "wb") as out_f:
#         out_f.setnchannels(1)
#         out_f.setsampwidth(2)  # number of bytes
#         out_f.setframerate(len(result))
#         out_f.writeframesraw(result)
