import re
import numpy as np
from itertools import combinations
from functools import cache

def parse_input(iname:str) -> np.ndarray:
    with open(iname, 'r') as f:
        lines = f.readlines()
    lines = [line.strip('\n').split(' ') for line in lines]
    lines = [[line[0], tuple(map(int, line[1].split(',')))] for line in lines]
    return lines

@cache
def nb_possibilities(group, count_target):
    group = group.strip('.')
    if not count_target:
        return 0 if "#" in group else 1
    if not group:
        return 1 if not count_target else 0
    
    if sum(count_target) > len(group):
        return 0
    if group[0] == '?':
        return nb_possibilities('#' + group[1:], count_target) + nb_possibilities(group[1:], count_target)
    if (len(group) != count_target[0] and group[count_target[0]] == '#') or '.' in group[:count_target[0]]:
        return 0
    return nb_possibilities(group[count_target[0] + 1:], count_target[1:])


def prob1():
    print("##########First part of the problem##########")
    lines = parse_input('input.1')
    total = 0
    for line, count_target in lines:
        nb_combinations = nb_possibilities(line, count_target)
        total += nb_combinations

    print(f"Total is {total}")

def prob2():
    print("##########Second part of the problem##########")
    lines = parse_input('input.1')
    total = 0
    for line, count_target in lines:
        line = '?'.join([line]*5)
        count_target = count_target*5
        nb_combinations = nb_possibilities(line, count_target)
        total += nb_combinations

    print(f"Total is {total}")


if __name__ == '__main__':
    prob1()
    prob2()