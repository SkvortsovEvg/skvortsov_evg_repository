import os
import re
from pprint import pprint


def read_text_file(file_path):
    with open(file_path, encoding="utf-8", mode="r") as sf:
        data = sf.read()
    return data.split('\n')


def open_setting_texts():
    path = f"{os.getcwd()}\\txt"
    os.chdir(path)

    output_list = []
    for file in os.listdir():
        if file.endswith(".txt"):
            file_path = f"{path}\{file}"
            tmp_list = read_text_file(file_path)
            output_list.append(tmp_list.copy())
            tmp_list.clear()
    return output_list


input_list = open_setting_texts()

output_list = []
tmp_list = []
for item in range(len(input_list[0])):
    line = re.split("\t", input_list[0][item])
    tmp_list = [line[0][1:3].upper()]
    tmp_list.append(line[1].strip())
    output_list.append(tmp_list.copy())

path = f"{os.getcwd()}\\domen_output_001.txt"

with open(path, encoding="utf-8" 'w+') as f:
    for item in output_list:
        s = " ".join(map(str, item))
        f.write(s + '\n')
    print("File written successfully")
f.close()

with open(path, encoding='utf-8', mode="r") as sf:
    data = sf.read()
    output_list = data.split('\n')
print(output_list)

# path = f"{os.getcwd()}\\txt\\domen.txt"
# with open(path) as sf:
#     data = sf.read()
#
# file = data.split('\n')
# print(file)

# def Coding(M, Key, Name_file):
#     f = open(Name_file, "r")
#     list = f.readlines()
#     mydict = {}
#     for i in range(len(list)):
#         mydict[list[i][0]] = int(list[i][(list[i].find("-") + 1):list[i].find('\\')])
#     print(mydict)
#
#     f.close()
