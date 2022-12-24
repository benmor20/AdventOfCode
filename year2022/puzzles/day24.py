from year2022.day2022 import Day2022
from typing import *
import math
from collections import deque


BLIZZARD_MEMO = {}


def move_blizzards(blizzards: FrozenSet[Tuple[complex, complex]], max_size: complex, time: int) -> FrozenSet[Tuple[complex, complex]]:
    real_time = time % math.lcm(int(max_size.real) - 1, int(max_size.imag) - 1)
    if real_time in BLIZZARD_MEMO:
        return BLIZZARD_MEMO[real_time]
    new_bliz = set()
    for pos, drctn in blizzards:
        new_pos = pos + drctn
        if new_pos.real == 0:
            new_pos = max_size.real - 1 + new_pos.imag * 1j
        elif new_pos.real == max_size.real:
            new_pos = 1 + new_pos.imag * 1j
        elif new_pos.imag == 0:
            new_pos = new_pos.real + max_size.imag * 1j - 1j
        elif new_pos.imag == max_size.imag:
            new_pos = new_pos.real + 1j
        new_bliz.add((new_pos, drctn))
    BLIZZARD_MEMO[real_time] = blizzards
    return frozenset(new_bliz)


def min_moves(blizzard: FrozenSet[Tuple[complex, complex]], size: complex):
    new_blizz = blizzard.copy()
    lcm = math.lcm(int(size.real) - 1, int(size.imag) - 1)
    for i in range(lcm):
        new_blizz = move_blizzards(new_blizz, size, i)
    seen = set()
    queue = deque()
    queue.append((1, 0, 0))
    parents = {(1, 0, 0): None}
    while len(queue) > 0:
        pos, time, state = queue.popleft()
        blizz = {b[0] for b in BLIZZARD_MEMO[(time+1) % lcm]}
        for move in (0, 1, -1, 1j, -1j):
            new_pos = pos + move
            if new_pos == size - 1 and state == 2:
                parents[(new_pos, time+1, state)] = pos, time, state
                return time + 1, parents
            if not (0 < new_pos.real < size.real) or not (0 < new_pos.imag < size.imag) and new_pos != 1 and new_pos != size - 1:
                continue
            new_state = state
            if (state == 0 and new_pos == size - 1) or (state == 1 and new_pos == 1):
                new_state += 1
            nxt = new_pos, time + 1, new_state
            if new_pos in blizz or nxt in seen:
                continue
            seen.add(nxt)
            queue.append(nxt)
            parents[nxt] = (pos, time, state)
    return -1, parents


def print_blizzard(blizz, size, cur_pos):
    nper = Counter(b[0] for b in blizz)
    to_drctn = {p: d for p, d in blizz if nper[p] == 1}
    drctn_map = {1: '>', -1: '<', 1j: 'v', -1j: '^'}
    for y in range(int(size.imag) + 1):
        for x in range(int(size.real) + 1):
            pos = x + y*1j
            if pos == cur_pos:
                print('E', end='')
                continue
            if pos in (1, size - 1):
                print('.', end='')
                continue
            if pos.real in (0, size.real) or pos.imag in (0, size.imag):
                print('#', end='')
                continue
            if nper[pos] == 0:
                print('.', end='')
                continue
            if nper[pos] == 1:
                print(drctn_map[to_drctn[pos]], end='')
                continue
            print(nper[pos], end='')
        print()
    print()


class Day(Day2022):
    @property
    def num(self) -> int:
        return 24

    def get_data(self, example=False):
        lines = super().get_data(example)
        data = set()
        for y, line in enumerate(lines):
            for x, c in enumerate(line):
                pos = x+y*1j
                if c == '>':
                    data.add((pos, 1))
                elif c == '<':
                    data.add((pos, -1))
                elif c == '^':
                    data.add((pos, -1j))
                elif c == 'v':
                    data.add((pos, 1j))
        return frozenset(data), (len(lines[0]) + len(lines) * 1j - 1 - 1j)

    def puzzle1(self):
        blizzards, size = self.get_data()
        res, paths = min_moves(blizzards, size)
        print(res)

    def puzzle2(self):
        data = self.get_data(True)
