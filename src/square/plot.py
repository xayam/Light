from liner import create_raw, encode

file_name = "fb536381.txt"

create_raw(file_name)
for i in range(16):
    print(i)
    encode(file_name + ".raw", num=i)
