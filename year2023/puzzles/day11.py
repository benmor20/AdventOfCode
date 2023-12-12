import itertools

from year2023.day2023 import Day2023
from typing import *
import numpy as np


class Day(Day2023):
    @property
    def num(self) -> int:
        return 11

    def get_data(self, example=False):
        lines = super().get_data(example)
        data = [[1 if c == '#' else 0 for c in line] for line in lines]
        galaxies = set()
        for ridx, row in enumerate(data):
            for cidx, elem in enumerate(row):
                if elem == 1:
                    galaxies.add(ridx + cidx * 1j)
        return data, galaxies

    def puzzle1(self):
        data, galaxies = self.get_data()
        arr = np.array(data)
        empty_rows = set(i for i in range(arr.shape[0]) if np.all(arr[i, :] == 0))
        empty_cols = set(i for i in range(arr.shape[1]) if np.all(arr[:, i] == 0))
        total_dist = 0
        for g1, g2 in itertools.combinations(galaxies, r=2):
            dist = 0
            minrow = int(min(g1.real, g2.real))
            maxrow = int(max(g1.real, g2.real))
            for row in range(minrow, maxrow):
                dist += 1000000 if row in empty_rows else 1
            mincol = int(min(g1.imag, g2.imag))
            maxcol = int(max(g1.imag, g2.imag))
            for col in range(mincol, maxcol):
                dist += 1000000 if col in empty_cols else 1
            # print(f'Dist from {g1} to {g2} is {dist}')
            total_dist += dist
        print(total_dist)

    def puzzle2(self):
        data = self.get_data(True)


def one_line():
    pass
