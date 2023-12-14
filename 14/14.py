import re
import numpy as np

def parse_input(iname:str) -> np.ndarray:
    with open(iname, 'r') as f:
        lines = f.readlines()
    lines = [list(line.strip('\n')) for line in lines]
    return np.array(lines)

def tilt(mat):
    new_mat = np.full(mat.T.shape, '.')
    for i, col in enumerate(mat.T):
        blockers, = np.where(col == '#')
        new_mat[i][blockers] = '#'

        blockers = blockers.tolist()
        blockers.append(len(col))

        prev_block = -1
        for block in blockers:
            nb_stones = np.count_nonzero(col[prev_block+1:block] == 'O')
            new_mat[i][prev_block+1:prev_block+1+nb_stones] = 'O'
            prev_block = block
    return new_mat.T

def cycle(mat):
    # print(mat)
    north = tilt(mat)
    # print(north)
    west = tilt(north.T).T
    # print(west)
    south = np.flipud(tilt(np.flipud(west)))
    east = np.fliplr(tilt(np.fliplr(south).T).T)
    return east

def score(mat):
    rows, _ = np.where(mat == 'O')
    result = np.sum(mat.shape[0] - rows)
    return result

def prob1():
    print("##########First part of the problem##########")
    mat = parse_input('input.1')
    tilted = tilt(mat)
    result = score(tilted)
    print(f"Total load is {result}")


def prob2():
    print("##########Second part of the problem##########")
    mat = parse_input('input.1')
    ncycles = 1000000000
    hashlist = []
    i = 0
    shape = mat.shape
    while True:
        mat = cycle(mat)
        i += 1
        h = ''.join(mat.ravel())
        if h in hashlist:
            loop_idx = hashlist.index(h)
            break
        hashlist.append(h)
    cycle_len = i - loop_idx - 1
    hash_idx = loop_idx + (ncycles - i)%cycle_len
    result = score(np.array(list(hashlist[hash_idx])).reshape(shape))
    print(f"Total load is {result}")

if __name__ == '__main__':
    prob1()
    prob2()
