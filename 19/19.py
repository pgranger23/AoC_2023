import re
from operator import lt, gt
from itertools import combinations

class Rule:
    def __init__(self, string, always_true=False) -> None:
        if always_true:
            self.always_true = True
            return
        self.always_true = False
        self.var = string[0]
        self.operation = lt if string[1] == '<' else gt
        self.value = int(string[2:])

    def check(self, part) -> bool:
        return self.always_true or self.operation(part[self.var], self.value)

class Workflow:
    def __init__(self, string) -> None:
        self.rules = []

        rule_strings = string.split(',')
        for rule_string in rule_strings:
            splitted = rule_string.split(':')
            if len(splitted) == 2:
                rule_cond, action = splitted
                rule = Rule(rule_cond)
            else:
                action = splitted[0]
                rule = Rule("", always_true=True)
            self.rules.append((rule, action))
    
    def get_next(self, part):
        for rule, action in self.rules:
            if rule.check(part):
                return action
            
class Node:
    def __init__(self, next_true, next_false, rule):
        self.next_true = next_true
        self.next_false = next_false
        self.rule = rule

def build_nodes(workflows):
    nodes = {}
    for name, wf in workflows.items():
        for i, (rule, action) in enumerate(wf.rules):
            nodes[(name, i)] = Node((action, 0), (name, i+1), rule)
    return nodes


def is_accepted(workflows, part):
    action = 'in'
    while action not in ['A', 'R']:
        wf = workflows[action]
        action = wf.get_next(part)
    return action == 'A'

def parse_input(iname:str):
    with open(iname, 'r') as f:
        lines = f.readlines()

    workflows = {}
    parts = []

    for i, line in enumerate(lines):
        if line == '\n':
            break
        name, rules = re.findall(r'(\w+){(.+)}', line)[0]
        workflows[name] = Workflow(rules)
    for line in lines[i+1:]:
        part = {}
        for var, value in re.findall(r'(\w)=(\d+)', line):
            part[var] = int(value)
        parts.append(part)

    return workflows, parts

def prob1():
    print("##########First part of the problem##########")
    workflows, parts = parse_input('input.1')
    rating = 0
    for part in parts:
        if is_accepted(workflows, part):
            rating += sum(part.values())

    print(f"Total rating is {rating}")


def prob2():
    print("##########Second part of the problem##########")
    workflows, parts = parse_input('input.1')

    nodes = build_nodes(workflows)
    
    mother_map = {}
    for node_id, node in nodes.items():
        if node.next_false in mother_map:
            mother_map[node.next_false].append((node_id, False))
        else:
            mother_map[node.next_false] = [(node_id, False)]

        if node.next_true in mother_map:
            mother_map[node.next_true].append((node_id, True))
        else:
            mother_map[node.next_true] = [(node_id, True)]

    #Backtrack
    paths = [[elt] for elt in mother_map[('A', 0)]]
    valid_paths = []
    while paths:
        path = paths.pop()
        if path[-1][0] == ('in', 0):
            valid_paths.append(path)
        else:
            mothers = mother_map[path[-1][0]]
            for mother in mothers:
                path_copy = path.copy()
                path_copy.append(mother)
                paths.append(path_copy)


    list_limits = []

    for path in valid_paths:
        limits = {
            'x': [1, 4000],
            'm': [1, 4000],
            'a': [1, 4000],
            's': [1, 4000],
        }
        for step in path:
            step_name, outcome = step
            node = nodes[step_name]
            rule = node.rule

            if outcome == True:
                if rule.always_true == True:
                    continue
                if rule.operation == lt:
                    limits[rule.var][1] = min(rule.value - 1, limits[rule.var][1])
                else:
                    limits[rule.var][0] = max(rule.value + 1, limits[rule.var][0])
            else:
                if rule.operation == lt:
                    limits[rule.var][0] = max(rule.value, limits[rule.var][0])
                else:
                    limits[rule.var][1] = min(rule.value, limits[rule.var][1])

        list_limits.append(limits)

    total_valid = 0

    for limits in list_limits:
        nb_valid = 1
        for low, high in limits.values():
            nb_valid *= (high - low + 1)
        total_valid += nb_valid

    print(f"Total number of valid parts is {total_valid}")

if __name__ == '__main__':
    prob1()
    prob2()
