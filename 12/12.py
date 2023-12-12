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

def count_damaged(group):
    return group.count('#')

def get_unk_pos(line):
    pos_list = []
    for i, ch in enumerate(line):
        if ch == '?':
            pos_list.append(i)
    return pos_list

def is_valid(line):
    groups = re.findall(r'#+', line)
    if len(groups) != 1:
        return False
    return True

@cache
def bruteforce_single(group, count):
    nb_damaged = count_damaged(group)
    unk_pos = get_unk_pos(group)

    if nb_damaged > count:
        return 0
    if nb_damaged == count:
        return is_valid(group)*1

    nb_to_add = count - nb_damaged

    nb_ok = 0
    ref = np.array([*group])
    for idxs in combinations(unk_pos, nb_to_add):
        proposition = ref.copy()
        proposition[list(idxs)] = '#'
        nb_ok += is_valid(''.join(proposition.tolist()))
    return nb_ok

@cache
def nb_possibilities(group, count_target):
    group = group.strip('.')
    if len(count_target) == 1:
        if '.' in group:
            new_groups = group.split('.')
            new_groups = [g for g in new_groups if g != '']
            total = 0
            for i in range(len(new_groups)):
                count = np.zeros(len(new_groups), dtype=int)
                count[i] = count_target[0]
                total = total + np.product([nb_possibilities(new_groups[j], (count[j],)) for j in range(len(new_groups))])
            return total
        if '#' in group:
            return bruteforce_single(group, count_target[0])
        if len(group) < count_target[0]:
            return 0
        if count_target[0] == 0:
            return 1
        return len(group) + 1 - count_target[0] #Formula with only ? in group
    
    if sum(count_target) >= len(group):
        return 0
    if group[0] == '?':
        return nb_possibilities('#' + group[1:], count_target) + nb_possibilities(group[1:], count_target)
    if group[count_target[0]] == '#':
        return 0
    return nb_possibilities(group[:count_target[0]], count_target[:1])*nb_possibilities(group[count_target[0] + 1:], count_target[1:])


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