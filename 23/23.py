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

hills = {
    '>': Direction.RIGHT,
    '<': Direction.LEFT,
    'v': Direction.DOWN,
    '^': Direction.UP
}

class Path:
    def __init__(self, i, j, d, dist, parent) -> None:
        self.i = i
        self.j = j
        self.direction = d
        self.distance = dist
        self.key = (self.i, self.j, self.direction)
        self.parent = parent
        self.visited_crossings = set()

    def add_visited_crossing(self, i:int, j:int) -> None:
        self.visited_crossings.add((i, j))

    def has_visited_crossing(self, i:int, j:int) -> bool:
        return (i, j) in self.visited_crossings
    
    def copy_visited_crossing(self, other:'Path') -> None:
        self.visited_crossings = other.visited_crossings.copy()
    
    def __lt__(self, other):
        return self.distance < other.distance

def parse_input(iname:str) -> np.ndarray:
    with open(iname, 'r') as f:
        lines = f.readlines()
    lines = [list(line.strip('\n')) for line in lines]
    return np.array(lines)

def in_bounds(i:int, j:int, shape:tuple[int]) -> bool:
    return (i >= 0) and (j >= 0) and (i < shape[0]) and (j < shape[1])

def find_intersections(mat):
    intersections = set()
    start = (0, np.argwhere(mat[0,:] == '.')[0][0])
    stop = (mat.shape[0] - 1, np.argwhere(mat[-1,:] == '.')[0][0])
    intersections.add(start)
    intersections.add(stop)

    nodes = set(map(tuple, np.argwhere(mat != '#').tolist()))

    for node in nodes:
        neighbors = 0
        for direc in Direction:
            i, j = node[0] + dir_map[direc][0], node[1] + dir_map[direc][1]
            if (i, j) in nodes:
                neighbors += 1
        if neighbors >= 3:
            intersections.add(node)
    return intersections

def compute_graph(mat):
    intersections = find_intersections(mat)
    graph = {point: {} for point in intersections}
    nodes = set(map(tuple, np.argwhere(mat != '#').tolist()))

    for point in intersections:
        seen = set()
        seen.add(point)

        to_visit = [(point, 0)]

        while to_visit:
            new_point, nsteps = to_visit.pop()
            if nsteps > 0 and new_point in intersections:
                graph[point][new_point] = nsteps
                continue

            for direc in Direction:
                i, j = new_point[0] + dir_map[direc][0], new_point[1] + dir_map[direc][1]
                if (i, j) not in seen and (i, j) in nodes:
                    to_visit.append(((i, j), nsteps + 1))
                    seen.add((i, j))
    return graph

def get_longest_path(graph, start, end):
    max_length = 0
    paths = [[[start], 0]]
    
    while paths:
        path, length = paths.pop()

        for node in graph[path[-1]]:
            if node in path:
                continue
            new_length = length + graph[path[-1]][node]
            if node == end:
                max_length = max(max_length, new_length)
                continue
            paths.append([path + [node], new_length])
    return max_length




def find_path(mat):
    paths = []

    start = (0, np.argwhere(mat[0,:] == '.')[0][0])
    stop = (mat.shape[0] - 1, np.argwhere(mat[-1,:] == '.')[0][0])

    paths.append(Path(start[0], start[1], Direction.DOWN, 0, None))
    valid_paths = []

    visited = set()

    while paths:
        path = heapq.heappop(paths)

        # if path.key in visited:
        #     continue

        visited.add(path.key)

        if path.i == stop[0] and path.j == stop[1]:
            valid_paths.append(path)
            continue

        for direc in Direction:
            if abs(direc.value - path.direction.value) == 2: #Dismiss reverse direction
                continue
            i, j = path.i + dir_map[direc][0], path.j + dir_map[direc][1]
            if not in_bounds(i, j, mat.shape): #Bad path
                continue
            if mat[i, j] == '#': #Unallowed tile
                continue

            if mat[i,j] in hills:
                if hills[mat[i, j]] != direc:
                    continue # Not an allowed direction for a hill
                        
            neighbor = Path(i, j, direc, path.distance - 1, path)
            heapq.heappush(paths, neighbor)
        
    return valid_paths
    

def prob1():
    print("##########First part of the problem##########")
    mat = parse_input('input.1')
    paths = find_path(mat)
    print(f"Longest distance is {-min([path.distance for path in paths])}")



def prob2():
    print("##########Second part of the problem##########")
    mat = parse_input('input.1')
    graph = compute_graph(mat)
    start = (0, np.argwhere(mat[0,:] == '.')[0][0])
    stop = (mat.shape[0] - 1, np.argwhere(mat[-1,:] == '.')[0][0])
    print(f"Longest distance is: {get_longest_path(graph, start, stop)}")

if __name__ == '__main__':
    prob1()
    prob2()
