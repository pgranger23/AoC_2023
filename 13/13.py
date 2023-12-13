import re
import numpy as np
from itertools import combinations
from functools import cache

def parse_input(iname:str) -> np.ndarray:
    with open(iname, 'r') as f:
        lines = f.readlines()
    inputs = [[]]
    for line in lines:
        if line == '\n':
            inputs.append([])
        else:
            inputs[-1].append([*(line.strip('\n'))])
    matrices = [np.array(inp) for inp in inputs]
    return matrices

def get_sym_row(mat:np.ndarray):
    for i in range(1, mat.shape[0]):
        arr1 = np.flipud(mat[:i])
        arr2 = mat[i:]
        ok = True
        size = min(arr1.shape[0], arr2.shape[0])
        for j in range(size):
            if np.any(arr1[j] != arr2[j]):
                ok = False
                break
        if ok:
            return i
    return 0

def get_sym_row_smudge(mat:np.ndarray):
    for i in range(1, mat.shape[0]):
        arr1 = np.flipud(mat[:i])
        arr2 = mat[i:]
        size = min(arr1.shape[0], arr2.shape[0])
        total_diff = 0
        for j in range(size):
            total_diff += np.count_nonzero(arr1[j] != arr2[j])
            if total_diff > 1:
                break
        if total_diff == 1:
            return i
    return 0



def prob1():
    print("##########First part of the problem##########")
    matrices = parse_input('input.1')
    total = 0
    for mat in matrices:
        row = get_sym_row(mat)
        col = get_sym_row(mat.T)
        total += col + 100*row
    print(f"Total is {total}")

def prob2():
    print("##########Second part of the problem##########")
    matrices = parse_input('input.1')
    total = 0
    for mat in matrices:
        row = get_sym_row_smudge(mat)
        col = get_sym_row_smudge(mat.T)
        total += 100*row + col
    print(f"Total is {total}")


if __name__ == '__main__':
    prob1()
    prob2()
