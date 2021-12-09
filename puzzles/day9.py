from puzzles.daybase import DayBase
import numpy as np
from heapq import heappush, heappop


class Day(DayBase):
    @property
    def num(self) -> int:
        return 9

    def get_data(self, example=False):
        return [[int(i) for i in row] for row in super().get_data(example)]

    def low_points(self, data):
        for i, row in enumerate(data):
            for j, val in enumerate(row):
                if i - 1 >= 0 and data[i - 1][j] <= val:
                    continue
                elif i + 1 < len(data) and data[i + 1][j] <= val:
                    continue
                if j - 1 >= 0 and data[i][j - 1] <= val:
                    continue
                elif j + 1 < len(row) and data[i][j + 1] <= val:
                    continue
                yield i, j

    def puzzle1(self):
        data = self.get_data()
        risk = 0
        for i, j in self.low_points(data):
            risk += data[i][j] + 1
        print(risk)

    def true_for_neigh(self, data, index, func):
        i, j = index
        res = {}
        if i - 1 >= 0:
            res[(i - 1, j)] = func(data[i - 1][j])
        if i + 1 < len(data):
            res[(i + 1, j)] = func(data[i + 1][j])
        if j - 1 >= 0:
            res[(i, j - 1)] = func(data[i][j - 1])
        if j + 1 < len(data[0]):
            res[(i, j + 1)] = func(data[i][j + 1])
        return res

    seen = set()
    def size(self, data, start):
        if start in self.seen:
            return 0
        self.seen.add(start)
        i, j = start
        val = data[i][j]
        if all(self.true_for_neigh(data, start, lambda v: v == 9 or v <= val).values()):
            return 1
        return sum(self.size(data, new) for new, true in
                   self.true_for_neigh(data, start, lambda v: v != 9 and v >= val).items() if true) + 1

    def puzzle2(self):
        data = self.get_data()
        heap = []
        for i, j in self.low_points(data):
            heappush(heap, -self.size(data, (i, j)))
            seen = set()
        print(-heappop(heap) * heappop(heap) * heappop(heap))
