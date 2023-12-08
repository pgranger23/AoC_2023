import re
from math import gcd

def parse_input(iname:str) -> list:

    with open(iname, 'r') as f:
        lines = f.readlines()
    directions = lines[0].strip('\n')
    codes = [re.findall(r'\w+', line) for line in lines[2:]]
    nodes = {code[0]: (code[1], code[2]) for code in codes}

    return directions, nodes

def prob1():
    print("##########First part of the problem##########")
    directions, nodes = parse_input('input.1')

    cur_node = 'AAA'
    step = 0
    while cur_node != 'ZZZ':
        instruction_idx = step%len(directions)
        idx = 0
        if directions[instruction_idx] == 'L':
            idx = 0
        else:
            idx = 1
        
        cur_node = nodes[cur_node][idx]
        step +=1
    print(f"Number of steps is {step}")


def prob2():
    print("##########Second part of the problem##########")

    directions, nodes = parse_input('input.1')

    cur_nodes = [node for node in nodes if node[-1] == 'A']
    distances = []
    for cur_node in cur_nodes:
        step = 0
        while cur_node[-1] != 'Z':
            instruction_idx = step%len(directions)
            idx = 0
            if directions[instruction_idx] == 'L':
                idx = 0
            else:
                idx = 1
            cur_node = nodes[cur_node][idx]
            step +=1
        distances.append(step)

    #Only works because of the specific input provided
    smaller_common_multiplier = 1
    for d in distances:
        smaller_common_multiplier = smaller_common_multiplier*d//gcd(smaller_common_multiplier, d)

    print(f"Number of steps is {smaller_common_multiplier}")

if __name__ == '__main__':
    prob1()
    prob2()