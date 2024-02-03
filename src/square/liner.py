import json
import os.path
import random
import sys
import wave

import numpy as np
from PIL import Image

width = 256
file_name = "fb536381.txt"


def progress(message):
    sys.stdout.write("\r" + message)
    sys.stdout.flush()

def create_random(width):
    with open("random.raw", mode="wb") as f:
        for _ in range(width):
            for _ in range(width):
                f.write(random.randint(0, 255).to_bytes(1, byteorder="little"))


def create_raw(file_name):
    with open(file_name, mode="rb") as finput:
        with open(file_name  + ".raw", mode="wb") as foutput:
            buf = True
            count = 0
            while buf:
                buf = finput.read(1)
                if buf:
                    foutput.write(buf)
                count += 1
                if count == 256 ** 2:
                    break


def reorder(file_name):
    if os.path.exists(file_name + ".json"):
        with open(file_name + ".json", mode="r") as f:
            moves = json.load(f)
            return moves
    raw = []
    with open(file_name, mode="rb") as f:
        while True:
            buf = f.read(1)
            if buf:
                code = int.from_bytes(buf, "little")
                raw.append(code)
            else:
                break
    moves = []
    pos = 0
    for char in range(256):
        progress(f"{char + 1}/256")
        while char in raw[pos:]:
            count = 0
            while pos + count < len(raw):
                if raw[pos + count] == char:
                    break
                count += 1
            raw = raw[:pos] + raw[pos + count:] + raw[pos:pos + count]
            pos += 1
            moves.append(count)

    # print(moves)
    # print(raw)
    print(len(moves), min(moves), max(moves), sep=":")
    print(len(raw), min(raw), max(raw), sep=":")

    json_string = json.dumps(moves)
    with open(file_name + ".json", mode="w") as f:
        f.write(json_string)

    return moves


def create_wav(file_name):
    create_raw(file_name)
    data = reorder(file_name + ".raw")
    zero = 0
    result = zero.to_bytes(2, "little")
    for d in data:
        result += d.to_bytes(2, "little")
    with wave.open(file_name + ".raw" + ".wav", "wb") as out_f:
        out_f.setnchannels(1)
        out_f.setsampwidth(2)  # number of bytes
        out_f.setframerate(len(result))
        out_f.writeframesraw(result)

create_raw(file_name)
reorder(file_name + ".raw")
