import itertools

from year2022.day2022 import Day2022
from typing import *
from collections import Counter


def rectangle(elves: Set[complex]) -> Tuple[complex, complex]:
    minx = int(min(e.real for e in elves))
    maxx = int(max(e.real for e in elves))
    miny = int(min(e.imag for e in elves))
    maxy = int(max(e.imag for e in elves))
    return minx+miny*1j, maxx+maxy*1j


def rectangle_size(elves: Set[complex]) -> int:
    tl, br = rectangle(elves)
    return int((br.real - tl.real + 1) * (br.imag - tl.imag + 1))


def print_elves(elves: Set[complex]):
    tl, br = rectangle(elves)
    for y in range(int(tl.imag) - 1, int(br.imag) + 2):
        for x in range(int(tl.real) - 1, int(br.real) + 2):
            elf = x+y*1j
            print('#' if elf in elves else '.', end='')
        print()
    print()


def perform_round(elves: Set[complex], order: List[Tuple[complex, complex, complex]]) -> Set[complex]:
    proposals = {}
    for elf in elves:
        if not any(elf+d in elves for d in (1, -1, 1j, -1j, 1+1j, 1-1j, -1+1j, -1-1j)):
            # print(f'No elves adjacent to {elf}')
            continue
        for chk in order:
            if any(elf+c in elves for c in chk):
                # print(f'{elf} cant go {chk[0]}')
                continue
            # print(f'{elf} proposes to go {chk[0]} (to {elf+chk[0]})')
            proposals[elf] = elf+chk[0]
            break
    # print(proposals)
    prop_cnt = Counter(proposals.values())
    new_elves = set()
    for elf in elves:
        if elf not in proposals:
            new_elves.add(elf)
            continue
        prop = proposals[elf]
        if prop_cnt[prop] > 1:
            new_elves.add(elf)
        else:
            new_elves.add(prop)
    return new_elves


class Day(Day2022):
    @property
    def num(self) -> int:
        return 23

    def get_data(self, example=False):
        lines = super().get_data(example)
        data = set()
        for y, line in enumerate(lines):
            for x, c in enumerate(line):
                if c == '#':
                    data.add(x + y*1j)
        return data

    def puzzle1(self):
        elves = self.get_data()
        order = [(-1j, -1j+1, -1j-1), (1j, 1j+1, 1j-1), (-1, -1+1j, -1-1j), (1, 1+1j, 1-1j)]
        for _ in range(10):
            elves = perform_round(elves, order)
            temp = order.pop(0)
            order.append(temp)
        print(rectangle_size(elves) - len(elves))

    def puzzle2(self):
        elves = self.get_data()
        order = [(-1j, -1j + 1, -1j - 1), (1j, 1j + 1, 1j - 1), (-1, -1 + 1j, -1 - 1j), (1, 1 + 1j, 1 - 1j)]
        for i in itertools.count(1):
            new_elves = perform_round(elves, order)
            if new_elves == elves:
                break
            elves = new_elves
            temp = order.pop(0)
            order.append(temp)
        print(i)
