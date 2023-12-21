import itertools

from year2023.day2023 import Day2023
from typing import *
import re
from collections import deque
from math import lcm
# import networkx as nx
# from matplotlib import pyplot as plt


class Module:
    def __init__(self, name: str, srcs: List[str], dsts: List[str]):
        self.name = name
        self.srcs = srcs
        self.dsts = dsts

    def pulse(self, pulse: bool, sender: str) -> Dict[str, bool]:
        return {}

    def binary_string(self) -> str:
        return ''


class Broadcaster(Module):
    def __init__(self, name: str, srcs: List[str], dsts: List[str]):
        super().__init__(name, srcs, dsts)

    def pulse(self, pulse: bool, sender: str) -> Dict[str, bool]:
        return {d: pulse for d in self.dsts}


class FlipFlop(Broadcaster):
    def __init__(self, name: str, srcs: List[str], dsts: List[str]):
        super().__init__(name, srcs, dsts)
        self.is_on = False

    def pulse(self, pulse: bool, sender: str) -> Dict[str, bool]:
        if pulse:
            return {}
        self.is_on = not self.is_on
        return super().pulse(self.is_on, sender)

    def binary_string(self) -> str:
        return '1' if self.is_on else '0'


class Conjunction(Broadcaster):
    def __init__(self, name: str, srcs: List[str], dsts: List[str]):
        super().__init__(name, srcs, dsts)
        self.remembered_pulses = {s: False for s in self.srcs}

    def pulse(self, pulse: bool, sender: str) -> Dict[str, bool]:
        self.remembered_pulses[sender] = pulse
        return super().pulse(not all(self.remembered_pulses.values()), sender)

    def binary_string(self) -> str:
        return ''.join('1' if self.remembered_pulses[s] else '0' for s in self.srcs)


MODULE_TYPES = {
    '': Broadcaster,
    '%': FlipFlop,
    '&': Conjunction,
    'none': Module
}


def to_modules(data) -> Dict[str, Module]:
    module_data = {n: (t, n, [], []) for t, n, _ in data}
    for type, name, dsts in data:
        module_data[name] = type, name, module_data[name][2], dsts
        for dst in dsts:
            if dst not in module_data:
                module_data[dst] = ('none', dst, [], [])
            module_data[dst][2].append(name)
    modules = {}
    for name, (type, _, srcs, dsts) in module_data.items():
        modules[name] = MODULE_TYPES[type](name, srcs, dsts)
    return modules


def push_button(modules: Dict[str, Module]) -> Optional[Tuple[int, int]]:
    num_high, num_low = 0, 1  # 1 for button push
    queue = deque()
    queue.append(('START', False, 'button'))
    while len(queue) > 0:
        name, pulse, src = queue.popleft()
        if name == 'END' and not pulse:
            return None
        outputs = modules[name].pulse(pulse, src)
        for dst, dst_pulse in outputs.items():
            queue.append((dst, dst_pulse, name))
            if dst_pulse:
                num_high += 1
            else:
                num_low += 1
    return num_high, num_low


class Day(Day2023):
    @property
    def num(self) -> int:
        return 20

    def get_data(self, example=False):
        lines = super().get_data(example)
        data = []
        for line in lines:
            if line[1] not in 'TZA':
                continue
            match = re.fullmatch(r'([%&]*)([a-z]+) -> ([a-z ,]+)', line, re.IGNORECASE)
            assert match is not None
            data.append((match.group(1), match.group(2), match.group(3).split(', ')))
        return data

    def puzzle1(self):
        return
        data = self.get_data()
        modules = to_modules(data)
        num_high, num_low = 0, 0
        for _ in range(1000):
            hi, lo = push_button(modules)
            num_high += hi
            num_low += lo
        print(num_high * num_low)

    def puzzle2(self):
        data = self.get_data()
        modules = to_modules(data)
        names = list(sorted(modules.keys()))
        seen = set()
        for i in itertools.count(1):
            binstr = ''.join(modules[n].binary_string() for n in names)
            print(binstr)
            if binstr in seen:
                assert False
            seen.add(binstr)
            res = push_button(modules)
            if res is None:
                print(i)
                break
        binstr = ''.join(modules[n].binary_string() for n in names)
        print(binstr)
        push_button(modules)
        binstr = ''.join(modules[n].binary_string() for n in names)
        print(binstr)


def one_line():
    pass
