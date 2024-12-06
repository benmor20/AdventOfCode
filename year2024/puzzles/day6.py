from year2024.day2024 import Day2024
from typing import *


DIRECTIONS = [-1, 1j, 1, -1j]


class Day(Day2024):
    @property
    def num(self) -> int:
        return 6

    def get_data(self, example=False):
        lines = super().get_data(example)
        obs = set()
        free = set()
        guard = None
        for i, line in enumerate(lines):
            for j, c in enumerate(line):
                pos = i + j * 1j
                if c == '#':
                    obs.add(pos)
                elif c == '^':
                    assert guard is None
                    guard = pos
                    free.add(pos)
                else:
                    free.add(pos)
        return free, obs, guard

    def puzzle1(self):
        free, obs, pos = self.get_data()
        drctn_idx = 0
        drctn = DIRECTIONS[drctn_idx]
        seen = set()
        while pos in free:
            seen.add(pos)
            new_pos = pos + drctn
            if new_pos in obs:
                drctn_idx += 1
                drctn_idx %= len(DIRECTIONS)
                drctn = DIRECTIONS[drctn_idx]
            else:
                pos = new_pos
        print(len(seen))

    def puzzle2(self):
        og_free, og_obs, og_pos = self.get_data()
        total = 0
        for test_place in og_free:
            if test_place == og_pos:
                continue
            free = og_free.copy()
            free.remove(test_place)
            obs = og_obs.copy()
            obs.add(test_place)
            seen = set()
            pos = og_pos
            drctn_idx = 0
            drctn = DIRECTIONS[drctn_idx]
            while pos in free:
                if (pos, drctn) in seen:
                    total += 1
                    break
                seen.add((pos, drctn))
                new_pos = pos + drctn
                if new_pos in obs:
                    drctn_idx += 1
                    drctn_idx %= len(DIRECTIONS)
                    drctn = DIRECTIONS[drctn_idx]
                else:
                    pos = new_pos
        print(total)


def one_line():
    pass
