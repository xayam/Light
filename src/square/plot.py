import json
import os.path

import matplotlib.pyplot as plt
from liner import create_raw, encode, decode


file_name = "fb536381.zip"

if os.path.exists(f"{file_name}.result.json"):
    with open(f"{file_name}.result.json", mode="r") as f:
        result = json.load(f)
        raw = result[-1][0]
        for r in range(len(result) - 1, -1, -1):
            moves = result[r][1]
            raw = decode(raw, moves)
        assert raw == create_raw(file_name)

        moves = result[-1][0]
        print(moves)
        for r in range(len(result) - 1, -1, -1):
            raw = result[r][1]
            moves = decode(moves, raw)
            break
        print(raw)
        print(moves)
else:
    result = []
    count = 0
    raw = create_raw(file_name)
    first = raw[:]
    print(first)
    while True:
        raw, moves = encode(raw)
        # plt.plot(raw)
        # plt.show()
        count += 1
        print(count)
        result.append([raw, moves])
        if max(moves) == 1 and max(raw) == 1:
        # if moves == raw:
            break
    json_string = json.dumps(result)
    with open(f"{file_name}.result.json", mode="w") as f:
        f.write(json_string)
