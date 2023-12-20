import re
from math import lcm

nb_sent = [0, 0]
            
class Module:
    def __init__(self, name:str, children_names:list[str]) -> None:
        self.name = name
        self.children_names = children_names
        self.signal_queue = []
        self.nb_low_pulses = 0 #For part2
        
    def init_children(self, modules:dict[str, 'Module']) -> None:
        self.children = []
        for name in self.children_names:
            module = modules[name]
            self.children.append(module)
            if isinstance(module, Conjunction):
                module.im_your_father(self.name)

    def send_signal(self, signal:int) -> None:
        for child in self.children:
            child.register_signal(signal, self.name)
        nb_sent[signal] += len(self.children)
        for child in self.children:
            child.process_signal()

    def register_signal(self, signal:int, sender:str) -> None:
        self.nb_low_pulses +=1 #For part2

    def process_signal(self) -> None:
        pass

class FlipFlop(Module):
    def __init__(self, name:str, children_names:list[str]) -> None:
        super().__init__(name, children_names)
        self.signal_status = 0

    def register_signal(self, signal:int, sender:str) -> None:
        self.signal_queue.append(signal)

    def process_signal(self) -> None:
        oldest_signal = self.signal_queue.pop(0)
        if oldest_signal == 1: #Ignore high signal
            return
        self.signal_status = (self.signal_status + 1)%2
        if self.signal_status == 1: #Was turned on
            self.send_signal(1)
        else: #Got turned off
            self.send_signal(0)

class Conjunction(Module):
    def __init__(self, name:str, children_names:list[str]) -> None:
        super().__init__(name, children_names)
        self.signal_status = {}

    def im_your_father(self, father_name:str) -> None:
        self.signal_status[father_name] = 0

    def register_signal(self, signal:int, sender:str) -> None:
        self.signal_queue.append((sender, signal))

    def process_signal(self) -> None:
        sender, signal = self.signal_queue.pop(0)
        self.signal_status[sender] = signal
        if 0 in self.signal_status.values():
            self.send_signal(1)
        else:
            self.send_signal(0)

class Broadcaster(Module):
    def __init__(self, name: str, children_names: list[str]) -> None:
        super().__init__(name, children_names)

    def register_signal(self, signal:int, sender:str) -> None:
        self.signal_queue.append(signal)

    def process_signal(self) -> None:
        signal = self.signal_queue.pop(0)
        self.send_signal(signal)

def parse_input(iname:str) -> dict[str, Module]:
    with open(iname, 'r') as f:
        lines = f.readlines()

    modules = {}

    for line in lines:
        matches = re.findall(r'([^->, \n]+)', line)
        name, children_names = matches[0], matches[1:]
        if name[0] == '%':
            module = FlipFlop(name[1:], children_names)
        elif name[0] == '&':
            module = Conjunction(name[1:], children_names)
        else:
            module = Broadcaster(name, children_names)
        modules[module.name] = module

    return modules

def prob1():
    print("##########First part of the problem##########")
    modules = parse_input('input.1')
    all_modules = modules.copy()
    for module in modules.values():
        for child_name in module.children_names:
            if not child_name in modules:
                all_modules[child_name] =  Module(child_name, []) #Adding the empty modules
        module.init_children(all_modules)

    for _ in range(1000):
        nb_sent[0] += 1
        modules['broadcaster'].send_signal(0)
    print(f"Result is {nb_sent[0]*nb_sent[1]}")


def prob2():
    print("##########Second part of the problem##########")
    #https://edotor.net/?engine=fdp#strict%20digraph%20%22%22%20%7B%0A%09vg%20-%3E%20lf%3B%0A%09vg%20-%3E%20vd%3B%0A%09lf%20-%3E%20nb%3B%0A%09vd%20-%3E%20lf%3B%0A%09vd%20-%3E%20tf%3B%0A%09vd%20-%3E%20nb%3B%0A%09vd%20-%3E%20cx%3B%0A%09vd%20-%3E%20hx%3B%0A%09vd%20-%3E%20lr%3B%0A%09dr%20-%3E%20kg%3B%0A%09kg%20-%3E%20lv%3B%0A%09cn%20-%3E%20mv%3B%0A%09cn%20-%3E%20pt%3B%0A%09mv%20-%3E%20pt%3B%0A%09mv%20-%3E%20hq%3B%0A%09pt%20-%3E%20jx%3B%0A%09pt%20-%3E%20rf%3B%0A%09pt%20-%3E%20vq%3B%0A%09pt%20-%3E%20cm%3B%0A%09pt%20-%3E%20rg%3B%0A%09rq%20-%3E%20bk%3B%0A%09rq%20-%3E%20gr%3B%0A%09bk%20-%3E%20xh%3B%0A%09bk%20-%3E%20ln%3B%0A%09bk%20-%3E%20zx%3B%0A%09gr%20-%3E%20bk%3B%0A%09gr%20-%3E%20mn%3B%0A%09vp%20-%3E%20bk%3B%0A%09vp%20-%3E%20lp%3B%0A%09lp%20-%3E%20bk%3B%0A%09lp%20-%3E%20jt%3B%0A%09lv%20-%3E%20jc%3B%0A%09lv%20-%3E%20tp%3B%0A%09jc%20-%3E%20tp%3B%0A%09jc%20-%3E%20qr%3B%0A%09tp%20-%3E%20dr%3B%0A%09tp%20-%3E%20kg%3B%0A%09tp%20-%3E%20qr%3B%0A%09tp%20-%3E%20km%3B%0A%09tp%20-%3E%20vj%3B%0A%09tp%20-%3E%20db%3B%0A%09sj%20-%3E%20vd%3B%0A%09sj%20-%3E%20rm%3B%0A%09rm%20-%3E%20vd%3B%0A%09rm%20-%3E%20st%3B%0A%09qr%20-%3E%20dk%3B%0A%09km%20-%3E%20dr%3B%0A%09km%20-%3E%20tp%3B%0A%09jx%20-%3E%20cn%3B%0A%09tf%20-%3E%20tg%3B%0A%09nb%20-%3E%20cg%3B%0A%09cx%20-%3E%20gp%3B%0A%09hx%20-%3E%20sb%3B%0A%09lr%20-%3E%20vg%3B%0A%09lr%20-%3E%20vd%3B%0A%09jt%20-%3E%20bk%3B%0A%09vj%20-%3E%20ps%3B%0A%09ps%20-%3E%20tp%3B%0A%09ps%20-%3E%20xf%3B%0A%09broadcaster%20-%3E%20km%3B%0A%09broadcaster%20-%3E%20lr%3B%0A%09broadcaster%20-%3E%20xh%3B%0A%09broadcaster%20-%3E%20rf%3B%0A%09xh%20-%3E%20bk%3B%0A%09xh%20-%3E%20ql%3B%0A%09rf%20-%3E%20pt%3B%0A%09rf%20-%3E%20dj%3B%0A%09dj%20-%3E%20pt%3B%0A%09dj%20-%3E%20gc%3B%0A%09gc%20-%3E%20pt%3B%0A%09gc%20-%3E%20cm%3B%0A%09cg%20-%3E%20vd%3B%0A%09cg%20-%3E%20hx%3B%0A%09ln%20-%3E%20tg%3B%0A%09tg%20-%3E%20rx%3B%0A%09fl%20-%3E%20pt%3B%0A%09fl%20-%3E%20sk%3B%0A%09sk%20-%3E%20pt%3B%0A%09lm%20-%3E%20bk%3B%0A%09lm%20-%3E%20tr%3B%0A%09tr%20-%3E%20bk%3B%0A%09tr%20-%3E%20vp%3B%0A%09vq%20-%3E%20tg%3B%0A%09cm%20-%3E%20rg%3B%0A%09rg%20-%3E%20sd%3B%0A%09gp%20-%3E%20vd%3B%0A%09gp%20-%3E%20sj%3B%0A%09db%20-%3E%20tg%3B%0A%09st%20-%3E%20vd%3B%0A%09jh%20-%3E%20bk%3B%0A%09jh%20-%3E%20lm%3B%0A%09xf%20-%3E%20tp%3B%0A%09xf%20-%3E%20bd%3B%0A%09bd%20-%3E%20tp%3B%0A%09bd%20-%3E%20gg%3B%0A%09gg%20-%3E%20tp%3B%0A%09dk%20-%3E%20tp%3B%0A%09dk%20-%3E%20vj%3B%0A%09mn%20-%3E%20bk%3B%0A%09mn%20-%3E%20jh%3B%0A%09ql%20-%3E%20bk%3B%0A%09ql%20-%3E%20zx%3B%0A%09zx%20-%3E%20rq%3B%0A%09sb%20-%3E%20vd%3B%0A%09sb%20-%3E%20cx%3B%0A%09sd%20-%3E%20pt%3B%0A%09sd%20-%3E%20jx%3B%0A%09hq%20-%3E%20pt%3B%0A%09hq%20-%3E%20fl%3B%0A%7D%0A
    binary_cycles = ["111001011111"[::-1], "100110101111"[::-1], "110010101111"[::-1], "110111111111"[::-1]]
    res = 1
    for cyc in binary_cycles:
        res = lcm(res, int(cyc, 2))
    print("Result is", res)

if __name__ == '__main__':
    prob1()
    prob2()
