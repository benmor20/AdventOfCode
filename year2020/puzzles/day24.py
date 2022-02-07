import numpy as np
from scipy.signal import correlate

from year2020.day2020 import Day2020
from utils.utils import *


drctn_updates = {
    'e': 1 + 0j,
    'w': -1 + 0j,
    'ne': 1 + 1j,
    'nw': 0 + 1j,
    'se': 0 - 1j,
    'sw': -1 - 1j
}

kernel = np.array([[1,  1, 0],
                   [1, 10, 1],
                   [0,  1, 1]])
lookup_table = np.zeros(17)
lookup_table[np.array([2, 11, 12])] = 1


def index_from_complex(cmplx):
    return int(cmplx.real), int(cmplx.imag)


def get_tile(instruction):
    return sum(drctn_updates[i] for i in instruction)


def print_hex_grid(grid):
    for i, row in enumerate(grid):
        d, m = divmod(len(grid) - i, 2)
        if m == 1:
            print(' ', end='')
        print('. ' * d, end='')
        print(' '.join('#' if v == 1 else '.' for v in row), end='')
        print(' .' * (i // 2))


class Day(Day2020):
    @property
    def num(self) -> int:
        return 24

    def get_data(self, example=False):
        lines = super().get_data(example)
        data = []
        for line in lines:
            i = 0
            instr = []
            while i < len(line):
                c = line[i]
                if c in 'sn':
                    instr.append(line[i:i+2])
                    i += 2
                else:
                    instr.append(c)
                    i += 1
            data.append(instr)
        return data

    def puzzles(self):
        instructions = self.get_data(True)
        black_tiles = set()

        for instr in instructions:
            tile = get_tile(instr)
            if tile in black_tiles:
                black_tiles.remove(tile)
            else:
                black_tiles.add(tile)
        print(f'On day 0 there are {len(black_tiles)} black tiles')
        print(f'The black tiles are {black_tiles}')

        large_num = max(len(i) for i in instructions) + 1
        lo = large_num + large_num * 1j
        hi = -lo
        for tile in black_tiles:
            lo = min(lo.real, tile.real) + min(lo.imag, tile.imag) * 1j
            hi = max(hi.real, tile.real) + max(hi.imag, tile.imag) * 1j
        grid_size = hi - lo + 1 + 1j

        grid = np.zeros(index_from_complex(grid_size))
        for tile in black_tiles:
            grid[index_from_complex(tile - lo)] = 1
        print_hex_grid(grid)

        print(f'Day 0: {int(np.sum(grid))}')
        for i in range(1, 101):
            corr = correlate(grid, kernel).astype(int)
            grid = lookup_table[corr]
            print(f'Day {i}: {int(np.sum(grid))}')
            if i <= 20:
                print_hex_grid(grid)
