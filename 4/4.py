import re
import numpy as np

def parse_input(iname:str) -> list:

    with open(iname, 'r') as f:
        lines = f.readlines()
    lines = [re.findall(r'[(\d+) ]+(?=|)', line) for line in lines]
    lines = [[int(line[0].strip(' ')), set(map(int, re.findall('\d+', line[1]))), set(map(int, re.findall('\d+', line[2])))] for line in lines]
    return lines

def prob1():
    print("##########First part of the problem##########")
    cards = parse_input('input.1')

    total = 0

    for card in cards:
        nb_winning = len(card[1].intersection(card[2]))
        if nb_winning > 0:
            total += 2**(nb_winning - 1)

    print(f"The total is {total}")


def prob2():
    print("##########Second part of the problem##########")
    cards = parse_input('input.1')
    nb_cards = np.ones(len(cards), dtype=int)

    for i, card in enumerate(cards):
        nb_winning = len(card[1].intersection(card[2]))
        if nb_winning > 0:
            nb_cards[i + 1: i + 1 + nb_winning] += nb_cards[i]


    total = np.sum(nb_cards)
    print(f"The total is {total}")

if __name__ == '__main__':
    prob1()
    prob2()