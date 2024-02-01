import json

from interpheration import compress, decompress, check


files = [
    "data/256.1.cp",
    "data/256.2.cp"
]


if __name__ == "__main__":

    decompress_files = []

    for file in files:
        compress_folder = compress(file)
        decompress_file = decompress(compress_folder)
        decompress_files.append([file, decompress_file])

    if not check(decompress_files[0][0], decompress_files[0][1]) or \
          not check(decompress_files[1][0], decompress_files[1][1]):
        raise Exception("\nSORRY, codepages check files is failed.")

    print("TRUE tests complete!!!")
