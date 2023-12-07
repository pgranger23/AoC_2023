import re
import numpy as np

def parse_input(iname:str) -> list:
    numbers_list = []
    symbols_list = []
    with open(iname, 'r') as f:
        lines = f.readlines()
    lines = [line.strip('\n') for line in lines]
    nrows = len(lines)
    ncols = len(lines[0])
    for i, line in enumerate(lines):
        numbers = re.finditer(r'\d+', line)
        for number in numbers:
            numbers_list.append([int(number.group(0)), number.span(), i])
        symbols = re.finditer(r'[^\d|^\.]', line)
        for symbol in symbols:
            symbols_list.append([symbol.group(0), symbol.span(), i])
    return (numbers_list, symbols_list, nrows, ncols)

def build_matrix(numbers:list, symbols:list, nrows:int, ncols:int) -> np.ndarray:
    mat = np.zeros((nrows, ncols), dtype=int)
    for number in numbers:
        mat[number[2], number[1][0]:number[1][1]] = number[0]
    for symbol in symbols:
        mat[symbol[2], symbol[1][0]] = -1

    return mat

def prob1():
    print("##########First part of the problem##########")
    numbers, symbols, nrows, ncols = parse_input('input.1')
    mat = build_matrix(numbers, symbols, nrows, ncols)

    total = 0
    valid = []
    for number in numbers:
        col_min = max(0, number[1][0] - 1)
        col_max = min(mat.shape[1], number[1][1] + 1)
        row_min = max(0, number[2] - 1)
        row_max = min(mat.shape[0], number[2] + 2)
        if -1 in mat[row_min:row_max, col_min:col_max]:
            valid.append(number)
    for num in valid:
        total += num[0]
    print(f"The total is {total}")


def prob2():
    print("##########Second part of the problem##########")
    numbers, symbols, nrows, ncols = parse_input('input.1')
    selected_symbols = [symbol for symbol in symbols if symbol[0] == '*']
    mat = build_matrix(numbers, selected_symbols, nrows, ncols)

    total = 0
    valid = []
    for symbol in selected_symbols:
        col_min = max(0, symbol[1][0] - 1)
        col_max = min(mat.shape[1], symbol[1][1] + 1)
        row_min = max(0, symbol[2] - 1)
        row_max = min(mat.shape[0], symbol[2] + 2)
        values = set(np.unique(mat[row_min:row_max, col_min:col_max])) - {0, -1}
        if len(values) == 2:
            total += np.prod(list(values))
    print(f"The total is {total}")

if __name__ == '__main__':
    prob1()
    prob2()