import numpy as np

def parse_input(iname:str):
    with open(iname, 'r') as f:
        lines = f.readlines()
    lines = [[list(map(int, elt.split(','))) for elt in line.strip('\n').split('~')] for line in lines]
    return lines

brick_id = 0

class Brick:
    def __init__(self, line:list) -> None:
        global brick_id
        self.x = [line[0][0], line[1][0]]
        self.y = [line[0][1], line[1][1]]
        self.z = [line[0][2], line[1][2]]
        self.id = brick_id
        brick_id += 1
        self.parents = []
        self.children = []

    def update_z(self, zmin:int) -> None:
        self.z = [zmin, zmin + self.z[1] - self.z[0]]

    def set_parent(self, parent:'Brick') -> None:
        if len(self.parents) == 0:
            self.update_z(parent.z[1] + 1)

        if self.z[0] == parent.z[1] + 1: #Directly below
            self.parents.append(parent)
            parent.children.append(self)

    def is_above(self, other:'Brick') -> bool:
        xlow = max(self.x[0], other.x[0])
        xhigh = min(self.x[1], other.x[1])

        ylow = max(self.y[0], other.y[0])
        yhigh = min(self.y[1], other.y[1])

        return (xlow <= xhigh) and (ylow <= yhigh)
    
    def __repr__(self) -> str:
        return f"id: {self.id} ; x: {self.x} ; y: {self.y} ; z: {self.z}"


def prob1():
    print("##########First part of the problem##########")
    lines = parse_input('input.1')
    lines.sort(key=lambda elt: elt[0][2])
    floor = Brick([[0, 0, 0], [1000000, 1000000, 0]])
    bricks = [floor]
    for i, line in enumerate(lines):
        brick = Brick(line)
        for j in range(i, -1, -1):
            other_brick = bricks[j]
            if brick.is_above(other_brick):
                brick.set_parent(other_brick)
        bricks.append(brick)
        bricks.sort(key=lambda elt: elt.z[1])

    non_disintegrable = set()

    for brick in bricks:
        if len(brick.parents) == 1: #Floor plus a single real one
            non_disintegrable.add(brick.parents[0].id)
    non_disintegrable.discard(0)
    nb_disintegrable = len(bricks) - 1 - len(non_disintegrable)
    print(f"Number of disintegrable bricks -> {nb_disintegrable}")



def prob2():
    print("##########Second part of the problem##########")
    global brick_id
    brick_id = 0
    lines = parse_input('input.1')
    lines.sort(key=lambda elt: elt[0][2])
    floor = Brick([[0, 0, 0], [1000000, 1000000, 0]])
    bricks = [floor]
    for i, line in enumerate(lines):
        brick = Brick(line)
        for j in range(i, -1, -1):
            other_brick = bricks[j]
            if brick.is_above(other_brick):
                brick.set_parent(other_brick)
        bricks.append(brick)
        bricks.sort(key=lambda elt: elt.z[1])

    nb_fall_count = 0
    nb_fall = {}

    bricks.pop(0)

    for brick in bricks[::-1]:
        falling = set([brick.id])
        children_queue = brick.children.copy()
        while children_queue:
            child = children_queue.pop()
            if len(set([parent.id for parent in child.parents]) - falling) == 0:
                falling.add(child.id)
                children_queue += child.children
        nb_fall[brick.id] = len(falling) - 1
        nb_fall_count += len(falling) - 1

    print(f"Number of falling bricks -> {nb_fall_count}")

if __name__ == '__main__':
    prob1()
    prob2()
