import re
import numpy as np
from dataclasses import dataclass

@dataclass
class Interval:
    start: int
    stop: int

    def intersect(self, other):
        if self.start >= other.stop:
            return None
        if self.stop <= other.start:
            return None
        
        low_intersect = max(self.start, other.start)
        high_intersect = min(self.stop, other.stop)

        return Interval(low_intersect, high_intersect)
    
    def __eq__(self, __value: object) -> bool:
        return (self.start == __value.start) and (self.stop == __value.stop)

    def subtract(self, other):
        # Assumes that other is totally contained in self
        if self == other:
            return None
        if self.start == other.start:
            return Interval(other.stop, self.stop)
        elif self.stop == other.stop:
            return Interval(self.start, other.start)
        else:
            return [Interval(self.start, other.start), Interval(other.stop, self.stop)]
    
    def tolist(self) -> list:
        return [self.start, self.stop]

def parse_input(iname:str) -> list:

    with open(iname, 'r') as f:
        lines = f.readlines()
    seeds = list(map(int, re.findall(r'\d+', lines[0])))
    steps = []
    cur_conversion = []
    for line in lines[3:]:
        if line == '\n':
            continue
        mapping = re.findall(r'\d+', line)
        if mapping:
            mapping = list(map(int, mapping))
            cur_conversion.append(mapping)
        else:
            steps.append(cur_conversion)
            cur_conversion = []
    steps.append(cur_conversion)
    return (seeds, steps)

def prob1():
    print("##########First part of the problem##########")
    seeds, steps = parse_input('input.1')
    seeds_init = seeds.copy()
    
    for conversions in steps:
        for i, seed in enumerate(seeds):
            for conversion in conversions:
                if conversion[1] <= seed < conversion[1] + conversion[2]:
                    seeds[i] = (seed - conversion[1]) + conversion[0]
                    break
    loc = np.min(seeds)
    print(f"The lowest location is {loc}")


def prob2():
    print("##########Second part of the problem##########")
    seeds, steps = parse_input('input.1')
    ranges = [[seeds[i], seeds[i+1] + seeds[i]] for i in range(0, len(seeds) - 1, 2)]
    for conversions in steps[:]:
        new_intervals = []
        while ranges:
            ran = ranges.pop()
            did_intersect = False
            for conversion in conversions:
                input_interval = Interval(*ran)
                compare_interval = Interval(conversion[1], conversion[1] + conversion[2])
                intersect = input_interval.intersect(compare_interval)
                if intersect:
                    did_intersect = True
                    new_interval = [conversion[0] + intersect.start - conversion[1], conversion[0] + intersect.stop - conversion[1]]
                    new_intervals.append(new_interval)
                    remains = input_interval.subtract(intersect)

                    if remains:
                        if not isinstance(remains, list):
                            remains = [remains]
                        for interval in remains:
                            ranges.append(interval.tolist())
            if not did_intersect:
                new_intervals.append(ran)
        ranges = new_intervals

    print(f"The lowest location is {min([ran[0] for ran in ranges])}")

if __name__ == '__main__':
    prob1()
    prob2()