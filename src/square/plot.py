import json
import os.path

import matplotlib.pyplot as plt
from liner import create_raw, encode, decode


file_name = "fb536381.txt"

if os.path.exists(f"{file_name}.result.json"):
    with open(f"{file_name}.result.json", mode="r") as f:
        result = json.load(f)
        decode(result)
else:
    result = []
    count = 0
    moves = create_raw(file_name)
    while True:
        raw = moves[:]
        how, moves = encode(moves)
        # plt.plot(raw)
        # plt.show()
        count += 1
        print(count)
        result.append([how, moves, raw])
        if max(moves) == 1 and max(raw) == 1:
            break
    json_string = json.dumps(result)
    with open(f"{file_name}.result.json", mode="w") as f:
        f.write(json_string)
