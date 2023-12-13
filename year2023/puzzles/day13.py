from year2023.day2023 import Day2023
from typing import *
import numpy as np


SYM_TO_NUM = {'.': 0, '#': 1}


def count_num_left(area: np.ndarray, part1: bool) -> Optional[int]:
    for col in range(1, area.shape[1]):
        left = area[:, :col]
        right = area[:, col:]
        shortest = min(left.shape[1], right.shape[1])
        left = left[:, -shortest:]
        right = right[:, :shortest]
        if np.sum(left[:, ::-1] != right) == (0 if part1 else 1):
            return col
    return None


class Day(Day2023):
    @property
    def num(self) -> int:
        return 13

    def get_data(self, example=False):
        lines = super().get_raw_data(example)
        sections = lines.split('\n\n')
        data = []
        for section in sections:
            rows = []
            for row in section.split('\n'):
                rows.append(np.array([SYM_TO_NUM[c] for c in row]))
            data.append(np.stack(rows))
        return data

    def puzzle1(self):
        data = self.get_data()
        num_vert = 0
        num_horiz = 0
        for area in data:
            vert = count_num_left(area, True)
            horiz = count_num_left(area.T, True)
            assert (vert is None) ^ (horiz is None)
            if vert is not None:
                num_vert += vert
            else:
                num_horiz += horiz
        print(100 * num_horiz + num_vert)

    def puzzle2(self):
        data = self.get_data()
        num_vert = 0
        num_horiz = 0
        for area in data:
            vert = count_num_left(area, False)
            horiz = count_num_left(area.T, False)
            assert (vert is None) ^ (horiz is None)
            if vert is not None:
                num_vert += vert
            else:
                num_horiz += horiz
        print(100 * num_horiz + num_vert)


def one_line():
    pass
