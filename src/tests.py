from interpheration import compress, decompress, check


files = [
    "256.1.cp",
    "256.2.cp"
]


if __name__ == "__main__":

    decompress_files = []

    for file in files:
        compress_folder = compress(file)
        decompress_file = decompress(compress_folder)
        decompress_files.append([file, decompress_file])

        if check(decompress_files[0][0], decompress_files[0][1]) and \
                check(decompress_files[1][0], decompress_files[1][1]):
            print("\nOK, codepages check success.")
        else:
            raise Exception("\nSORRY, codepages check files is failed.")