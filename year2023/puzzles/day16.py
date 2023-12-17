import itertools

from year2023.day2023 import Day2023
from typing import *
import sys
from collections import deque


MIRRORS = {
    '.': {
        1: [1],
        -1: [-1],
        1j: [1j],
        -1j: [-1j],
    },
    '/': {
        1: [-1j],
        -1: [1j],
        1j: [-1],
        -1j: [1]
    },
    '\\': {
        1: [1j],
        -1: [-1j],
        1j: [1],
        -1j: [-1],
    },
    '|': {
        1: [1],
        -1: [-1],
        1j: [1, -1],
        -1j: [1, -1],
    },
    '-': {
        1: [1j, -1j],
        -1: [1j, -1j],
        1j: [1j],
        -1j: [-1j],
    }
}


def num_energized(data, pos: complex, drctn: complex) -> int:
    energized = set()
    queue = deque()
    queue.append((pos, drctn))
    while len(queue) > 0:
        pos, drctn = queue.pop()
        if pos not in data:
            continue
        if (pos, drctn) in energized:
            continue
        energized.add((pos, drctn))
        new_drctns = MIRRORS[data[pos]][drctn]
        for new_drctn in new_drctns:
            queue.append((pos + new_drctn, new_drctn))
    return len(set(e[0] for e in energized))


class Day(Day2023):
    @property
    def num(self) -> int:
        return 16

    def get_data(self, example=False):
        lines = super().get_data(example)
        data = {r + c * 1j: lines[r][c] for r, c in itertools.product(range(len(lines)), range(len(lines[0])))}
        return data, len(lines), len(lines[0])

    def puzzle1(self):
        data, _, _ = self.get_data()
        print(num_energized(data, 0, 1j))

    def puzzle2(self):
        data, nrows, ncols = self.get_data()
        best = -1
        for row in range(nrows):
            energized = max(num_energized(data, row, 1j), num_energized(data, row + (ncols - 1) * 1j, -1j))
            if energized > best:
                best = energized
        for col in range(ncols):
            energized = max(num_energized(data, col * 1j, 1), num_energized(data, nrows - 1 + col * 1j, -1))
            if energized > best:
                best = energized
        print(best)



def one_line():
    pass
