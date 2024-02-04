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
    how = []
    for char in range(max(raw) + 1):
        progress(f"{char + 1}/{max(raw) + 1}")
        while char in raw[pos:]:
            # curr = pos + count
            count = 0
            while pos + count < len(raw):
                if raw[pos + count] == char:
                    break
                count += 1
            raw = raw[:pos] + raw[pos + count:] + raw[pos:pos + count]
            pos += 1
            moves.append(count)
        how.append([char, pos])
    print("")
    print(len(moves), min(moves), max(moves), sep=":")
    print(len(raw), min(raw), max(raw), sep=":")
    return how, moves, raw


def decode(result):
    counts = result[0][0]
    moves = result[0][1]
    raw = result[0][2]
    print(moves)

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
