import itertools

from year2023.day2023 import Day2023
from typing import *


def simulate_steps(plots: Set[complex], start: complex, nsteps: Union[int, List[int]]) -> List[int]:
    if isinstance(nsteps, int):
        nsteps = [nsteps]
    allowed_poses = {start}
    res = []
    for n in range(nsteps[-1]):
        new_poses = set()
        for pos in allowed_poses:
            for drctn in (1, -1, 1j, -1j):
                new_pos = pos + drctn
                if new_pos in plots:
                    new_poses.add(new_pos)
        allowed_poses = new_poses
        if n + 1 in nsteps:
            res.append(len(allowed_poses))

    # nrows = int(max(p.real for p in plots)) + 1
    # ncols = int(max(p.imag for p in plots)) + 1
    # for r in range(nrows):
    #     if r % 7 == 0:
    #         print('-' * (ncols + ncols // 7 + 1))
    #     for c in range(ncols):
    #         if c % 7 == 0:
    #             print('|', end='')
    #         pos = r + c * 1j
    #         print('O' if pos in allowed_poses else ('.' if pos in plots else '#'), end='')
    #     print('|')
    # print('-' * (ncols + ncols // 7 + 1))

    return res


class Day(Day2023):
    @property
    def num(self) -> int:
        return 21

    def get_data(self, example=False):
        lines = super().get_data(example)
        plots = set()
        rocks = set()
        start = -1
        for row, line in enumerate(lines):
            for col, c in enumerate(line):
                pos = row + col * 1j
                if c == 'S':
                    assert start == -1
                    start = pos
                    plots.add(pos)
                elif c == '.':
                    plots.add(pos)
                elif c == '#':
                    rocks.add(pos)
                else:
                    assert False
        return plots, rocks, start

    def puzzle1(self):
        is_ex = False
        NUM_STEPS = 6 if is_ex else 64
        plots, rocks, start = self.get_data(is_ex)
        print(simulate_steps(plots, start, NUM_STEPS))

    def puzzle2(self):
        is_ex = False
        NUM_STEPS = 45 if is_ex else 26501365

        if is_ex:
            plots = set(r + c * 1j for r, c in itertools.product(range(NUM_STEPS * 2 + 1), repeat=2))
            start = NUM_STEPS + NUM_STEPS * 1j
            ans = simulate_steps(plots, start, NUM_STEPS)[0]
            print(ans)

        plots, _, start = self.get_data(2 if is_ex else False)
        nrows = int(max(p.real for p in plots)) + 1  # for input, nrows == ncols

        full_square_steps = NUM_STEPS // nrows - 1
        print(full_square_steps)
        num_full_squares = 2 * (full_square_steps ** 2 + full_square_steps) + 1
        num_full_outer_color = (full_square_steps + 1) ** 2
        num_full_odd = num_full_outer_color if NUM_STEPS % 2 == 0 else (num_full_squares - num_full_outer_color)
        num_full_even = num_full_squares - num_full_odd
        print(num_full_odd, num_full_even)

        full_square_odd, full_square_even = simulate_steps(plots, start, [nrows, nrows + 1])
        print(full_square_odd, full_square_even)
        total = num_full_odd * full_square_odd + num_full_even * full_square_even
        big_square_steps = nrows + nrows // 2 - 1
        little_square_steps = nrows // 2 - 1
        for new_start in (0, nrows - 1, (nrows - 1) * 1j, nrows - 1 + (nrows - 1) * 1j):
            little_amt, big_amt = tuple(simulate_steps(plots, new_start, [little_square_steps, big_square_steps]))
            total += full_square_steps * big_amt + (full_square_steps + 1) * little_amt
        for new_start in (start.real, start.imag * 1j, start.real + (nrows - 1) * 1j, nrows - 1 + start.imag * 1j):
            total += simulate_steps(plots, new_start, nrows - 1)[0]
        print(total)


def one_line():
    pass
