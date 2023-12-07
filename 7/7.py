import re
import numpy as np

def parse_input(iname:str) -> list:

    with open(iname, 'r') as f:
        lines = f.readlines()
    lines = [line.strip('\n').split(' ') for line in lines]

    return lines

def translate_figures(ch:str, fig_map:dict):
    if ch.isdigit():
        return int(ch)
    return fig_map[ch]
    

def hand_ordering(hand:list, fig_map:dict):
    key = hand[2] + list(map(lambda x:translate_figures(x, fig_map), hand[0]))
    return key
    

def prob1():
    print("##########First part of the problem##########")
    hands = parse_input('input.1')
    fig_map = {
        'T': 10,
        'J': 11,
        'Q': 12,
        'K': 13,
        'A': 14,
    }
    for hand in hands:
        counter = {}
        for char in hand[0]:
            if char in counter:
                counter[char] += 1
            else:
                counter[char] = 1
        hand.append(sorted(list(counter.values()), reverse=True))

    sorted_hands = sorted(hands, key=lambda x: hand_ordering(x, fig_map))
    
    result = 0
    for i, hand in enumerate(sorted_hands):
        result += (i+1)*int(hand[1])
    print(f"The result is {result}")
    


def prob2():
    print("##########Second part of the problem##########")
    hands = parse_input('input.1')
    fig_map = {
        'T': 10,
        'J': 1,
        'Q': 12,
        'K': 13,
        'A': 14,
    }

    for hand in hands:
        counter = {}
        for char in hand[0]:
            if char in counter:
                counter[char] += 1
            else:
                counter[char] = 1
        if 'J' in counter:
            if len(counter) > 1: #Only if not 5J
                nb_jokers = counter['J']
                del counter['J']
                max_key = max(counter, key=counter.get)
                counter[max_key] += nb_jokers
        hand.append(sorted(list(counter.values()), reverse=True))

    sorted_hands = sorted(hands, key=lambda x:hand_ordering(x, fig_map))
    
    result = 0
    for i, hand in enumerate(sorted_hands):
        result += (i+1)*int(hand[1])
    print(f"The result is {result}")

if __name__ == '__main__':
    prob1()
    prob2()