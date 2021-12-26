from year2020.day2020 import Day2020_3
from collections import Counter
import numpy as np


class Day(Day2020_3):
    @property
    def num(self) -> int:
        return 10

    def get_data(self, example: bool = False):
        return [int(i) for i in super().get_data(example)]

    def product(self, vals):
        res = 1
        for v in vals:
            res *= v
        return res

    memo = {}
    def num_ways(self, joltages, target):
        if target in self.memo:
            return self.memo[target]
        if target == 0:
            return 1
        if target not in joltages:
            return 0
        ways1 = self.num_ways(joltages, target - 1)
        ways2 = self.num_ways(joltages, target - 2)
        ways3 = self.num_ways(joltages, target - 3)
        ways = ways1 + ways2 + ways3
        # print(f'There are {ways1} ways to get to {target - 1} and {ways3} ways to get to {target - 3}, for a total of {ways} ways to get to {target}')
        self.memo[target] = ways
        return ways

    def puzzle(self, num=1):
        data = self.get_data()
        if num == 1:
            data = [0] + sorted(data)
            data = data + [data[-1] + 3]
            print(self.product(Counter(np.array(data[1:]) - np.array(data[:-1])).values()))
        else:
            print(self.num_ways(set(data + [max(data) + 3]), max(data) + 3))
