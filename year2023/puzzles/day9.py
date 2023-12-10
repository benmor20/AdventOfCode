from year2023.day2023 import Day2023
from typing import *
import numpy as np


class Day(Day2023):
    @property
    def num(self) -> int:
        return 9

    def get_data(self, example=False):
        lines = super().get_data(example)
        data = [[int(i) for i in l.split(' ')] for l in lines]
        return data

    def puzzle1(self):
        data = self.get_data()
        total = 0
        for line in data:
            arrs = []
            cur_arr = np.array(line)
            while np.any(cur_arr != 0):
                arrs.append(cur_arr)
                cur_arr = cur_arr[1:] - cur_arr[:-1]
            total += sum(arr[-1] for arr in arrs)
        print(total)

    def puzzle2(self):
        data = self.get_data()
        total = 0
        for line in data:
            arrs = []
            cur_arr = np.array(line)
            while np.any(cur_arr != 0):
                arrs.append(cur_arr)
                cur_arr = cur_arr[1:] - cur_arr[:-1]
            prec = 0
            for arr in arrs[::-1]:
                prec = arr[0] - prec
            total += prec
        print(total)


def one_line():
    pass
