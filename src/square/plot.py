import json

import matplotlib.pyplot as plt
from liner import create_raw, encode


file_name = "fb536381.txt"

moves = create_raw(file_name)
while True:
    raw = moves[:]
    moves = encode(moves)
    plt.plot(raw)
    plt.show()
    if max(moves) == 1 and max(raw) == 1:
        json_string = json.dumps(moves)
        with open(f"{file_name}.moves.json", mode="w") as f:
            f.write(json_string)
        json_string = json.dumps(raw)
        with open(f"{file_name}.raw.json", mode="w") as f:
            f.write(json_string)
        break
