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

dir_change = {
    '\\': {
        Direction.RIGHT: Direction.DOWN,
        Direction.LEFT: Direction.UP,
        Direction.UP: Direction.LEFT,
        Direction.DOWN: Direction.RIGHT
    },
    '/': {
        Direction.RIGHT: Direction.UP,
        Direction.LEFT: Direction.DOWN,
        Direction.UP: Direction.RIGHT,
        Direction.DOWN: Direction.LEFT
    }
}

reverse_dir = {
    Direction.UP: Direction.DOWN,
    Direction.DOWN: Direction.UP,
    Direction.LEFT: Direction.RIGHT,
    Direction.RIGHT: Direction.LEFT,
}

def parse_input(iname:str) -> np.ndarray:
    with open(iname, 'r') as f:
        lines = f.readlines()
    lines = [list(line.strip('\n')) for line in lines]
    return np.array(lines)

def in_bounds(i:int, j:int, shape:tuple[int]) -> bool:
    return (i >= 0) and (j >= 0) and (i < shape[0]) and (j < shape[1])

def get_energized(i0, j0, dir0, mat):
    energized = set()
    beams = [((i0, j0), dir0)]
    
    while beams:
        (i, j), direction = beams.pop()
        while in_bounds(i, j, mat.shape):
            elt = mat[i, j]
            if (i, j, direction) in energized:
                break
            energized.add((i, j, direction))

            if elt == '.':
                pass
            elif elt == '|':
                if direction == Direction.RIGHT or direction == direction.LEFT:
                    beams.append(((i+1, j), Direction.DOWN))
                    beams.append(((i-1, j), Direction.UP))
                    break
            elif elt == '-':
                if direction == Direction.UP or direction == direction.DOWN:
                    beams.append(((i, j+1), Direction.RIGHT))
                    beams.append(((i, j-1), Direction.LEFT))
                    break
            else:
                direction = dir_change[elt][direction]

            i += dir_map[direction][0]
            j += dir_map[direction][1]
    return energized

def prob1():
    print("##########First part of the problem##########")
    mat = parse_input('input.1')
    energized = get_energized(0, 0, Direction.RIGHT, mat)
    nb_energized = len(set([(en[0], en[1]) for en in energized]))
    print(f"Nb energized is: {nb_energized}")


def prob2():
    print("##########Second part of the problem##########")
    mat = parse_input('input.1')
    configs = set()
    for i in range(mat.shape[0]):
        configs.add((i, 0, Direction.RIGHT))
        configs.add((i, mat.shape[1] - 1, Direction.LEFT))
    for j in range(mat.shape[1]):
        configs.add((0, j, Direction.DOWN))
        configs.add((mat.shape[0] - 1, j, Direction.UP))

    max_nb = 0

    for c in configs:
        energized = get_energized(*c, mat)
        nb_energized = len(set([(en[0], en[1]) for en in energized]))
        max_nb = max(max_nb, nb_energized)
    print(f"Max nb energized is: {max_nb}")

if __name__ == '__main__':
    prob1()
    prob2()
