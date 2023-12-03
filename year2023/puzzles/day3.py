import itertools

from year2023.day2023 import Day2023
from typing import *
import numpy as np
from scipy.signal import correlate2d


def num_at_index(line, idx) -> int:
    assert line[idx] in '1234567890'
    start_idx = idx
    while line[start_idx] in '1234567890' and start_idx >= 0:
        start_idx -= 1
    start_idx += 1
    num = 0
    for c in line[start_idx:]:
        if c not in '1234567890':
            return num
        num *= 10
        num += int(c)
    return num


def is_sym(data: np.ndarray, row_idx: int, col_idx: int) -> bool:
    if row_idx < 0 or row_idx >= data.shape[0] or col_idx < 0 or col_idx >= data.shape[1]:
        return False
    return data[row_idx, col_idx] < 0


def get_num(data: np.ndarray, coords: np.ndarray) -> int:
    row_idx = coords[0]
    col_idx = coords[1]
    if row_idx < 0 or row_idx >= data.shape[0] or col_idx < 0 or col_idx >= data.shape[1]:
        return False
    if data[row_idx, col_idx] > 0:
        return data[row_idx, col_idx]
    return 0


class Day(Day2023):
    @property
    def num(self) -> int:
        return 3

    def get_data(self, example=False):
        lines = super().get_data(example)
        symbols = list(set(''.join(lines)) - set('.0123456789'))
        symbols.remove('*')
        symbols.insert(0, '*')
        data = []
        count = Counter()
        for line in lines:
            row = np.zeros((len(line), ))
            for idx, c in enumerate(line):
                if c in '0123456789':
                    num = num_at_index(line, idx)
                    row[idx] = num
                    count[num] += 1
                elif c != '.':
                    row[idx] = -(symbols.index(c) + 1)
            data.append(row)
        return np.stack(data)

    def puzzle1(self):
        data = self.get_data()
        # print(data)
        kernel = np.ones((3, 3))
        conv = correlate2d(data, kernel, mode='same')
        is_num = data > 0

        cur_num = 0
        total = 0
        for row_idx in range(data.shape[0]):
            for col_idx in range(data.shape[1]):
                num = data[row_idx, col_idx]
                if num <= 0:
                    cur_num = 0
                    continue
                if num == cur_num:
                    continue
                cur_num = num
                num_digs = len(str(int(num)))
                is_counted = False
                # print(f'{num} is len {num_digs} at {row_idx}, {col_idx}')
                if is_sym(data, row_idx, col_idx - 1):
                    # print(f'{num} counted at r-1, c')
                    is_counted = True
                if is_sym(data, row_idx, col_idx + num_digs):
                    # print(f'{num} counted at r+{num_digs}, c')
                    is_counted = True
                for offset in range(-1, num_digs + 1):
                    if is_sym(data, row_idx - 1, col_idx + offset):
                        # print(f'{num} counted at r-1, c+{offset}')
                        is_counted = True
                    if is_sym(data, row_idx + 1, col_idx + offset):
                        # print(f'{num} counted at r+1, c+{offset}')
                        is_counted = True
                if is_counted:
                    # print(f'{num} is counted')
                    total += num
        print(int(total))

    def puzzle2(self):
        data = self.get_data()
        offsets = [np.array([a, b]) for a, b in itertools.product(range(-1, 2), range(-1, 2)) if not (a == 0 and b == 0)]
        total = 0
        for row_idx in range(data.shape[0]):
            for col_idx in range(data.shape[1]):
                num = data[row_idx, col_idx]
                if num != -1:
                    continue
                coords = np.array([row_idx, col_idx])
                adj_nums = set()
                for off in offsets:
                    adj_num = get_num(data, coords + off)
                    if adj_num > 0:
                        adj_nums.add(adj_num)
                if len(adj_nums) == 2:
                    adj_lst = list(adj_nums)
                    total += adj_lst[0] * adj_lst[1]
        print(total)


def one_line():
    pass
