import itertools
from typing import *
import numpy as np

import utils.utils
from year2019.day2019 import Day2019


class Day(Day2019):
    @property
    def num(self) -> int:
        return 8

    def get_data(self, example: Union[bool, int] = False):
        lines = super().get_data(example)
        data = [int(i) for i in lines[0]]
        return data, (3, 2) if example else (25, 6)

    def puzzles(self):
        data, size = self.get_data()
        data_arr: np.ndarray = np.array(data).reshape(-1, *size[::-1])
        counts = [np.sum(data_arr == i, axis=(1, 2)) for i in range(np.max(data_arr)+1)]
        least_zeros_idx = min(range(len(counts[0])), key=counts[0].item)
        print(f'P1 ans is {counts[1][least_zeros_idx] * counts[2][least_zeros_idx]}\n')

        res_img = np.zeros(size[::-1])
        for i, j in itertools.product(range(size[1]), range(size[0])):
            res_img[i, j] = [p for p in data_arr[:, i, j] if p != 2][0] == 1
        utils.utils.print_grid(res_img)
