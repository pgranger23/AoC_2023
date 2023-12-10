import re
import numpy as np
from enum import Enum

class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

dir_map = {
    Direction.LEFT: (0, -1),
    Direction.RIGHT: (0, 1),
    Direction.UP: (-1, 0),
    Direction.DOWN: (1, 0),
}

dir_short = {
    Direction.LEFT: 'L',
    Direction.RIGHT: 'R',
    Direction.UP: 'U',
    Direction.DOWN: 'D',
}

char_map = {
    '-': {
        Direction.RIGHT: Direction.RIGHT,
        Direction.LEFT: Direction.LEFT
    },
    '|': {
        Direction.UP: Direction.UP,
        Direction.DOWN: Direction.DOWN
    },
    'L': {
        Direction.DOWN: Direction.RIGHT,
        Direction.LEFT: Direction.UP
    },
    'F': {
        Direction.LEFT: Direction.DOWN,
        Direction.UP: Direction.RIGHT
    },
    '7': {
        Direction.UP: Direction.LEFT,
        Direction.RIGHT: Direction.DOWN
    },
    'J': {
        Direction.DOWN: Direction.LEFT,
        Direction.RIGHT: Direction.UP
    }
}

def parse_input(iname:str) -> np.ndarray:
    with open(iname, 'r') as f:
        lines = f.readlines()
    lines = [list(line.strip('\n')) for line in lines]
    return np.array(lines)

def prob1():
    print("##########First part of the problem##########")
    mat = parse_input('input.1')
    start = np.hstack(np.where(mat == 'S'))
    
    #Finding the starting direction
    #Assuming start is not on a border...
    for dir in Direction:
        pos = start + dir_map[dir]
        char = mat[pos[0], pos[1]]
        if char in char_map:
            if dir in char_map[char]:
                break #We found a good starting char
    length = 1
    while char != 'S':
        length += 1
        #We should be in the loop now, just have to explore it
        dir = char_map[char][dir]
        pos = pos + dir_map[dir]
        char = mat[pos[0], pos[1]]

    print(f"Number of steps required: {int(length/2)}")
        

def prob2():
    print("##########Second part of the problem##########")
    mat = parse_input('input.1')
    dir_mat = np.full(mat.shape, '.')
    start = np.hstack(np.where(mat == 'S'))
    
    #Finding the starting direction
    #Assuming start is not on a border...
    for dir in Direction:
        pos = start + dir_map[dir]
        char = mat[pos[0], pos[1]]
        if char in char_map:
            if dir in char_map[char]:
                break #We found a good starting char
    length = 1
    dir_mat[start[0], start[1]] = '7' #HARDCODED for my input!!!
    while char != 'S':
        
        length += 1
        #We should be in the loop now, just have to explore it
        dir = char_map[char][dir]
        dir_mat[pos[0], pos[1]] = mat[pos[0], pos[1]]
        pos = pos + dir_map[dir]
        char = mat[pos[0], pos[1]]

        
    cum0 = np.cumsum(np.isin(dir_mat, ['L', '7']), axis=0)//2 + np.cumsum(np.isin(dir_mat, ['J', 'F']), axis=0)//2 + np.cumsum(dir_mat == '-', axis=0)

    result = (cum0%2 != 0) & (cum0 != 0) & (dir_mat == '.')

    print(f"Number enclosed: {np.count_nonzero(result)}")

if __name__ == '__main__':
    prob1()
    prob2()