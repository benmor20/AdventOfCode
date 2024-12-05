import itertools

from year2024.day2024 import Day2024
from typing import *


DRCTNS = [drctn for drctn in itertools.product(range(-1, 2), range(-1, 2)) if drctn != (0, 0)]


def add_tuple(p1, p2):
    return p1[0] + p2[0], p1[1] + p2[1]


def mult_tuple(tup, scale):
    return tup[0] * scale, tup[1] * scale


class Day(Day2024):
    @property
    def num(self) -> int:
        return 4

    def puzzle1(self):
        data = self.get_data()
        rows, cols = len(data), len(data[0])
        num_xmas = 0
        for x, y in itertools.product(range(rows), range(cols)):
            if data[x][y] == 'X':
                for drctn in DRCTNS:
                    is_xmas = True
                    for idx, letter in enumerate('XMAS'):
                        newx, newy = add_tuple((x, y), mult_tuple(drctn, idx))
                        if newx < 0 or newx >= rows or newy < 0 or newy >= cols or data[newx][newy] != letter:
                            is_xmas = False
                            break
                    num_xmas += is_xmas
        print(num_xmas)

    def puzzle2(self):
        data = self.get_data()
        rows, cols = len(data), len(data[0])
        num_xmas = 0
        for x, y in itertools.product(range(1, rows - 1), range(1, cols - 1)):
            pos = (x, y)
            if data[x][y] == 'A':
                tl = add_tuple(pos, (1, 1))
                br = add_tuple(pos, (-1, -1))
                tr = add_tuple(pos, (1, -1))
                bl = add_tuple(pos, (-1, 1))
                tl_let = data[tl[0]][tl[1]]
                br_let = data[br[0]][br[1]]
                tr_let = data[tr[0]][tr[1]]
                bl_let = data[bl[0]][bl[1]]
                if f'{tl_let}{br_let}' in ('SM', 'MS') and f'{tr_let}{bl_let}' in ('SM', 'MS'):
                    num_xmas += 1
        print(num_xmas)


import numpy as np
from scipy.signal import correlate2d


def one_line():
    return '\n'.join([grid := np.array([['XMAS'.index(c) for c in line.strip()] for line in open('year2024/data/day4data.txt', 'r').readlines()]), p1base := np.array([[1, 4, 16, 64]]), p1kernels := [p1base, p1base.T, np.diagflat(p1base), np.diagflat(p1base)[::-1, :]], str(sum(np.sum(np.isin(correlate2d(grid, kernel, fillvalue=1), [27, 228])) for kernel in p1kernels)), str(np.sum(np.isin(correlate2d(grid, np.array([[1, 0, 4], [0, 16, 0], [64, 0, 256]])), [367, 487, 997, 877])))][-2:])
