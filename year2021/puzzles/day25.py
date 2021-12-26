from year2021.day2021 import Day2021
import numpy as np
from scipy.signal import correlate2d
import itertools


west_kernel = np.array([[0, 0, 0], [10, 1, 0], [0, 0, 0]])
north_kernel = np.array([[0, 10, 0], [0, 1, 0], [0, 0, 0]])
east_kernel = np.array([[0, 0, 0], [0, 1, 10], [0, 0, 0]])
south_kernel = np.array([[0, 0, 0], [0, 1, 0], [0, 10, 0]])


def step_dir(grid, dir, kernel1, kernel2):
    empty = grid == 0
    direc = grid == dir
    corr = 2 * direc + empty
    move = correlate2d(corr, kernel1, mode='same', boundary='wrap') == 21
    leave = correlate2d(corr, kernel2, mode='same', boundary='wrap') == 12
    grid[move] = dir
    grid[leave] = 0
    return grid


def step(grid):
    grid = step_dir(grid, 1, west_kernel, east_kernel)
    grid = step_dir(grid, 2, north_kernel, south_kernel)
    return grid


class Day(Day2021):
    @property
    def num(self) -> int:
        return 25

    @property
    def year(self) -> int:
        return 2021

    def get_data(self, example=False):
        lines = super().get_data(example)
        data = []
        for line in lines:
            row = []
            for c in line:
                if c == '>':
                    row.append(1)
                elif c == 'v':
                    row.append(2)
                else:
                    row.append(0)
            data.append(row)
        return np.array(data)

    def puzzle1(self):
        grid = self.get_data()
        for i in itertools.count():
            prev = grid.copy()
            grid = step(grid)
            if np.all(grid == prev):
                print(i + 1)
                return

    def puzzle2(self):
        pass
