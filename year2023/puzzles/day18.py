import itertools

from year2023.day2023 import Day2023
from typing import *
import re
import numpy as np


DIRECTION_STRINGS = 'RDLU'
DIRECTIONS = {
    'U': -1,
    'D': 1,
    'L': -1j,
    'R': 1j
}


def print_board(board):
    for row in range(int(min(p.real for p in board)), int(max(p.real for p in board)) + 1):
        for col in range(int(min(p.imag for p in board)), int(max(p.imag for p in board)) + 1):
            pos = row + col * 1j
            print('S' if pos == 0 else ('#' if pos in board else '.'), end='')
        print()
    print()


# https://stackoverflow.com/questions/41077185/fastest-way-to-shoelace-formula
def shoelace(x_y):
    x_y = np.array(x_y)
    x_y = x_y.reshape(-1,2)

    x = x_y[:,0]
    y = x_y[:,1]

    S1 = np.sum(x*np.roll(y,-1))
    S2 = np.sum(y*np.roll(x,-1))

    area = .5*np.absolute(S1 - S2)

    return area


class Day(Day2023):
    @property
    def num(self) -> int:
        return 18

    def get_data(self, example=False):
        lines = super().get_data(example)
        data = []
        for line in lines:
            match = re.fullmatch(r'([A-Z]) (\d+) \(#([a-z\d]+)\)', line)
            data.append((match.group(1), int(match.group(2)), match.group(3)))
        return data

    def puzzle1(self):
        data = self.get_data()
        exterior = {0}
        pos = 0
        for drctn_str, dist, _ in data:
            drctn = DIRECTIONS[drctn_str]
            exterior.update(pos + drctn * (d + 1) for d in range(dist))
            pos += drctn * dist

        interior = set()
        queue = [1 + 1j]  # Not necessarily a good start but works on test and my actual
        while len(queue) > 0:
            pos = queue.pop()
            interior.add(pos)
            for drctn in (1, -1, 1j, -1j):
                new_pos = pos + drctn
                if new_pos not in exterior and new_pos not in interior:
                    queue.append(new_pos)
        print(len(interior.union(exterior)))

    def puzzle2(self):
        data = self.get_data()
        len_ext = 0
        coords = []
        pos = 0
        part2 = True
        for drctn_str, dist, hexcode in data:
            if part2:
                dist = int(hexcode[:-1], 16)
                drctn_str = DIRECTION_STRINGS[int(hexcode[-1])]
            drctn = DIRECTIONS[drctn_str]
            len_ext += dist
            coords.append([pos.real, pos.imag])
            pos += drctn * dist
        print('Shoelace')
        len_int = shoelace(coords)
        print(len_int + len_ext // 2 + 1)


def one_line():
    pass
