import re
import numpy as np

color_map = {
    "red": 0,
    "green": 1,
    "blue": 2
}

def parse_draw(string:str) -> list[int]:
    result = [0, 0, 0]
    elts = string.split(',')
    for elt in elts:
        nb, color = re.findall(r'(\d+) ([a-z]+)', elt)[0]
        result[color_map[color]] = int(nb)
    return result

def parse_input(iname:str) -> list:
    with open(iname, 'r') as f:
        lines = f.readlines()
    lines = [line.strip('\n') for line in lines]
    matches = [re.findall(r'Game (\d+)|(?=[:|;]([^;]*))+', line) for line in lines]
    inputs = []
    for match in matches:
        id = int(match[0][0])
        draws = np.vstack([parse_draw(draw[-1].strip(' ')) for draw in match[1:]])
        inputs.append((id, draws))
    return inputs

def prob1():
    print("##########First part of the problem##########")
    games = parse_input('input.1')
    limits = np.array([12, 13, 14])

    total = 0

    for nb, draws in games:
        if np.min(limits - draws) >= 0:
            total += nb
    print(f"The result is {total}")

def prob2():
    print("##########Second part of the problem##########")
    games = parse_input('input.1')
    total = 0

    for nb, draws in games:
        power = np.prod(np.max(draws, axis=0))
        total += power
    print(f"The result is {total}")

if __name__ == '__main__':
    prob1()
    prob2()