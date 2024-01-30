import pprint

width = 256
files = [
    # "video1.zip",
    # "fb536381.txt",
    "fb536381.zip",
]


def read_values(file_name):
    print(f"Reading file '{file_name}'")
    with open(file_name, mode="rb") as f:
        buffer = True
        values = [[]]
        y = 0
        x = 0
        s = ""
        while buffer:
            buffer = f.read(1)
            if buffer:
                b = int.from_bytes(buffer, "little")
                s += f"{b:08b}".rjust(8, "0")
                x += 1
                if len(s) == width:
                    split = [int(i) for i in list(s)]
                    values[-1].append(split)
                    s = ""
                    x = 0
                    y += 1
                if y == width:
                    x = 0
                    y = 0
                    values.append([])
    values.append([s])
    return values


def get_circles(values):
    n = width
    mat = [[0] * n for _ in range(n)]
    st, m = 1, 0
    mat[n // 2][n // 2] = n * n
    r = 0
    r1 = []
    r0 = []
    for v in range(n // 2):
        # Заполнение верхней горизонтальной матрицы
        for i in range(n - m):
            val = int(values[v][i + v])
            if r % 2 == 0:
                r1.append({"y": v, "x": i + v, "d": val})
            else:
                r0.append({"y": v, "x": i + v, "d": val})
            mat[v][i + v] = val
            st += 1
            # i+=1
        # Заполнение правой вертикальной матрицы
        for i in range(v + 1, n - v):
            val = int(values[i][- v - 1])
            if r % 2 == 0:
                r1.append({"y": i, "x": - v - 1, "d": val})
            else:
                r0.append({"y": i, "x": - v - 1, "d": val})
            mat[i][- v - 1] = val
            st += 1
            # i+=1
        # Заполнение нижней горизонтальной матрицы
        for i in range(v + 1, n - v):
            val = int(values[- v - 1][- i - 1])
            if r % 2 == 0:
                r1.append({"y": - v - 1, "x": - i - 1, "d": val})
            else:
                r0.append({"y": - v - 1, "x": - i - 1, "d": val})
            mat[-v - 1][- i - 1] = val
            st += 1
            # i+=1
        # Заполнение левой вертикальной матрицы
        for i in range(v + 1, n - (v + 1)):
            val = int(values[- i - 1][v])
            if r % 2 == 0:
                r1.append({"y": - i - 1, "x": v, "d": val})
            else:
                r0.append({"y": - i - 1, "x": v, "d": val})
            mat[-i - 1][v] = val
            st += 1
            # i+=1
        # v+=1
        m += 2
        r += 1
    # Вывод результата на экран
    # for i in mat:
    #     print(*i)
    return r1, r0


def sort_circles(r1, r0):
    changes = []
    x1 = 0
    # r = r1 + r0
    x0 = 0
    while x0 < len(r0):
        if r0[x0]["d"] == 1:
            while (x1 < len(r1)) and (r1[x1]["d"] != 0):
                x1 += 1
            if x1 == len(r1):
                break
            r1[x1]["d"], r0[x0]["d"] = r0[x0]["d"], r1[x1]["d"]
            changes.append([r1[x1], r0[x0]])
            x1 += 1
        x0 += 1
    return changes


def make_moves(data, changes):
    for c in changes:
        b = data[c[0]["y"]][c[0]["x"]]
        data[c[0]["y"]][c[0]["x"]], data[c[1]["y"]][c[1]["x"]] = \
            data[c[1]["y"]][c[1]["x"]], data[c[0]["y"]][c[0]["x"]]
        data[c[1]["y"]][c[1]["x"]] = b
    return data


if __name__ == "__main__":
    for file in files:
        data = read_values(file)
        ring1, ring0 = get_circles(data[0])
        # pprint.pprint(data[0])
        moves = sort_circles(ring1, ring0)
        print(len(moves))
        result = make_moves(data[0], moves)
        # pprint.pprint(result)
        break
