from tqdm import trange
import os

ErrRate = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
       31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50]

str0 = ""
for i in ErrRate:
    str0 += str(i/500) + ","
str0 += "\n"
file_handle = open('GroupRate_Recall.txt', mode='a')
file_handle.write(str0)
file_handle.close()
for i in trange(10):
    for errrate in ErrRate:
        str1 = "python test.py" + " 1" + " " + str(errrate*2)
        os.system(str1)
    file_handle = open('GroupRate_Recall.txt', mode='a')
    file_handle.write("\n")
    file_handle.close()
