from year2021.day2021 import Day2021
import numpy as np


class Day(Day2021):
    @property
    def num(self) -> int:
        return 5

    def get_data(self, example=False):
        data = super().get_data(example)
        lines = []
        for line in data:
            points_str = line.split(' -> ')
            lines.append(tuple([tuple([int(i) for i in pt_str.split(',')]) for pt_str in points_str]))
        return lines

    def grid_size(self, lines) -> int:
        max_val = 0
        for line in lines:
            for point in line:
                for val in point:
                    if val > max_val:
                        max_val = val
        return max_val + 1

    def puzzle1(self):
        return
        lines = self.get_data()
        size = self.grid_size(lines)
        grid = np.zeros((size, size))
        non_aligned = 0
        for line in lines:
            x1, y1 = line[0]
            x2, y2 = line[1]
            if x1 == x2:
                low, high = min(y1, y2), max(y1, y2)
                grid[x1, low:high+1] += 1
            elif y1 == y2:
                low, high = min(x1, x2), max(x1, x2)
                grid[low:high+1, y1] += 1
            else:
                non_aligned += 1
        print(non_aligned)
        print(grid)
        print(np.sum(grid >= 2))

    def puzzle2(self):
        lines = self.get_data()
        size = self.grid_size(lines)
        grid = np.zeros((size, size))
        for line in lines:
            x1, y1 = line[0]
            x2, y2 = line[1]
            if x1 == x2:
                low, high = min(y1, y2), max(y1, y2)
                grid[x1, low:high + 1] += 1
            elif y1 == y2:
                low, high = min(x1, x2), max(x1, x2)
                grid[low:high + 1, y1] += 1
            else:
                lowx, highx = min(x1, x2), max(x1, x2)
                lowy, highy = min(y1, y2), max(y1, y2)
                flip = (x1 > x2) ^ (y1 > y2)
                grid[lowx:highx+1, lowy:highy+1] += np.eye(highx - lowx + 1)[::-1 if flip else 1]
        print(grid)
        print(np.sum(grid >= 2))
