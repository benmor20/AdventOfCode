from year2023.day2023 import Day2023
from typing import *
import re
import numpy as np


class Day(Day2023):
    @property
    def num(self) -> int:
        return 4

    def get_data(self, example=False):
        lines = super().get_data(example)
        data = []
        for line in lines:
            line = line.split(': ')[1]
            win_str, has_str = tuple(line.split(' | '))
            win, has = set(), set()
            for match in re.split(' +', win_str):
                match = match.strip()
                if len(match) == 0:
                    continue
                win.add(int(match))
            for match in re.split(' +', has_str):
                match = match.strip()
                if len(match) == 0:
                    continue
                has.add(int(match))
            data.append((win, has))
        return data

    def puzzle1(self):
        data = self.get_data()
        total = 0
        for win, has in data:
            intersect = win.intersection(has)
            num_intersect = len(intersect)
            if num_intersect == 0:
                continue
            total += 2 ** (num_intersect - 1)
        print(total)

    def puzzle2(self):
        data = self.get_data()
        copies = np.ones((len(data),), dtype=int)
        for idx, (win, has) in enumerate(data[:-1]):
            intersect = win.intersection(has)
            num_intersect = len(intersect)
            copies[idx+1:min(len(data), idx+num_intersect+1)] += copies[idx]
        print(sum(copies))


def one_line():
    return '\n'.join([stripped := [line.split(': ')[1] for line in open('year2023/data/day4data.txt', 'r').readlines()], overlap := [len({int(i) for i in re.split(' +', line.split(' | ')[0]) if len(i) > 0}.intersection({int(i) for i in re.split(' +', line.split(' | ')[1]) if len(i) > 0})) for line in stripped], str(sum(int(2 ** (num - 1)) for num in overlap)), ''][-2:])
