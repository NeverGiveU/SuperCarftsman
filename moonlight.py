# -*- coding:utf-8 -*-

import numpy as np
import itertools
from PIL import Image

def commbinations(arr, length, length_rest, start, line, commbination):
    if len(arr) == 0:
        commbination.append(line)
    else:
        min_width = arr.sum() + len(arr) - 1
        for i in range(start, start+length_rest-min_width+1):
            line_ = line.copy()
            line_[i:i+arr[0]] = True
            start = i+arr[0]+1
            length_rest = length-start
            commbinations(arr[1:], length, length_rest, start, line_, commbination)

def check(matrix, hor):
    length = matrix.shape[0]
    for col_num in range(length):
        col = matrix[:, col_num]
        count = 0
        flag = 0
        for i in range(length):
            if col[i] > 0:
                count += 1
            else:
                pass
            if count > 0:
                if (i < length-1 and col[i+1] == 0) or i == length-1:
                    if flag >= len(hor[col_num]):
                        return False
                    else:
                        if hor[col_num][flag] == count:
                            count = 0
                            flag += 1
                        else:
                            return False
    return True
def genC(C, length):
    cs = C[0]
    for i in range(1, length):
        print("Getting Dicar of {}".format(i))
        Res = itertools.product(cs, C[i])
        cs = []
        for res in Res:
            res_ = []
            for j in range(len(res)):
                if type(res[j]) == tuple:
                    res_ += list(res[j])
                else:
                    res_.append(res[j])
            cs.append(tuple(res_))
    for i in range(len(cs)):
        temp = cs[i]
        temp_ = []
        for j in range(len(temp)):
            if type(temp[j]) == tuple:
                temp_ += list(temp[j])
            else:
                temp_.append(temp[j])
        cs[i] = temp_
    return cs

def moon_light():
    ver_len = []
    hor_len = []
    length = int(input("Input the size of moon light: "))
    matrix = []
    line = [False]*length
    for i in range(length):
        matrix.append(line)
    matrix = np.array(matrix)
    print("The connections along vertical directions:")
    for L in range(length):
        num = input('\t>> ')
        conn = num.split(" ")
        for i in range(len(conn)):
            conn[i] = int(conn[i])
        ver_len.append(conn)
    print("The connections along horizontal directions:")
    for L in range(length):
        num = input('\t>> ')
        conn = num.split(" ")
        for i in range(len(conn)):
            conn[i] = int(conn[i])
        hor_len.append(conn)
    COMMBINATION = []
    for L in range(length):
        print("Get combination of line: {}".format(L))
        commbination = []
        line = np.array([False]*length)
        arr = np.array(ver_len[L])
        commbinations(arr, length, length, 0, line, commbination)
        COMMBINATION.append(commbination)
    C = []
    print("Finished computing the combinations")
    for i in range(length):
        l = len(COMMBINATION[i])
        C.append([j for j in range(l)])
    cs = genC(C, length)
    print("Finished geting the combinations")
    for _cs_ in cs:
        matrix = []
        for line_num in range(length):
            matrix.append(COMMBINATION[line_num][_cs_[line_num]])
        matrix = np.array(matrix)
        matrix = matrix.astype(np.uint8)
        if check(matrix, hor_len) == True:
            matrix = matrix.repeat(100, axis=0)
            matrix = matrix.repeat(100, axis=1)
            Image.fromarray(matrix*255).convert('L').show()
            break
    
if __name__ == '__main__':
    moon_light()
