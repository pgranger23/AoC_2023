import re
import numpy as np

def parse_input(iname:str) -> list:

    with open(iname, 'r') as f:
        lines = f.readlines()
    lines = [list(map(int, line.strip('\n').split(' '))) for line in lines]

    return lines

def prob1():
    print("##########First part of the problem##########")
    lines = parse_input('input.1')
    score = 0
    for line in lines:
        
        cur_line = np.array(line, dtype=int)
        seq_list = [cur_line]
        while np.count_nonzero(cur_line) != 0:
            cur_line = np.diff(cur_line)
            seq_list.append(cur_line)
        
        local_score = 0
        for seq in seq_list:
            local_score += seq[-1]
        score += local_score
    print(f"Total score is {score}")
        

def prob2():
    print("##########Second part of the problem##########")
    lines = parse_input('input.1')
    score = 0
    for line in lines:
        
        cur_line = np.array(line, dtype=int)
        seq_list = [cur_line]
        while np.count_nonzero(cur_line) != 0:
            cur_line = np.diff(cur_line)
            seq_list.append(cur_line)
        
        value = 0
        for seq in seq_list[::-1]:
            value = seq[0] - value
        score += value
    print(f"Total score is {score}")

if __name__ == '__main__':
    prob1()
    prob2()