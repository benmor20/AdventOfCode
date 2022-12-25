import itertools

from year2022.day2022 import Day2022
from typing import *


ROCKS = [
    {0, 1, 2, 3},
    {1, 1j, 1+1j, 2+1j, 1+2j},
    {0, 1, 2, 2+1j, 2+2j},
    {0, 1j, 2j, 3j},
    {0, 1, 1j, 1+1j}
]


class Rock:
    def __init__(self, rock_type: int, pos: complex):
        self._rock_type = rock_type
        self._pos = pos

    @property
    def pos(self) -> complex:
        return self._pos

    @property
    def points(self) -> Set[complex]:
        return {p + self.pos for p in ROCKS[self._rock_type]}

    def update_pos(self, amt: complex):
        self._pos += amt

    def hit_wall(self, fallen: Set[complex]) -> bool:
        if any(p.real < 0 or p.imag < 1 or p.real > 6 for p in self.points):
            return True
        return any(p in fallen for p in self.points)

    def push_and_fall(self, arrow: str, fallen: Set[complex]) -> Tuple[bool, Set[complex]]:
        drctn = 1 if arrow == '>' else -1
        self.update_pos(drctn)
        if self.hit_wall(fallen):
            self.update_pos(-drctn)
        self.update_pos(-1j)
        done = self.hit_wall(fallen)
        if done:
            self.update_pos(1j)
            fallen.update(self.points)
        return done, fallen

    def heights(self) -> List[int]:
        return [max([int(p.imag) for p in self.points if p.real == i] + [0]) for i in range(7)]


def print_cave(rock: Optional[Rock], fallen: Set[complex], max_height: int):
    for y in range(max_height + 6, 0, -1):
        print('|' + ''.join('@' if rock is not None and x+y*1j in rock.points else ('#' if x+y*1j in fallen else '.') for x in range(7)) + '|')
    print('+-------+\n')


def drop_rock(data: str, vent_idx: int, rock_num: int, height: int, fallen: Set[complex]) -> Tuple[Set[complex], int, int]:
    rock = Rock(rock_num, 2 + (height + 4) * 1j)
    # print_cave(rock, fallen, height)
    while True:
        done, fallen = rock.push_and_fall(data[vent_idx], fallen)
        vent_idx += 1
        vent_idx %= len(data)
        if done:
            rock_height = int(max(p.imag for p in rock.points))
            if rock_height > height:
                height = rock_height
            break
    return fallen, vent_idx, height


def drop_nrocks(data: str, nrocks: int, fallen: Optional[Set[complex]] = None, rock_type: int = 0, vent_idx: int = 0) -> int:
    max_height = 0 if fallen is None else int(max(p.imag for p in fallen))
    og_height = max_height
    if fallen is None:
        fallen = set()
    for i in range(nrocks):
        # print(f'rock_type = {(i + rock_type) % len(ROCKS)}, {vent_idx = }, height = {max_height - og_height}')
        fallen, vent_idx, max_height = drop_rock(data, vent_idx, (i + rock_type) % len(ROCKS), max_height, fallen)
        # print_cave(None, fallen, height)
    return max_height - og_height


def find_cycle(order: List) -> Tuple[int, int]:
    for i in range(2, len(order), 2):
        period = i // 2
        if order[-period:] == order[-i:-period]:
            return len(order) - i, period
    return len(order), 0


def drop_until_cycle(data) -> Tuple[Set[complex], int, int, int, int, int, int]:
    fallen = set()
    max_height = 0
    vent_idx = 0
    order = []
    heights = []
    for i in itertools.count():
        state = i % len(ROCKS), vent_idx
        order.append(state)
        heights.append(max_height)
        # print(f'{state}\t{i}\t{max_height}')
        fallen, vent_idx, max_height = drop_rock(data, vent_idx, i % len(ROCKS), max_height, fallen)
        startup, period = find_cycle(order)
        if period > 0:
            return fallen, startup, heights[startup], period, heights[period + startup] - heights[startup], (i + 1) % len(ROCKS), vent_idx
        # print_cave(None, fallen, max_height)


def height_after_nrocks(data: str, nrocks: int) -> int:
    fallen, startup_amt, startup_height, period_amt, period_height, nxt_rock, vent_idx = drop_until_cycle(data)
    nperiods, nleft = divmod(nrocks - startup_amt, period_amt)
    rem_height = 0 if nleft == 0 else drop_nrocks(data, nleft, fallen, nxt_rock, vent_idx)
    # print(f'{startup_amt = }, {startup_height = }, {period_amt = }, {period_height = }, {nperiods = }, {nleft = }, {rem_height = }')
    return startup_height + nperiods * period_height + rem_height


class Day(Day2022):
    @property
    def num(self) -> int:
        return 17

    def get_data(self, example=False):
        lines = super().get_data(example)
        return lines[0]

    def puzzle1(self):
        data = self.get_data()
        print(drop_nrocks(data, 2022))

    def puzzle2(self):
        data = self.get_data()
        print(height_after_nrocks(data, 1000000000000))
