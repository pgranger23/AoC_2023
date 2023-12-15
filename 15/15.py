import re
import numpy as np

def parse_input(iname:str) -> np.ndarray:
    with open(iname, 'r') as f:
        line = f.readline()
    seq = line.split(',')
    return seq

def compute_hash(string:str) -> int:
    value = 0
    for ch in string:
        value += ord(ch)
        value = (value*17)%256
    return value


def prob1():
    print("##########First part of the problem##########")
    seq = parse_input('input.1')
    total = 0
    for item in seq:
        total += compute_hash(item)
    print(f"Total is: {total}")


def prob2():
    print("##########Second part of the problem##########")
    seq = parse_input('input.1')

    boxes = [[] for i in range(256)]
    hashtab = [{} for i in range(256)]
    for item in seq:
        if item[-1] == '-':
            label = item[:-1]
            box_id = compute_hash(label)
            if label in hashtab[box_id]:
                idx = hashtab[box_id][label]
                boxes[box_id].pop(idx)
                del hashtab[box_id][label]
                for label, i in hashtab[box_id].items():
                    if i > idx:
                        hashtab[box_id][label] -= 1
        else:
            label, focal = item.split('=')
            focal = int(focal)
            box_id = compute_hash(label)
            if label in hashtab[box_id]:
                idx = hashtab[box_id][label]
                boxes[box_id][idx] = focal
            else:
                boxes[box_id].append(focal)
                hashtab[box_id][label] = len(boxes[box_id]) - 1
    focusing_power = 0
    for i, box in enumerate(boxes):
        for j, focal in enumerate(box):
            focusing_power += (i+1)*(j+1)*focal
    print(f"Focusing power is: {focusing_power}")

if __name__ == '__main__':
    prob1()
    prob2()
