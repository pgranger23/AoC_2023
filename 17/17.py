import numpy as np
from enum import Enum
import heapq

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

class Path:
    def __init__(self, i, j, d, nb, dist) -> None:
        self.i = i
        self.j = j
        self.direction = d
        self.nb_steps_in_dir = nb
        self.distance = dist
        self.key = (self.i, self.j, self.direction, self.nb_steps_in_dir)
    
    def __lt__(self, other):
        return (self.distance, self.nb_steps_in_dir) < (other.distance, other.nb_steps_in_dir)

def parse_input(iname:str) -> np.ndarray:
    with open(iname, 'r') as f:
        lines = f.readlines()
    lines = [list(map(int, list(line.strip('\n')))) for line in lines]
    return np.array(lines)

def in_bounds(i:int, j:int, shape:tuple[int]) -> bool:
    return (i >= 0) and (j >= 0) and (i < shape[0]) and (j < shape[1])

def find_path(mat):
    paths = []
    paths.append(Path(0, 0, Direction.RIGHT, 0, 0))
    paths.append(Path(0, 0, Direction.DOWN, 0, 0))
    stop_i, stop_j = mat.shape[0] - 1, mat.shape[1] - 1

    visited = set()

    while paths:
        path = heapq.heappop(paths)        

        if path.key in visited:
            continue

        visited.add(path.key)

        if path.i == stop_i and path.j == stop_j:
            return path.distance

        for direc in Direction:
            if abs(direc.value - path.direction.value) == 2: #Dismiss reverse direction
                continue
            nb_steps = path.nb_steps_in_dir + 1
            if (direc.value + path.direction.value)%2 == 1: #Orthogonal direction
                nb_steps = 1
            if nb_steps > 3: #Stop at 3 in same dir
                continue
            i, j = path.i + dir_map[direc][0], path.j + dir_map[direc][1]
            if not in_bounds(i, j, mat.shape): #Bad path
                continue
                        
            neighbor = Path(i, j, direc, nb_steps, path.distance + mat[i, j])
            heapq.heappush(paths, neighbor)

def find_path2(mat):
    paths = []
    paths.append(Path(0, 0, Direction.RIGHT, 0, 0))
    paths.append(Path(0, 0, Direction.DOWN, 0, 0))
    stop_i, stop_j = mat.shape[0] - 1, mat.shape[1] - 1

    visited = set()

    while paths:
        path = heapq.heappop(paths)        

        if path.key in visited:
            continue

        visited.add(path.key)

        if path.i == stop_i and path.j == stop_j and path.nb_steps_in_dir >= 4:
            return path.distance

        for direc in Direction:
            if abs(direc.value - path.direction.value) == 2: #Dismiss reverse direction
                continue
            nb_steps = path.nb_steps_in_dir + 1
            if (direc.value + path.direction.value)%2 == 1: #Orthogonal direction
                if path.nb_steps_in_dir < 4: #Not allowed to turn
                    continue
                nb_steps = 1
            if nb_steps > 10: #Stop at 3 in same dir
                continue
            i, j = path.i + dir_map[direc][0], path.j + dir_map[direc][1]
            if not in_bounds(i, j, mat.shape): #Bad path
                continue
                        
            neighbor = Path(i, j, direc, nb_steps, path.distance + mat[i, j])
            heapq.heappush(paths, neighbor)  

def prob1():
    print("##########First part of the problem##########")
    mat = parse_input('input.1')
    distance = find_path(mat)
    print(f"Shortest distance is {distance}")



def prob2():
    print("##########Second part of the problem##########")
    mat = parse_input('input.1')
    distance = find_path2(mat)
    print(f"Shortest distance is {distance}")

if __name__ == '__main__':
    prob1()
    prob2()
