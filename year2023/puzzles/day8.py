import itertools
import re
from math import lcm
from year2023.day2023 import Day2023
from typing import *


DIRS = {'R': 1, 'L': 0}


def repeat(string):
    while True:
        yield from string


def repeat_with_idx(string):
    while True:
        yield from enumerate(string)


class State:
    def __init__(self, node, instr_idx, first_step_cnt):
        self.node = node
        self.instr_idx = instr_idx
        self.first_step_count = first_step_cnt

    def __hash__(self):
        return hash((self.node, self.instr_idx))

    def __eq__(self, other):
        return self.node == other.node and self.instr_idx == other.instr_idx

    def __repr__(self):
        return str((self.node, self.instr_idx))


class Day(Day2023):
    @property
    def num(self) -> int:
        return 8

    def get_data(self, example=False):
        text = super().get_raw_data(example)
        instr, node_str = tuple(text.split('\n\n'))
        nodes = {}
        for line in node_str.split('\n'):
            match = re.match(r'([A-Z\d]+) = \(([A-Z\d]+), ([A-Z\d]+)\)', line)
            nodes[match.group(1)] = (match.group(2), match.group(3))
        return instr, nodes

    def puzzle1(self):
        instr, nodes = self.get_data()
        current_node = 'AAA'
        step_cnt = 0
        for dir in repeat(instr):
            if current_node == 'ZZZ':
                break
            step_cnt += 1
            current_node = nodes[current_node][DIRS[dir]]
        print(step_cnt)

    def puzzle2(self):
        instr, nodes = self.get_data()
        start_nodes = [n for n in nodes if n[-1] == 'A']
        ans = 1
        for node in start_nodes:
            step_cnt = 0
            for dir in repeat(instr):
                if node[-1] == 'Z':
                    break
                step_cnt += 1
                node = nodes[node][DIRS[dir]]
            ans = lcm(ans, step_cnt)
        print(ans)


def one_line():
    pass
