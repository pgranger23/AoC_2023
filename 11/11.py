import re
import numpy as np

def parse_input(iname:str) -> np.ndarray:
    with open(iname, 'r') as f:
        lines = f.readlines()
    lines = [list(line.strip('\n')) for line in lines]
    return np.array(lines)

def get_expanded_lists(mat:np.ndarray) -> tuple[list]:
    lines = []
    cols = []
    for i, line in enumerate(mat):
        if np.all(line == '.'):
            lines.append(i)

    for i, col in enumerate(mat.T):
        if np.all(col == '.'):
            cols.append(i)

    return (lines, cols)

def prob1():
    print("##########First part of the problem##########")
    mat = parse_input('input.1')
    exp_lines, exp_cols = get_expanded_lists(mat)
    coeff = 2
    galaxies = list(zip(*np.where(mat == '#')))
    total_dist = 0
    for i in range(len(galaxies)):
        x1, y1 = galaxies[i]
        for j in range(i+1, len(galaxies)):
            x2, y2 = galaxies[j]
            total_dist += abs(x1 - x2) + abs(y1 - y2)

            for line_idx in exp_lines:
                if (x1 - line_idx)*(x2 - line_idx) < 0:
                    total_dist += (coeff - 1)
            for col_idx in exp_cols:
                if (y1 - col_idx)*(y2 - col_idx) < 0:
                    total_dist += (coeff - 1)
    print(f"Total dist is: {total_dist}")
        

def prob2():
    print("##########Second part of the problem##########")
    mat = parse_input('input.1')
    exp_lines, exp_cols = get_expanded_lists(mat)
    coeff = 1000000
    galaxies = list(zip(*np.where(mat == '#')))
    total_dist = 0
    for i in range(len(galaxies)):
        x1, y1 = galaxies[i]
        for j in range(i+1, len(galaxies)):
            x2, y2 = galaxies[j]
            total_dist += abs(x1 - x2) + abs(y1 - y2)

            for line_idx in exp_lines:
                if (x1 - line_idx)*(x2 - line_idx) < 0:
                    total_dist += (coeff - 1)
            for col_idx in exp_cols:
                if (y1 - col_idx)*(y2 - col_idx) < 0:
                    total_dist += (coeff - 1)
    print(f"Total dist is: {total_dist}")


if __name__ == '__main__':
    prob1()
    prob2()