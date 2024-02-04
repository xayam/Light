import json

import matplotlib.pyplot as plt
from liner import create_raw, encode


file_name = "random.txt"

moves = create_raw(file_name)
count = 0
while True:
    raw = moves[:]
    moves = encode(moves)
    # plt.plot(raw)
    # plt.show()
    count += 1
    if max(moves) == 1 and max(raw) == 1:
        json_string = json.dumps(moves)
        with open(f"{file_name}.moves.json", mode="w") as f:
            f.write(json_string)
        break
print(count)