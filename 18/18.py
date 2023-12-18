import numpy as np

dir_map = {
    'U': -1,
    'D': 1,
    'L': -1j,
    'R': 1j,
    '0': 1j,
    '1': 1,
    '2': -1j,
    '3': -1
}

def parse_input(iname:str) -> np.ndarray:
    with open(iname, 'r') as f:
        lines = f.readlines()
    lines = [line.strip('\n').split(' ') for line in lines]
    lines = [(dir_map[line[0]], int(line[1]), line[2][1:-1]) for line in lines]
    return lines

def build_graph(lines):
    node = 0 + 0j
    nodes = set([node])
    edges = []

    for direction, length, color in lines:
        for i in range(length):
            new_node = node + direction
            nodes.add(new_node)
            edges.append((node, new_node, color))
            node = new_node
    return nodes, edges

def flood_fill(nodes, start):
    to_visit = [start]
    internal_nodes = set()
    while to_visit:
        node = to_visit.pop()
        if node in internal_nodes:
            continue
        internal_nodes.add(node)
        for direction in [1, -1, -1j, 1j]:
            new_node = node + direction
            if new_node not in nodes:
                to_visit.append(new_node)
    return len(internal_nodes) + len(nodes)

def shoelace(edges):
    area = 0
    contour = 2
    for i in range(len(edges)):
        P1 = edges[i][0]
        P2 = edges[(i+1)%len(edges)][0]
        area += (P1.real*P2.imag - P1.imag*P2.real)
        contour += edges[i][1]
    return int((abs(area) + contour)/2)

def prob1():
    print("##########First part of the problem##########")
    lines = parse_input('input.1')
    nodes, edges = build_graph(lines)
    result = flood_fill(nodes, 1 + 1j)
    print(f"Number of cubic meters of lava: {result}")


def prob2():
    print("##########Second part of the problem##########")
    lines = parse_input('input.1')
    instructions = [(int(line[2][1:6], 16), dir_map[line[2][-1]]) for line in lines]
    node = 0j
    edges = []
    for length, direction in instructions:
        edges.append((node, length, direction))
        node = node + length*direction
    result = shoelace(edges)
    print(f"Number of cubic meters of lava: {result}")


if __name__ == '__main__':
    prob1()
    prob2()
