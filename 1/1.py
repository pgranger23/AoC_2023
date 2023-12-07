import re

def read_input(iname:str) -> 'list[str]':
    with open(iname, 'r') as f:
        lines = f.readlines()
    lines = [line.strip('\n') for line in lines]
    return lines

numbers_text = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9
}


def convert_to_int(elt):
    if elt.isdigit():
        return int(elt)
    else:
        return numbers_text[elt]

def prob1():
    print("##########First part of the problem##########")
    lines = read_input('input.1')
    digits = [[int(ch) for ch in line if ch.isdigit()] for line in lines]
    numbers = [L[0]*10 + L[-1] for L in digits]
    total = sum(numbers)
    print(f"The sum is: {total}")

def prob2():
    print("##########Second part of the problem##########")
    lines = read_input('input.1')
    matches = [re.findall(r'(?=(\d|one|two|three|four|five|six|seven|eight|nine))', line) for line in lines]
    numbers = [convert_to_int(match[0])*10 + convert_to_int(match[-1]) for match in matches]
    total = sum(numbers)
    print(f"The sum is: {total}")

if __name__ == '__main__':
    prob1()
    prob2()