from year2020.day2020 import Day2020

from scipy.signal import correlate
import numpy as np


def make_kernel(dims):
    kernel = np.ones([3 for _ in range(dims)])
    kernel[tuple(1 for _ in range(dims))] = 0
    return kernel.astype(int)


KERNEL = make_kernel(3)


def print_grid(grid, logical=True):
    if len(grid.shape) == 4:
        for space in grid:
            print_grid(space, logical)
            print()
    else:
        for plane in grid:
            for row in plane:
                if logical:
                    print(''.join(['#' if v else '.' for v in row]))
                else:
                    print(''.join([str(int(v)) for v in row]))
            print()


def truncate_grid(grid):
    ranges = []
    for i, s in enumerate(grid.shape):
        slices = [slice(None) for _ in range(len(grid.shape))]
        last_empty = True
        low_range, high_range = 0, None
        for j in range(s):
            slices[i] = j
            empty = np.all(grid[tuple(slices)] == 0)
            # print(f'On dim {i}, element {j}, empty is: {empty}, and val is:')
            # print(grid[tuple(slices)])
            if not empty and last_empty and low_range == 0:
                low_range = j
            if empty and not last_empty:
                high_range = j
            last_empty = empty
        ranges.append(slice(low_range, high_range))
    # print(ranges)
    return grid[tuple(ranges)]


def update(grid, kernel=KERNEL):
    counts = correlate(grid, kernel)
    big = np.zeros(counts.shape)
    big[tuple(slice(1, -1) for _ in range(len(grid.shape)))] = grid
    big = big == 1
    return (counts == 3) | (big & (counts == 2))


class Day(Day2020):
    @property
    def num(self) -> int:
        return 17

    def get_data(self, example=False):
        return np.array([[[c == '#' for c in l] for l in super().get_data(example)]])

    def puzzles(self):
        grid = self.get_data()
        grid2 = np.array([grid.copy()])

        for _ in range(6):
            grid = update(grid)
        print(np.sum(grid))

        kernel2 = make_kernel(4)
        for _ in range(6):
            grid2 = update(grid2, kernel=kernel2)
        print(np.sum(grid2))
