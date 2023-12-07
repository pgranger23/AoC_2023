import re
import numpy as np

def parse_input(iname:str) -> list:

    with open(iname, 'r') as f:
        lines = f.readlines()
    times = list(map(int, re.findall(r'\d+', lines[0])))
    distances = list(map(int, re.findall(r'\d+', lines[1])))

    return (times, distances)
    

def prob1():
    print("##########First part of the problem##########")
    times, distances = parse_input('input.1')
    product = 1
    eps = 1e-9
    for t, d in zip(times, distances):
        delta = t*t - 4*d
        assert(delta > 0)
        xmin = np.ceil((t - np.sqrt(delta))/2 + eps)
        xmax = np.floor((t + np.sqrt(delta))/2 - eps)

        nb_wins = int(xmax - xmin) + 1
        product *= nb_wins
    print(f"The result is {product}")
    


def prob2():
    print("##########Second part of the problem##########")
    times, distances = parse_input('input.1')
    t = int(''.join(map(str, times)))
    d = int(''.join(map(str, distances)))
    eps = 1e-9
    delta = t*t - 4*d
    assert(delta > 0)
    xmin = np.ceil((t - np.sqrt(delta))/2 + eps)
    xmax = np.floor((t + np.sqrt(delta))/2 - eps)

    nb_wins = int(xmax - xmin) + 1

    print(f"The result is {nb_wins}")

if __name__ == '__main__':
    prob1()
    prob2()