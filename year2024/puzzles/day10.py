from year2024.day2024 import Day2024
from typing import *


DIRECTIONS = [1, -1, 1j, -1j]


class Day(Day2024):
    @property
    def num(self) -> int:
        return 10

    def get_data(self, example=False):
        lines = super().get_data(example)
        data = {}
        for i, line in enumerate(lines):
            for j, c in enumerate(line):
                data[i + j * 1j] = int(c)
        return data

    def do_puzzle(self, part1, example=False):
        data = self.get_data(example)
        trailheads = [pos for pos, lvl in data.items() if lvl == 0]
        total = 0
        for trailhead in trailheads:
            queue = [trailhead]
            seen = set()
            ends = []
            while len(queue) > 0:
                node = queue.pop()
                seen.add(node)
                if data[node] == 9:
                    ends.append(node)
                    continue
                for drctn in DIRECTIONS:
                    nxt = node + drctn
                    if nxt in data and data[nxt] == data[node] + 1:
                        queue.append(nxt)
            total += len(set(ends) if part1 else ends)
        print(total)

    def puzzle1(self):
        self.do_puzzle(True)

    def puzzle2(self):
        self.do_puzzle(False)


def one_line():
    pass
